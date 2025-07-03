# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from extractor import ExtractListings
from send_email import Email
from dotenv import load_dotenv
import os

load_dotenv()
email_password = os.getenv("EMAIL_PASSWORD")

extraction = ExtractListings()
emailer = Email(email_password)
app = Flask(__name__)

# Allow requests from Vercel and localhost
CORS(app, origins=[
    "https://research-park-job-alerts.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
])

@app.route("/api/subscribe", methods=["POST"])
def subscribe():
    """API endpoint to subscribe to job alerts"""
    try:
        data = request.get_json()
        email = data.get("email")
        

        print("recieved")
        if not email:
            return jsonify({"error": "Email is required"}), 400
        
        # # Send confirmation email
        # emailer.send_email(
        #     "kingicydiamond@gmail.com", 
        #     email, 
        #     "Job Alerts Confirmation", 
        #     "Welcome to Research Park's Job Alerts. Whenever a job alert releases on research park, you will hear first! However, before you can enroll, you must be approved by the creator of this program!"
        # )
        
        # Add email to database
        extraction.add_email(email)
        
        return jsonify({
            "success": True,
            "message": "Successfully subscribed to job alerts!"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "UIUC Research Park Job Alerts"}), 200

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get basic statistics about the service"""
    try:
        # You can add more stats here based on your data
        return jsonify({
            "total_subscribers": len(extraction.get_emails()) if hasattr(extraction, 'get_emails') else 0,
            "service": "UIUC Research Park Job Alerts"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)