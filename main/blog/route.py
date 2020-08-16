"""
blog controller
"""
import os,glob,json
from datetime import datetime
import mysql.connector as sql
from main.dbConnect.db_conn import Connect

from flask import (Blueprint, render_template, flash,
                  session, redirect, request, url_for,
                   make_response, jsonify)

blog = Blueprint('blog', __name__)

# VIEWS #

# visible to anyone
@blog.route("/blog", methods=["GET","POST"])
def blog_page():
  blogs = get_blogs()
  context = {"blogs": blogs}
  return render_template('blog/blog.html', title='Blogs', **context)


# MODEL #
# route only available to staff
@blog.route("/blog/new", methods=["GET", "POST"])
def blog_post():  
  # check if user is authorized to view page
  if session.get('is_staff'):
    # if method is post
    if request.method == "POST":
      # get form data
      blog_title = request.form['blog_title']
      # get the published iframe
      blog_content = request.form['blog_content']
      # get the blog link
      blog_link = request.form['blog_link']
      # split before closure in so as to add class
      b = blog_content.split("></iframe>")
      # add class and close
      blog_content = b[0] + (' class="doc"></iframe>')

      emp_id = session['staff_id']
      # insert data to database
      new_blog(blog_title, blog_content, blog_link, emp_id)
      return redirect(url_for('blog.blog_post'))
    return render_template('blog/newBlog.html', title='New Blog')
  return redirect(url_for('user_auth.staff_login'))

@blog.route("/blog/new2",methods=["GET","POST"])
def new_blog_post():
  if session.get('is_staff'):
    if request.method == "POST":
      # get blog title
      # get blog image
      pass


# comment/reply post route only for registered users accepts posts only
@blog.route("/blog/reply", methods=["POST"])
def blog_reply():
  #if request.method=="POST":
  # check if user is registered
  if session['logged_in'] == True:
    req = request.get_json()
    # get id of blog being replied to
    main_blogs_id = req.get('post_id')
    blog_reply = req.get('post_content')
    user_registration_id = session['reg_id']
    # submit to database
    reply_blog(blog_reply, main_blogs_id, user_registration_id)

    # make response
    if request.headers['Content-Type']=='application/json':
      res = make_response(jsonify(main_blogs_id, blog_reply), 200)
      return res
    

# edit route takes in the blog id
@blog.route("/blog/delete",methods=["POST"])
def blog_delete():
  if request.method == 'POST':
    req = request.form.get('del_btn')
    delete_blog(req)
    flash('The blog has been successfully deleted','success')
    return redirect(url_for('blog.blog_page'))

# CONTROLLERS #
    
# login to database and fetch the blogs
def get_blogs():
  """
  fetch blogs from database
  """
  # instanciate database
  conn = Connect()
  # connect to the database
  con = conn.connect_db()
  # create cursor object
  myCur = con.cursor(buffered=True, dictionary=True)

  # get blogs and details of who posted
  """blogs_query =
  select main_blogs.id,blog_title,blog_content,date_created,blog_link,last_name,first_name,
  blog_reply,reply_date,main_blogs_id,basic_user_details_id
  from main_blogs left join blogs_history 
  on main_blogs.id = main_blogs_id inner join employee on employee_id = employee.id 
  inner join basic_user_details on basic_user_details_id = basic_user_details.id;
  """
  
  blogs_query = """
  select main_blogs.id,blog_title,blog_content,date_created,blog_link,last_name,first_name
  from main_blogs inner join employee on employee_id = employee.id 
  inner join basic_user_details on basic_user_details_id = basic_user_details.id;
  """
  #reqs="main_blogs.id,blog_title,blog_content,date_created,last_name,first_name"
  myCur.execute(blogs_query)
  blogs = myCur.fetchall()
  #print(files)
  return blogs



# insert to database an new blog
def new_blog(blog_title, blog_content, blog_link, employee_id):
  """
  insert a new blog into main_blogs table.
  args: blog_title,blog_content,date_created,employee_id(from session)
  other params: date_created
  """
  # instanciate database
  conn = Connect()
  # connect to the database
  con = conn.connect_db()
  # create cursor object
  myCur = con.cursor(buffered=True, dictionary=True)

  # get insert blogs
  main_blog_query = """
    insert into main_blogs (blog_title, blog_content, date_created, blog_link, employee_id)
    values(%(blog_title)s, %(blog_content)s, %(date_created)s,%(blog_link)s, %(employee_id)s)
    """
  date_created = datetime.utcnow()

  blog_data = {
      'blog_title': blog_title, 'blog_content': blog_content, 'date_created': date_created,
      'blog_link':blog_link, 'employee_id': employee_id}
  try:
    myCur.execute(main_blog_query, blog_data)
    # commit the data
    con.commit()

    # close cursor
    myCur.close()

    # close connection
    con.close()

    # advise user of results
    flash(f'new blog: {blog_title}', 'success')

  except(sql.Error, sql.Warning):
      # log the error
      #logging.basicConfig(filename=app.config['LOGGING_FOLDER'] + 'user_reg.log',
      #                    level=logging.ERROR)
      #logging.warning(f'{e}')
      # print(e)
      flash('could not create blog', 'error')

# insert to database a blog reply
def reply_blog(blog_reply, main_blogs_id, user_registration_id):
  """
  insert a reply blog into blogs_history table.
  args: blog_reply, main_blogs_id, user_registration_id(from session)
  other params: reply_date
  """
  # instanciate database
  conn = Connect()
  # connect to the database
  con = conn.connect_db()
  # create cursor object
  myCur = con.cursor(buffered=True, dictionary=True)

  # get employee_id
  reply_blog_query = """
    insert into blogs_history (blog_reply, reply_date, main_blogs_id, user_registration_id)
    values(%(blog_reply)s, %(reply_date)s, %(main_blogs_id)s, %(user_registration_id)s)
    """
  reply_date = datetime.utcnow()

  blog_data = {
      'blog_reply': blog_reply, 'reply_date': reply_date,
      'main_blogs_id': main_blogs_id, 'user_registration_id': user_registration_id}
  try:
    myCur.execute(reply_blog_query, blog_data)
    # commit the data
    con.commit()

    # close cursor
    myCur.close()

    # close connection
    con.close()

    # advise user of results
    flash('reply posted', 'success')

  except(sql.Error, sql.Warning) as e:
      # log the error
      #logging.basicConfig(filename=app.config['LOGGING_FOLDER'] + 'user_reg.log',
      #                    level=logging.ERROR)
      #logging.warning(f'{e}')
      print(e)
      flash('could not post blog reply', 'error')

def delete_blog(id):
  """
  permanently delete a main blog
  args: id of the blog
  """
  # instanciate database
  conn = Connect()
  # connect to the database
  con = conn.connect_db()
  # create cursor object
  myCur = con.cursor(buffered=True, dictionary=True)

  # get employee_id
  delete_query = """
    delete from main_blogs where id = %(id)s
    """
  blog_data = {'id': id}
  
  try:
    myCur.execute(delete_query, blog_data)
    # commit the data
    con.commit()

    # close cursor
    myCur.close()

    # close connection
    con.close()

  except(sql.Error, sql.Warning) as e:
      # log the error
      #logging.basicConfig(filename=app.config['LOGGING_FOLDER'] + 'user_reg.log',
      #                    level=logging.ERROR)
      #logging.warning(f'{e}')
      print(e)
      flash('could not post blog reply', 'error')
