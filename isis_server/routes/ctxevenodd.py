from flask import request, jsonify
from flask_expects_json import expects_json
from pysis import IsisPool
from pysis.exceptions import ProcessError

from ..ISISCommand import ISISCommand
from ..ISISRequest import ISISRequest
from ..input_validation import get_json_schema
from ..logger import get_logger

CMD_NAME = "ctxevenodd"
logger = get_logger(CMD_NAME)


@expects_json(get_json_schema())
def post_ctx_even_odd():
    """
    Called when a client POSTs to /ctxevenodd
    """

    isis_request = ISISRequest(request)

    output_files = list()
    error = None

    try:
        ctxevenodd = ISISCommand(CMD_NAME)
        ctxevenodd.run(*isis_request.input_files)

        output_files = isis_request.upload_output()

    except ProcessError as e:
        error = e.stderr.decode("utf-8")
        logger.error("{} threw an error: {}".format(CMD_NAME, error))

    isis_request.cleanup()

    return jsonify({
        "to": output_files,
        "err": error
    })
