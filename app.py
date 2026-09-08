from flask import Flask

app = Flask(__name__)

from flask import request

@app.route("/api/v1/files", methods=["POST"])
def get_files():
    file=request.files["file"]
    return file