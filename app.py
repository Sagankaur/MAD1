import csv
import sys
from pyhtml import *
import matplotlib.pyplot as plt
from jinja2 import Template

def generate_student_html(student_id):
    student_data={}
    total_marks=0
    data=[]
    f= open('data.csv','r')
    for reader in f.readlines()[1:]:
        data.append(reader.strip().split(','))
    f.close()
    for row in data:
        if row[0] == student_id:
            student_data[row[1]] = row[2] #{couse:marks}
            total_marks += int(row[2])
    if not student_data:
        return generate_error()
    else:
        html_output = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>
                Student Data
            </title>
        </head>
        <body>
            <h1>
            Student Details
            </h1>
            <table border ='1' >
            <tr>
                <th>Student id</th>
                <th>Course id</th>
                <th>Marks</th>
            </tr>
            {%for i in student_data %}
            <tr>
                <td>{{student_id}}</td>
                <td>{{i}}</td>
                <td>{{student_data[i]}}</td>
            </tr>
            {%endfor%}
            <tr>
                <td colspan="2">Total Marks</td>
                <td>{{total_marks}}</td>
            </tr>
            </table>
        </body>
        </html>
        '''
        Temp= Template(html_output)
        out = Temp.render(student_id=student_id,total_marks=total_marks,student_data=student_data)
        f=open('output.html', 'w')
        f.write(out)
        f.close()
def generate_course_html(course_id):
    marks=[]
    data=[]
    f= open('data.csv','r')
    for reader in f.readlines()[1:]:
        data.append(reader.strip().split(', '))
    f.close()
    for row in data:
        if row[1] == course_id: #course id same?
            marks.append(int(row[2])) #marks will be appended 
    if len(marks)<=0:
        return generate_error()
    elif len(marks)>=1:
        Average_Marks=round(sum(marks)/len(marks),1)
        Max_marks=max(marks)
        plt.hist(marks, bins=10, color='skyblue', edgecolor='black')
        plt.xlabel('Marks')
        plt.ylabel('Frequency')
        plt.savefig('histogram.png')

        html_output='''
        <!DOCTYPE html>
        <html>
            <head>
                <title>
                    Course Data
                </title>
            </head>
            <body>
                <h1> Course Details</h1>
                <table border="1">
                    <tr>
                        <th>Average Marks</th>
                        <th>Maximum Marks</th>
                    </tr>
                    <tr>
                        <td>{{Average_Marks}}</td>
                        <td>{{Max_marks}}</td>
                    </tr>
                </table>
                <img src='histogram.png' alt='Histogram'>
            </body>
        </html> '''
        temp=Template(html_output)
        out=temp.render(Average_Marks=Average_Marks,Max_marks=Max_marks)
        f=open('output.html', 'w')
        f.write(out)
        f.close()
        
def generate_error():
    html_output= html(head(title('Something went wrong')),
    body(h1('Wrong Inputs'),
    h2('Something went wrong')))

    with open('output.html', 'w') as f:
        f.write(str(html_output))

if len(sys.argv)!=3:
    generate_error()
else:
    flag = sys.argv[1]
    id_value = sys.argv[2]
    if flag == '-s':
        generate_student_html(id_value)
    elif flag == '-c':
        generate_course_html(id_value)
    else:
        generate_error()
