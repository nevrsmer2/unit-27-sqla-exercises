from flask import Flask, flash, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension

from models import Post, PostTag, Tag, User, connect_db, db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'kiti3sRdbes7'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


'''----------ROUTES----------'''


@app.route('/')
def root():
    '''Show recent list of posts, most-recent first'''

    posts = Post.query.order_by(Post.created_at.desc()).limit(8).all()
    return render_template('posts/homepage.html', posts=posts)


@app.route('/users')
def show_users_list():
    '''Render the page that lists all users'''
    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('users/index.html', users=users)


@app.route('/users/add', methods=['GET'])
def render_add_user_form():
    '''Renders form to add a user to DB'''
    return render_template('users/add.html')


@app.route('/users/add', methods=['POST'])
def submit_new_user_form():
    '''Handles form action to submit a new user's details to dB'''

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Show a page with info on a specific user"""

    posts = Post.query.filter(Post.user_id == user_id)
    user = User.query.get_or_404(user_id)
    return render_template('users/details.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def edit_user_profilet(user_id):
    '''Render the form to update a user'''

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def users_update(user_id):
    '''Handle POST request to update user details on DB'''
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    '''Functionality to delete a user'''
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


'''--------------------PART 2----------------------'''


@app.route('/posts/<int:user_id>/new')
def show_add_post_form(user_id):
    '''Show form to add a post'''

    tags = Tag.query.all()
    user = User.query.get_or_404(user_id)
    return render_template('/posts/new.html', user=user, tags=tags)

    'Updated route to add option to select tag when creating a post'


@app.route('/posts/<int:user_id>/new', methods=['GET', 'POST'])
def commit_new_post_form(user_id):
    '''Functionality to ccommit new post along with selected tags'''

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(
        title=request.form['post-title'],
        content=request.form['post-content'],
        user_id=user_id,
        tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect("/users")

    '''Previous route for adding a new post'''

    # @app.route('/posts/<int:user_id>/new', methods=['GET', 'POST'])
# def commit_new_post_form(user_id):
#     '''Submit new post to DB'''

#     new_post = Post(
#         title=request.form['post-title'],
#         content=request.form['post-content'],
#         user_id=user_id)

#     db.session.add(new_post)
#     db.session.commit()

#     return redirect("/users")


@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    '''Render a page with content for a specific post'''

    post = Post.query.get_or_404(post_id)
    return render_template('posts/post.html', post=post)

    '''Route updated to show options to update avaialble tags when editing a post'''


@app.route('/posts/<int:post_id>/edit')
def show_update_post_form(post_id):
    '''Render form to edit a user's post'''

    tags = Tag.query.all()
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', tags=tags, post=post)

    '''Code before updating to show optinn to edit tages when editing a post'''

# @app.route('/posts/<int:post_id>/edit')
# def show_update_post_form(post_id):
#     '''Render form to edit a user's post'''

#     post = Post.query.get_or_404(post_id)
#     return render_template('posts/edit.html', post=post)


# @app.route('/posts/<int:post_id>/edit', methods=['POST'])
# def commit_update_post_form(post_id):
#     '''Commit changes made on edit post form'''

#     post = Post.query.get_or_404(post_id)
#     post.title = request.form['title']
#     post.content = request.form['content']

#     db.session.add(post)
#     db.session.commit()
#     return redirect(f'/users/{post.user_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def posts_destroy(post_id):
    '''Functionality to delete a user's  post'''

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')


@app.errorhandler(404)
def page_not_found(e):
    '''Show 404 NOT FOUND page.'''

    return render_template('404.html'), 404


'''----------------PART 3 - Tag Routes---------------'''


@app.route('/tags')
def show_tags_list():
    '''Show a list of all tags on oall pages'''
    tags = Tag.query.all()

    return render_template('tags/index.html', tags=tags)


@app.route('/tags/new')
def show_new_tag_form():
    '''Show the form to create a post tag'''

    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)


@app.route('/tags/new', methods=['POST'])
def tags_new():
    '''Functionality to commit newly-created tag to DB'''

    post_ids = [int(num) for num in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    '''Show all posts related to a given tag'''

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    '''Show form to edit a tag'''

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def tags_edit(tag_id):
    '''Functionality to update edits to a tag on DB'''

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def tags_destroy(tag_id):
    '''Functionality to delete a tag'''

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')
