import smtplib, glob, json
from email.message import EmailMessage
from flask import (Blueprint, render_template, session,
                   flash, redirect, request, url_for)

contact = Blueprint('contact', __name__)

@contact.route("/contact",methods=["GET","POST"])
def contact_page():
  if request.method == "POST":
    
    # get data from fields
    sending_addr = 'info@techpoint.systems' # the request form address
    email_from = request.form['email'] # the person writing the email
    subject = request.form['subject']
    message = request.form['message'].strip()

    msg = EmailMessage()
    # subject
    msg['subject'] = subject
    # sending address
    msg['From'] = f'Request from Contact Form <{sending_addr}>'
    msg['To'] = 'james.mukuya@gmail.com'
    # message body
    msg.set_content(f'Sender: <{email_from}>, Message:{message}')
    
    # get credentials from file
    credentials = get_auth()
    with smtplib.SMTP_SSL(credentials[0], 465) as smtp:
        smtp.login(credentials[1], credentials[2])
        smtp.send_message(msg)

    flash("Thank you for contacting Living Peak Group.\
          Your message has been sent","success")
    return redirect(url_for('contact.contact_page'))
  return render_template('contact/contact.html', title='Contact')


# get the credentials from secure file
def get_auth():
    for files in glob.iglob('**/*.json', recursive=True):
        with open(files) as f:
            data = json.load(f)
            url = data.get('test_SSL_URL')
            user_name = data.get('test_email_user')
            user_pass = data.get('test_email_pass')
    return url, user_name, user_pass
