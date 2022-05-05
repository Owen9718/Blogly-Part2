"""Blogly application."""

from crypt import methods
from flask import Flask,redirect,render_template,request,flash
from models import db, connect_db,User,Post


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

connect_db(app)
db.create_all()

@app.route('/')
def users():

    return redirect('/users')


@app.route('/users')
def list_users():
    users = User.query.order_by(User.last_name,User.first_name).all()
    return render_template('users.html',users = users)


@app.route('/users/new')
def create_user():

    return render_template('home.html')


@app.route('/users/new', methods= ['POST'])
def add_user():
    image_url = request.form['url'] if request.form['url']!= "" else None
    new_user = User(first_name = request.form['first'],last_name = request.form['last'],image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route(f'/users/<int:user_id>')
def user_info(user_id):
    user = User.query.get_or_404(user_id)
    print('THIS IS IMAGE', user.image_url)
    return render_template('user_info.html', user= user)


@app.route(f'/users/<int:user_id>/edit')
def edit_temp(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit.html',user = user)


@app.route(f'/users/<int:user_id>/edit', methods =["POST"])
def save_user_edit(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first']
    user.last_name = request.form['last']
    user.image_url = request.form['image']

    db.session.add(user)
    db.session.commit()
    return redirect('/users')


@app.route(f'/users/<int:user_id>/delete', methods =["POST"])
def delete(user_id):

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route(f'/users/<int:user_id>/posts/new')
def post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('post_form.html',user=user)

@app.route(f'/users/<int:user_id>/posts/new', methods = ['POST'])
def post_create(user_id):
    title = request.form['title']
    content = request.form['content']
    user = User.query.get_or_404(user_id)
    post = Post(title = title,content = content, user_id = user.id)
    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' added.")
    return redirect(f'/users/{user_id}')


@app.route(f'/posts/<int:post_id>')
def post_details(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_info.html', post = post)

@app.route(f'/posts/<int:post_id>/edit')
def show_edit(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html',post=post)

@app.route(f'/posts/<int:post_id>/edit', methods=['POST'])
def save_post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' saved.")
    return redirect(f'/posts/{post.id}')


@app.route(f'/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' deleted.")
    return redirect(f'/users/{post.user_id}')