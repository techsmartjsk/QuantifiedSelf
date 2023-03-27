from flask import Flask,jsonify,render_template,Response
from QSApp.config import local_conf
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_restful import Resource,Api,request
import jwt
from datetime import datetime
from QSApp.exceptions import AuthError, NotFoundError, ValidationError, InternalError
from QSApp.jwtSetup import auth_required,get_username_with_token,get_token
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from flask_cors import CORS
from flask_caching import Cache
import pdfkit

app=Flask(__name__,template_folder='templates')

app.config.from_object(local_conf)

cache_config={
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_HOST": "0.0.0.0",
    "CACHE_REDIS_PORT": "6379"
}

cache = Cache(config=cache_config)
cache.init_app(app)

CORS(app, resources={r'/*': {'origins': '*'}})

db = SQLAlchemy(app)

#Schemas
from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

class TrackerSchema(ma.Schema):
    class Meta:
        fields = ('tracker_id','name','desc','tracker_type','settings','user_id')

class LogsSchema(ma.Schema):
    class Meta:
        fields = ('id','timestamp','value','note','tracker_id')

tracker_schema = TrackerSchema()
tracker_schema = TrackerSchema(many=True)

log_schema = LogsSchema()
log_schema = LogsSchema(many=True)

#Models
class User(db.Model):
    __tablename__ = "users"
    username=db.Column(db.String,primary_key=True, nullable=False)
    password=db.Column(db.String(20), nullable=False)
    name=db.Column(db.String,nullable=False)
    email=db.Column(db.String, nullable=False)
    seen_today=db.Column(db.Boolean, default=True)

    trackers = db.relationship("Tracker",backref="users")
    def __repr__(self):
        return f"<USER {self.username}>"

class Tracker(db.Model):
    __tablename__ = "usertrackers"
    tracker_id = db.Column(db.BigInteger().with_variant(db.Integer,"sqlite"),primary_key=True,nullable=False)
    name = db.Column(db.String(20), nullable=False)
    desc = db.Column(db.String,nullable=False)
    tracker_type = db.Column(db.String,nullable=False)
    settings = db.Column(db.String,nullable=False)

    user_id = db.Column(db.String, db.ForeignKey('users.username'))
    user = db.relationship('User')

    trackerLogs = db.relationship("TrackerStatus")

    def __repr__(self):
        return self.name


class TrackerStatus(db.Model):
    id= db.Column(db.BigInteger().with_variant(db.Integer,"sqlite"),primary_key=True)
    timestamp = db.Column(db.DateTime,nullable=False)
    value = db.Column(db.String,nullable=False)
    note = db.Column(db.String,nullable=False)

    tracker_id = db.Column(db.Integer, db.ForeignKey('usertrackers.tracker_id'))
    tracker = db.relationship('Tracker')

    def __repr__(self):
        return self.name

db.create_all()


api = Api(app)
baseURL=app.config["BASE_URL"]


def user_object_if_username_exists_else_err(username):
    try:
        if username==get_username_with_token():
            user_we_want = User.query.filter(User.username==username).first()
            if user_we_want:
                return user_we_want
            else:
                raise NotFoundError(404,"Username is incorrect or does not exist")
        else:
            raise AuthError("Token is not valid for resource requeested", "UNAUTH")
    except:
        raise InternalError()


#Login Form

class Login(Resource):
    def post(self):
        now = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
        try:
            if request.headers.get('Content-Type')=='application/json':
                args=json.loads(request.data)
            else:
                args=request.form
            uname=args["username"]
            pswd=args["pswd"]
            print(uname,pswd)
        except:
            raise InternalError()
        
        if uname is None or pswd is None:
            raise ValidationError(status_code= 400,error_message= "Username or password can't be empty", error_code="EMPFLD")
        user_we_want = User.query.filter(User.username==uname).first()
        if user_we_want:
            if user_we_want.password==pswd:
                expirationTime = now + timedelta(hours=24)
                token = jwt.encode({"username" : user_we_want.username, "iat": now,"exp":expirationTime},key="QS App",algorithm='HS256') #we can add some hasning things here later.
                return {
                    "token": token,
                    "username": user_we_want.username,
                    "name": user_we_want.name,
                    "email": user_we_want.email
                }
            else:
                raise ValidationError(status_code=400,error_message="Incorrect Password",error_code="INCPW")
        else:
            raise NotFoundError(404,"Username does not exist or incorrect")
 
    
#Sign Up From

class Signup(Resource):
    def post(self):
        now = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
        if request.headers.get('Content-Type')=='application/json':
            args=json.loads(request.data)
        else:
            args=request.form
        if args["username"] is None or args["name"]is None or args["email"]is None or args["pswd"] is None:
            raise ValidationError(status_code= 400,error_message= "one or more fields couldn't be empty",error_code="EMPFLD")
            #raise an error if fields are empty
        user_requested=User.query.filter(User.username==args["username"]).first()
        if user_requested:
            #if user is found
            raise ValidationError(status_code= 409,error_message="Username exists",error_code="UNAEX")
        # try:
        new_user= User(username=args["username"], name=args["name"], password=args["pswd"], email=args["email"],seen_today=True)
        db.session.add(new_user)
        db.session.commit()
        expirationTime = now + timedelta(hours=24)
        token = jwt.encode({"username" : new_user.username, "iat": now,"exp":expirationTime},key="QS App",algorithm='HS256')

        return {
            "token": token,
            "username": new_user.username,
            "name": new_user.name,
            "email": new_user.email
        }

