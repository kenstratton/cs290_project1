# __init__.py


# Config --------------------------------------------------

import os
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])




# Extensions ----------------------------------------------

from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

mail = Mail(app)
toolbar = DebugToolbarExtension(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)




# Assets ----------------------------------------------
#* scssはwebpackでの実装に変更

# from flask_assets import Environment, Bundle
# assets = Environment(app)
# assets.url = app.static_url_path
# bundles = {
#     'main_scss': Bundle(
#         'scss/sample.scss',
#         filters='libsass',
#         output='main.css'
#     )
# }
# assets.register(bundles)





# Blueprints ----------------------------------------------

# import project.views
from project.admin.views import admin_bp
from project.user.views import user_bp

app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)




# Error handlers ------------------------------------------

# No permission to access the server
@app.errorhandler(403)
def forbidden_page(e):
    return render_template("errors/403.html"), 403

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

# Internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('errors/500.html'), 500