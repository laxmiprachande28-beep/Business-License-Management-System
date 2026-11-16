import webbrowser
import os
from dotenv import load_dotenv

load_dotenv()
from threading import Timer
from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
client = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=5000
)

db = client["business_license_db"]

applicants_collection = db["applicants"]
applications_collection = db["applications"]
licenses_collection = db["licenses"]
payments_collection = db["payments"]
renewals_collection = db["renewals"]


def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Please login as administrator.", "error")
            return redirect(url_for("admin_login"))
        return function(*args, **kwargs)
    return wrapper


@app.route("/")
def index():
    return render_template(
        "index.html",
        applicant_count=applicants_collection.count_documents({}),
        application_count=applications_collection.count_documents({}),
        license_count=licenses_collection.count_documents({}),
        payment_count=payments_collection.count_documents({}),
        recent_applicants=list(
            applicants_collection.find().sort("_id", -1).limit(5)
        ),
        recent_applications=list(
            applications_collection.find().sort("_id", -1).limit(5)
        )
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            applicant = {
                "name": request.form.get("name", "").strip(),
                "email": request.form.get("email", "").strip().lower(),
                "phone": request.form.get("phone", "").strip(),
                "address": request.form.get("address", "").strip(),
                "applicant_type": request.form.get("applicant_type", "").strip(),
                "registration_date": datetime.now().strftime("%Y-%m-%d")
            }

            if not all(applicant[key] for key in [
                "name", "email", "phone", "address", "applicant_type"
            ]):
                flash("Please fill in all fields.", "error")

            elif applicants_collection.find_one({"email": applicant["email"]}):
                flash("Applicant with this email already exists.", "error")

            else:
                applicants_collection.insert_one(applicant)
                flash("Applicant registered successfully!", "success")
                return redirect(url_for("register"))

        except Exception as e:
            print("Registration error:", e)
            flash("Registration failed: " + str(e), "error")

    return render_template("register.html")


@app.route("/applicants")
def applicants():
    records = list(applicants_collection.find().sort("_id", -1))
    return render_template(
        "records.html",
        title="Applicant Records",
        records=records
    )


@app.route("/business-application", methods=["GET", "POST"])
def business_application():
    if request.method == "POST":
        try:
            email = request.form.get("applicant_email", "").strip().lower()
            business_name = request.form.get("business_name", "").strip()
            business_type = request.form.get("business_type", "").strip()
            business_address = request.form.get("business_address", "").strip()

            if not all([email, business_name, business_type, business_address]):
                flash("Please fill in all fields.", "error")

            else:
                applicant = applicants_collection.find_one({"email": email})

                if not applicant:
                    flash("Applicant not found. Register this email first.", "error")

                else:
                    application = {
                        "applicant_id": applicant["_id"],
                        "applicant_name": applicant["name"],
                        "applicant_email": email,
                        "business_name": business_name,
                        "business_type": business_type,
                        "business_address": business_address,
                        "status": "Pending",
                        "application_date": datetime.now().strftime("%Y-%m-%d")
                    }

                    applications_collection.insert_one(application)
                    flash("Business application submitted successfully!", "success")
                    return redirect(url_for("applications"))

        except Exception as e:
            print("Business application error:", e)
            flash("Application failed: " + str(e), "error")

    return render_template("business_application.html")


@app.route("/applications")
def applications():
    records = list(applications_collection.find().sort("_id", -1))
    return render_template(
        "applications.html",
        records=records
    )


@app.route("/licenses", methods=["GET", "POST"])
def licenses():
    if request.method == "POST":
        try:
            email = request.form.get("applicant_email", "").strip().lower()
            business_name = request.form.get("business_name", "").strip()
            license_type = request.form.get("license_type", "").strip()
            duration = request.form.get("duration", "").strip()

            if not all([email, business_name, license_type, duration]):
                flash("Please fill in all fields.", "error")

            else:
                applicant = applicants_collection.find_one({"email": email})

                if not applicant:
                    flash("Applicant not found. Register the applicant first.", "error")

                else:
                    license_record = {
                        "applicant_id": applicant["_id"],
                        "applicant_name": applicant["name"],
                        "applicant_email": email,
                        "business_name": business_name,
                        "license_type": license_type,
                        "duration": duration,
                        "license_number": "BL-" + datetime.now().strftime("%Y%m%d%H%M%S%f"),
                        "status": "Active",
                        "issue_date": datetime.now().strftime("%Y-%m-%d")
                    }

                    licenses_collection.insert_one(license_record)
                    flash("License issued successfully!", "success")
                    return redirect(url_for("licenses"))

        except Exception as e:
            print("License error:", e)
            flash("License creation failed: " + str(e), "error")

    records = list(licenses_collection.find().sort("_id", -1))
    return render_template("licenses.html", records=records)


@app.route("/payments", methods=["GET", "POST"])
def payments():
    if request.method == "POST":
        try:
            email = request.form.get("applicant_email", "").strip().lower()
            business_name = request.form.get("business_name", "").strip()
            amount = float(request.form.get("amount", 0))
            method = request.form.get("payment_method", "").strip()
            status = request.form.get("payment_status", "").strip()

            if not all([email, business_name, method, status]) or amount <= 0:
                flash("Enter valid payment details.", "error")

            else:
                payment = {
                    "applicant_email": email,
                    "business_name": business_name,
                    "amount": amount,
                    "payment_method": method,
                    "payment_status": status,
                    "payment_date": datetime.now().strftime("%Y-%m-%d")
                }

                payments_collection.insert_one(payment)
                flash("Payment saved successfully!", "success")
                return redirect(url_for("payments"))

        except ValueError:
            flash("Please enter a valid payment amount.", "error")

        except Exception as e:
            print("Payment error:", e)
            flash("Payment failed: " + str(e), "error")

    records = list(payments_collection.find().sort("_id", -1))
    return render_template("payments.html", records=records)


@app.route("/renewals", methods=["GET", "POST"])
def renewals():
    if request.method == "POST":
        try:
            license_number = request.form.get("license_number", "").strip()
            email = request.form.get("applicant_email", "").strip().lower()
            period = request.form.get("renewal_period", "").strip()

            if not all([license_number, email, period]):
                flash("Please fill in all fields.", "error")

            else:
                license_record = licenses_collection.find_one({
                    "license_number": license_number,
                    "applicant_email": email
                })

                if not license_record:
                    flash("License not found. Check license number and email.", "error")

                else:
                    renewal = {
                        "license_number": license_number,
                        "applicant_email": email,
                        "business_name": license_record["business_name"],
                        "renewal_period": period,
                        "status": "Pending",
                        "renewal_date": datetime.now().strftime("%Y-%m-%d")
                    }

                    renewals_collection.insert_one(renewal)
                    flash("Renewal request submitted successfully!", "success")
                    return redirect(url_for("renewals"))

        except Exception as e:
            print("Renewal error:", e)
            flash("Renewal failed: " + str(e), "error")

    records = list(renewals_collection.find().sort("_id", -1))
    return render_template("renewals.html", records=records)


@app.route("/view-records")
def view_records():
    all_records = {
        "Applicants": list(applicants_collection.find().sort("_id", -1)),
        "Applications": list(applications_collection.find().sort("_id", -1)),
        "Licenses": list(licenses_collection.find().sort("_id", -1)),
        "Payments": list(payments_collection.find().sort("_id", -1)),
        "Renewals": list(renewals_collection.find().sort("_id", -1))
    }

    return render_template(
        "view_records.html",
        all_records=all_records
    )


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == os.getenv("ADMIN_USERNAME") and password == os.getenv("ADMIN_PASSWORD"):
            session["admin_logged_in"] = True
            flash("Administrator login successful!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Incorrect username or password.", "error")

    return render_template("admin_login.html")


@app.route("/admin-dashboard")
@admin_required
def admin_dashboard():
    return render_template(
        "index.html",
        applicant_count=applicants_collection.count_documents({}),
        application_count=applications_collection.count_documents({}),
        license_count=licenses_collection.count_documents({}),
        payment_count=payments_collection.count_documents({}),
        recent_applicants=list(
            applicants_collection.find().sort("_id", -1).limit(5)
        ),
        recent_applications=list(
            applications_collection.find().sort("_id", -1).limit(5)
        )
    )


@app.route("/admin-logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    flash("You have logged out.", "success")
    return redirect(url_for("admin_login"))


@app.route("/db-status")
def db_status():
    try:
        client.admin.command("ping")
        return "MongoDB connected successfully. Database: " + db.name
    except Exception as e:
        return "MongoDB connection failed: " + str(e), 500


if __name__ == "__main__":
    try:
        client.admin.command("ping")

        print("Business License Management System")
        print("Database:", db.name)
        print("MongoDB connection successful!")
        print("Starting Flask application...")

        Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:5000/")).start()

        app.run(debug=True, use_reloader=False)

    except Exception as e:
        print("MongoDB connection failed:", str(e))
