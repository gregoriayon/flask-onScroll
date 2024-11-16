from app import db, app

class Item(db.Model):
    # __table__ = "items"
    id = db.Column(db.Integer, primary_key=True, autoincremeent=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    
with app.app_context():
    db.create_all()
