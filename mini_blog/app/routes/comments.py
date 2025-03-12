from flask import Blueprint, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Post, Comment
from app.forms import CommentForm

comments_bp = Blueprint('comments', __name__, url_prefix='/comments')

@comments_bp.route('/post/<int:post_id>/add', methods=['POST'])
@login_required
def add_comment(post_id):
    """Add a comment to a post"""
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            author=current_user,
            post=post
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
    
    return redirect(url_for('posts.view_post', post_id=post_id))

@comments_bp.route('/<int:comment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    """Edit a comment"""
    comment = Comment.query.get_or_404(comment_id)
    
    # Check if current user is the author
    if comment.author != current_user:
        abort(403)  # Forbidden
    
    form = CommentForm()
    if form.validate_on_submit():
        comment.content = form.content.data
        db.session.commit()
        flash('Your comment has been updated!', 'success')
        return redirect(url_for('posts.view_post', post_id=comment.post_id))
    elif request.method == 'GET':
        # Pre-populate form with existing data
        form.content.data = comment.content
    
    return render_template('comments/edit.html', 
                          title='Edit Comment', 
                          form=form, 
                          comment=comment)

@comments_bp.route('/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """Delete a comment"""
    comment = Comment.query.get_or_404(comment_id)
    
    # Check if current user is the author
    if comment.author != current_user:
        abort(403)  # Forbidden
    
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('posts.view_post', post_id=post_id))