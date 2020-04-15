"""
This module is used for adding namespaces to the api.
"""
from flask import make_response
from flask_restplus import Api

from src.api.converters import CONVERTERS

API = Api(
    title="Kultura Converter API",
    version="1.0.0",
    description="API for Kultura converter.",
    contact_email="joergenson@eboy.dk",
    doc="/",
    default_mediatype="application/json",
    contact_url="https://github.com/joergenson/kultura-converter",
)


@API.representation("application/xml")
def xml(data, code, headers=None):
    resp = make_response(data, code)
    resp.headers.extend(headers or {})
    return resp


API.add_namespace(CONVERTERS)
