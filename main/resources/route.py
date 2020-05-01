"""
render and control resources
the filename is in the db, the route is available in our downloads folder
"""
import smtplib,os
from main import app
from email.message import EmailMessage

from main.resources.form import ResourceRequestForm
from flask import (Blueprint, render_template, flash, redirect, request, url_for,
                    make_response, jsonify)

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
    req = request.get_json()
    email_addr = req.get('email')
    file_name = req.get('filename')
    #print('request object',req.get('email'))
    
    # create an instance of msg
    msg = EmailMessage()
    # subject
    msg['subject'] = 'Attached File'
    # sending address
    sending_addr = 'info@techpoint.systems'
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
    file_path = app.config['MISC_UPLOAD_FOLDER']
    full_path = os.path.join(file_path, file_name)

    # read the file
    with open(full_path, 'rb') as f:
        file_data = f.read()

    # add attachment to mail
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream',
                       filename=file_name)

    #with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
    with smtplib.SMTP_SSL('techpoint.systems', 465) as smtp:
        #### login credentials. must find way to hide #########
        smtp.login('info@techpoint.systems', 'K@zumi@1')
        smtp.send_message(msg)
    # make a response object
    if request.headers['content-type']=='application/json':
        res = make_response(jsonify(req), 200)
        return res

    return req

@resources.route("/mail-trial")
def mail_send():
    msg = EmailMessage()
    msg['subject'] = 'Attached File'
    sending_addr = 'info@techpoint.systems'
    recipients = ['james.mukuya@gmail.com', 'souzevannam@gmail.com']
    #msg['From'] = 'info@techpoint.systems'
    msg['From'] = f'Living Peak Group <{sending_addr}>'
    msg['To'] = ", ".join(recipients)
    msg.set_content('You are receiving this email because you requested,\
            a file download from...')# this is the body
    
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
