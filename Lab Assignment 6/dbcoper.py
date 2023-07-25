from app import *
app.app_context().push()
# fetcher = enrollments.query.all()

# for fetch in fetcher:
#     en = Enrollment(student_id=fetch.estudent_id,course_id=fetch.ecourse_id)
#     db.session.add(en)
# db.session.commit()
print(Student.query.filter_by(student_id=482003300).first())