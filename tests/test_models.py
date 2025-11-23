"""
Tests de modelos
"""
from app.models import User, Post, Comment

def test_user_password_hashing(app):
    """Test de hash de contraseñas"""
    with app.app_context():
        user = User(username='test', email='test@test.com')
        user.set_password('password123')
        
        assert user.password_hash != 'password123'
        assert user.check_password('password123')
        assert not user.check_password('wrongpassword')

def test_user_roles(app):
    """Test de roles de usuario"""
    with app.app_context():
        # Usuario normal
        user = User(username='user', email='user@test.com', role='user')
        assert not user.is_admin()
        assert not user.is_editor()
        
        # Editor
        editor = User(username='editor', email='editor@test.com', role='editor')
        assert not editor.is_admin()
        assert editor.is_editor()
        
        # Admin
        admin = User(username='admin', email='admin@test.com', role='admin')
        assert admin.is_admin()
        assert admin.is_editor()

def test_post_creation(app):
    """Test de creación de publicación"""
    from app.models import db
    
    with app.app_context():
        user = User(username='author', email='author@test.com')
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()
        
        post = Post(
            title='Test Post',
            content='Test Content',
            category='tecnologia',
            user_id=user.id
        )
        db.session.add(post)
        db.session.commit()
        
        assert post.id is not None
        assert post.author.username == 'author'
        assert post.category == 'tecnologia'

def test_comment_creation(app):
    """Test de creación de comentario"""
    from app.models import db
    
    with app.app_context():
        user = User(username='commenter', email='commenter@test.com')
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()
        
        post = Post(title='Post', content='Content', user_id=user.id)
        db.session.add(post)
        db.session.commit()
        
        comment = Comment(
            content='Great post!',
            user_id=user.id,
            post_id=post.id
        )
        db.session.add(comment)
        db.session.commit()
        
        assert comment.id is not None
        assert comment.author.username == 'commenter'
        assert comment.post.title == 'Post'
