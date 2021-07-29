import json

import pytest

from s3handle.create_obj import app


def test_lambda_handler():
    pass
    ret = app.lambda_handler("", "")
    # data = json.loads(ret)
    #
    # assert ret["statusCode"] == 200
    # assert "message" in ret["body"]
    # assert data["message"] == "hello world"
    # assert "location" in data.dict_keys()
