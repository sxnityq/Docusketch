from flask import Flask

def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'very strong secret key'
    
    from .views import views
    app.register_blueprint(views, url_prefix='/docusketch/v1/api/')
    
    return app
    