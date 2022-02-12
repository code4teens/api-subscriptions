from flask import Blueprint, jsonify, request

from database import db_session
from models import Subscription
from schemata import SubscriptionSchema

api_subscriptions = Blueprint('api_subscriptions', __name__)


@api_subscriptions.route('/subscriptions')
def get_subscriptions():
    subscriptions = Subscription.query.order_by(Subscription.id).all()
    data = SubscriptionSchema(many=True).dump(subscriptions)

    return jsonify(data), 200


@api_subscriptions.route('/subscriptions', methods=['POST'])
def create_subscription():
    keys = ['email']

    if sorted([key for key in request.json]) == sorted(keys):
        email = request.json.get('email')
        existing_subscription = Subscription.query.filter_by(email=email)\
            .one_or_none()

        if existing_subscription is None:
            subscription_schema = SubscriptionSchema()

            try:
                subscription = subscription_schema.load(request.json)
            except Exception as _:
                data = {
                    'title': 'Bad Request',
                    'status': 400,
                    'detail': 'Some values failed validation'
                }

                return data, 400
            else:
                db_session.add(subscription)
                db_session.commit()
                data = {
                    'title': 'Created',
                    'status': 201,
                    'detail': f'Subscription created'
                }

                return data, 201
        else:
            data = {
                'title': 'Conflict',
                'status': 409,
                'detail': 'Subscription already exists'
            }

            return data, 409
    else:
        data = {
            'title': 'Bad Request',
            'status': 400,
            'detail': 'Missing some keys or contains extra keys'
        }

        return data, 400
