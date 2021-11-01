import os

DEBUG = True
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
PROPAGATE_EXCEPTIONS = True
SECRET_KEY = os.environ["APP_SECRET_KEY"]
SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOADED_IMAGES_DEST = os.path.join("static", "images")
UPLOADED_IMAGES_DEST = os.path.join("static", "images")  # manage root folder
JWT_BLOCKLIST_ENABLED = True
JWT_BLOCKLIST_TOKEN_CHECKS = [
    "access",
    "refresh",
]  # allow blacklisting for access and refresh tokens

