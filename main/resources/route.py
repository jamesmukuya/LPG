"""
render and control resources
the filename is in the db, the route is available in our downloads folder
"""
from main import app
import mysql.connector as sql
import smtplib, os, glob, json
from email.message import EmailMessage
from main.dbConnect.db_conn import Connect
from main.resources.form import ResourceRequestForm
from flask import (Blueprint, render_template, flash, redirect, request, url_for,
                    make_response, jsonify)

resources = Blueprint('resources', __name__)

def get_files_db():
    """
    fetch files from database and check if they exist in the filesystem
    return the filenames that exist in both
    """
    # instanciate database
    conn = Connect()
    # connect to the database
    con = conn.connect_db()
    # create cursor object
    myCur = con.cursor(buffered=True, dictionary=True)

    # get employee_id
    files_query = """
    select * from file_system
    """
    myCur.execute(files_query)
    files = myCur.fetchall()
    #print(files)
    return files

def get_files_local():
    # get filenames locally
    names = [os.path.basename(x)
             for x in glob.iglob('**/*.png', recursive=True)]
    return names

@resources.route("/resources", methods=["GET", "POST"])
def resources_page():
    # get available resources from the server and pass to context
    db_files = get_files_db()
    local_files = get_files_local()
    filename = []
    # check if filenames in db match the local filenames
    for f in db_files:
        if f['filename'] in local_files:
            # append the filenames
            #print(f)
            filename.append(f)
    #credentials = get_auth()
    #print(credentials[0],credentials[1],credentials[2])
    # if user is not logged in render this form to display on request
    form = ResourceRequestForm()
    context={'form':form,'filename':filename}
    return render_template('resources/resources.html', title='Resources', **context)

@resources.route("/resources-request",methods=["POST"])
def resources_get_link():
    """
    accepts post requests with the filename and email address to send to.
    we then get the file and send as attachment to the email
    """
    req = request.get_json()
    email_addr = req.get('email')
    file_name = req.get('filename')
    #print('request object',req.get('email'))
    
    # create an instance of msg
    msg = EmailMessage()
    # subject
    msg['subject'] = 'Attached File'
    # sending address
    #sending_addr = 'info@techpoint.systems'
    sending_addr = 'info@livingpeak.org'
    # multiple recipients
    #recipients = ['james.mukuya@gmail.com', email_addr]
    #msg['From'] = 'info@techpoint.systems'

    # to have your name before the address
    msg['From'] = f'Living Peak Group <{sending_addr}>'
    # sending to multiple recipients
    #msg['To'] = ", ".join(recipients)

    # sending to one recipient
    msg['To'] = email_addr
    # message body
    msg.set_content(
        'You are receiving this email because you requested a file download from...'
        )  # this is the body

    #sending an attachement
    # get path and read the file
    for file_path in glob.iglob(f'**/{file_name}', recursive=True):
        with open(file_path, 'rb') as f:
            file_data = f.read()

    # add attachment to mail
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream',
                       filename=file_name)

    #with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
    credentials = get_auth()
    with smtplib.SMTP_SSL(credentials[0], 465) as smtp:
        smtp.login(credentials[1], credentials[2])
        smtp.send_message(msg)
    # make a response object
    if request.headers['content-type']=='application/json':
        res = make_response(jsonify(req), 200)
        return res

    return req

# get the credentials from secure file
def get_auth():
    for files in glob.iglob('**/*.json', recursive=True):
        with open(files) as f:
            data = json.load(f)
            url = data.get('test_SSL_URL')
            user_name = data.get('test_email_user')
            user_pass = data.get('test_email_pass')
    return url, user_name, user_pass
    
