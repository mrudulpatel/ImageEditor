from flask import Flask, render_template, flash, request, redirect, url_for
import cv2
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}



app = Flask(__name__)

app.secret_key = "super secret key"

@app.route("/")
def hello_word():
    return render_template("index.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        #    Upload file to server
        if 'file' not in request.files:
            flash('No file part')
            return "Error no file received..."
        file = request.files['file']
        operation = request.form['operation']
        if file.filename == '':
            flash("No selected file")
            return "Error no file selected..."
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            newFileName = processImage(filename, operation)
            # Write the code to download the image
            # return f"<a href='{newFileName}' download='true'>Click to Download</a> <br> <a href='/'>Go back</a>"
            flash(f"<a href='{newFileName}' download='true'>Click to Download</a>")
        return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def processImage(filename, operation):
    image = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            newfilename = f"static/{filename}"
            cv2.imwrite(newfilename, gray)
            return newfilename
        case "cpng":
            png = cv2.imread(f"uploads/{filename}")
            newfilename = f"static/{filename.split('.')[0] + '.png'}"
            cv2.imwrite(newfilename, png)
            return newfilename
        case "cjpg":
            jpg = cv2.imread(f"uploads/{filename}")
            newfilename = f"static/{filename.split('.')[0] + '.jpg'}"
            cv2.imwrite(newfilename, jpg)
            return newfilename
        case "cwebp":
            webp = cv2.imread(f"uploads/{filename}")
            newfilename = f"static/{filename.split('.')[0] + '.webp'}"
            cv2.imwrite(newfilename, webp)
            return newfilename
            


app.run(debug=True)
