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

@app.route('/')
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
    print(data)
    
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



if __name__ == '__main__':
    app.run(debug=True)
