from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc
from decouple import config

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        
        # Placeholder for sending or processing the message
        flash("Thank you for reaching out!", "success")
        return redirect(url_for("contact"))
    
    return render_template("contact.html")

# Connect to the database (replace 'database.db' with your database file)
def get_db_connection():
    server = config('SERVER')
    database = config('DATABASE')
    username = config('DB_USERNAME')
    password = config('DB_PASSWORD')
    driver= '{ODBC Driver 17 for SQL Server}'

    conn = pyodbc.connect(
        f'DRIVER={driver};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )
    return conn

@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    if request.method == "POST":
        query = request.form["query"]
        conn = get_db_connection()
        results = conn.execute(
            "SELECT TOP 50 cardName, filepath, boxCode FROM [dbo].[tbl_MTGCardLibrary] WHERE cardName LIKE ?", 
            ('%' + query + '%',)
        ).fetchall()
        conn.close()
    return render_template("search.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
