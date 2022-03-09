from unicodedata import name
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from helper import get_matnet, get_data

app = Flask(__name__)

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class NameForm(FlaskForm):
    name = StringField('Key in your MATNET (e.g. 567X4567)', validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():
    matnets = get_matnet()
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        matnet = form.name.data
        if matnet.upper() in matnets:
            # empty the form field
            form.name.data = ""
            # redirect the browser to another route and template
            return redirect( url_for('result', id=matnet) )
        else:
            message = f"MATNET {matnet} is not in our database."
    return render_template('index.html', form=form, message=message)

@app.route('/matnet/<id>')
def result(id):
    # run function to get actor data based on the id in the path
    data = get_data(id)
    print(data)  
    if name == "Unknown":
        # redirect the browser to the error template
        return render_template('404.html'), 404
    else:
        # pass all the data for the selected actor to the template
        return render_template('result.html', id=id, name='xxx', photo='xxx', data=data)

# 2 routes to handle errors - they have templates too

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# keep this as is
if __name__ == '__main__':
    app.run()
