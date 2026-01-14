from flask import Flask
from flask_cors import CORS
from routes import blueprints

"""
SHACL Dashboard Backend App (Development Version)

- Serves ONLY the API (Flask)
- Frontend is served by Vite (localhost:5173)
- Avoids port 80 (macOS permission issues)
"""

app = Flask(__name__)
CORS(app)

for bp in blueprints:
    app.register_blueprint(bp)


@app.route("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5001
    )
