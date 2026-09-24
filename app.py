from flask import Flask
import os

app = Flask(__name__)
app.json.ensure_ascii = False
app.json.sort_keys = False
app.json.compact = False

from models import File
from models import AnalysisResult
from extensions import db
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:2952246@localhost:5432/analytics-api"
db.init_app(app)

from flask import request
import data_processor

from datetime import datetime

@app.route("/upload", methods=["POST"])
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

@app.route("/data/stats", methods=["GET"])
def get_stats():
    file_id=request.args.get("file_id")
    if file_id is None:
        return {"error": "file_id is required"}, 400
    
    file=File.query.get(file_id)
    if file is None:
            return {"error": "File not found"}, 404
    stat=data_processor.calculate_statistics(data_processor.file_to_dataframe(file))

    new_result=AnalysisResult(file_id=file_id, mean=stat.get("mean"), median=stat.get("median"), correlation=stat.get("correlation"),created_at=datetime.now())
    
    db.session.add(new_result)
    db.session.commit()

    return stat

@app.route("/data/clean", methods=["GET"])
def get_clean_data():
    file_id=request.args.get("file_id")
    if file_id is None:
        return {"error": "file id is required"}, 400
    
    file=File.query.get(file_id)
    if file is None:
        return {"error": "File not found"}, 404
    
    cleaned_data=data_processor.clean_data(data_processor.file_to_dataframe(file))
    json_cleaned_data=cleaned_data.to_json(orient='records', indent=2, force_ascii=False)

    return json_cleaned_data

@app.route("/files/<int:file_id>", methods=["GET"])
def read_file(file_id):
    file=File.query.get(file_id)
    if file is None:
        return {"error": "File not found"}, 404

    return {"id": file.id, "filename": file.filename, "file_type": file.file_type, "created_at": file.created_at}

@app.route("/files/<int:file_id>", methods=["PUT"])
def update_file(file_id):
    file=File.query.get(file_id)
    if file is None:
        return {"error": "File not found"}, 404

    try:
        new_file=request.files["file"]
    except KeyError:
        return {"error": "File is required"}, 400

    new_file_type=os.path.splitext(new_file.filename)[1].lower()
    file.filename=new_file.filename
    file.file_type=new_file_type
    file.file_data=new_file.read()
    file.created_at=datetime.now()

    db.session.commit()

    return {"id": file.id, "filename": file.filename, "file_type": file.file_type, "created_at": file.created_at}

@app.route("/files/<int:file_id>", methods=["DELETE"])
def delete_file(file_id):
    file=File.query.get(file_id)
    if file is None:
        return {"error": "File not found"}, 404

    db.session.delete(file)
    db.session.commit()

    return {"ok": "file is deleted"}
    