from views import app
from models import connect_to_db

if __name__ == '__main__':
    app.secret_key = 'secretzzzz'
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)
    # if app.debug:
    from flask_debugtoolbar import DebugToolbarExtension
    DebugToolbarExtension()
    app.run()
