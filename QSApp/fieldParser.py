from flask_restful import fields

login_signup_response={
    "username": fields.String,
    "name": fields.String,
    "email": fields.String,
    "token": fields.String(attribute="fs_uniquifier")
}


tracker_response = {
    "tracker_id":fields.String,
    "name":fields.String,
    "desc":fields.String,
    "tracker_type":fields.String,
    "settings":fields.String,
    "user":fields.String
}

tracker_status_response = {
    "tracker":fields.String,
    "timestamp":fields.DateTime,
    "value":fields.String,
    "note":fields.String
}