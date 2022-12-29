from dicmath import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equation = db.Column(db.Integer)
    line = db.Column(db.Integer)
    block = db.Column(db.Integer)
    data = db.Column(db.String(100))
