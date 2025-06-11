from flask_restx import fields

from app.users.namespace import api

register_model = api.model("Register", {
    "username": fields.String(required=True),
    "password": fields.String(required=True),
})

login_model = api.clone("Login", register_model)

password_update_model = api.model("PasswordUpdate", {
    "password": fields.String(required=True),
})

token_response = api.model("TokenResponse", {
    "message": fields.String,
    "access_token": fields.String,
})

message_response = api.model("MessageResponse", {
    "message": fields.String,
})
