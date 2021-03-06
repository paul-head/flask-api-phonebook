from flask import Flask, render_template, request, redirect, url_for, flash
from flask_restful import Api, Resource, fields, marshal_with, abort, reqparse
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

    def __init__(self, id, first_name, last_name, phone_number):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def __repr__(self):
        return f"Contact(first_name = {self.first_name}, last_name = {self.last_name}, number = {self.phone_number})"


db.create_all()


phone_num_args = reqparse.RequestParser()
phone_num_args.add_argument("first_name", type=str, help="First Name is required", required=True)
phone_num_args.add_argument("last_name", type=str, help="Last Name is required", required=True)
phone_num_args.add_argument("phone_number", type=str, help="Phone number is required", required=True)


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


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = PhoneBook.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('index'))


resource_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'phone_number': fields.String,
}


class PhoneBookResource(Resource):
    @marshal_with(resource_fields)
    def get(self, contact_id):
        result = PhoneBook.query.filter_by(id=contact_id).first()
        print(result)
        if not result:
            abort(404, message="Could not find contact")
        return result

    @marshal_with(resource_fields)
    def put(self, contact_id):
        args = phone_num_args.parse_args()
        result = PhoneBook.query.filter_by(id=contact_id).first()
        if result:
            abort(409, message="already exist")

        contact1 = PhoneBook(
            id=contact_id,
            first_name=args['first_name'],
            last_name=args['last_name'],
            phone_number=args['phone_number']
        )

        db.session.add(contact1)
        db.session.commit()

        return contact1, 201


api.add_resource(PhoneBookResource, '/api/<int:contact_id>')

if __name__ == '__main__':
    app.run(debug=True)
