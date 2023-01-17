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

    if math.startswith('Équation'):
        cmd = math.split()
        session['equation'] = int(cmd[1]) if len(cmd) > 1 else 1
        return ('', 204)

    else:
        blocks = parse_equation(math)

        equation = session['equation'] if 'equation' in session else 1
        last = db.session.query(Item).filter_by(equation=equation).order_by(Item.id.desc()).first()
        line = last.line + 1 if last else 1

        db.session.add_all([Item(equation=equation, line=line, block=i+1, data=v) for i, v in enumerate(blocks)])
        db.session.commit()

        return redirect(url_for('index'))


@app.route('/clear')
def clear():
    session['equation'] = 1
    db.session.query(Item).delete()
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/export')
def export():
    items = db.session.query(Item).all()
    equations = items_to_equations(items)
    export_pdf(equations)
    return ('', 204)
