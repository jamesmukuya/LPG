"""
render and control resources
the filename is in the db, the route is available in our downloads folder
"""
import smtplib,os
from main import app
from email.message import EmailMessage

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

@resources.route("/resources-request",methods=["POST"])
def resources_get_link():
    """
    accepts post requests with the filename and email address to send to.
    we then get the file and send as attachment to the email
    """
    return 'this is a file request'

@resources.route("/mail-trial")
def mail_send():
    msg = EmailMessage()
    msg['subject'] = 'Hello there'
    msg['From'] = 'info@techpoint.systems'
    msg['To'] = 'james.mukuya@gmail.com'
    msg.set_content('this is an email from python')# this is the body
    
    #sending an attachement
    file_name = 'link.txt'
    file_path = app.config['MISC_UPLOAD_FOLDER']
    full_path = os.path.join(file_path, file_name)
    
    with open(full_path, 'rb') as f:
        file_data = f.read()

    msg.add_attachment(file_data, maintype='application', subtype='octet-stream',
        filename=file_name)
    
    #with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
    with smtplib.SMTP_SSL('techpoint.systems',465) as smtp:
        #smtp.login('james.mukuya@gmail.com', 'kq@12345')
        smtp.login('info@techpoint.systems', 'K@zumi@1')
        smtp.send_message(msg)

    return 'this message was sent'
