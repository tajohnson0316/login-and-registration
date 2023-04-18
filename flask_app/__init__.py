from flask import Flask
import re

# application
app = Flask(__name__)
app.secret_key = "This is my secret key - there are many like it, but this one is mine"

# database
DATABASE = "login_db"
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
