from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# Database Configuration (Assuming PostgreSQL is running inside Docker)
DB_HOST = "host.docker.internal"  # Update if using Docker container name or IP
DB_NAME = "mydb"
DB_USER = "postgres"
DB_PASSWORD = "password"

# Connect to PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Set upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    image = request.files.get("image")  # Image is now optional

    if not (name and email):
        return "Name and email are required!", 400

    image_path = None  # Default to None if no image is uploaded

    if image:
        filename = secure_filename(image.filename)
        local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(local_path)
        image_path = local_path  # Store local path in DB

    # Commented out S3 upload logic
    # try:
    #     s3.upload_file(local_path, S3_BUCKET, filename)
    #     s3_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{filename}"
    # except Exception as e:
    #     return f"Error uploading file: {str(e)}", 500

    # Save data to database with local image path
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, image_url, created_at) VALUES (%s, %s, %s, %s)",
            (name, email, image_path, datetime.utcnow())  # Store local path instead of S3 URL
        )
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        return f"Error saving to database: {str(e)}", 500

    return render_template('success.html', name=name, image_path=image_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
