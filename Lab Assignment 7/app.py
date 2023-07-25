from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///week7_database.sqlite3'
db = SQLAlchemy(app)
app.app_context().push()

class student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)

class course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

class enrollments(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey(student.student_id), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey(course.course_id), nullable=False)


@app.route('/')
def index():
    fetcher = student.query.all()
    return render_template("index.html",studentList=fetcher)

@app.route("/student/create",methods=["GET","POST"])
def student_create():
    if request.method=="POST":
        roll = request.form["roll"]
        fname = request.form["f_name"]
        lname = request.form["l_name"]

        if student.query.filter_by(roll_number=roll).first():
            return render_template("student_exist.html")
        student_adder = student(first_name=fname,last_name=lname,roll_number=roll)
        db.session.add(student_adder)
        db.session.commit()
        return redirect("/")
    return render_template("student_create.html")

@app.route('/student/<int:student_id>/update',methods=["GET","POST"])
def student_update(student_id):
    if request.method=="POST":
        fname = request.form["f_name"]
        lname = request.form["l_name"]
        cour = request.form["course"]
        cour_id = cour[7:8]
        
        fetched = student.query.filter_by(student_id=student_id).first()
        fetched.first_name = fname
        fetched.last_name = lname
        
        enr = enrollments(estudent_id=student_id,ecourse_id=cour_id)
        db.session.add(enr)
        db.session.commit()
        return redirect("/")
    fetcher = student.query.filter_by(student_id=student_id).first()
    course_fetch = course.query.all()
    return render_template("student_update.html",student=fetcher,courseList=course_fetch)

@app.route('/student/<int:student_id>/delete')
def student_delete(student_id):
    student_fetcher = student.query.filter_by(student_id=student_id).first()
    db.session.delete(student_fetcher)
    enroll_fetcher = enrollments.query.filter_by(estudent_id=student_id).all()
    for enroll in enroll_fetcher:
        db.session.delete(enroll)
    db.session.commit()
    return redirect("/")

@app.route('/student/<int:student_id>')
def student_get(student_id):
    stu_fetcher = student.query.filter_by(student_id=student_id).first()
    enc = enrollments.query.filter_by(estudent_id=student_id).all()
    courseList = []
    for i in enc:
        id = i.ecourse_id
        cour = course.query.filter_by(course_id=id).first()
        courseList.append(cour)
    return render_template("student_get.html",student=stu_fetcher,courseList=courseList)

@app.route('/student/<int:student_id>/withdraw/<int:course_id>')
def student_enr_delete(student_id,course_id):
    fetcher = enrollments.query.filter_by(estudent_id=student_id,ecourse_id=course_id).all()
    for i in fetcher:
        db.session.delete(i)
    db.session.commit()
    return redirect("/")

@app.route('/courses')
def course_index():
    fetcher = course.query.all()
    return render_template("course_index.html",courseList=fetcher)

@app.route('/course/create', methods=["GET","POST"])
def course_create():
    if request.method=="POST":
        code = request.form["code"]
        cname = request.form["c_name"]
        desc = request.form["desc"]

        if course.query.filter_by(course_code=code).first():
            return render_template("course_exist.html")
        
        course_adder = course(course_code=code,course_name=cname,course_description=desc)
        db.session.add(course_adder)
        db.session.commit()
        return redirect("/courses")
    return render_template("course_create.html")

@app.route('/course/<int:course_id>/update',methods=["GET","POST"])
def course_update(course_id):
    if request.method=="POST":
        cname = request.form["c_name"]
        desc = request.form["desc"]
        
        fetched = course.query.filter_by(course_id=course_id).first()
        fetched.course_name = cname
        fetched.course_description = desc
        db.session.commit()
        return redirect("/courses")
    fetcher = course.query.filter_by(course_id=course_id).first()
    return render_template("course_update.html",course=fetcher)

@app.route('/course/<int:course_id>/delete')
def course_delete(course_id):
    course_fetch = course.query.filter_by(course_id=course_id).first()
    db.session.delete(course_fetch)
    enroll_fetch = enrollments.query.filter_by(ecourse_id=course_id).all()
    for fetch in enroll_fetch:
        db.session.delete(fetch)
    db.session.commit()
    return redirect("/courses")

@app.route("/course/<int:course_id>")
def course_get(course_id):
    fetcher = course.query.filter_by(course_id=course_id).first()
    enc = enrollments.query.filter_by(ecourse_id=course_id).all()
    studentList = []
    for enroll in enc:
        stud = student.query.filter_by(student_id=enroll.estudent_id).first()
        studentList.append(stud)
    return render_template("course_get.html",course=fetcher,studentList=studentList)
if __name__=="__main__":
    app.run(debug=True)