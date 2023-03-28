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
    try:
        current_equation = session.get('equation', 1)
        user_text = speech_to_text()
        text_to_speech(user_text)
        math_command = text_to_math(user_text)

        # Change equation: "Équation [nº de l'équation]"
        if math_command.startswith('Équation'):
            cmd = math_command.split()
            session['equation'] = int(cmd[1]) if len(cmd) > 1 else 1

        # Read a line: "Lire/Relire ligne [nº de la ligne]"
        elif math_command.startswith('Lire') or math_command.startswith('Relire'):
            cmd = math_command.split()
            line = int(cmd[2])
            items = db.session.query(Item).filter_by(equation=current_equation, line=line).order_by(Item.block).all()
            line_text = ''.join(item.data for item in items)
            text_to_speech(line_text)

        # Edit a line: "Modifier ligne [nº de la ligne], [nouvelle ligne]"
        elif math_command.startswith('Modifier') or math_command.startswith('Modifiez'):
            cmd = math_command.split()
            line = int(cmd[2])
            blocks = parse_equation(' '.join(cmd[3:]))
            db.session.query(Item).filter_by(equation=current_equation, line=line).delete()
            db.session.add_all([Item(equation=current_equation, line=line, block=i+1, data=v) for i, v in enumerate(blocks)])
            db.session.commit()

        # Delete a line: "Supprimer ligne [nº de la ligne]"
        elif math_command.startswith('Supprimer') or math_command.startswith('Supprimez'):
            cmd = math_command.split()
            line = cmd[2]
            db.session.query(Item).filter_by(equation=current_equation, line=line).delete()
            db.session.query(Item).filter(Item.equation == current_equation, Item.line > line).update({Item.line: Item.line - 1}, synchronize_session='fetch')
            db.session.commit()

        # Copy/paste a line: "Copier ligne [nº de la ligne], coller ligne [nº de la ligne]"
        elif math_command.startswith('Copier') or math_command.startswith('Copiez'):
            cmd = math_command.split()
            last_line = db.session.query(Item).filter_by(equation=current_equation).order_by(Item.line.desc()).first()
            line = cmd[2] if len(cmd) >= 3 else last_line.line
            items = db.session.query(Item).filter_by(equation=current_equation, line=line).all()
            line_text = ' '.join(item.data for item in items)
            blocks = parse_equation(line_text)
            newline = cmd[5] if len(cmd) >= 6 else last_line.line + 1
            db.session.query(Item).filter(Item.equation == current_equation, Item.line >= newline).update({Item.line: Item.line + 1}, synchronize_session='fetch')
            db.session.add_all([Item(equation=current_equation, line=newline, block=i+1, data=v) for i, v in enumerate(blocks)])
            db.session.commit()

        # Cut/paste a line: "Couper ligne [nº de la ligne], coller ligne [nº de la ligne]"
        elif math_command.startswith('Couper') or math_command.startswith('Coupez'):
            cmd = math_command.split()
            last_line = db.session.query(Item).filter_by(equation=current_equation).order_by(Item.line.desc()).first()
            line = cmd[2] if len(cmd) >= 3 else last_line.line
            items = db.session.query(Item).filter_by(equation=current_equation, line=line).all()
            line_text = ' '.join(item.data for item in items)
            db.session.query(Item).filter_by(equation=current_equation, line=line).delete()
            db.session.query(Item).filter(Item.equation == current_equation, Item.line > line).update({Item.line: Item.line - 1}, synchronize_session='fetch')
            db.session.commit()
            blocks = parse_equation(line_text)
            newline = cmd[5] if len(cmd) >= 6 else last_line.line + 1
            db.session.query(Item).filter(Item.equation == current_equation, Item.line>= newline).update({Item.line: Item.line + 1}, synchronize_session='fetch')
            db.session.add_all([Item(equation=current_equation, line=newline, block=i+1, data=v) for i, v in enumerate(blocks)])
            db.session.commit()

        # Add a line: "[nouvelle ligne]"
        else:
            blocks = parse_equation(math_command)
            last_line = db.session.query(Item).filter_by(equation=current_equation).order_by(Item.line.desc()).first()
            line = last_line.line + 1 if last_line else 1
            db.session.add_all([Item(equation=current_equation, line=line, block=i+1, data=v) for i, v in enumerate(blocks)])
            db.session.commit()

    except:
        error_message = "Une erreur s'est produite lors du traitement de votre commande. Veuillez réessayer."
        text_to_speech(error_message)

    finally:
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
