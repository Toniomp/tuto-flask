from flask import Flask
from flask_bootstrap import Bootstrap5
import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(
                __file__),p
            
        )
    )


app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL']=True
bootstrap = Bootstrap5(app)

app.config['SECRET_KEY']='03bba81e-d941-469e-ad47-5e7d83cbcaa9'
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../myapp.db'))
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"