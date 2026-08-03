from flask import Flask, render_template, request, send_file
import os

from src.predict import IntrusionDetector

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

detector = IntrusionDetector()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file selected"

    file = request.files["file"]

    if file.filename == "":
        return "No file selected"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    results = detector.predict_dataset(filepath)

    table = results.head(50).to_html(
        classes="table",
        index=False
    )

    total = len(results)
    normal = (results["Prediction"] == "Normal").sum()
    attack = (results["Prediction"] == "Attack").sum()

    return render_template(
        "results.html",
        table=table,
        total=total,
        normal=normal,
        attack=attack
    )


@app.route("/download")
def download():
    return send_file(
        "outputs/predictions.csv",
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)