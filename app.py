from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_file
)

import sqlite3
import os
import requests
import joblib

from reportlab.pdfgen import canvas
from sklearn.metrics.pairwise import cosine_similarity

# ===================================
# Flask App
# ===================================

app = Flask(__name__)

app.secret_key = "omnientry_secret_key"

DB_PATH = "database/omnientry.db"

# ===================================
# AI Model
# ===================================

vectorizer = joblib.load("model/vectorizer.pkl")
data = joblib.load("model/services.pkl")


# ===================================
# Database Connection
# ===================================

def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# ===================================
# AI Recommendation
# ===================================

def recommend(query):

    query_vector = vectorizer.transform([query])

    service_vectors = vectorizer.transform(
        data["keywords"]
    )

    similarity = cosine_similarity(
        query_vector,
        service_vectors
    )

    index = similarity.argmax()

    return data.iloc[index]


# ===================================
# Home Page
# ===================================

@app.route("/")
def home():

    conn = get_connection()

    categories = conn.execute("""

    SELECT category_name

    FROM categories

    ORDER BY category_name

    """).fetchall()

    service_count = conn.execute("""

    SELECT COUNT(*)

    FROM services

    """).fetchone()[0]

    category_count = conn.execute("""

    SELECT COUNT(*)

    FROM categories

    """).fetchone()[0]

    featured_services = conn.execute("""

    SELECT id,
           service_name,
           category_name

    FROM services

    LIMIT 8

    """).fetchall()

    conn.close()

    return render_template(

        "index.html",

        categories=categories,

        services=service_count,

        category_count=category_count,

        featured_services=featured_services

    )
# ===================================
# Login
# ===================================

@app.route("/login", methods=["GET", "POST"])

def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        conn = get_connection()

        user = conn.execute("""

        SELECT *

        FROM users

        WHERE email=?

        AND password=?

        """,(email,password)).fetchone()

        conn.close()

        if user:

            session["user_id"] = user["id"]

            session["user_name"] = user["full_name"]

            flash("Login Successful")

            return redirect("/")

        else:

            flash("Invalid Email or Password")

    return render_template("login.html")

# ===================================
# Register
# ===================================

@app.route("/register",methods=["GET","POST"])

def register():

    if request.method=="POST":

        name=request.form["name"]

        email=request.form["email"]

        password=request.form["password"]

        conn=get_connection()

        try:

            conn.execute("""

            INSERT INTO users(

            full_name,

            email,

            password

            )

            VALUES(?,?,?)

            """,(name,email,password))

            conn.commit()

            flash("Registration Successful")

            return redirect("/login")

        except:

            flash("Email Already Exists")

        finally:

            conn.close()

    return render_template("register.html")
# ===================================
# Logout
# ===================================

@app.route("/logout")

def logout():

    session.clear()

    flash("Logged Out Successfully")

    return redirect("/")
# ===================================
# Category Page
# ===================================

@app.route("/category/<category_name>")
def category(category_name):

    conn = get_connection()

    services = conn.execute("""
        SELECT *
        FROM services
        WHERE category_name=?
    """,(category_name,)).fetchall()

    conn.close()

    return render_template(
        "category.html",
        category=category_name,
        services=services
    )


# ===================================
# Service Details
# ===================================

@app.route("/service/<int:id>")
def service(id):

    conn = get_connection()

    service = conn.execute("""
        SELECT *
        FROM services
        WHERE id=?
    """,(id,)).fetchone()

    related = conn.execute("""
        SELECT id,service_name
        FROM services
        WHERE category_name=?
        AND id!=?
        LIMIT 5
    """,(service["category_name"],id)).fetchall()

    conn.close()

    return render_template(
        "service.html",
        service=service,
        related=related
    )


# ===================================
# Normal Search
# ===================================

@app.route("/search",methods=["POST"])
def search():

    keyword=request.form["search"]

    conn=get_connection()

    conn.execute(
        "INSERT INTO search_history(keyword) VALUES(?)",
        (keyword,)
    )

    conn.commit()

    results=conn.execute("""

        SELECT *

        FROM services

        WHERE service_name LIKE ?

        OR category_name LIKE ?

    """,(

        "%"+keyword+"%",

        "%"+keyword+"%"

    )).fetchall()

    conn.close()

    return render_template(

        "category.html",

        category="Search Results",

        services=results

    )


# ===================================
# AI Search
# ===================================

@app.route("/ai_search",methods=["POST"])
def ai_search():

    query=request.form["search"]

    conn=get_connection()

    conn.execute(
        "INSERT INTO search_history(keyword) VALUES(?)",
        (query,)
    )

    conn.commit()

    conn.close()

    result=recommend(query)

    return redirect(
        url_for(
            "service",
            id=int(result["id"])
        )
    )
# ===================================
# Favorites
# ===================================

