# app.py
from flask import Flask, request, redirect, render_template
from extractor import ExtractListings

extraction = ExtractListings()
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form["email"]
        extraction.add_email(email)
        return render_template("success.html")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
