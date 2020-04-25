"""
render and control resources
the filename is in the db, the route is available in our downloads folder
"""
from main.resources.form import ResourceRequestForm
from flask import (Blueprint, render_template,flash, redirect, request, url_for)

resources = Blueprint('resources', __name__)

@resources.route("/resources", methods=["GET", "POST"])
def resources_page():
    # get available resources from the server and pass to context
    filename='link.txt'
    # if user is not logged in render this form to display on request
    form = ResourceRequestForm()
    context={'form':form,'filename':filename}
    return render_template('resources/resources.html', title='Resources', **context)


@resources.route("/resources-link")
def resources_get_link():
    # use an expiring token 10mins
    # use a uuid per download
    pass