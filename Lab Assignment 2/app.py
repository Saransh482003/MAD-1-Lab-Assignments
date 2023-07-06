import sys
from jinja2 import Template
import matplotlib.pyplot as plt

params = sys.argv[1:]
id = params[1]
error_temp = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Something Went Wrong</title>
</head>
<body>
    <h1>Wrong Inputs</h1>
    <p>Something went wrong</p>
</body>
</html>"""


data = []
f = open("data.csv","r")
for i in f.readlines()[1:]:
    data.append(i.strip().split(", "))
f.close()


out=""""""
if params[0]=="-s":
    cour = {}
    total = 0
    for i in data:
        if i[0]==id:
            cour[i[1]] = i[2]
            total += int(i[2])
    if len(cour)>0:
        stu = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Data</title>
</head>
<body>
    <h1>Student Details</h1>
    <table border="1">
        <tr>
            <th>Student ID</th>
            <th>Course ID</th>
            <th>Marks</th>
        </tr>
        {% for i in cour %}
        <tr>
            <td>{{ id }}</td>
            <td>{{ i }}</td>
            <td>{{ cour[i] }}</td>
        </tr>
        {% endfor %}
        <tr>
            <td colspan="2" style="text-align: center;">Total Marks</td>
            <td>{{ total }}</td>
        </tr>
    </table>
</body>
</html>
"""
        TEMP = Template(stu)
        out = TEMP.render(cour=cour,id=id,total=total)
    else:
        TEMP = Template(error_temp)
        out = TEMP.render()

elif params[0]=="-c":
    marks = []
    for i in data:
        if i[1]==id:
           marks.append(int(i[2]))

    if len(marks)>0:
        avg = round(sum(marks)/len(marks),1)
        maxer = max(marks)

        crs = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Course Data</title>
</head>
<body>
    <h1>Course Details</h1>
    <table border="1">
        <tr>
            <th>Average Marks</th>
            <th>Maximum Marks</th>
        </tr>
        <tr>
            <td>{{ avg }}</td>
            <td>{{ maxer }}</td>
        </tr>
    </table>
    <img src="histo.png" alt="Histogram">
</body>
</html>
        """

        plt.hist(marks)
        plt.xlabel("Marks")
        plt.ylabel("Frequency")
        plt.savefig("histo.png")
        TEMP = Template(crs)
        out = TEMP.render(avg=avg,maxer=maxer)
    else:
        TEMP = Template(error_temp)
        out = TEMP.render()

else:
    TEMP = Template(error_temp)
    out = TEMP.render()

outer = open("output.html","w")
outer.write(out)
outer.close()
