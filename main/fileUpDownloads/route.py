"""
file upload and downloads
"""
import os, string
from main import app
from datetime import datetime
import mysql.connector as sql
from main.dbConnect.db_conn import Connect
from werkzeug.utils import secure_filename
from flask import (Blueprint, send_from_directory, abort, render_template,
                    flash,redirect,request,url_for, session)

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

def allowed_thumbnail(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_THUMBNAILS']

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
        # check thumbnail
        if 'thumbnail_file' not in request.files:
            flash('No thumbnail', 'error')
            #return render_template("uploadHtml/upload-file.html", title='Upload')
            return redirect(request.url)
        file = request.files['file']
        # THUMBNAIL
        thumbnail = request.files['thumbnail_file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file','error')
            return redirect(request.url)
        
        if thumbnail.filename == '':
            flash('No thumbnail selected', 'error')
            return redirect(request.url)
        # file is loaded and meets requirements
        # get the destination folder and save the file
        if file and allowed_file(file.filename) and allowed_thumbnail(thumbnail.filename):
            filename = secure_filename(file.filename)
            # thumbnail
            thumbnail_name = secure_filename(thumbnail.filename)

            # get title, description, flag and cost
            file_title = string.capwords(request.form['file_title'])
            descr = request.form['description']
            flag = request.form['flag']
            cost = request.form['cost']
            
            # get the destination folder selected
            dest_name = request.form['location']
            # create destination path
            dest = os.path.join(
                app.config['UPLOAD_FOLDER'], dest_name)
            
            # if the destination is a directory
            #if not os.path.isdir(dest):
                #os.mkdir(dest)

            # check if file exists in destination
            if os.path.exists(os.path.join(dest, filename)):
                flash(f'The file: {filename}, already EXISTS', 'error')
                return redirect(url_for('upload_file.upload'))

            try:
                # save the file on disk
                file.save(os.path.join(dest, filename))
                # save thumbnail
                thumbnail.save(os.path.join(dest, thumbnail_name))

                # create a reference in the db
                insert_file(file_title=file_title, file_descr=descr, filename=filename,
                            file_flag=flag, date_time=datetime.utcnow(), file_cost=cost,
                            thumbnail=thumbnail_name, emp_no=session['emp_no'])

                flash(f'{file_title} has been uploaded', 'success')
                return redirect(url_for('resources.resources_page'))

            # if directory does not exist create one
            # use os.makedirs()
            except FileNotFoundError:
                os.mkdir(app.config['UPLOAD_FOLDER'] + dest_name)
                file.save(os.path.join(dest, filename))
                # save thumbnail
                thumbnail.save(os.path.join(dest, thumbnail_name))

                # create a reference in the db
                insert_file(file_title=file_title, file_descr=descr, filename=filename,
                            file_flag=flag, date_time=datetime.utcnow(), file_cost=cost,
                            thumbnail=thumbnail_name, emp_no=session['emp_no'])
                flash(f'{file_title} has been uploaded', 'success')

                return redirect(url_for('resources.resources_page'))

            except Exception as e:
                flash(f'AN ERROR HAS OCCURED,{e}, contact admin for rectification',
                'error')

            #return redirect(url_for('uploaded_file',
                                    #filename=filename))
            #return render_template("uploadHtml/upload-file.html", title='Upload')
    return render_template("uploadHtml/upload-file.html", title='Upload')


@upload_file.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
"""
@upload_file.route('/sql')
def sql_trial():
    insert_file(file_title='New file', file_descr='new_file', filename='new.pdf',
        file_flag='free', date_time=datetime.utcnow(), file_cost=0.0, emp_no='LPG0')
    return 'insert successful'
"""

def insert_file(file_title, filename, file_descr, file_flag, file_cost,
                date_time, thumbnail, emp_no):
    # instanciate database
    conn = Connect()
    # connect to the database
    con = conn.connect_db()
    # create cursor object
    myCur = con.cursor(buffered=True, dictionary=True)

    # get employee_id
    emp_id_query = """
    select employee.id from employee where emp_no=%(emp_no)s
    """
    myCur.execute(emp_id_query, {'emp_no': emp_no})
    emp_id = myCur.fetchone()

    # basic data query
    insert_file_query = """
        INSERT INTO file_system(file_title, filename, file_descr, file_flag, file_cost,
                                 date_time, thumbnail, employee_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
    
    #(SELECT employee.id FROM employee WHERE employee.emp_no= % (emp_no)s)
    file_data = (file_title, filename, file_descr, file_flag, file_cost,
                 date_time, thumbnail, emp_id['id'])
    #print(file_data)
    try:
        # execute the query
        myCur.execute(insert_file_query, file_data)

        # commit the data
        con.commit()

        # close cursor
        myCur.close()

        # close connection
        con.close()
    except (sql.Error, sql.Warning) as e:
        flash(f'could not insert file {e}', 'error')
        print('could not insert file', e)
