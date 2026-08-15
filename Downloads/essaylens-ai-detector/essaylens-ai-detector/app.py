from flask import Flask, render_template, request, jsonify
from detector import analyze_text

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/analyze")
def analyze():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if len(text.split()) < 40:
        return jsonify({"error": "Please enter at least 40 words for a meaningful analysis."}), 400
    return jsonify(analyze_text(text))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