class TrackerRoutes(Resource):
    @auth_required
    def post(self):
        if request.headers.get('Content-Type')=='application/json':
            args=json.loads(request.data)
        else:
            args=request.form

        newTracker = Tracker(name=args["name"],desc=args["desc"],
        tracker_type=args["tracker_type"],settings=args["settings"],user_id=args["username"])
        db.session.add(newTracker)
        db.session.commit()

        return {
            "Tracker":"created",
        }


class TrackerAll(Resource):
    @auth_required
    @cache.cached(timeout=36000, key_prefix='All Trackers')
    def get(self,username):
        user_we_want=user_object_if_username_exists_else_err(username)
        if user_we_want:
            trackers = db.session.query(Tracker).filter_by(user_id=username)
            result = tracker_schema.dump(trackers)

        else:
            raise NotFoundError(404,"Username is incorrect or does not exist")
        
        return jsonify(result)

    @auth_required
    def post(self,username):
        user_we_want=user_object_if_username_exists_else_err(username)
        if user_we_want:
            if request.headers.get('Content-Type')=='application/json':
                    args=json.loads(request.data)
            else:
                args=request.form

            newTracker = Tracker(name=args["name"],desc=args["desc"],
            tracker_type=args["tracker_type"],settings=args["settings"],user_id=username)
            db.session.add(newTracker)
            db.session.commit()

        else:
            raise NotFoundError(404,"Username is incorrect or does not exist")
        
        return jsonify({
            "Tracker":"created"
        })

class TrackerLogs(Resource):
    @auth_required
    def post(self,tracker_id):
        if request.headers.get('Content-Type')=='application/json':
                args=json.loads(request.data)
        else:
                args=request.form

        newTrackerLogs = TrackerStatus(
                timestamp = datetime.now(),
                value = args["value"],
                note = args["note"],
                tracker_id = tracker_id,
            )
        db.session.add(newTrackerLogs)
        db.session.commit()

        return jsonify({
            "Tracker Log":"created"
        })

    @auth_required
    def get(self,tracker_id):
        trackers = db.session.query(TrackerStatus).filter_by(tracker_id=tracker_id)
        result = log_schema.dump(trackers)

        return jsonify(result)


class Logs(Resource):
    @auth_required
    def delete(self,id):
        db.session.query(TrackerStatus).filter_by(id=id).delete()
        db.session.commit()
        return jsonify({
            "log":"deleted"
        })

    @auth_required
    def put(self,id):
        t = TrackerStatus.query.filter_by(id=id).first()
        if request.headers.get('Content-Type')=='application/json':
                args=json.loads(request.data)
        else:
                args=request.form

        t.note = args["note"]
        t.value = args["value"]
        db.session.commit()

        return jsonify({
            "Tracker Log":"edited"
        })

    @auth_required
    def get(self,id):
        t = db.session.query(TrackerStatus).filter_by(id=id)
        result = log_schema.dump(t)
        
        return jsonify(result)

class TrackerOnce(Resource):           
    @auth_required
    def delete(self,username,tracker_id):
        user_we_want=user_object_if_username_exists_else_err(username)
        if user_we_want:
            db.session.query(Tracker).filter_by(tracker_id=tracker_id).delete()
            db.session.query(TrackerStatus).filter_by(tracker_id=tracker_id).delete()
            db.session.commit()

        else:
            raise NotFoundError(404,"Username is incorrect or does not exist")

        return jsonify({
            "Tracker":"deleted"
        })

    @auth_required
    def put(self,tracker_id,username):
        t = Tracker.query.filter_by(tracker_id=tracker_id).first()

        if request.headers.get('Content-Type')=='application/json':
                args=json.loads(request.data)
        else:
                args=request.form

        t.name = args["name"]
        t.desc = args["desc"]
        t.tracker_type = args["tracker_type"]
        t.settings = args["settings"]
        db.session.commit()

        return jsonify({
            "Tracker":"edited"
        })

    @auth_required
    def get(self,tracker_id,username):
        user_we_want=user_object_if_username_exists_else_err(username)
        if user_we_want:
            trackers = Tracker.query.filter_by(tracker_id=tracker_id,user_id=username)
            result = tracker_schema.dump(trackers)

        else:
            raise NotFoundError(404,"Username is incorrect or does not exist")

        return jsonify(result)

class DownloadTracker(Resource):
    @auth_required
    def get(self):
        # Get the HTML output
        out = render_template("export.html")
        
        # PDF options
        options = {
            "orientation": "landscape",
            "page-size": "A4",
            "margin-top": "1.0cm",
            "margin-right": "1.0cm",
            "margin-bottom": "1.0cm",
            "margin-left": "1.0cm",
            "encoding": "UTF-8",
        }
        
        # Build PDF from HTML 
        pdf = pdfkit.from_string(out, options=options)
        
        # Download the PDF
        return Response(pdf, mimetype="application/pdf")


class isauth(Resource):
    @auth_required
    def get(self):
        return ({
            "auth": True,
            "username": get_username_with_token()
        })


api.add_resource(Login,"/api/login")
api.add_resource(Signup,"/api/signup")
api.add_resource(TrackerAll,"/tracker/<string:username>")
api.add_resource(TrackerOnce,"/tracker/<string:username>/<string:tracker_id>")
api.add_resource(TrackerLogs,"/tracker/<int:tracker_id>/")
api.add_resource(DownloadTracker,'/tracker/export')
api.add_resource(Logs,"/log/<int:id>/")
api.add_resource(isauth,"/api/isAuth")

if __name__=="__main__":
    app.run(debug=True)