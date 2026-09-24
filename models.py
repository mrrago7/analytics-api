from extensions import db

class File(db.Model):
    __tablename__="files"
    id=db.Column(db.Integer, primary_key=True)
    filename=db.Column(db.String)
    file_type=db.Column(db.String)
    file_data=db.Column(db.LargeBinary)
    created_at=db.Column(db.DateTime)

    
