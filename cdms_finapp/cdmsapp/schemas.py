from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class PlainEventSchema(Schema):
    event_id = fields.Int(dump_only=True)
    event_title = fields.Str(required=True)
    event_venue = fields.Str(required=True)
    event_address=fields.Str(required=True)
    event_date = fields.Str(required=True)
    event_time = fields.Str(required=True)

class TokenBlockListSchema(Schema):
    id = fields.Int(dump_only=True)
    jti = fields.Str(required=True)
    created_at = fields.Str(required=True)

class PlainParticipantSchema(Schema):
    id=fields.Int(dump_only=True)
    fullname = fields.Str(required=True)
    designation = fields.Str(required=True)
    email = fields.Str(required=True)
    mobilenumber = fields.Str(required=True)
    state = fields.Str(required=True)
    district = fields.Str(required=True)
    block = fields.Str(required=True)
    grampanchayat = fields.Str(required=True)

class ParticpantSchema(PlainParticipantSchema):
    event_id = fields.Int(required=True, load_only=True)
    event = fields.Nested(PlainEventSchema(), dump_only=True)

class EventSchema(PlainEventSchema):
    participants = fields.List(fields.Nested(PlainParticipantSchema()), dump_only=True)
    
# External API models
class IndiaPincodeSchema(Schema):
    searchby = fields.Str()
    value = fields.Int()
# end External API
class projectDataSchema(Schema):
    id = fields.Int()
    shortname = fields.Str()
    fullname =fields.Str()
    germanname = fields.Str()
    project_number = fields.Str()
    from_date = fields.Str()
    to_date =fields.Str()
    comm_value = fields.Float()
    av = fields.Str()
    dv = fields.Str()
    fm = fields.Str()
    vgk = fields.Str()

class pywfSchema(Schema):
    id = fields.Int()
    year = fields.Str()
    fullname =fields.Str()
    tag = fields.Str()
    budget = fields.Str()
    allocated = fields.Str()
    planned =fields.Str()

class FinancialDataSchema(Schema):
    id = fields.Int()
    month_year = fields.Str()
    minor_head = fields.Str()
    planned = fields.Str()
    actuals = fields.Str()