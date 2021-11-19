from main import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "flasklogin-users"
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False)
    
    email = db.Column(db.String(40), unique=True, nullable=False)
    
    password = db.Column(db.String(200), nullable=False)
    
    is_admin = db.Column(db.Boolean(), nullable=False, server_default="False")

    is_superadmin = db.Column(db.Boolean(), nullable=False, server_default="False")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    