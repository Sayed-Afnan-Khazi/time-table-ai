import random
import csv
import os
from prettytable import PrettyTable, from_csv, DOUBLE_BORDER

class Class:
    def __init__(self, faculty, name_code, group, hours):
        self.faculty = faculty
        self.name_code = name_code
        self.group = group
        self.hours = hours
        self.original_hours = self.hours

        if self.name_code.endswith('L'):
            # For laboratory classes
            self.class_type = 'L'
            faculties = self.faculty.split('+')
            self.faculty1 = faculties[0]
            self.faculty2 = faculties[1]
        else:
            # For theory classes
            self.class_type = 'T'

    def __str__(self):
        return f"{self.faculty} conducting {self.hours} of {self.name_code}"
    
    def format(self):
        return f"{self.faculty} - {self.name_code} - {self.group}"

class Break(Class):
    def __init__(self) -> None:
        self.faculty = None
        self.name_code = None
        self.group = None
        self.hours = None
    def format(self):
        return str(None)


faculties_set = set()
groups_set = set()

# Read the csv file classes.csv
def read_classes():
    global faculties_set, groups_set
    classes = []
    with open('classes.csv', 'r') as file:
        for line in file:
            faculty, name_code, group, hours = line.strip().split(',')
            faculties_set.add(faculty)
            groups_set.add(group)
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
timeslots = {'A': '7:30-8:30', 'B': '8:30-9:30', 'C': '9:30-10:30', 'M_BREAK':'10:30-11:00','D': '11:00-11:50', 'E': '11:50-12:40', 'F': '12:40-13:30', 'L_BREAK':'13:30-14:30','G': '14:30-15:30', 'H': '15:30-16:30', 'I': '16:30-17:30'}

# rooms: IS101, IS102, IS103 (for now)
rooms = ['IS101', 'IS102', 'IS103']

# labs: ISLAB1, ISLAB2 (for now)
labs = ['ISLAB1', 'ISLAB2']

places = rooms + labs

def init_time_table(days, timeslots, places):
    time_table = {}
    for day in days:
        time_table[day] = {}
        for time in timeslots.keys():
            time_table[day][time] = {}
            for room in places:
                if time == 'M_BREAK' or time == 'L_BREAK':
                    time_table[day][time][room] = Break()
                else:
                    time_table[day][time][room] = None

    return time_table

