"""
file upload and downloads
"""
from main import app
from flask import Blueprint, send_from_directory, abort, render_template
#from flask import render_template
download_file = Blueprint('download_file', __name__)
upload_file = Blueprint('upload_file', __name__)
download_route = Blueprint('download_route', __name__)

@download_route.route("/file-download")
def dwnld_rte():
    # only logged in users can visit this route
    return render_template("downloadHtml/download_file.html",title='Download')

#@download_file.route("/download")
@download_file.route("/download/<path:filename>")
def download(filename):
	# the link should be avalilable if the current user is authenticated
    # filename will be obtained from a link
    #filename = "link.txt"
    try:
        return send_from_directory(app.config['MISC_UPLOAD_FOLDER'],
            filename=filename,as_attachment=True)
    except FileNotFoundError:
        abort(404)

@upload_file.route("/upload/", methods=["POST"])
def upload():
    return "route to upload files"
