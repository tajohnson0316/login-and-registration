from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, EMAIL_REGEX, app
from flask import flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # Create user
    @classmethod
    def create_one(cls, data):
        query = """ 
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """

        return connectToMySQL(DATABASE).query_db(query, data)

    # Get user with id
    @classmethod
    def get_one(cls, data):
        query = """ 
        SELECT *
        FROM users
        WHERE id = %(id)s;
        """

        result = connectToMySQL(DATABASE).query_db(query, data)

        if len(result) == 0:
            return None

        return cls(result[0])

    # Get user with email
    @classmethod
    def get_one_with_email(cls, data):
        query = """ 
        SELECT *
        FROM users
        WHERE email = %(email)s;
        """

        result = connectToMySQL(DATABASE).query_db(query, data)

        if len(result) == 0:
            return None

        print(f"User info: {result[0]}")

        return cls(result[0])

    # User validation
    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data["first_name"]) < 2:
            flash(
                "Please provide a valid name: at least 3 characters", "error_first_name"
            )
            is_valid = False
        if len(data["last_name"]) < 2:
            flash(
                "Please provide a valid name: at least 3 characters", "error_last_name"
            )
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("Please provide a valid email", "error_email")
            is_valid = False
        if len(data["password"]) == 0:
            flash("Please provide a password", "error_password")
            is_valid = False
        if data["confirm_password"] != data["password"]:
            flash("Passwords must match", "error_password")
            is_valid = False
        if User.get_one_with_email(data) != None:
            flash("An account already exists with this email", "error_email")
            is_valid = False
        return is_valid

    # Login email validation
    @staticmethod
    def validate_login_email(email):
        is_valid = True
        if not EMAIL_REGEX.match(email):
            flash("Please provide a valid email address", "error_login_email")
            is_valid = False
        if User.get_one_with_email({"email": email}) == None:
            flash(
                "No account found. Please check email and try again",
                "error_login_email",
            )
            is_valid = False

        return is_valid

    # Login password validation
    @staticmethod
    def validate_password(hashed_password, unhashed_password):
        is_valid = True
        if len(unhashed_password) == 0:
            flash("Please provide a password", "error_login_password")
            is_valid = False
        if not bcrypt.check_password_hash(hashed_password, unhashed_password):
            flash("Invalid password", "error_login_password")
            is_valid = False

        return is_valid

    # Encrypt password
    @staticmethod
    def encrypt_string(text):
        return bcrypt.generate_password_hash(text)
