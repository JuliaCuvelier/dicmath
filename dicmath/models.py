from dicmath import db


class Item(db.Model):
    """Represents an individual item of an equation.

    Attributes:
        id (int): The unique identifier for the item.
        equation (int): The equation number to which the item belongs.
        line (int): The line number within the equation.
        block (int): The block number within the line.
        data (str): The data contained in the item (e.g., a mathematical symbol or number).
    """
    id = db.Column(db.Integer, primary_key=True)
    equation = db.Column(db.Integer)
    line = db.Column(db.Integer)
    block = db.Column(db.Integer)
    data = db.Column(db.String(100))
