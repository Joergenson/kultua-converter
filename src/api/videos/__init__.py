import datetime
from http import HTTPStatus

import jwt
from flask import current_app, request
from flask_restplus import Namespace, Resource
from sqlalchemy import or_

from src.api.auth_resource import AuthResource
from src.api.videos.decorators import id_to_video, create_video, check_password
from src.api.videos.fields import SERIALIZE_FIELDS, SIGNUP_FIELDS, LOGIN_FIELDS
from src.models.videos import Video

VIDEOS = Namespace(name="videos", description="Endpoints for videos.")

MODEL = VIDEOS.model(name="video_model", model=SERIALIZE_FIELDS)
SIGNUP_MODEL = VIDEOS.model(name="videos_signup_model", model=SIGNUP_FIELDS)


@VIDEOS.route("/")
class ListVideos(Resource):
    @VIDEOS.marshal_list_with(MODEL)
    @VIDEOS.param(name="q", description="query property, search for name, email and role.")
    def get(self):
        query_prop = request.args.get("q", None)
        if query_prop is None:
            results = Video.query.all()
        else:
            q = f"%{query_prop}%"
            query = Video.query.filter(
                or_(
                    Video.name.ilike(q),
                    Video.email.ilike(q)
                )
            )
            results = query.all()
        return Video.serialize_list(results), HTTPStatus.OK

    @VIDEOS.expect(SIGNUP_MODEL)
    @VIDEOS.marshal_with(MODEL)
    @create_video
    def post(self, video: Video):
        # send_confirmation_email(video=video)
        return video.serialize(), HTTPStatus.CREATED


@VIDEOS.route("/<string:video_id>")
class VideoById(AuthResource):
    @VIDEOS.marshal_with(MODEL)
    @id_to_video
    def get(self, video: Video):
        return video.serialize(), HTTPStatus.OK

    @VIDEOS.marshal_with(MODEL)
    @id_to_video
    def update(self, video):
        # TODO(HTTP Update provide all keys.)
        return video.serialize(), HTTPStatus.OK

    @VIDEOS.marshal_with(MODEL)
    @id_to_video
    def patch(self, video):
        # TODO(provide a single key and update its value, let everything else remain as it is.)
        return video.serialize(), HTTPStatus.OK

    @VIDEOS.marshal_with(MODEL)
    @id_to_video
    def delete(self, video):
        if video.remove():
            # 2XX - success
            # 4XX - Client error
            # 5XX - Server error
            return "", HTTPStatus.NO_CONTENT  # 204
        return "", HTTPStatus.INTERNAL_SERVER_ERROR  # 500


@VIDEOS.route("/login")
class VideoLogin(Resource):
    @VIDEOS.expect(LOGIN_MODEL)
    @check_password
    def post(self, video: Video):
        token = jwt.encode(payload={"email": video.email,
                                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           key=current_app.config["SECRET_KEY"],
                           algorithm="HS256")

        return {"token": token.decode("UTF-8")}, HTTPStatus.OK
