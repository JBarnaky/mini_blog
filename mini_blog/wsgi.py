from app import create_app, db
from app.models import User, Post, Comment, Rating

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Provides key objects to flask shell"""
    return {
        'db': db, 
        'User': User, 
        'Post': Post, 
        'Comment': Comment, 
        'Rating': Rating
    }

if __name__ == '__main__':
    app.run(debug=True)