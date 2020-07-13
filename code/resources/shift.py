from datetime import datetime
from flask_restful import Resource, reqparse
from models.shift import ShiftModel
from models.user import UserModel

class Shift(Resource):
    pass

class ShiftList(Resource):
    
    def get(self):
        shifts = ShiftModel.query.all()
        return {'shifts': [shift.json() for shift in shifts]}

class ShiftClockIn(Resource):

    def post(self, id):
        user = UserModel.query.filter_by(id=id).first()

        shift = ShiftModel.query.filter_by(user_id=user.id, clocked_out_at=None).first()

        if user is None:
            return {'message': 'Unable to find user.'}

        if shift:
            return {'message': 'You are already clocked in.'}

        shift = ShiftModel(user_id=user.id)
        shift.save()

        return {'message': f"You clocked in at {shift.clocked_in_at}."}

class ShiftClockOut(Resource):

    def post(self, id):
        user = UserModel.query.filter_by(id=id).first()

        if user is None:
            return {'message': 'Unable to find user.'}

        shift = ShiftModel.query.filter_by(user_id=user.id, clocked_out_at=None).first()

        if shift:
            shift.clocked_out_at = datetime.now()
            diff = shift.clocked_out_at - shift.clocked_in_at
            minutes = diff.seconds / 60
            hours = minutes / 60
            shift.shift_duration = format(hours, ".2f")
            shift.save()
            return {'message': f"You clocked out at {shift.clocked_out_at}."}

        return {'message': 'You are not currently clocked in.'}
