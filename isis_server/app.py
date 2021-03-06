from flask import Flask

from .routes import get_command, get_all_commands, post_start, post_cog, \
    post_email
from .routes.isis import post_spiceinit, post_mro_ctx_2_isis, post_ctx_cal, \
    post_ctx_even_odd, post_cam_2_map, post_isis_2_std
from .xml_reader import XMLReader
from .S3Client import S3Client
from os import path, listdir


STATUS_SERVER_ERROR = 500
STATUS_BAD_REQUEST = 400
XML_LOCATION = path.relpath(path.join(path.dirname(__file__), "..", "xml"))


def get_command_xml():
    """
    :return: A list of all the XML file in the data directory
    """
    all_files = [path.join(XML_LOCATION, f) for f in listdir(XML_LOCATION)]
    return [XMLReader.get_isis_command(f) for f in all_files]


# Create the app
app = Flask(__name__)
app.s3_client = S3Client()
app.isis_commands = get_command_xml()

# ===========
# App routes
# ===========

# Add xml routes
app.add_url_rule('/commands/<command_name>', view_func=get_command, methods=["GET"])
app.add_url_rule('/commands', view_func=get_all_commands, methods=["GET"])

# Add n8n node routes
app.add_url_rule('/start', view_func=post_start, methods=["POST"])
app.add_url_rule('/email', view_func=post_email, methods=["POST"])
app.add_url_rule('/spiceinit', view_func=post_spiceinit, methods=["POST"])
app.add_url_rule('/mroctx2isis', view_func=post_mro_ctx_2_isis, methods=["POST"])
app.add_url_rule('/ctxcal', view_func=post_ctx_cal, methods=["POST"])
app.add_url_rule('/ctxevenodd', view_func=post_ctx_even_odd, methods=["POST"])
app.add_url_rule('/cam2map', view_func=post_cam_2_map, methods=["POST"])
app.add_url_rule('/isis2std', view_func=post_isis_2_std, methods=["POST"])
app.add_url_rule('/cog', view_func=post_cog, methods=["POST"])