@app.route("/favorite/<int:service_id>")
def favorite(service_id):

    if "user_id" not in session:
        flash("Please Login First")
        return redirect("/login")

    conn = get_connection()

    conn.execute("""
        INSERT INTO favorites(user_id,service_id)
        VALUES(?,?)
    """,(session["user_id"],service_id))

    conn.commit()
    conn.close()

    flash("Service Added to Favorites")

    return redirect(url_for("service",id=service_id))


# ===================================
# View Favorites
# ===================================

@app.route("/favorites")
def favorites():

    if "user_id" not in session:
        return redirect("/login")

    conn=get_connection()

    services=conn.execute("""

    SELECT services.*

    FROM favorites

    JOIN services

    ON favorites.service_id=services.id

    WHERE favorites.user_id=?

    """,(session["user_id"],)).fetchall()

    conn.close()

    return render_template(
        "favorites.html",
        services=services
    )


# ===================================
# Recently Viewed
# ===================================

@app.route("/recent")
def recent():

    if "user_id" not in session:
        return redirect("/login")

    conn=get_connection()

    recent=conn.execute("""

    SELECT services.*

    FROM recently_viewed

    JOIN services

    ON recently_viewed.service_id=services.id

    WHERE recently_viewed.user_id=?

    ORDER BY viewed_at DESC

    LIMIT 10

    """,(session["user_id"],)).fetchall()

    conn.close()

    return render_template(
        "recent.html",
        services=recent
    )


# ===================================
# Chatbot
# ===================================

@app.route("/chatbot")
def chatbot():

    return render_template("chatbot.html")


# ===================================
# Dashboard
# ===================================

@app.route("/dashboard")
def dashboard():

    conn=get_connection()

    service_count=conn.execute(
        "SELECT COUNT(*) FROM services"
    ).fetchone()[0]

    category_count=conn.execute(
        "SELECT COUNT(*) FROM categories"
    ).fetchone()[0]

    user_count=conn.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        services=service_count,
        categories=category_count,
        users=user_count
    )


# ===================================
# Analytics
# ===================================

@app.route("/analytics")
def analytics():

    conn=get_connection()

    history=conn.execute("""

    SELECT keyword,
    COUNT(*) total

    FROM search_history

    GROUP BY keyword

    ORDER BY total DESC

    LIMIT 10

    """).fetchall()

    conn.close()

    return render_template(
        "analytics.html",
        history=history
    )


# ===================================
# Admin
# ===================================

@app.route("/admin")
def admin():

    conn=get_connection()

    services=conn.execute("""

    SELECT *

    FROM services

    ORDER BY category_name

    """).fetchall()

    conn.close()

    return render_template(
        "admin.html",
        services=services
    )


# ===================================
# About
# ===================================

@app.route("/about")
def about():

    return render_template("about.html")


# ===================================
# Contact
# ===================================

@app.route("/contact")
def contact():

    return render_template("contact.html")
# ===================================
# Search History
# ===================================

@app.route("/history")
def history():

    conn = get_connection()

    history = conn.execute("""
        SELECT *
        FROM search_history
        ORDER BY search_time DESC
    """).fetchall()

    conn.close()

    return render_template(
        "history.html",
        history=history
    )


# ===================================
# Feedback
# ===================================

@app.route("/feedback", methods=["GET","POST"])
def feedback():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = get_connection()

        conn.execute("""
            INSERT INTO feedback(name,email,message)
            VALUES(?,?,?)
        """,(name,email,message))

        conn.commit()
        conn.close()

        flash("Thank you for your feedback!")

        return redirect("/")

    return render_template("feedback.html")


# ===================================
# News Page
# ===================================

@app.route("/news")
def news():

    news = [

        "SSC CGL Notification Released",

        "PM Kisan Registration Open",

        "National Scholarship Portal Started",

        "Passport Online Services Updated",

        "New Aadhaar Update Rules Announced"

    ]

    return render_template(
        "news.html",
        news=news
    )


# ===================================
# PDF Download
# ===================================

@app.route("/download/<int:id>")
def download(id):

    conn = get_connection()

    service = conn.execute("""
        SELECT *
        FROM services
        WHERE id=?
    """,(id,)).fetchone()

    conn.close()

    filename = f"service_{id}.pdf"

    pdf = canvas.Canvas(filename)

    pdf.setFont("Helvetica-Bold",18)
    pdf.drawString(180,800,"OmniEntry AI")

    pdf.setFont("Helvetica",12)

    pdf.drawString(60,760,f"Service : {service['service_name']}")
    pdf.drawString(60,730,f"Category : {service['category_name']}")
    pdf.drawString(60,700,f"Eligibility : {service['eligibility']}")
    pdf.drawString(60,670,f"Documents : {service['documents']}")
    pdf.drawString(60,640,f"Fee : {service['fees']}")
    pdf.drawString(60,610,f"Website : {service['website']}")

    pdf.save()

    return send_file(
        filename,
        as_attachment=True
    )


# ===================================
# Error Pages
# ===================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "error.html",
        message="Page Not Found"
    ),404


@app.errorhandler(500)
def internal_error(error):

    return render_template(
        "error.html",
        message="Internal Server Error"
    ),500


# ===================================
# Run Project
# ===================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
