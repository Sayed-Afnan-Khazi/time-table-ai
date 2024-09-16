from flask import Flask, render_template, request, flash, redirect, url_for
from generate_timetable import utils
from generate_timetable.time_table import generate_time_table

app = Flask(__name__, template_folder='templates', static_url_path='', static_folder='static')
app.secret_key = 'super duper secret key'

inputted_classes = [
    ["UKK", "20CB610", "CSBS-6", "3"],
    ["VHY", "20CB620", "CSBS-6", "5"],
    ["SP", "20CB630", "CSBS-6", "5"],
    ["VBK", "20CB662", "CSBS-6", "4"],
    ["SN", "20CB673", "CSBS-6", "4"],
    ["UKK+PMKS", "22CB610L", "CSBS-6", "2"],
    ["UKK+TM", "22CB610L", "CSBS-6", "2"],
    ["VBK", "22CB410", "CSBS-4", "3"],
    ["RJP", "22CB420", "CSBS-4", "3"],
    ["PMKS", "22CB430", "CSBS-4", "5"],
    ["VA", "22CB440", "CSBS-4", "5"],
    ["SG", "22CB450", "CSBS-4", "2"],
    ["FELIX", "22CB460", "CSBS-4", "2"],
    ["VBK+RSA", "22CB410L", "CSBS-4", "2"],
    ["RJP+LMS", "22CB410L", "CSBS-4", "2"],
    ["LMS", "20IS610", "ISE-6", "4"],
    ["MN", "20IS620", "ISE-6", "5"],
    ["CKR", "20IS630", "ISE-6", "3"],
    ["SG", "20IS642", "ISE-6", "3"],
    ["LMS+VA", "20IS67L", "ISE-6", "3"],
    ["CKR+SG", "20IS67L", "ISE-6", "3"],
    ["DSV", "22CB210", "CSBS-2", "4"],
    ["TM", "22CB230", "CSBS-2", "3"],
    ["RMN", "22CB240", "CSBS-2", "3"],
    ["LMS", "22CB250", "CSBS-2", "2"],
    ["TM", "B1-22CB230L", "CSBS-2", "2"],
    ["TM", "B2-22CB230L", "CSBS-2", "2"],
    ["RMN", "B1-22CB240L", "CSBS-2", "2"],
    ["RMN", "B2-22CB240L", "CSBS-2", "2"],
    ["VL", "22IS410", "ISE-4B", "4"],
    ["TSK", "22IS420", "ISE-4B", "4"],
    ["RSA", "22IS430", "ISE-4B", "5"],
    ["NA", "22IS440", "ISE-4B", "5"],
    ["TM", "22IS450", "ISE-4B", "3"],
    ["SAS", "B1-22IS46L", "ISE-4B", "3"],
    ["VL", "B2-22IS46L", "ISE-4B", "3"],
    ["TM", "B2-22IS47L", "ISE-4B", "3"],
    ["TM", "B1-22IS47L", "ISE-4B", "3"],
    ["VL", "22IS410", "ISE-4A", "4"],
    ["TSK", "22IS420", "ISE-4A", "4"],
    ["RSA", "22IS430", "ISE-4A", "5"],
    ["NA", "22IS440", "ISE-4A", "5"],
    ["MPS", "22IS450", "ISE-4A", "3"],
    ["VL", "B1-22IS46L", "ISE-4A", "3"],
    ["VL", "B2-22IS46L", "ISE-4A", "3"],
    ["MPS", "B2-22IS47L", "ISE-4A", "3"],
    ["MPS", "B1-22IS47L", "ISE-4A", "3"]
]
inputted_fixed_classes = [
    ['PM', '20CB650', 'CSBS-6', 'Wednesday', '8:30-9:30'],
    ['PM', '20CB650', 'CSBS-6', 'Wednesday', '9:30-10:30'],
      ['MDL', '20HU612', 'CSBS-6', 'Friday', '7:30-8:30'],
     ['MDL', '20HU612', 'CSBS-6', 'Thursday', '12:40-13:30'], ['KD', '20CB640', 'CSBS-6', 'Friday', '8:30-9:30'], ['KD', '20CB640', 'CSBS-6', 'Friday', '9:30-10:30'], ['CSB', '20HU412', 'CSBS-4', 'Tuesday', '11:00-11:50'], ['CSB', '20HU412', 'CSBS-4', 'Saturday', '11:00-11:50'], ['PM', '22CB470', 'CSBS-4', 'Thursday', '8:30-9:30'], ['PM', '22CB470', 'CSBS-4', 'Thursday', '9:30-10:30'], ['MDL', '20HU612', 'ISE-6', 'Friday', '11:00-11:50'], ['MDL', '20HU612', 'ISE-6', 'Friday', '12:40-13:30'], ['NC', '22CB220', 'CSBS-2', 'Monday', '11:50-12:40'], ['NC', '22CB220', 'CSBS-2', 'Tuesday', '12:40-13:30'], ['NC', '22CB220', 'CSBS-2', 'Wednesday', '12:40-13:30'], ['NC', '22CB220', 'CSBS-2', 'Thursday', '12:40-13:30'], ['NC', '22CB220', 'CSBS-2', 'Saturday', '11:00-11:50'], ['PM', '22CB260', 'CSBS-2', 'Wednesday', '14:30-15:30'], ['PM', '22CB260', 'CSBS-2', 'Saturday', '11:50-12:40'], ['AHK', '22MA412', 'ISE-4B', 'Tuesday', '11:00-11:50'], ['AHK', '22MA412', 'ISE-4B', 'Wednesday', '7:30-8:30'], ['AHK', '22MA412', 'ISE-4B', 'Saturday', '11:00-11:50'], ['SU', '22HU412', 'ISE-4B', 'Monday', '12:40-13:30'], ['SU', '22HU412', 'ISE-4B', 'Saturday', '9:30-10:30'], ['AHK', '22MA412', 'ISE-4A', 'Monday', '11:50-12:40'], ['AHK', '22MA412', 'ISE-4A', 'Tuesday', '8:30-9:30'], ['AHK', '22MA412', 'ISE-4A', 'Friday', '11:50-12:40'], ['CSB', '22HU412', 'ISE-4A', 'Monday', '11:00-11:50'], ['CSB', '22HU412', 'ISE-4A', 'Thursday', '12:40-13:30']]
