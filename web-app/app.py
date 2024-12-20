from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
import threading
from generate_timetable import utils
from generate_timetable.time_table import run_backtrack_algo_with_threads as generate_time_table

app = Flask(__name__, template_folder='templates', static_url_path='', static_folder='static')
app.secret_key = 'super duper secret key'

# inputted_classes_1 = [
#     ["UKK", "20CB610", "CSBS-6", "3",'M'],
#     ["VHY", "20CB620", "CSBS-6", "5",'M'],
#     ["SP", "20CB630", "CSBS-6", "5",'M'],
#     ["VBK", "20CB662", "CSBS-6", "4",'M'],
#     ["SN", "20CB673", "CSBS-6", "4",'M'],
#     ["UKK+PMKS", "22CB610L", "CSBS-6", "2",'A'],
#     ["UKK+TM", "22CB610L", "CSBS-6", "2",'A'],
#     ["VBK", "22CB410", "CSBS-4", "3",'A'],
#     ["RJP", "22CB420", "CSBS-4", "3",'A'],
#     ["PMKS", "22CB430", "CSBS-4", "5",'A'],
#     ["VA", "22CB440", "CSBS-4", "5",'A'],
#     ["SG", "22CB450", "CSBS-4", "2",'A'],
#     ["FELIX", "22CB460", "CSBS-4", "2",'A'],
#     ["VBK+RSA", "22CB410L", "CSBS-4", "2",'M'],
#     ["RJP+LMS", "22CB410L", "CSBS-4", "2",'M'],
#     ["LMS", "20IS610", "ISE-6", "4","M"],
#     ["MN", "20IS620", "ISE-6", "5","M"],
#     ["CKR", "20IS630", "ISE-6", "3","M"],
#     ["SG", "20IS642", "ISE-6", "3","M"],
#     ["LMS+VA", "20IS67L", "ISE-6", "3","A"],
#     ["CKR+SG", "20IS67L", "ISE-6", "3","A"],
#     ["DSV", "22CB210", "CSBS-2", "4",'A'],
#     ["TM", "22CB230", "CSBS-2", "3",'A'],
#     ["RMN", "22CB240", "CSBS-2", "3",'A'],
#     ["LMS", "22CB250", "CSBS-2", "2",'A'],
#     ["TM", "B1-22CB230L", "CSBS-2", "2",'M'],
#     ["TM", "B2-22CB230L", "CSBS-2", "2",'A'],
#     ["RMN", "B1-22CB240L", "CSBS-2", "2",'M'],
#     ["RMN", "B2-22CB240L", "CSBS-2", "2",'A'],
#     ["VL", "22IS410", "ISE-4B", "4",'M'],
#     ["TSK", "22IS420", "ISE-4B", "4",'M'],
#     ["RSA", "22IS430", "ISE-4B", "5",'M'],
#     ["NA", "22IS440", "ISE-4B", "5",'M'],
#     ["TM", "22IS450", "ISE-4B", "3",'M'],
#     ["SAS", "B1-22IS46L", "ISE-4B", "3",'M'],
#     ["VL", "B2-22IS46L", "ISE-4B", "3",'A'],
#     ["TM", "B2-22IS47L", "ISE-4B", "3",'M'],
#     ["TM", "B1-22IS47L", "ISE-4B", "3",'A'],
#     ["VL", "22IS410", "ISE-4A", "4",'A'],
#     ["TSK", "22IS420", "ISE-4A", "4",'A'],
#     ["RSA", "22IS430", "ISE-4A", "5",'A'],
#     ["NA", "22IS440", "ISE-4A", "5",'A'],
#     ["MPS", "22IS450", "ISE-4A", "3",'A'],
#     ["VL", "B1-22IS46L", "ISE-4A", "3",'A'],
#     ["VL", "B2-22IS46L", "ISE-4A", "3",'M'],
#     ["MPS", "B2-22IS47L", "ISE-4A", "3",'M'],
#     ["MPS", "B1-22IS47L", "ISE-4A", "3",'A']
# ]
# inputted_fixed_classes_1 = [
#     ['PM', '20CB650', 'CSBS-6', 'Wednesday', '8:30-9:30'],
#     ['PM', '20CB650', 'CSBS-6', 'Wednesday', '9:30-10:30'],
#       ['MDL', '20HU612', 'CSBS-6', 'Friday', '7:30-8:30'],
#      ['MDL', '20HU612', 'CSBS-6', 'Thursday', '12:40-13:30'], ['KD', '20CB640', 'CSBS-6', 'Friday', '8:30-9:30'], ['KD', '20CB640', 'CSBS-6', 'Friday', '9:30-10:30'], ['CSB', '20HU412', 'CSBS-4', 'Tuesday', '11:00-11:50'], ['CSB', '20HU412', 'CSBS-4', 'Saturday', '11:00-11:50'], ['PM', '22CB470', 'CSBS-4', 'Thursday', '8:30-9:30'], ['PM', '22CB470', 'CSBS-4', 'Thursday', '9:30-10:30'], ['MDL', '20HU612', 'ISE-6', 'Friday', '11:00-11:50'], ['MDL', '20HU612', 'ISE-6', 'Friday', '12:40-13:30'], ['NC', '22CB220', 'CSBS-2', 'Monday', '11:50-12:40'], ['NC', '22CB220', 'CSBS-2', 'Tuesday', '12:40-13:30'], ['NC', '22CB220', 'CSBS-2', 'Wednesday', '12:40-13:30'], ['NC', '22CB220', 'CSBS-2', 'Thursday', '12:40-13:30'], ['NC', '22CB220', 'CSBS-2', 'Saturday', '11:00-11:50'], ['PM', '22CB260', 'CSBS-2', 'Wednesday', '14:30-15:30'], ['PM', '22CB260', 'CSBS-2', 'Saturday', '11:50-12:40'], ['AHK', '22MA412', 'ISE-4B', 'Tuesday', '11:00-11:50'], ['AHK', '22MA412', 'ISE-4B', 'Wednesday', '7:30-8:30'], ['AHK', '22MA412', 'ISE-4B', 'Saturday', '11:00-11:50'], ['SU', '22HU412', 'ISE-4B', 'Monday', '12:40-13:30'], ['SU', '22HU412', 'ISE-4B', 'Saturday', '9:30-10:30'], ['AHK', '22MA412', 'ISE-4A', 'Monday', '11:50-12:40'], ['AHK', '22MA412', 'ISE-4A', 'Tuesday', '8:30-9:30'], ['AHK', '22MA412', 'ISE-4A', 'Friday', '11:50-12:40'], ['CSB', '22HU412', 'ISE-4A', 'Monday', '11:00-11:50'], ['CSB', '22HU412', 'ISE-4A', 'Thursday', '12:40-13:30']]
# inputted_lab_professors_1 = [
#     "SU",
#     "VL",
#     "LMS",
#     "VBK",
#     "TM",
#     "TSK",
#     "PMKS",
#     "RMN",
#     "SG",
#     "RJP",
#     "RSA",
#     "SN",
#     "NA",
#     "MPS"
# ]
inputted_classes = [
    ["MPS", "20IS731", "ISE-7", "3", "M"],
    ["VBK", "20IS721", "ISE-7", "3", "M"],
    ["BSM", "20IS710", "ISE-7", "4", "M"],
    ["SG", "20CB710", "CSBS-7", "4", "A"],
    ["SP", "20CB742", "CSBS-7", "4", "A"],
    ["VA", "20CB752", "CSBS-7", "4", "A"],
    ["BSM+RSA", "B1-20CB76L", "CSBS-7", "2", "M"],
    ["VBK+NA", "B2-20CB76L", "CSBS-7", "2", "M"],
    ["VHY", "22IS510", "ISE-5A", "4", "M"],
    ["UKK", "22IS520", "ISE-5A", "4", "M"],
    ["RJP", "22IS530", "ISE-5A", "4", "M"],
    ["PSJ", "22IS540", "ISE-5A", "4", "M"],
    ["LMS+VK", "B1-22IS57L", "ISE-5A", "3", "M"],
    ["VBK+VP", "B2-22IS57L", "ISE-5A", "3", "M"],
    ["SAS+MPS", "B1-22IS58L", "ISE-5A", "3", "M"],
    ["PSJ+SN", "B2-22IS58L", "ISE-5A", "3", "M"],
    ["VHY", "22IS510", "ISE-5B", "4", "A"],
    ["UKK", "22IS520", "ISE-5B", "4", "A"],
    ["RJP", "22IS530", "ISE-5B", "4", "A"],
    ["PSJ", "22IS540", "ISE-5B", "4", "A"],
    ["TM+F2", "B1-22IS57L", "ISE-5B", "3", "A"],
    ["SR+F1", "B2-22IS57L", "ISE-5B", "3", "A"],
    ["SR+VK", "B1-22IS58L", "ISE-5B", "3", "A"],
    ["TSK+F2", "B2-22IS58L", "ISE-5A", "3", "A"],
    ["TM", "22CB510", "CSBS-5", "3", "A"],
    ["SR", "22CB520", "CSBS-5", "3", "A"],
    ["DSV", "22CB550", "CSBS-5", "2", "A"],
    ["MN", "22CB572", "CSBS-5", "4", "A"],
    ["MN+F2", "B1-22CB510L", "CSBS-5", "2", "A"],
    ["LMS+F1", "B1-22CB510L", "CSBS-5", "2", "A"],
    ["NA+F1", "B1-22CB520L", "CSBS-5", "2", "A"],
    ["TM+F2", "B1-22CB520L", "CSBS-5", "2", "A"],
    ["SAS", "22IS310", "ISE-3A", "4", "M"],
    ["NA", "22IS320", "ISE-3A", "4", "M"],
    ["CKR", "22IS330", "ISE-3A", "3", "M"],
    ["RAS", "22IS340", "ISE-3A", "3", "M"],
    ["VL", "22IS350", "ISE-3A", "3", "M"],
    ["SN", "22HU311", "ISE-3A", "2", "M"],
    ["PSJ+F1", "B1-22IS36L", "ISE-3A", "3", "M"],
    ["TM+SAS", "B2-22IS36L", "ISE-3A", "3", "M"],
    ["RSA+F2", "B1-22IS37L", "ISE-3A", "3", "M"],
    ["VBK+VP", "B2-22IS37L", "ISE-3A", "3", "M"],
    ["SAS", "22IS310", "ISE-3B", "4", "A"],
    ["NA", "22IS320", "ISE-3B", "4", "A"],
    ["CKR", "22IS330", "ISE-3B", "3", "A"],
    ["RAS", "22IS340", "ISE-3B", "3", "A"],
    ["VL", "22IS350", "ISE-3B", "3", "A"],
    ["SR", "22HU311", "ISE-3B", "2", "A"],
    ["MPS+TM", "B1-22IS36L", "ISE-3B", "3", "A"],
    ["MN+VK", "B2-22IS36L", "ISE-3B", "3", "A"],
    ["VK+F1", "B1-22IS37L", "ISE-3B", "3", "A"],
    ["SR+RSA", "B2-22IS37L", "ISE-3B", "3", "A"],
    ["TSK", "22CB310", "CSBS-3", "4", "M"],
    ["MPS", "22CB320", "CSBS-3", "4", "M"],
    ["DSV", "22CB330", "CSBS-3", "3", "M"],
    ["LMS", "22CB340", "CSBS-3", "3", "M"],
    ["SN", "22CB350", "CSBS-3", "4", "M"],
    ["SAS", "22HU311", "CSBS-3", "2", "M"],
    ["DSV+SN", "B1-22CB330", "CSBS-3", "2", "M"],
    ["VP+SR", "B2-22CB330", "CSBS-3", "2", "M"],
    ["SN+TSK", "B1-22CB340", "CSBS-3", "2", "M"],
    ["VA+TM", "B2-22CB340", "CSBS-3", "2", "M"]
]
inputted_fixed_classes = [
    ["SR", "20IS741", "B1-ISE-7", "Friday", "7:30-8:30"],
    ["SR", "20IS741", "B1-ISE-7", "Friday", "8:30-9:30"],
    ["SN", "20IS742", "B2-ISE-7", "Friday", "7:30-8:30"],
    ["SN", "20IS742", "B2-ISE-7", "Friday", "8:30-9:30"],
    ["SR", "20IS741", "B1-ISE-7", "Saturday", "11:00-11:50"],
    ["SN", "20IS742", "B2-ISE-7", "Saturday", "11:00-11:50"],
    ["PMKS", "20IS753", "ISE-7", "Saturday", "7:30-8:30"],
    ["PMKS", "20IS753", "ISE-7", "Saturday", "8:30-9:30"],
    ["PMKS", "20IS753", "ISE-7", "Friday", "11:00-11:50"],
    ["FELIX", "20CB710", "CSBS-7", "Wednesday", "15:30-16:30"],
    ["FELIX", "20CB710", "CSBS-7", "Wednesday", "16:30-17:30"],
    ["FELIX", "20CB710", "CSBS-7", "Thursday", "15:30-16:30"],
    ["FELIX", "20CB710", "CSBS-7", "Friday", "14:30-15:30"],
    ["FELIX", "20CB730", "CSBS-7", "Wednesday", "16:30-17:30"],
    ["FELIX", "20CB730", "CSBS-7", "Thursday", "14:30-15:30"],
    ["FELIX", "20CB730", "CSBS-7", "Friday", "15:30-16:30"],
    ["FELIX", "20CB730", "CSBS-7", "Saturday", "7:30-8:30"],
    ["LMS", "22IS562", "B1-ISE-5", "Monday", "11:00-11:50"],
    ["LMS", "22IS562", "B1-ISE-5", "Tuesday", "11:00-11:50"],
    ["LMS", "22IS562", "B1-ISE-5", "Wednesday", "11:00-11:50"],
    ["TSK", "22IS563", "B2-ISE-5", "Monday", "11:00-11:50"],
    ["TSK", "22IS563", "B2-ISE-5", "Tuesday", "11:00-11:50"],
    ["TSK", "22IS563", "B2-ISE-5", "Wednesday", "11:00-11:50"],
    ["TM", "22IS551", "B1-ISE-5", "Tuesday", "12:40-13:30"],
    ["VK", "22IS552", "B2-ISE-5", "Tuesday", "12:40-13:30"],
    ["TM", "22IS551", "B1-ISE-5", "Thursday", "12:40-13:30"],
    ["VK", "22IS552", "B2-ISE-5", "Thursday", "12:40-13:30"],
    ["TM", "22IS551", "B1-ISE-5", "Friday", "14:30-15:30"],
    ["VK", "22IS552", "B2-ISE-5", "Friday", "14:30-15:30"],
    ["PMKS", "22CB561", "B1-CSBS-5", "Monday", "11:00-11:50"],
    ["PMKS", "22CB561", "B1-CSBS-5", "Tuesday", "11:00-11:50"],
    ["PMKS", "22CB561", "B1-CSBS-5", "Wednesday", "11:00-11:50"],
    ["VBK", "22CB562", "B2-CSBS-5", "Monday", "11:00-11:50"],
    ["VBK", "22CB562", "B2-CSBS-5", "Tuesday", "11:00-11:50"],
    ["VBK", "22CB562", "B2-CSBS-5", "Wednesday", "11:00-11:50"],
    ["MP", "22CB530", "CSBS-5", "Monday", "16:30-17:30"],
    ["MP", "22CB530", "CSBS-5", "Wednesday", "15:30-16:30"],
    ["MP", "22CB530", "CSBS-5", "Wednesday", "16:30-17:30"],
    ["FELIX", "22CB540", "CSBS-5", "Monday", "14:30-15:30"],
    ["FELIX", "22CB540", "CSBS-5", "Monday", "15:30-16:30"],
    ["FELIX", "22CB540", "CSBS-5", "Wednesday", "14:30-15:30"],
    ["RJ", "22MA312", "ISE-3A", "Monday", "7:30-8:30"],
    ["RJ", "22MA312", "ISE-3A", "Tuesday", "9:30-10:30"],
    ["RJ", "22MA312", "ISE-3A", "Wednesday", "11:00-11:50"],
    ["DK", "22CB360", "CSBS-3", "Friday", "8:30-9:30"],
    ["DK", "22CB360", "CSBS-3", "Friday", "9:30-10:30"]
]
inputted_lab_professors = []
valid_paths = []


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
        course_session = request.form['course_session']
        if not course_facilitator or not course_code or not course_group or not course_hours_required or not course_session:
            flash('Please fill all fields!', 'danger')
        else:
            inputted_classes.append([course_facilitator,course_code,course_group,course_hours_required,course_session])
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
    global inputted_classes, inputted_fixed_classes, inputted_lab_professors, valid_paths
    if request.method == 'POST':
        utils.classes_to_csv(inputted_classes)
        map_fixed_classes_timeslots(inputted_fixed_classes)
        utils.fixed_classes_to_csv(inputted_fixed_classes)
        utils.lab_professors_to_csv(inputted_lab_professors)
        inputted_classes = []
        inputted_fixed_classes = []
        inputted_lab_professors = []
        generate_time_table()
        valid_paths = utils.getValidOutputPaths()
        return redirect('/timetable')
    else:
        return render_template('generate_timetable.html',classes=list(enumerate(inputted_classes)),fixed_classes=list(enumerate(inputted_fixed_classes)),lab_professors=list(enumerate(inputted_lab_professors)))

