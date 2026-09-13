from flask import Flask

app = Flask(__name__)

from flask import request
import data_processor

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

    data=data_processor.clean_data(data)
    
    json_data=data.to_json(orient='records', indent=2)
    return json_data