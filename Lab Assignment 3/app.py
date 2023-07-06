from flask import Flask, render_template, request
import matplotlib.pyplot as plt
plt.switch_backend("agg")
 
app = Flask(__name__)

data = []
f = open("data.csv","r")
for i in f.readlines()[1:]:
    data.append(i.strip().split(", "))
f.close()


@app.route("/", methods=["GET","POST"])
def executer():
    if request.method=="POST":
        try:
            typer = request.form["ID"]
            id = request.form["id_value"]
        except:
            return render_template("error.html")
        if typer=="student_id":
            total = 0
            student = {}
            for i in data:
                if i[0]==id:
                    total += int(i[2])
                    student[i[1]] = i[2]
            if len(student)>0:
                return render_template("student.html",student=student,total=total,id=id)
            else:
                return render_template("error.html")
        
        elif typer=="course_id":
            marks = []
            for i in data:
                if i[1]==id:
                    marks.append(int(i[2]))
            if len(marks)>0:
                plt.clf()
                fig = plt.figure()
                plt.hist(marks)
                plt.xlabel("Marks")
                plt.ylabel("Frequency")
                plt.savefig("static/hist.png")
                return render_template("course.html",average=round(sum(marks)/len(marks),1),maxer=max(marks))
            else:
                return render_template("error.html")
        
        else:
            return render_template("error.html")
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True) 