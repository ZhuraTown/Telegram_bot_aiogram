from flask import Flask
from .views import app_route


def create_app():
    app_flask = Flask(__name__)
    app_flask.register_blueprint(app_route)
    return app_flask


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000, host='0.0.0.0')
