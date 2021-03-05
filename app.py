from flask import Flask, render_template, request, redirect, url_for, flash
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "Secret Key"
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# can be moved to separate module
class PhoneBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(), nullable=False)

    def __init__(self, first_name, last_name, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def __repr__(self):
        return f"Contact(first_name = {self.first_name}, last_name = {self.last_name}, number = {self.phone_number})"


db.create_all()


@app.route('/')
def index():
    contacts = PhoneBook.query.all()
    return render_template('index.html', contacts=contacts)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']

        mydata = PhoneBook(first_name=first_name,
                           last_name=last_name,
                           phone_number=phone_number)

        db.session.add(mydata)
        db.session.commit()

        # flash("Contact created successfully")

        return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = PhoneBook.query.get(request.form.get('id'))

        my_data.first_name = request.form['first_name']
        my_data.last_name = request.form['last_name']
        my_data.phone_number = request.form['phone_number']

        db.session.commit()

        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
