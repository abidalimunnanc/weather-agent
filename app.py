from flask import Flask, request, render_template_string
from agent import run_agent

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather Agent</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: teal; }
        input { padding: 10px; width: 300px; }
        button { padding: 10px; background: teal; color: white; border: none; }
        .response { margin-top: 20px; padding: 10px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <h1>🌤️ Gemini Weather Agent</h1>
    <form method="POST">
        <input type="text" name="query" placeholder="Ask about the weather..." required>
        <button type="submit">Ask</button>
    </form>
    {% if response %}
    <div class="response"><b>Answer:</b> {{ response }}</div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        query = request.form.get("query")
        response = run_agent(query)
    return render_template_string(HTML, response=response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
