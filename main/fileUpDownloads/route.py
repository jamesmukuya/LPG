"""
file upload and downloads
"""
import os, string
from main import app
from flask import (Blueprint, send_from_directory, abort, render_template,
                    flash,redirect,request,url_for)
from werkzeug.utils import secure_filename

download_file = Blueprint('download_file', __name__)
upload_file = Blueprint('upload_file', __name__)

#@download_file.route("/download/<filename>")
@download_file.route("/download/<path:filename>")
def download(filename):
    #filename = "link.txt"
    try:
        return send_from_directory(app.config['MISC_UPLOAD_FOLDER'],
            filename=filename,as_attachment=True)
    except FileNotFoundError:
        abort(404)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@upload_file.route("/upload", methods=["GET","POST"])
def upload():
    
    #print(app.config['UPLOAD_FOLDER']+'somedir/'+'this.txt')
    if request.method == 'POST':
        # check if user is authenticated to upload files
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'error')
            #return render_template("uploadHtml/upload-file.html", title='Upload')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file','error')
            return redirect(request.url)
        # file is loaded and meets requirements
        # get the destination folder and save the file
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # get title, description and flag
            file_title = string.capwords(request.form['file_title'])
            descr = request.form['description']
            flag = request.form['flag']
            
            # get the destination folder selected
            dest_name = request.form['location']
            # create destination path
            dest = os.path.join(
                app.config['UPLOAD_FOLDER'], dest_name)
            
            # if the destination is a directory
            if not os.path.isdir(dest):
                os.mkdir(dest)
            try:
                #save the file
                file.save(os.path.join(dest, filename))
                flash(f'{file_title} has been uploaded', 'success')
                return redirect(url_for('upload_file.upload'))
                #return render_template("uploadHtml/upload-file.html", title='Upload')
            # if directory does not exist create one
            except FileNotFoundError:
                os.mkdir(app.config['UPLOAD_FOLDER'] + dest_name)
                
            except Exception as e:
                flash(f'AN ERROR HAS OCCURED,{e}, contact admin for rectification',
                'error')
            # save the file
            file.save(os.path.join(dest,filename))

            #return redirect(url_for('uploaded_file',
                                    #filename=filename))
            return render_template("uploadHtml/upload-file.html", title='Upload')
    return render_template("uploadHtml/upload-file.html", title='Upload')


@upload_file.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
