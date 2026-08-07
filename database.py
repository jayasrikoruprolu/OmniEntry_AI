import sqlite3

conn = sqlite3.connect("database/omnientry.db")
cursor = conn.cursor()

# ===========================
# Create Tables
# ===========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS services(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT,
    service_name TEXT,
    eligibility TEXT,
    documents TEXT,
    fees TEXT,
    website TEXT
)
""")

# Delete old data
cursor.execute("DELETE FROM categories")
cursor.execute("DELETE FROM services")

# ===========================
# Categories
# ===========================

categories = [

("Education",),
("Jobs",),
("Health",),
("Travel",),
("Passport",),
("Aadhaar",),
("PAN Card",),
("Driving Licence",),
("Banking",),
("Agriculture",),
("Business",),
("Certificates",),
("Scholarships",),
("Home",)

]

cursor.executemany(
"INSERT INTO categories(category_name) VALUES(?)",
categories
)

# ===========================
# Services
# ===========================

services = [

# ---------------- Education ----------------

("Education","B.Tech Admission","Intermediate","Marks Memo","1000","https://www.apsche.ap.gov.in"),

("Education","BCA Admission","Intermediate","Marks Memo","800","https://www.apsche.ap.gov.in"),

("Education","MBA Admission","Degree","Degree Certificate","1200","https://www.apsche.ap.gov.in"),

("Education","MCA Admission","Degree","Degree Certificate","1000","https://www.apsche.ap.gov.in"),

("Education","B.Sc Admission","Intermediate","Marks Memo","500","https://www.apsche.ap.gov.in"),

("Education","Medical Admission","Intermediate BiPC","Marks Memo","1500","https://www.nmc.org.in"),

("Education","Law Admission","Intermediate","Marks Memo","1000","https://www.barcouncilofindia.org"),

("Education","Polytechnic","10th Pass","10th Memo","500","https://www.sbtet.ap.gov.in"),

("Education","ITI Admission","10th Pass","10th Memo","300","https://www.ncvtmis.gov.in"),

("Scholarships","National Scholarship","Student","Income Certificate","0","https://scholarships.gov.in"),

# ---------------- Jobs ----------------

("Jobs","SSC CGL","Degree","Degree Certificate","100","https://ssc.gov.in"),

("Jobs","SSC CHSL","Intermediate","Marks Memo","100","https://ssc.gov.in"),

("Jobs","UPSC Civil Services","Degree","Degree Certificate","100","https://upsc.gov.in"),

("Jobs","Bank PO","Degree","Degree Certificate","850","https://ibps.in"),

("Jobs","Railway Recruitment","10th/Degree","Aadhaar","500","https://www.rrbcdg.gov.in"),

("Jobs","Police Recruitment","Intermediate","Aadhaar","300","https://slprb.ap.gov.in"),

("Jobs","Forest Department","Degree","Aadhaar","250","https://forest.ap.gov.in"),

("Jobs","Village Secretariat","Degree","Aadhaar","200","https://gramasachivalayam.ap.gov.in"),

("Jobs","Software Jobs","Degree","Resume","0","https://www.ncs.gov.in"),

("Jobs","Apprenticeship","ITI/Degree","Certificates","0","https://www.apprenticeshipindia.gov.in"),

# ---------------- Health ----------------

("Health","Ayushman Bharat","Citizen","Aadhaar","0","https://pmjay.gov.in"),

("Health","ABHA Health Card","Citizen","Aadhaar","0","https://abha.abdm.gov.in"),

("Health","Health Insurance","Citizen","Aadhaar","0","https://irdai.gov.in"),

("Health","Vaccination Certificate","Citizen","Aadhaar","0","https://cowin.gov.in"),

("Health","Blood Bank Services","Citizen","ID Proof","0","https://eraktkosh.in"),


# ---------------- Passport ----------------

("Passport","New Passport","Citizen","Aadhaar","1500","https://passportindia.gov.in"),
("Passport","Passport Renewal","Citizen","Old Passport","1500","https://passportindia.gov.in"),
("Passport","Track Passport","Application Number","Application ID","0","https://passportindia.gov.in"),

# ---------------- Aadhaar ----------------

("Aadhaar","New Aadhaar","Citizen","Birth Certificate","0","https://uidai.gov.in"),
("Aadhaar","Aadhaar Update","Citizen","Aadhaar","50","https://uidai.gov.in"),
("Aadhaar","Mobile Number Update","Citizen","Aadhaar","50","https://uidai.gov.in"),
("Aadhaar","Address Update","Citizen","Address Proof","50","https://uidai.gov.in"),

# ---------------- PAN Card ----------------

("PAN Card","New PAN Card","Citizen","Aadhaar","110","https://protean-tinpan.com"),
("PAN Card","PAN Correction","Citizen","PAN Card","110","https://protean-tinpan.com"),
("PAN Card","Link PAN with Aadhaar","Citizen","PAN & Aadhaar","0","https://incometax.gov.in"),

# ---------------- Driving Licence ----------------

("Driving Licence","Learning Licence","18+","Aadhaar","200","https://parivahan.gov.in"),
("Driving Licence","Driving Licence","18+","Learning Licence","500","https://parivahan.gov.in"),
("Driving Licence","DL Renewal","Citizen","Old Licence","300","https://parivahan.gov.in"),
("Driving Licence","Duplicate Licence","Citizen","Old Licence","300","https://parivahan.gov.in"),

# ---------------- Banking ----------------

("Banking","Open Savings Account","Citizen","Aadhaar, PAN","0","https://sbi.co.in"),
("Banking","Education Loan","Student","Admission Letter","0","https://sbi.co.in"),
("Banking","Home Loan","Citizen","Income Proof","0","https://sbi.co.in"),
("Banking","PM Jan Dhan Yojana","Citizen","Aadhaar","0","https://pmjdy.gov.in"),
("Banking","Debit Card","Account Holder","Bank Passbook","0","https://sbi.co.in"),

# ---------------- Agriculture ----------------

("Agriculture","PM Kisan","Farmer","Land Documents","0","https://pmkisan.gov.in"),
("Agriculture","Soil Health Card","Farmer","Land Records","0","https://soilhealth.dac.gov.in"),
("Agriculture","Crop Insurance","Farmer","Land Documents","0","https://pmfby.gov.in"),
("Agriculture","Kisan Credit Card","Farmer","Land Documents","0","https://pmkisan.gov.in"),

# ---------------- Business ----------------

("Business","GST Registration","Business Owner","PAN","0","https://gst.gov.in"),
("Business","GST Return Filing","Business Owner","GST Number","0","https://gst.gov.in"),
("Business","Udyam Registration","MSME","PAN","0","https://udyamregistration.gov.in"),
("Business","Trade License","Business Owner","Identity Proof","500","https://services.india.gov.in"),

# ---------------- Certificates ----------------

("Certificates","Income Certificate","Citizen","Aadhaar","50","https://services.india.gov.in"),
("Certificates","Caste Certificate","Citizen","Aadhaar","50","https://services.india.gov.in"),
("Certificates","Birth Certificate","Citizen","Hospital Record","50","https://services.india.gov.in"),
("Certificates","Death Certificate","Citizen","Medical Certificate","50","https://services.india.gov.in"),
("Certificates","Residence Certificate","Citizen","Aadhaar","50","https://services.india.gov.in"),

# ---------------- Home ----------------

("Home","PMAY Housing Scheme","Citizen","Income Certificate","0","https://pmaymis.gov.in"),
("Home","Property Registration","Citizen","Sale Deed","500","https://registration.ap.gov.in"),
("Home","Electricity Connection","Citizen","Address Proof","500","https://www.apspdcl.in"),

# ---------------- Travel ----------------

("Travel","Flight Booking","Citizen","ID Proof","0","https://www.airindia.com"),
("Travel","Train Reservation","Citizen","ID Proof","0","https://www.irctc.co.in"),
("Travel","Bus Reservation","Citizen","ID Proof","0","https://www.apsrtconline.in")

]

# ===========================
# Search History Table
# ===========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS search_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS favorites(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    service_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(service_id) REFERENCES services(id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS recently_viewed(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    service_id INTEGER,
    viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(service_id) REFERENCES services(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
INSERT OR IGNORE INTO admin(username,password)
VALUES('admin','admin123')
""")


