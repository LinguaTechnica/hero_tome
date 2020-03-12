from flask import Flask
from models import connect_to_db


def app_factory(config_obj):
    """
    Create a new application instance.
    :param config_obj: `str` with dot notation (ex. 'app.settings.prod')
    :return: `Flask` app object
    """
    app = Flask(__name__)
    app.config.from_object(config_obj)

    # Initialize modules
    connect_to_db(app)

    # Register all blueprints
    # register_all_blueprints(app)

    # Return application process
    return app
