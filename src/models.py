from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)   #nullable el espacio no puede quedar vacio
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
           # "username": self.username,
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    done = db.Column(db.Boolean(), nullable=False)
    label = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Todo %r>' % self.label

    def serialize(self):
        return {
            "id": self.id,
            "label": self.label,
            "done": self.done,
            # do not serialize the password, its a security breach
        }