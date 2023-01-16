from flask import redirect, render_template, session, url_for

from dicmath import app, db
from dicmath.models import Item
from dicmath.utils import *


@app.route('/')
def index():
    items = db.session.query(Item).all()
    equations = items_to_equations(items)
    return render_template('index.html', equations=equations)


@app.route('/listen')
def listen():
    text = speech_to_text()
    text_to_speech(text)

    math = text_to_math(text)
    blocks = parse_equation(math)

    last = db.session.query(Item).order_by(Item.equation.desc(), Item.line.desc(), Item.block.desc()).first()
    equation = last.equation if last else 1
    line = last.line + 1 if last else 1

    db.session.add_all([Item(equation=equation, line=line, block=i+1, data=v) for i, v in enumerate(blocks)])
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/clear')
def clear():
    db.session.query(Item).delete()
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/export')
def export():
    items = db.session.query(Item).all()
    equations = items_to_equations(items)
    export_pdf(equations)
    return ('', 204)
