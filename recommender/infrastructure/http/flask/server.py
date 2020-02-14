from flask import Flask


class FlaskServer:

    app = Flask("mgr")

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    def get_server(self):
        return self.app
