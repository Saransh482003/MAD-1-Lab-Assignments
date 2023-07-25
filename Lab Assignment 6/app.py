from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'
api = Api(app)
db = SQLAlchemy(app)
app.app_context().push()

# Data Tables
class course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String, nullable=False)
    course_code = db.Column(db.String, unique=True,nullable=False)
    course_description = db.Column(db.String)
class student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
class Enrollment(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey(student.student_id), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(course.course_id),nullable=False)

# Rest Endpoints
#course
course_put_parser = reqparse.RequestParser()
course_put_parser.add_argument("course_name",type=str,help="Enter course Name")
course_put_parser.add_argument("course_code",type=str,help="Enter course Code")
course_put_parser.add_argument("course_description",type=str,help="Enter course Description")

course_post_parser = reqparse.RequestParser()
course_post_parser.add_argument("course_name",type=str,help="Enter course Name",required=True)
course_post_parser.add_argument("course_code",type=str,help="Enter course Code",required=True)
course_post_parser.add_argument("course_description",type=str,help="Enter course Description",required=True)

class getcourse(Resource):
    def get(self,course_id):
        fetcher = course.query.filter_by(course_id=course_id).first()
        result = {
            "course_id" : fetcher.course_id,
            "course_name" : fetcher.course_name,
            "course_code" : fetcher.course_code,
            "course_description" : fetcher.course_description            
        }
        return result
    def post(self):
        args = course_post_parser.parse_args()
        if (course.query.filter_by(course_code=args["course_code"]).first()==None):
            adder = course(course_name=args["course_name"],course_code=args["course_code"],course_description=args["course_description"])
            db.session.add(adder)
            db.session.commit()
            fetcher = course.query.filter_by(course_code=args["course_code"]).first()
            result = {
                "course_id" : fetcher.course_id,
                "course_name" : fetcher.course_name,
                "course_code" : fetcher.course_code,
                "course_description" : fetcher.course_description            
            }
            return result
        abort(409)
        
    def put(self,course_id):
        args = course_put_parser.parse_args()
        fetcher = course.query.filter_by(course_id=course_id).first()
        if args["course_name"]:
            fetcher.course_name = args["course_name"]
        if args["course_code"]:
            fetcher.course_code = args["course_code"]
        if args["course_description"]:
            fetcher.course_description = args["course_description"]
        db.session.commit()
        return self.get(course_id)
    
    def delete(self,course_id):
        fetcher = course.query.filter_by(course_id=course_id).first()
        if fetcher==None:
            abort(409)
        else:
            db.session.delete(fetcher)
            db.session.commit()
        

#student
student_put_parser = reqparse.RequestParser()
student_put_parser.add_argument("first_name",type=str,help="Enter First Name")
student_put_parser.add_argument("last_name",type=str,help="Enter Last Name")
student_put_parser.add_argument("roll_number",type=str,help="Enter Roll Number")

student_post_parser = reqparse.RequestParser()
student_post_parser.add_argument("first_name",type=str,help="Enter First Name",required=True)
student_post_parser.add_argument("last_name",type=str,help="Enter Last Name",required=True)
student_post_parser.add_argument("roll_number",type=str,help="Enter Roll Number",required=True)
class getstudent(Resource):
    def get(self,student_id):
        fetcher = student.query.filter_by(student_id=student_id).first()
        result = {
            "student_id" : fetcher.student_id,
            "first_name" : fetcher.first_name,
            "last_name" : fetcher.last_name,
            "roll_number" : fetcher.roll_number           
        }
        return result
    def post(self):
        args = student_post_parser.parse_args()
        if (student.query.filter_by(roll_number=args["roll_number"]).first()==None):
            adder = student(first_name=args["first_name"],last_name=args["last_name"],roll_number=args["roll_number"])
            db.session.add(adder)
            db.session.commit()
            fetcher = student.query.filter_by(roll_number=args["roll_number"]).first()
            result = {
                "student_id" : fetcher.student_id,
                "first_name" : fetcher.first_name,
                "last_name" : fetcher.last_name,
                "roll_number" : fetcher.roll_number           
            }
            return result
        abort(409)
    
    def put(self,student_id):
        args = student_put_parser.parse_args()
        fetcher = student.query.filter_by(student_id=student_id).first()
        if args["first_name"]:
            fetcher.first_name = args["first_name"]
        if args["last_name"]:
            fetcher.last_name = args["last_name"]
        if args["roll_number"]:
            fetcher.roll_number = args["roll_number"]
        db.session.commit()
        return self.get(student_id)
    
    def delete(self,student_id):
        fetcher = student.query.filter_by(student_id=student_id).first()
        if fetcher==None:
            abort(409)
        else:
            db.session.delete(fetcher)
            db.session.commit()
    
#Enrollment
enroll_post = reqparse.RequestParser()
enroll_post.add_argument("course_id",type=int,help="Enter course ID",required=True)
class getenrollment(Resource):
    def get(self,student_id):
        fetcher = Enrollment.query.filter_by(student_id=student_id).all()
        result = []
        for fetch in fetcher:
            subresult = {
                "enrollment_id": fetch.enrollment_id,
                "student_id": fetch.student_id,
                "course_id": fetch.course_id
            }
            result.append(subresult)
        return result
    
    def post(self,student_id):
        args = enroll_post.parse_args()
        en = Enrollment(student_id=student_id,course_id=args["course_id"])
        db.session.add(en)
        db.session.commit()
        return self.get(student_id)
    
    def delete(self,student_id,course_id):
        fetcher = Enrollment.query.filter_by(student_id=student_id,course_id=course_id).all()
        for fetch in fetcher:
            db.session.delete(fetch)
        db.session.commit()

api.add_resource(getcourse,"/api/course","/api/course/<int:course_id>")
api.add_resource(getstudent,"/api/student","/api/student/<int:student_id>")
api.add_resource(getenrollment,"/api/student/<int:student_id>/course","/api/student/<int:student_id>/course/<int:course_id>")

if "__main__"==__name__:
    app.run(debug=True)