@app.route('/timetable')
def timetable():
    global valid_paths
    if valid_paths == []:
        valid_paths = utils.getValidOutputPaths()
        if valid_paths == []:
            flash('No timetables generated yet!', 'danger')
            return redirect('/')
    facultywise_outputs = []
    groupwise_outputs = []
    roomwise_outputs = []
    for path in valid_paths:
        if 'facultywise_outputs' in path:
            facultywise_outputs.append([path[36:],path])
        elif 'groupwise_outputs' in path:
            groupwise_outputs.append([path[34:],path])
        elif 'roomwise_outputs' in path:
            roomwise_outputs.append([path[33:],path])
    return render_template('timetable.html', 
                           facultywise_outputs=facultywise_outputs,
                            groupwise_outputs=groupwise_outputs, 
                            roomwise_outputs=roomwise_outputs)


@app.route('/get_timetable')
def get_timetable():
    path = request.args.get('path')
    global valid_paths
    if valid_paths == []:
        flash('No timetables generated yet!', 'danger')
        return redirect('/')
    path = path.replace(' ','+') # For those pesky lab classes names with pluses being converted to spaces while url encoding
    if path in valid_paths:
        with open(f'./generate_timetable/outputs/{path}') as file:
            timetable_raw_html = file.read()
            timetable_raw_html = timetable_raw_html.replace('No class scheduled',' ') # For neater tables
        return render_template('display_timetable.html',timetable_raw_html=timetable_raw_html, timetable_name=path.replace('tabular_outputs/','').replace(".txt",''))
    else:
        flash('Invalid timetable path! Please generate timetables', 'danger')
        return redirect('/generate_timetable')

if __name__ == '__main__':
    app.run(port=8000,debug=True)