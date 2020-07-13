from db import db
from datetime import datetime

class ShiftModel(db.Model):
    __tablename__ = 'shifts'

    id = db.Column(db.Integer, primary_key=True)
    clocked_in_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    clocked_out_at = db.Column(db.DateTime)
    private_hours = db.Column(db.Float)
    regular_hours = db.Column(db.Float)
    shift_duration = db.Column(db.Float(precision=2))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'shift_duration': self.shift_duration,
            'clocked_in_at': str(self.clocked_in_at),
            'clocked_out_at': str(self.clocked_out_at),
            'private_hours': self.private_hours,
            'regular_hours': self.regular_hours,
            'user': self.user.json()
        }