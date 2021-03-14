from flask_expects_json import expects_json
from flask import request, jsonify, current_app
from uuid import uuid4
from os import remove as remove_file
from os import path
from tempfile import gettempdir

from ..logger import get_logger

from pysis import isis
from pysis.exceptions import ProcessError

CMD_NAME = "mroctx2isis"

MRO_CTX_SCHEMA = {
    "type": "object",
    "properties": {
        "from": {"type": "string"},
        "args": {
            "type": "object",
            "properties": {},
        },
    },
    "required": ["args", "from"],
    "additionalProperties": False
}

logger = get_logger(CMD_NAME)


@expects_json(MRO_CTX_SCHEMA)
def post_mro_ctx_2_isis():
    """
    Called when a client POSTs to /mroctx2isis
    """

    # Either output_file or err will be set, but not both
    # output_file is set on success
    # err is set on failure
    input_file = None
    output_file = None
    error = None

    try:
        input_file = current_app.s3_client.download(request.json["from"])

        temp_file_name = path.join(gettempdir(), "{}.cub".format(str(uuid4())))

        logger.debug("Running mroctx2isis...")

        isis.mroctx2isis(from_=input_file, to=temp_file_name)

        output_file = current_app.s3_client.upload(temp_file_name)

        logger.debug("{} completed".format(CMD_NAME))

    except ProcessError as e:
        error = e.stderr.decode("utf-8")
        logger.error("{} threw an error: {}".format(CMD_NAME, error))

    # Clean up
    if input_file is not None and path.exists(input_file):
        remove_file(input_file)

    if output_file is not None and path.exists(output_file):
        remove_file(output_file)

    return jsonify({
        "to": output_file,
        "err": error
    })