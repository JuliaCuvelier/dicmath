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
    equation = session.get('equation', 1)
    text = speech_to_text()
    text_to_speech(text)
    math = text_to_math(text)

    # Change equation: "Équation [nº de l'équation]"
    if math.startswith('Équation'):
        cmd = math.split()
        session['equation'] = int(cmd[1]) if len(cmd) > 1 else 1

    # Read a line: "Ligne [nº de la ligne]"
    elif math.startswith('Ligne'):
        cmd = math.split()
        line = int(cmd[1])
        items = db.session.query(Item).filter_by(equation=equation, line=line).order_by(Item.block).all()
        line_text = ''.join(item.data for item in items)
        text_to_speech(line_text)

    # Edit a line: "Modifier ligne n, [nouvelle ligne]"
    elif math.startswith('Modifier') or math.startswith('Modifiez'):
        cmd = math.split()
        line = cmd[2]
        blocks = parse_equation(' '.join(cmd[3:]))
        db.session.query(Item).filter_by(equation=equation, line=line).delete()
        db.session.add_all([Item(equation=equation, line=line, block=i+1, data=v) for i, v in enumerate(blocks)])
        db.session.commit()

    # Delete a line: "Supprimer ligne [nº de la ligne]"
    elif math.startswith('Supprimer') or math.startswith('Supprimez'):
        cmd = math.split()
        line = cmd[2]
        db.session.query(Item).filter_by(equation=equation, line=line).delete()
        db.session.query(Item).filter(Item.equation == equation, Item.line > line).update({Item.line: Item.line - 1}, synchronize_session="fetch")
        db.session.commit()

    # Add a line: "[nouvelle ligne]"
    else:
        blocks = parse_equation(math)
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
