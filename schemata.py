from marshmallow import fields, post_load, Schema

from models import Subscription


class SubscriptionSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.String()
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_subscription(self, data, **kwargs):
        return Subscription(**data)
