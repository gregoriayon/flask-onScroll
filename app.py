from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
# app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:201830011@localhost/test_01'
db = SQLAlchemy(app)

# from models import *
# from routes import *

class Item(db.Model):
    # __table__ = "items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    member_type = db.Column(db.String(120), nullable=True)
    age = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'member_type': self.member_type,
            'age': self.age
        }
    
with app.app_context():
    db.create_all()


@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])


@app.route('/item/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify(item.to_dict())


@app.route('/item', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = Item(name=data['name'], description=data.get('description'))
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

@app.route('/index')
def onScrollPagination():
    # ALTER TABLE item
    # ADD COLUMN member_type VARCHAR DEFAULT 'dealer';

    # ALTER TABLE item
    # ADD COLUMN age INT DEFAULT 0;


    # INSERT INTO Item (name, description, member_type, age)
    # SELECT
    #     -- Generate random names
    #     'Item-' || trunc(random() * 1000)::TEXT AS name,
        
    #     -- Generate random descriptions
    #     'Description-' || trunc(random() * 100)::TEXT AS description,
        
    #     -- Random member_type values ('Gold', 'Silver', 'Bronze')
    #     CASE
    #         WHEN random() < 0.33 THEN 'Gold'
    #         WHEN random() < 0.66 THEN 'Silver'
    #         ELSE 'Bronze'
    #     END AS member_type,
        
    #     -- Random age between 18 and 65
    #     trunc(random() * (65 - 18) + 18)::INT AS age
    # FROM
    #     generate_series(1, 100);

    return render_template('index.html')

@app.route('/on-scroll-data')
def onScrollData():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)
    

    # Query the database
    query = Item.query.order_by(Item.age.asc())
    paginated_data = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Serialize the data
    data = {
        'items': [{
            'id': item.id,
            'name': item.name,
            'age': item.age,
            'member_type': item.member_type,
            'description': item.description

        } for item in paginated_data.items],
        'total': paginated_data.total,
        'pages': paginated_data.pages,
        'per_page': paginated_data.per_page,
        'current_page': paginated_data.page
    }
    # print(data)
    return jsonify(data)


# @app.route('/item/<int:id>', methods=['PUT'])
# def update_item(id):
#     data = request.get_json()
#     item = Item.query.get_or_404(id)
#     item.name = data['name']
#     item.description = data.get('description')
#     db.session.commit()
#     return jsonify(item.to_dict())


# @app.route('/item/<int:id>', methods=['DELETE'])
# def delete_item(id):
#     item = Item.query.get_or_404(id)
#     db.session.delete(item)
#     db.session.commit()
#     return '', 204

## -- user model
class users(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)
    photo = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    users_roles = db.Column(db.String)
    acc_type = db.Column(db.String)
    user_id = db.Column(db.String)
    branch = db.Column(db.String)
    name = db.Column(db.String)
    email_status = db.Column(db.String)
    phone_status = db.Column(db.String)
    phone = db.Column(db.String)
    account_status = db.Column(db.String)
    exchange = db.Column(db.String)
    dealer_group_id = db.Column(db.String)
    max_login = db.Column(db.Integer)
    logged_in = db.Column(db.Integer)
    last_login = db.Column(db.String)
    login_ip = db.Column(db.String)
    premium = db.Column(db.Boolean)
    premium_start_date = db.Column(db.String)
    premium_end_date = db.Column(db.String)
    max_login_mobile = db.Column(db.Integer)
    logged_in_mobile = db.Column(db.Integer)
    total_max_login = db.Column(db.Integer)
    total_logged_in = db.Column(db.Integer)
    margin_allowed = db.Column(db.Boolean, default=False)
    ac_status_update_by = db.Column(db.String)
    ac_status_update_time = db.Column(db.String)
    parking_enabled = db.Column(db.Boolean, default=False)
    is_bulk_order = db.Column(db.Boolean, default=False)
    first_login = db.Column(db.Boolean, default=False)
    login_otp = db.Column(db.Boolean, default=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)

    def get_name(self):
        return str(self.username)

    def get_role(self):
        return str(self.users_roles).lower()

    def get_email(self):
        return str(self.email)

    def get_phone(self):
        return str(self.phone)

@app.route('/')
def userRegister():
    return render_template('register.html')


import re
import uuid
from sqlalchemy import text

from utils import utils

@app.route('/adduser', methods=['POST'])
def addNewUser():
    form = request.get_json()
    # print(Config.BROKER_NAME)

    if not form:
        return jsonify(error="Invalid or missing JSON payload"), 400

    required_fields = ['users_roles', 'branch', 'username', 'password', 'confirm_password']
    user_role = form.get('users_roles', '').lower()
    if user_role == 'brokertrader':
        required_fields.append('exchange')
    
    if user_role == 'client':
        required_fields += ['phone', 'email']

    missing_fields = [field for field in required_fields if field not in form or not form[field]]
    if missing_fields:
        return jsonify(errors=[f"{field} is required" for field in missing_fields]), 400

    username = form['username'].strip()
    password = form['password']
    cpassword = form['confirm_password']
    email = form.get('email', None)
    phone = form.get('phone', None)
    new_otp = str(utils.random_num(5))

    if len(username) > 25:
        return jsonify(errors=["Username can't be more than 25 characters"]), 400

    if not re.match("^[a-zA-Z0-9_]*$", username):
        return jsonify(errors=["Username can only contain letters, numbers, and underscores"]), 400

    if password != cpassword:
        return jsonify(errors=["Passwords do not match"]), 400
    
    if email and not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        return jsonify(errors=["Invalid email format"]), 400

    # try:
    #     password_errors = utils.validate_password_policy(password)
    #     if password_errors:
    #         return jsonify(errors=password_errors), 400
    # except Exception as ex:
    #     return jsonify(errors=["Password validation error", str(ex)]), 500

    exist = users.query.filter(users.username.ilike(username)).first()
    if exist:
        return jsonify(errors=["User already exists"]), 400

    new_user = users()
    new_user.username = username
    new_user.password = utils.hash_password(password)
    new_user.email = email.strip() if email else email
    # new_user.photo = form.get('photo', '')
    new_user.users_roles = user_role
    new_user.acc_type = 'UFTC'  # hardcoded broker name (or replace)
    new_user.user_id = 'b_' + str(uuid.uuid4())
    new_user.branch = form['branch']
    new_user.name = form.get('name', None)
    new_user.phone = phone
    new_user.exchange = form.get('exchange', None)
    new_user.email_status = 'Verified'
    new_user.phone_status = 'Verified'
    new_user.account_status = 'inactive'
    new_user.premium = False
    new_user.margin_allowed = str(form.get('margin_allowed', 'false')).lower() == 'true'
    new_user.parking_enabled = str(form.get('parking_enabled', 'false')).lower() == 'true'
    new_user.is_bulk_order = str(form.get('is_bulk_order', 'false')).lower() == 'true'
    new_user.first_login = True
    new_user.max_login = 1
    new_user.max_login_mobile = 1
    new_user.logged_in = 0
    new_user.logged_in_mobile = 0
    new_user.total_max_login = 1
    new_user.total_logged_in = 0

    try:
        setting_query = text("""
            INSERT INTO user_settings (user_id, username, sms_status, email_status, otp)
            VALUES (:user_id, :username, FALSE, TRUE, :otp)
        """)
        db.session.execute(setting_query, {
            "user_id": new_user.user_id,
            "username": username,
            "otp": new_otp
        })

        profile_query = text("""
            INSERT INTO user_profiles (cln_id, username, profile_id, profile_name, profile_data, selected_pid)
            VALUES (:cln_id, :username, '1', 'Default', 'localstorage', TRUE)
        """)
        db.session.execute(profile_query, {
            "cln_id": new_user.user_id,
            "username": username
        })

        db.session.add(new_user)
        db.session.commit()

        # if email:
        #     utils.send_account_info(
        #         form.get('name', ''),
        #         username,
        #         email,
        #         password
        #     )

        return jsonify(message=["User created successfully"]), 201

    except Exception as ex:
        db.session.rollback()
        return jsonify(errors=["Error inserting record", str(ex)]), 500



if __name__ == '__main__':
    app.run(debug=True)