# ===========================
# User Search Analytics
# ===========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS analytics(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT,
    user_id INTEGER,
    search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ===========================
# Notifications
# ===========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Default Notifications

cursor.execute("""
INSERT OR IGNORE INTO notifications(id,title,message)
VALUES
(1,'SSC CGL','SSC CGL Notification Released'),
(2,'Passport','Passport Online Services Updated'),
(3,'PM Kisan','PM Kisan Registration Started'),
(4,'Scholarship','National Scholarship Portal Open')
""")

# ===========================
# User Profile
# ===========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS profile(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    phone TEXT,
    address TEXT,
    profile_photo TEXT
)
""")

# ===========================
# Chat History
# ===========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS chatbot_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_question TEXT,
    bot_answer TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ===========================
# Login History
# ===========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS login_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ===========================
# Popular Searches
# ===========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS popular_searches(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT UNIQUE,
    total INTEGER DEFAULT 1
)
""")

# ===========================
# Bookmarks
# ===========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookmarks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    service_id INTEGER
)
""")

# ===========================
# Contact Messages
# ===========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS contact_messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    subject TEXT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.executemany("""
INSERT INTO services(
category_name,
service_name,
eligibility,
documents,
fees,
website
)
VALUES(?,?,?,?,?,?)
""", services)

cursor.execute("SELECT category_name, service_name FROM services")

rows = cursor.fetchall()

for row in rows:
    print(row)
conn.commit()
conn.close()

print("Database Created Successfully")