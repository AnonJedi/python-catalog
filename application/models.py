from application import db, bcrypt


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.set_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def set_password_hash(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def __repr__(self):
        return '<Admin username=%s password=%s >' % \
               (self.username, self.password)
