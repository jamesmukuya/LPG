"""
render and control resources
the filename is in the db, the route is available in our downloads folder
"""
from main import app
from main.resources.form import ResourceRequestForm
from flask import (Blueprint, render_template, send_from_directory,abort,
                   flash, redirect, request, url_for)

resources = Blueprint('resources', __name__)

@resources.route("/resources", methods=["GET", "POST"])
def resources_page():
    form = ResourceRequestForm()
    context={'form':form}
    return render_template('resources/resources.html', title='Resources', **context)

@resources.route("/resources-download/<filename>", methods=["POST"])
def resources_direct_download():
    filename = "link.txt"
    try:
        return send_from_directory(app.config['MISC_UPLOAD_FOLDER'],
                                   filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)
    pass


@resources.route("/resources-download", methods=["POST"])
def resources_get_link():
    pass
