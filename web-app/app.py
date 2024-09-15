from flask import Flask, render_template, request, flash, redirect, url_for
from generate_timetable import utils

app = Flask(__name__, template_folder='templates', static_url_path='', static_folder='static')
app.secret_key = 'super duper secret key'

classes = []
fixed_classes = []
lab_professors = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_classes', methods=['POST','GET'])
def add_classes():
    global classes
    if request.method == 'POST':
        course_facilitator = request.form['course_facilitator']
        course_code = request.form['course_code']
        course_group = request.form['course_group']
        course_hours_required = request.form['course_hours_required']
        if not course_facilitator or not course_code or not course_group or not course_hours_required:
            flash('Please fill all fields!', 'danger')
        else:
            classes.append([course_facilitator,course_code,course_group,course_hours_required])
            flash('Class added!', 'success')
        return render_template('add_classes.html',classes=list(enumerate(classes)))
    else:
        return render_template('add_classes.html',classes=list(enumerate(classes)))
    
@app.route('/delete_class/<ind>')
def delete_class(ind):
    global classes
    ind = int(ind)
    if ind not in range(len(classes)):
        flash('Invalid delete index!', 'danger')
        return render_template('add_classes.html',classes=list(enumerate(classes))), 400
    else:
        classes.pop(ind)
        flash('Class deleted!', 'success')
        return render_template('add_classes.html',classes=list(enumerate(classes)))
    
@app.route('/add_fixed_classes', methods=['POST','GET'])
def add_fixed_classes():
    global fixed_classes
    print(fixed_classes)
    if request.method == 'POST':
        course_facilitator = request.form['course_facilitator']
        course_code = request.form['course_code']
        course_group = request.form['course_group']
        course_day = request.form['course_day']
        course_timeslot = request.form['course_timeslot']
        if not course_facilitator or not course_code or not course_group or not course_day or not course_timeslot:
            flash('Please fill all fields!', 'danger')
        else:
            fixed_classes.append([course_facilitator,course_code,course_group,course_day,course_timeslot])
            flash('Fixed class added!', 'success')
        return render_template('add_fixed_classes.html',fixed_classes=list(enumerate(fixed_classes)))
    else:
        return render_template('add_fixed_classes.html',fixed_classes=list(enumerate(fixed_classes)))
    
@app.route('/delete_fixed_class/<ind>')
def delete_fixed_class(ind):
    global fixed_classes
    ind = int(ind)
    if ind not in range(len(fixed_classes)):
        flash('Invalid delete index!', 'danger')
        return render_template('add_fixed_classes.html',fixed_classes=list(enumerate(fixed_classes)))
    else:
        fixed_classes.pop(ind)
        flash('Fixed class deleted!', 'success')
        return render_template('add_fixed_classes.html',fixed_classes=list(enumerate(fixed_classes)))
    
@app.route('/add_lab_professors', methods=['POST','GET'])
def add_lab_professors():
    global lab_professors
    if request.method == 'POST':
        if not request.form['professor_name']:
            flash('Please fill all fields!', 'danger')
            return render_template('add_lab_professors.html',lab_professors=list(enumerate(lab_professors)))
        lab_professors.append(request.form['professor_name'])
        flash('Lab professor added!', 'success')
        return render_template('add_lab_professors.html',lab_professors=list(enumerate(lab_professors)))
    else:
        return render_template('add_lab_professors.html',lab_professors=list(enumerate(lab_professors)))

@app.route('/delete_lab_professor/<ind>')
def delete_lab_professor(ind):
    global lab_professors
    ind = int(ind)
    if ind not in range(len(lab_professors)):
        flash('Invalid delete index!', 'danger')
        return render_template('add_lab_professors.html',lab_professors=list(enumerate(lab_professors)))
    else:
        lab_professors.pop(ind)
        flash('Lab professor deleted!', 'success')
        return render_template('add_lab_professors.html',lab_professors=list(enumerate(lab_professors)))

if __name__ == '__main__':
    app.run(port=8000,debug=True)