inputted_lab_professors = [
    "SU",
    "VL",
    "LMS",
    "VBK",
    "TM",
    "TSK",
    "PMKS",
    "RMN",
    "SG",
    "RJP",
    "RSA",
    "SN",
    "NA",
    "MPS"
]

def map_fixed_classes_timeslots(fixed_classes):
    fixed_classes_timeslots_map = {'7:30-8:30': 'A', '8:30-9:30': 'B', '9:30-10:30': 'C', '10:30-11:00': 'M_BREAK', '11:00-11:50': 'D', '11:50-12:40': 'E', '12:40-13:30': 'F', '13:30-14:30': 'L_BREAK', '14:30-15:30': 'G', '15:30-16:30': 'H', '16:30-17:30': 'I'}
    for fixed_class in fixed_classes:
        fixed_class[-1] = fixed_classes_timeslots_map[fixed_class[-1]]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_classes', methods=['POST','GET'])
def add_classes():
    global inputted_classes
    if request.method == 'POST':
        course_facilitator = request.form['course_facilitator']
        course_code = request.form['course_code']
        course_group = request.form['course_group']
        course_hours_required = request.form['course_hours_required']
        if not course_facilitator or not course_code or not course_group or not course_hours_required:
            flash('Please fill all fields!', 'danger')
        else:
            inputted_classes.append([course_facilitator,course_code,course_group,course_hours_required])
            flash('Class added!', 'success')
        return render_template('add_classes.html',classes=list(enumerate(inputted_classes)))
    else:
        return render_template('add_classes.html',classes=list(enumerate(inputted_classes)))
    
