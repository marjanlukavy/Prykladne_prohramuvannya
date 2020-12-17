from flask import Flask

def create_app():

    app = Flask(__name__)


    @app.route("/api/v1/hello-world-<id>", methods=["GET"])
    def returnHello(id):
        return "Hello World "+id

    return app