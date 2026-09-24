from flask import Flask
import os

app = Flask(__name__)

from models import File
from extensions import db
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:2952246@localhost:5432/analytics-api"
db.init_app(app)

from flask import request
import data_processor

from datetime import datetime

@app.route("/api/v1/files", methods=["POST"])
def get_files():
    try:
        file=request.files["file"]
    except KeyError:
        return {"error": "File is required"}, 400
    try:
        data=data_processor.read_file(file)
    except data_processor.UnsupportedFileType:
        return {"error": "Unsupported file type"}, 415

    file_type = os.path.splitext(file.filename)[1].lower()
    new_file=File(filename=file.filename,file_type=file_type,file_data=file.read(),created_at=datetime.now())

    db.session.add(new_file)
    db.session.commit()

    data=data_processor.clean_data(data)
    
    json_data=data.to_json(orient='records', indent=2)
    return json_data

with app.app_context():
    db.create_all()
    print("Tables created")