def print_time_table(time_table):
    # Note to self: You can directly convert prettytable to HTML and display it on a webpage.
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
    # All in one file
    output_dir = 'tabular_outputs'
    os.makedirs(output_dir, exist_ok=True)

    table = PrettyTable()
    table.set_style(DOUBLE_BORDER)
    table.border = True
    table.field_names = ["Day"] + [timeslots[slot] for slot in slots]
    for day, slots in time_table.items():
        current_day = []
        for slot, rooms in slots.items():
                slot_data = PrettyTable()
                slot_data.field_names = ['Room', 'Faculty','Subject','Group']
                for room, cls in rooms.items():
                    if cls:
                        slot_data.add_row([room,cls.faculty,cls.name_code,cls.group])
                    else:
                        slot_data.add_row([room, 'No','class','scheduled'])
                current_day.append(slot_data)
        table.add_row([day] +current_day)
    mystring = table.get_string()
    with open(os.path.join(output_dir, f"allinone.txt"), 'w') as file:
        file.write(mystring)

    # class "group" wise
    output_dir = 'tabular_outputs/groupwise_outputs'
    os.makedirs(output_dir, exist_ok=True)

    for group in groups_set:
        table = PrettyTable()
        table.set_style(DOUBLE_BORDER)
        table.border = True
        table.field_names = ["Day"] + [timeslots[slot] for slot in slots]
        for day, slots in time_table.items():
            current_day = []
            for slot, rooms in slots.items():
                scheduled_flag = False
                for room, cls in rooms.items():
                    if cls and cls.group == group:
                        slot_data = f"{room} - {cls.faculty} - {cls.name_code}"
                        scheduled_flag = True
                else:
                    if scheduled_flag:
                        current_day.append(slot_data)
                    else:
                        current_day.append('No class scheduled')
            table.add_row([day] +current_day)
        mystring = table.get_string()
        with open(os.path.join(output_dir, f"{group}.txt"), 'w') as file:
            file.write(mystring)
    
    # faculty wise
    output_dir = 'tabular_outputs/facultywise_outputs'
    os.makedirs(output_dir, exist_ok=True)

    for faculty in faculties_set:
        table = PrettyTable()
        table.set_style(DOUBLE_BORDER)
        table.border = True
        table.field_names = ["Day"] + [timeslots[slot] for slot in slots]
        for day, slots in time_table.items():
            current_day = []
            for slot, rooms in slots.items():
                scheduled_flag = False
                for room, cls in rooms.items():
                    if cls and cls.faculty == faculty:
                        slot_data = f"{room} - {cls.group} - {cls.name_code}"
                        scheduled_flag = True
                else:
                    if scheduled_flag:
                        current_day.append(slot_data)
                    else:
                        current_day.append('No class scheduled')
            table.add_row([day] +current_day)
        mystring = table.get_string()
        with open(os.path.join(output_dir, f"{faculty}.txt"), 'w') as file:
            file.write(mystring)
    
    # room wise
    output_dir = 'tabular_outputs/roomwise_outputs'
    os.makedirs(output_dir, exist_ok=True)

    for room in places:
        table = PrettyTable()
        table.set_style(DOUBLE_BORDER)
        table.border = True
        table.field_names = ["Day"] + [timeslots[slot] for slot in slots]
        for day, slots in time_table.items():
            current_day = []
            for slot, rooms in slots.items():
                scheduled_flag = False
                for r, cls in rooms.items():
                    if cls and r == room:
                        slot_data = f"{cls.faculty} - {cls.group} - {cls.name_code}"
                        scheduled_flag = True
                else:
                    if scheduled_flag:
                        current_day.append(slot_data)
                    else:
                        current_day.append('No class scheduled')
            table.add_row([day] +current_day)
        mystring = table.get_string()
        with open(os.path.join(output_dir, f"{room}.txt"), 'w') as file:
            file.write(mystring)


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
    
    priority = []
    timings = list(timeslots.keys())
    for day in days:
        for current_timeslot, time in enumerate(timings):
            for i, room in enumerate(places):
                if cls.class_type == 'L':
                    # For labs
                    if room not in labs:
                        continue
                    
                    if cls.original_hours == 3:
                        # For 3 hour labs
                        if current_timeslot+2 >= len(timings):
                            continue
                        if (time_table[day][time][room] is None
                            and time_table[day][timings[current_timeslot+1]][room] is None
                            and time_table[day][timings[current_timeslot+2]][room] is None
                            and cls.faculty1 not in [time_table[day][time][r].faculty if time_table[day][time][r] else None for r in places]
                            and cls.faculty1 not in [time_table[day][timings[current_timeslot+1]][r].faculty if time_table[day][timings[current_timeslot+1]][r] else None for r in places]
                            and cls.faculty1 not in [time_table[day][timings[current_timeslot+2]][r].faculty if time_table[day][timings[current_timeslot+2]][r] else None for r in places]
                            and cls.faculty2 not in [time_table[day][time][r].faculty if time_table[day][time][r] else None for r in places]
                            and cls.faculty2 not in [time_table[day][timings[current_timeslot+1]][r].faculty if time_table[day][timings[current_timeslot+1]][r] else None for r in places]
                            and cls.faculty2 not in [time_table[day][timings[current_timeslot+2]][r].faculty if time_table[day][timings[current_timeslot+2]][r] else None for r in places]
                            and cls.group not in [time_table[day][time][r].group if time_table[day][time][r] else None for r in places]
                            and cls.group not in [time_table[day][timings[current_timeslot+1]][r].group if time_table[day][timings[current_timeslot+1]][r] else None for r in places]
                            and cls.group not in [time_table[day][timings[current_timeslot+2]][r].group if time_table[day][timings[current_timeslot+2]][r] else None for r in places]
                            and cls.hours > 0):

                            priority.append((day,current_timeslot,room))
                    
                    # For 2 hour labs
                    if current_timeslot+1 >= len(timings):
                            continue
                    if (time_table[day][time][room] is None
                        and time_table[day][timings[current_timeslot+1]][room] is None
                        and cls.faculty1 not in [time_table[day][time][r].faculty if time_table[day][time][r] else None for r in places]
                        and cls.faculty1 not in [time_table[day][timings[current_timeslot+1]][r].faculty if time_table[day][timings[current_timeslot+1]][r] else None for r in places]
                        and cls.faculty2 not in [time_table[day][time][r].faculty if time_table[day][time][r] else None for r in places]
                        and cls.faculty2 not in [time_table[day][timings[current_timeslot+1]][r].faculty if time_table[day][timings[current_timeslot+1]][r] else None for r in places]
                        and cls.group not in [time_table[day][time][r].group if time_table[day][time][r] else None for r in places]
                        and cls.group not in [time_table[day][timings[current_timeslot+1]][r].group if time_table[day][timings[current_timeslot+1]][r] else None for r in places]
                        and cls.hours > 0):

                        priority.append((day,current_timeslot,room))

                else:
                    # For regular classes
                    if room in labs:
                        continue
                    if (time_table[day][time][room] is None
                        and cls.faculty not in [time_table[day][time][r].faculty if time_table[day][time][r] else None for r in places]
                        and cls.group not in [time_table[day][time][r].group if time_table[day][time][r] else None for r in places]
                        and cls.hours > 0):

                        priority.append((day,current_timeslot,room))

    
    # Sorting the priority list based on whether there was a previous class for the group or faculty
    def sort_priority(allotable_location):
        # This is kinda our heuristic function to make the previous greedy allotment a bit more cohesive.
        day, current_timeslot, room = allotable_location
        score = 0
        # Cohesiveness based on previous class
        if time_table[day][timings[current_timeslot-1]][room] and cls.group in [time_table[day][timings[current_timeslot-1]][room].group if time_table[day][timings[current_timeslot-1]][room] else None for room in places]:
            score += 1
        if time_table[day][timings[current_timeslot-1]][room] and cls.faculty in [time_table[day][timings[current_timeslot-1]][room].faculty if time_table[day][timings[current_timeslot-1]][room] else None for room in places]:
            score += 1
        # Prefer the class that leads to days with less than or equal to 5 hours of classes in a day
        if sum([1 for slot in timings if time_table[day][slot][room] and time_table[day][slot][room].faculty == cls.faculty]) <= 5:
            score += 1
        if sum([1 for slot in timings if time_table[day][slot][room] and time_table[day][slot][room].group == cls.group]) <= 5:
            score += 1
        # Prefer classes where the time difference between the first class and the last class (for both students and faculties) is less than  or equal to 6 hours
        faculty_slots = [slot for slot in timings if time_table[day][slot][room] and time_table[day][slot][room].faculty == cls.faculty]
        faculty_slots = [slot for slot in faculty_slots if slot not in ['M_BREAK','L_BREAK']]
        if faculty_slots:
            min_slot = min(faculty_slots)
            max_slot = max(faculty_slots)
            # Using ord instead of properly comparing hours cause I'm lazy
            if ord(max_slot) - ord(min_slot) <= 4:
                # 7 to include a break
                score += 1
        group_slots = [slot for slot in timings if time_table[day][slot][room] and time_table[day][slot][room].group == cls.group]
        group_slots = [slot for slot in group_slots if slot not in ['M_BREAK','L_BREAK']]
        if group_slots:
            min_slot = min(group_slots)
            max_slot = max(group_slots)
            # Using ord instead of properly comparing hours cause I'm lazy
            if ord(max_slot) - ord(min_slot) <= 4:
                # 7 to include a break
                score += 1

        return score

    priority.sort(key=sort_priority, reverse=True)

    for priority_loc in priority:
        day, current_timeslot, room = priority_loc
        hours = cls.hours
        if cls.class_type == 'L':
            if hours == 3:
                time_table[day][timings[current_timeslot]][room] = cls
                time_table[day][timings[current_timeslot+1]][room] = cls
                time_table[day][timings[current_timeslot+2]][room] = cls
                cls.hours -= 3
                print("Allotted",cls.format())

                if backtrack_schedule(time_table, classes):
                    return True

                time_table[day][timings[current_timeslot]][room] = None
                time_table[day][timings[current_timeslot+1]][room] = None
                time_table[day][timings[current_timeslot+2]][room] = None
                cls.hours += 3
                print("De-Allotted",cls.format())
            elif hours == 2:
                time_table[day][timings[current_timeslot]][room] = cls
                time_table[day][timings[current_timeslot+1]][room] = cls
                cls.hours -= 2
                print("Allotted",cls.format())

                if backtrack_schedule(time_table, classes):
                    return True

                time_table[day][timings[current_timeslot]][room] = None
                time_table[day][timings[current_timeslot+1]][room] = None
                cls.hours += 2
                print("De-Allotted",cls.format())
        else:
            time_table[day][timings[current_timeslot]][room] = cls
            cls.hours -= 1
            print("Allotted",cls.format())

            if backtrack_schedule(time_table, classes):
                return True

            time_table[day][timings[current_timeslot]][room] = None
            cls.hours += 1
            print("De-Allotted",cls.format())
    
    return False

def schedule_classes(time_table, classes):
    return backtrack_schedule(time_table, classes)


if __name__ == '__main__':
    classes = read_classes()
    time_table = init_time_table(days, timeslots, places)
    print(schedule_classes(time_table, classes))
    print_time_table(time_table)