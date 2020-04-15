from flask_restplus import fields

EXPECT_FIELDS = {
    "url": fields.String(required=True),
}

SERIALIZE_FIELDS = {
    "url": fields.String(),
    "resolution": fields.String()
}
CONVERTER_FIELDS = {
    "url": fields.String(required=True),
    "name": fields.String(required=True),
}
