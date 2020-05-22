"""
blog controller
"""
from flask import (Blueprint, render_template, flash, redirect, request, url_for,
                   make_response, jsonify)

blog = Blueprint('blog', __name__)

@blog.route("/blog")
def blog_page():
  return render_template('blog/blog.html', title='Blogs')

@blog.route("/blog/new", methods=["GET", "POST"])
def blog_post():
  return render_template('blog/newBlog.html', title='New Blog')

@blog.route("/blog/edit",methods=["GET","POST"])
def blog_edit():
  return render_template('blog/editBlog.html', title='Edit Blog')
