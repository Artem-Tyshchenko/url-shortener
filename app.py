from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from random import choices
from datetime import datetime, timedelta
import string
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(6))
    exp_date =  db.Column('exp_date', db.DateTime)

    def __init__(self, long, short, exp_date):
        self.long = long
        self.short = short
        self.exp_date = exp_date

def shorten_url():
    characters = string.digits + string.ascii_letters
    rand_string = ''.join(choices(characters, k=6))
    short_url = Urls.query.filter_by(short=rand_string).first()
    if not short_url:
        return rand_string


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        url_received = request.form["nm"]
        found_url = Urls.query.filter_by(long=url_received).first()
        if found_url:
            if found_url.exp_date < datetime.now():
                db.session.delete(found_url)
                exp_date = datetime.now() + timedelta(minutes=60)
                short_url = shorten_url()
                print(short_url)
                new_url = Urls(url_received, short_url, exp_date)
                db.session.add(new_url)
                db.session.commit()
                return redirect(url_for("display_short_url", url=short_url))
            else:
                return redirect(url_for("display_short_url", url=found_url.short))
        else:
            exp_date = datetime.now() + timedelta(minutes=60)
            short_url = shorten_url()
            print(short_url)
            new_url = Urls(url_received, short_url, exp_date)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))
    else:
        return render_template('url_page.html')

@app.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first() 
    if long_url:
        return redirect(long_url.long)
    else:
        return f'<h1>Url doesn`t exist</h1>'

@app.route('/display/<url>')
def display_short_url(url):
    return render_template('shorturl.html', short_url_display=url)

if __name__ == '__main__':
    app.run(port=5000, debug=False)
