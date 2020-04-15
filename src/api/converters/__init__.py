import os
import shutil
import subprocess
from http import HTTPStatus

from flask import send_from_directory
from flask_restplus import Namespace, Resource

from src.api.converters.decorators import url_from_body, name_from_body
from src.api.converters.fields import SERIALIZE_FIELDS, EXPECT_FIELDS, CONVERTER_FIELDS
from src.m3u8_playlist.playlist_converter import fetch_all_urls, generate_list_of_files
from src.m3u8_playlist.playlist_grapper import resolutions
from src.m3u8_playlist.playlist_parser import get_playlist_uris, get_base_url

CONVERTERS = Namespace(name="converters", description="Endpoints for converters.")

SERIALIZE_MODEL = CONVERTERS.model(name="converter_serialize_model", model=SERIALIZE_FIELDS)
EXPECT_MODEL = CONVERTERS.model(name="converter_expect_model", model=EXPECT_FIELDS)
CONVERT_MODEL = CONVERTERS.model(name="converter_expect_model", model=CONVERTER_FIELDS)


@CONVERTERS.route("/")
class ListConverters(Resource):
    # Get possible resolutions.
    @CONVERTERS.expect(EXPECT_MODEL)
    @CONVERTERS.marshal_with(SERIALIZE_MODEL)
    @url_from_body
    def get(self, url):
        res = resolutions(url=url)
        return {"resolutions": res}, HTTPStatus.OK

    @CONVERTERS.expect(CONVERT_MODEL)
    @url_from_body
    @name_from_body
    def post(self, url, name):
        # Download all the parts.
        playlist_urls = get_playlist_uris(playlist_url=url)

        # part name
        base_url = get_base_url(playlist_url=url)

        # Combine to one video file.
        fetch_all_urls(uris=playlist_urls, part_name=base_url)

        generate_list_of_files()
        # Serve the file.
        filename = f"{name}.mp4"
        directory = "/tmp/video_parts"

        subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "parts.txt", "-c", "copy",
                        os.path.join(directory, filename)])
        shutil.rmtree(directory)

        return send_from_directory(directory=directory, filename=filename)
