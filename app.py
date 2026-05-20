from flask import Flask, render_template, request, jsonify
import os
from extractor import analyze_paper

# Start the Flask app
app = Flask(__name__)

# Tell Flask where uploaded files go
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    """
    Home page.
    When someone visits localhost:5000 this runs
    and returns the index.html page.
    """
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    This runs when the user uploads a PDF and clicks Analyze.
    It receives the file, saves it, analyzes it,
    deletes it, and returns the result as JSON.
    """

    # Make sure a file was sent
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # Make sure user actually selected something
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Make sure it is a PDF
    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Please upload a PDF file"}), 400

    # Save the file temporarily
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # Run the analysis
    try:
        result = analyze_paper(filepath)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Delete the file after processing
        # We never permanently store user files
        if os.path.exists(filepath):
            os.remove(filepath)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)