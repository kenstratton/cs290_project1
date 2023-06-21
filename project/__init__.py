# __init__.py


# Config --------------------------------------------------

import os
from flask import Flask, request, render_template

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
    return render_template("management/errors/403.html"), 403

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('management/errors/404.html', path=request.path), 404

# Internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('management/errors/500.html'), 500

# Views for Incidents -------------------------------------

# Maintenance page
@app.route('/maintenance')
def under_maintenace():
    return render_template('management/maintenance.html')