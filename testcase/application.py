from sanic import Sanic
from sanic.response import json as jsonify

import sys
sys.path.append("..")
from tracer import set_tracer, Tracer

app = Sanic("for_testcase")

SUCCESS = 0
ERROR = 101


@app.route("/login", methods=["GET"])
async def login(request):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username:
        return jsonify({"code": ERROR, "message": "empty username"}, status=400)
    if not password:
        return jsonify({"code": ERROR, "message": "empty password"}, status=400)

    if username == "admin" and password == "1234567":
        return jsonify(
            {
                "code": SUCCESS,
                "data": {"token": "59QN8jDdfaPWWi"},
                "message": "success",
            },
            status=200,
        )
    else:
        return jsonify({"code": ERROR, "message": "wrong account info"}, status=400)


@app.route("/signup", methods=["POST"])
async def new_user(request):
    username = request.json.get("username")
    password = request.json.get("password")

    if username is None or password is None:
        return jsonify(
            {"code": ERROR, "message": "fields should not empty"}, status=400
        )
    if username == "admin":
        return jsonify(
            {"code": ERROR, "message": "username already exists"}, status=400
        )
    return jsonify({"code": SUCCESS, "message": "success"}, status=200)


if __name__ == "__main__":
    t = Tracer('./')
    set_tracer(t.tracer)
    app.run()
    t.tracer_end()
