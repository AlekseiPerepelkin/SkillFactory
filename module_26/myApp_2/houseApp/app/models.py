from app import db

class Flat(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(100), index=True, unique=False)
    city =  db.Column(db.String(20))
    rooms = db.Column(db.Integer)
    area = db.Column(db.String(5))
    floor = db.Column(db.Integer)
    cost = db.Column(db.Integer)

    def __repr__(self):
        return '<Объевление {}>'.format(self.title)