@app.route('/delete_class/<ind>', methods=['POST'])
def delete_class(ind):
    global inputted_classes
    ind = int(ind)
    if ind not in range(len(inputted_classes)):
        flash('Invalid delete index!', 'danger')
        return render_template('add_classes.html',classes=list(enumerate(inputted_classes))), 400
    else:
        inputted_classes.pop(ind)
        flash('Class deleted!', 'success')
        return render_template('add_classes.html',classes=list(enumerate(inputted_classes)))
    
@app.route('/add_fixed_classes', methods=['POST','GET'])
def add_fixed_classes():
    global inputted_fixed_classes
    print(inputted_fixed_classes)
    if request.method == 'POST':
        course_facilitator = request.form['course_facilitator']
        course_code = request.form['course_code']
        course_group = request.form['course_group']
        course_day = request.form['course_day']
        course_timeslot = request.form['course_timeslot']
        if not course_facilitator or not course_code or not course_group or not course_day or not course_timeslot:
            flash('Please fill all fields!', 'danger')
        else:
            inputted_fixed_classes.append([course_facilitator,course_code,course_group,course_day,course_timeslot])
            flash('Fixed class added!', 'success')
        return render_template('add_fixed_classes.html',fixed_classes=list(enumerate(inputted_fixed_classes)))
    else:
        return render_template('add_fixed_classes.html',fixed_classes=list(enumerate(inputted_fixed_classes)))
    
@app.route('/delete_fixed_class/<ind>')
def delete_fixed_class(ind):
    global inputted_fixed_classes
    ind = int(ind)
    if ind not in range(len(inputted_fixed_classes)):
        flash('Invalid delete index!', 'danger')
        return render_template('add_fixed_classes.html',fixed_classes=list(enumerate(inputted_fixed_classes)))
    else:
        inputted_fixed_classes.pop(ind)
        flash('Fixed class deleted!', 'success')
        return render_template('add_fixed_classes.html',fixed_classes=list(enumerate(inputted_fixed_classes)))
    
@app.route('/add_lab_professors', methods=['POST','GET'])
def add_lab_professors():
    global inputted_lab_professors
    if request.method == 'POST':
        if not request.form['professor_name']:
            flash('Please fill all fields!', 'danger')
            return render_template('add_lab_professors.html',lab_professors=list(enumerate(inputted_lab_professors)))
        inputted_lab_professors.append(request.form['professor_name'])
        flash('Lab professor added!', 'success')
        return render_template('add_lab_professors.html',lab_professors=list(enumerate(inputted_lab_professors)))
    else:
        return render_template('add_lab_professors.html',lab_professors=list(enumerate(inputted_lab_professors)))

@app.route('/delete_lab_professor/<ind>')
def delete_lab_professor(ind):
    global inputted_lab_professors
    ind = int(ind)
    if ind not in range(len(inputted_lab_professors)):
        flash('Invalid delete index!', 'danger')
        return render_template('add_lab_professors.html',lab_professors=list(enumerate(inputted_lab_professors)))
    else:
        inputted_lab_professors.pop(ind)
        flash('Lab professor deleted!', 'success')
        return render_template('add_lab_professors.html',lab_professors=list(enumerate(inputted_lab_professors)))

@app.route('/generate_timetable', methods=['POST','GET'])
def generate_timetable():
    global inputted_classes, inputted_fixed_classes, inputted_lab_professors
    if request.method == 'POST':
        utils.classes_to_csv(inputted_classes)
        map_fixed_classes_timeslots(inputted_fixed_classes)
        utils.fixed_classes_to_csv(inputted_fixed_classes)
        utils.lab_professors_to_csv(inputted_lab_professors)
        inputted_classes = []
        inputted_fixed_classes = []
        inputted_lab_professors = []
        generate_time_table()
        return render_template('timetable.html')
    else:
        return render_template('generate_timetable.html',classes=list(enumerate(inputted_classes)),fixed_classes=list(enumerate(inputted_fixed_classes)),lab_professors=list(enumerate(inputted_lab_professors)))

if __name__ == '__main__':
    app.run(port=8000,debug=True)