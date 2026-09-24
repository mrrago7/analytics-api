from extensions import db

class File(db.Model):
    __tablename__="files"
    id=db.Column(db.Integer, primary_key=True)
    filename=db.Column(db.String)
    file_type=db.Column(db.String)
    file_data=db.Column(db.LargeBinary)
    created_at=db.Column(db.DateTime)

class AnalysisResult(db.Model):
    __tablename__="analytics"
    id=db.Column(db.Integer, primary_key=True)
    file_id=db.Column(db.Integer)
    mean=db.Column(db.JSON)
    median=db.Column(db.JSON)
    correlation=db.Column(db.JSON)
    created_at=db.Column(db.DateTime)