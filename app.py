from flask import Flask
import os

app = Flask(__name__)
app.json.ensure_ascii = False
app.json.sort_keys = False
app.json.compact = False

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
    file.seek(0)
    file_type = os.path.splitext(file.filename)[1].lower()
    new_file=File(filename=file.filename,file_type=file_type,file_data=file.read(),created_at=datetime.now())

    db.session.add(new_file)
    db.session.commit()
    
    json_data=data.to_json(orient='records', indent=2, force_ascii=False)
    return json_data

with app.app_context():
    db.create_all()
    print("Tables created")

@app.route("/data/stats", methods=["GET"])
def get_stats():
    file_id=request.args.get("file_id")
    file=File.query.get(file_id)
    if file is None:
            return {"error": "File not found"}, 404
    stat=data_processor.calculate_statistics(data_processor.file_to_dataframe(file))

    return stat
