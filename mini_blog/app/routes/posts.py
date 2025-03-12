from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Post, Comment, Rating
from app.forms import PostForm, RatingForm, CommentForm

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/')
def index():
    """Home page with list of posts"""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('posts/index.html', title='Home', posts=posts)

@posts_bp.route('/post/<int:post_id>')
def view_post(post_id):
    """View a specific post"""
    post = Post.query.get_or_404(post_id)
    rating_form = RatingForm()
    comment_form = CommentForm()
    
    # Check if user has already rated this post
    user_rating = None
    if current_user.is_authenticated:
        user_rating = Rating.query.filter_by(
            user_id=current_user.id, post_id=post_id).first()
        if user_rating:
            rating_form.value.data = str(user_rating.value)
    
    return render_template('posts/view.html', 
                          title=post.title, 
                          post=post, 
                          rating_form=rating_form,
                          comment_form=comment_form,
                          user_rating=user_rating,
                          Comment=Comment)

@posts_bp.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create a new post"""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('posts.view_post', post_id=post.id))
    
    return render_template('posts/create.html', title='Create Post', form=form)

@posts_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Edit an existing post"""
    post = Post.query.get_or_404(post_id)
    
    # Check if current user is the author
    if post.author != current_user:
        abort(403)  # Forbidden
    
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.view_post', post_id=post.id))
    elif request.method == 'GET':
        # Pre-populate form with existing data
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template('posts/edit.html', title='Edit Post', form=form, post=post)

@posts_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a post"""
    post = Post.query.get_or_404(post_id)
    
    # Check if current user is the author
    if post.author != current_user:
        abort(403)  # Forbidden
    
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('posts.index'))

@posts_bp.route('/post/<int:post_id>/rate', methods=['POST'])
@login_required
def rate_post(post_id):
    """Rate a post"""
    post = Post.query.get_or_404(post_id)
    form = RatingForm()
    
    if form.validate_on_submit():
        # Check if user has already rated this post
        rating = Rating.query.filter_by(
            user_id=current_user.id, post_id=post_id).first()
        
        if rating:
            # Update existing rating
            rating.value = int(form.value.data)
            flash('Your rating has been updated!', 'success')
        else:
            # Create new rating
            rating = Rating(
                value=int(form.value.data),
                user=current_user,
                post=post
            )
            db.session.add(rating)
            flash('Your rating has been submitted!', 'success')
        
        db.session.commit()
    
    return redirect(url_for('posts.view_post', post_id=post_id))

