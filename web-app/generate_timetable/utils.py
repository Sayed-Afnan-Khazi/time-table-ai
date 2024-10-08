import csv, os
def classes_to_csv(classes,csv_file_path='./generate_timetable/inputs/classes.csv'):
    '''Format expected:
        Course facilitator, course code (represents the subject), class (group of students), hours required per week, session (M for morning and A for afternoon)

Example:
[
    ["Afnan", "20CB001", "CSBS-1", "5",'M'],
    ...
]
'''
    with open(csv_file_path, mode='w') as file:
        writer = csv.writer(file)
        for iclass in classes:
            writer.writerow(iclass)

def fixed_classes_to_csv(classes,csv_file_path='./generate_timetable/inputs/fixed_classes.csv'):
    '''The format is for classes of 1 hour, to schedule multiple classes, put them in new lines:

> Format:

    Course facilitator, course code (represents the subject), class (group of students), day, timeslot

> Days:
Monday, Tuesday, Wednesday, Thursday, Friday, Saturday

> Timeslot codes:

A(7:30-8:30), B(8:30-9:30), C(9:30-10:30),
D(11:00-11:50), E(11:50-12:40), F(12:40-1:30),
G(2:30-3:30), H(3:30-4:30), I(4:30-5:30)

> Examples:

# Scheduling 12:40-1:30 for ISE-3
["JK", "20IS300", "ISE-3", "Tuesday", "F"]

# Scheduling 7:30-9:30 (two classes: 7:30-8:30 and 8:30-9:30) for CSBS-1
[
["AFK", "20CB001", "CSBS-1", "Monday", "A"],
["AFK", "20CB001", "CSBS-1", "Monday", "B"]
]'''

    with open(csv_file_path, mode='w') as file:
        writer = csv.writer(file)
        for iclass in classes:
            writer.writerow(iclass)

def lab_professors_to_csv(professors,csv_file_path='./generate_timetable/inputs/lab_professors.csv'):
    '''Takes a list of professors and writes them to a csv file.
    expects a list of professors like: ['prof1','prof2','prof3']'''
    with open(csv_file_path, mode='w') as file:
        writer = csv.writer(file)
        for professor in professors:
            writer.writerow([professor])

def getValidOutputPaths():
    '''Returns a list of valid output paths for the timetable'''
    valid_paths = ['allinone.txt']
    for x in os.listdir('./generate_timetable/outputs/tabular_outputs/facultywise_outputs'):
        valid_paths.append(f'tabular_outputs/facultywise_outputs/{x}')
    for x in os.listdir('./generate_timetable/outputs/tabular_outputs/groupwise_outputs'):
        valid_paths.append(f'tabular_outputs/groupwise_outputs/{x}')
    for x in os.listdir('./generate_timetable/outputs/tabular_outputs/roomwise_outputs'):
        valid_paths.append(f'tabular_outputs/roomwise_outputs/{x}')
    return valid_paths

if __name__ == '__main__':
    for x in getValidOutputPaths():
        print(x)
