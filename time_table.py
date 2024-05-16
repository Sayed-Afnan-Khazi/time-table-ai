import random
import csv
import os

class Class:
    def __init__(self, faculty, name_code, group, hours):
        self.faculty = faculty
        self.name_code = name_code
        self.group = group
        self.hours = hours
        self.original_hours = self.hours

    def __str__(self):
        return f"{self.faculty} conducting {self.hours} of {self.name_code}"
    
    def format(self):
        return f"{self.faculty} - {self.name_code} - {self.group}"
    
# Read the csv file classes.csv
def read_classes():
    classes = []
    with open('classes.csv', 'r') as file:
        for line in file:
            faculty, name_code, group, hours = line.strip().split(',')
            classes.append(Class(faculty, name_code, group, int(hours)))
    return classes

## Structure of the 3D hash table:

# { day_of_week: {time: {room: [Class] | None }}}

# Parameters Considered:

# day_of_week: 1-6 (Monday-Saturday) # Need to implement Saturday till 1:30PM
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# timeslots are represented as:
# A(7:30-8:30), B(8:30-9:30), C(9:30-10:30),
# D(11:00-11:50), E(11:50-12:40), F(12:40-1:30),
# G(2:30-3:30), H(3:30-4:30), I(4:30-5:30)
timeslots = {'A': '7:30-8:30', 'B': '8:30-9:30', 'C': '9:30-10:30', 'D': '11:00-11:50', 'E': '11:50-12:40', 'F': '12:40-1:30', 'G': '2:30-3:30', 'H': '3:30-4:30', 'I': '4:30-5:30'}

# rooms: IS101, IS102, IS103 (for now)
rooms = ['IS101', 'IS102', 'IS103']

def init_time_table(days, timeslots, rooms):
    time_table = {}
    for day in days:
        time_table[day] = {}
        for time in timeslots.keys():
            time_table[day][time] = {}
            for room in rooms:
                time_table[day][time][room] = None

    return time_table

def print_time_table(time_table):
    global timeslots
    output_dir = 'outputs'
    os.makedirs(output_dir, exist_ok=True)
    
    for day, slots in time_table.items():
        day_file = os.path.join(output_dir, f"{day.lower()}.csv")
        
        with open(day_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time Slot', 'Room', 'Class'])
            
            for slot, rooms in slots.items():
                for room, cls in rooms.items():
                    if cls is not None:
                        writer.writerow([timeslots[slot], room, cls.format()])
                    else:
                        writer.writerow([timeslots[slot], room, 'No class scheduled'])

def class_to_allot(classes):
    random.shuffle(classes) # To introduce randomness and make it non-deterministic.
    for cls in classes:
        if cls.hours > 0:
            return cls
    return None


def backtrack_schedule(time_table, classes):
    
    cls = class_to_allot(classes)
    if cls is None:
        return True
    
    for day in days:
        for time in timeslots.keys():
            for room in rooms:
                if time_table[day][time][room] is None and cls.faculty not in [time_table[day][time][r].faculty if time_table[day][time][r] else None for r in rooms] and cls.group not in [time_table[day][time][r].group if time_table[day][time][r] else None for r in rooms] and cls.hours > 0:
                    time_table[day][time][room] = cls
                    cls.hours -= 1
                    print("Allotted",cls.format())

                    if backtrack_schedule(time_table, classes):
                        return True

                    time_table[day][time][room] = None
                    cls.hours += 1
                    print("De-Allotted",cls.format())
    
    return False

def schedule_classes(time_table, classes):
    return backtrack_schedule(time_table, classes)

def create_faculty_hours_allotted_table(time_table):
    global classes
    # Calculate the total hours allotted for each faculty
    faculty_hours = {}
    for day, slots in time_table.items():
        for slot, rooms in slots.items():
            for room, cls in rooms.items():
                if cls is not None:
                    if cls.faculty not in faculty_hours:
                        faculty_hours[cls.faculty] = 1
                    faculty_hours[cls.faculty] += 1

    # Calculate the original hours to be allotted for each faculty
    original_hours = {}
    for cls in classes:
        if cls.faculty not in original_hours:
            original_hours[cls.faculty] = cls.original_hours
        original_hours[cls.faculty] += cls.original_hours
    
    # Save faculty names and their total hour count in outputs/faculty_hours_allotted.csv
    output_dir = 'outputs'
    os.makedirs(output_dir, exist_ok=True)
    faculty_hours_file = os.path.join(output_dir, 'faculty_hours_allotted.csv')
    
    with open(faculty_hours_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Faculty', 'Total Hours Allotted', 'Total Hours to be Allotted'])
        
        for faculty, hours in faculty_hours.items():
            writer.writerow([faculty, hours, original_hours[faculty]])
    
    return faculty_hours

if __name__ == '__main__':
    classes = read_classes()
    time_table = init_time_table(days, timeslots, rooms)
    print(schedule_classes(time_table, classes))
    create_faculty_hours_allotted_table(time_table)
    print_time_table(time_table)