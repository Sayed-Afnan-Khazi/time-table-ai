# @Sayed-Afnan-Khazi's backtracking algorithm for time table generation. 
import random
import csv
import os
import threading
import multiprocessing
import warnings
from prettytable import PrettyTable, from_csv, DOUBLE_BORDER

def generate_time_table():
        # days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], 
        # timeslots={'A': '7:30-8:30', 'B': '8:30-9:30', 'C': '9:30-10:30', 'M_BREAK':'10:30-11:00','D': '11:00-11:50', 'E': '11:50-12:40', 'F': '12:40-13:30', 'L_BREAK':'13:30-14:30','G': '14:30-15:30', 'H': '15:30-16:30', 'I': '16:30-17:30'}, 
        # rooms=['IS101', 'IS002', 'IS103','IS001'], 
        # labs=['ISLAB1', 'ISLAB2'],base_output_dir='./generate_timetable/outputs', base_input_dir='./generate_timetable/inputs'):
    base_output_dir='./generate_timetable/outputs'
    base_input_dir='./generate_timetable/inputs'

    # Days of the week: (Monday-Saturday) and Saturday till 1:30PM is included. (check init_time_table() for more info
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    # timeslots are represented as:
    # A(7:30-8:30), B(8:30-9:30), C(9:30-10:30),
    # D(11:00-11:50), E(11:50-12:40), F(12:40-1:30),
    # G(2:30-3:30), H(3:30-4:30), I(4:30-5:30)
    timeslots = {'A': '7:30-8:30', 'B': '8:30-9:30', 'C': '9:30-10:30', 'M_BREAK':'10:30-11:00','D': '11:00-11:50', 'E': '11:50-12:40', 'F': '12:40-13:30', 'L_BREAK':'13:30-14:30','G': '14:30-15:30', 'H': '15:30-16:30', 'I': '16:30-17:30'}

    # rooms: IS101, IS102, IS103 (for now)
    rooms = ['IS101', 'IS002', 'IS103','IS001']

    # labs: ISLAB1, ISLAB2 (for now)
    labs = ['ISLAB1', 'ISLAB2']

    places = rooms + labs

    def get_lab_professors():
        # Read from csv file
        lab_professors = set()
        with open(base_input_dir+'/lab_professors.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                lab_professors.add(row[0].strip())
        return lab_professors

    lab_professors_allotable = get_lab_professors()

    class Class:
        def __init__(self, faculty, name_code, group, hours, class_session):
            self.faculty = faculty
            self.name_code = name_code
            self.group = group
            self.hours = hours
            self.original_hours = self.hours
            self.class_session = class_session

            if self.name_code.endswith('L'):
                # For laboratory classes
                self.class_type = 'L'
                faculties = self.faculty.split('+')
                if len(faculties) == 2:
                    # Both faculties were specified for the lab
                    self.faculty1 = faculties[0]
                    self.faculty2 = faculties[1]
                    lab_professors_allotable.discard(faculties[0]) # Just in case
                    lab_professors_allotable.discard(faculties[1]) # Just in case
                if len(faculties) == 1:
                    # Only one faculty was specified for the lab
                    if faculties[0] in lab_professors_allotable:
                        # The main faculty assigned is in the lab professors list
                        # Assign to the lab and remove from the set
                        self.faculty1 = faculties[0]
                        # Pick a random lab professor
                        try:
                            self.faculty2 = random.choice(list(lab_professors_allotable))
                            while self.faculty2 == self.faculty1:
                                self.faculty2 = random.choice(list(lab_professors_allotable))
                        except IndexError:
                            raise IndexError("No lab professors left to allot, please add more lab professors in lab_professors.csv file.")
                        
                        self.faculty = self.faculty1 + '+' + self.faculty2
                    else:
                        # The main faculty assigned is not in the lab professors list
                        # Pick a random lab professor
                        self.faculty1 = faculties[0]
                        try:
                            self.faculty2 = random.choice(list(lab_professors_allotable))
                            while self.faculty2 == self.faculty1:
                                self.faculty2 = random.choice(list(lab_professors_allotable))
                        except IndexError:
                            raise IndexError("No lab professors left to allot, please add more lab professors in lab_professors.csv file.")
                        self.faculty = self.faculty1 + '+' + self.faculty2
                    # lab_professors_allotable.discard(faculties[0]) 
                    # lab_professors_allotable.discard(self.faculty2)
            else:
                # For theory classes
                self.class_type = 'T'
                self.faculty1 = None # Should we put the faculty's name in this?
                self.faculty2 = None

        def __str__(self):
            return f"{self.faculty} conducting {self.hours} of {self.name_code}"
        
        def format(self):
            if self.class_type == 'L':
                return f"{self.faculty1} + {self.faculty2} - {self.name_code} - {self.group}"
            else:
                return f"{self.faculty} - {self.name_code} - {self.group}"

    class Break(Class):
        def __init__(self) -> None:
            self.faculty = None
            self.name_code = None
            self.group = None
            self.hours = None
            self.class_session = None
        def format(self):
            return "BREAK"
        
    class FixedClass(Class):
        # Note: Labs aren't considered for fixed classes for now
        def __init__(self, faculty, name_code, group, day, time):
            self.faculty = faculty
            self.name_code = name_code
            self.group = group
            if day not in days:
                raise ValueError("Invalid day, refer format for days of the week")
            else: 
                self.day = day
            if time not in timeslots.keys():
                raise ValueError("Invalid time, refer format for timeslot keys")
            else:
                self.time = time
            if self.name_code.endswith('L'):
                raise ValueError("Labs are not considered for fixed classes for now, please remove the 'L' from the name_code in fixed_classes.csv file. This clas will be considered as a theory class.")
            self.class_type = 'T'
            self.faculty1 = None # Should improve this with a super() call in the future.
            self.faculty2 = None
        
        def format(self):
            return f"{self.faculty} - {self.name_code} - {self.group} [PRE-ALLOTTED]"


    # Global variables
    classes = []
    fixed_classes = []
    faculties_set = set()
    groups_set = set()

    # Read the csv files
    def read_classes():
        with open(base_input_dir+'/classes.csv', 'r') as file:
            for line in file:
                faculty, name_code, group, hours, class_session = line.strip().split(',')
                faculty, name_code, group, hours, class_session = faculty.strip(), name_code.strip(), group.strip(), hours.strip(), class_session.strip()
                faculties_set.add(faculty)
                groups_set.add(group)
                classes.append(Class(faculty, name_code, group, int(hours), class_session))
        with open(base_input_dir+'/fixed_classes.csv', 'r') as file:
            for line in file:
                faculty, name_code, group, day, time = line.strip().split(',')
                faculty, name_code, group, day, time = faculty.strip(), name_code.strip(), group.strip(), day.strip(), time.strip()
                faculties_set.add(faculty)
                groups_set.add(group)
                fixed_classes.append(FixedClass(faculty, name_code, group, day, time))
        return classes, fixed_classes

    ## Structure of the 3D hash table (time table):

    # { day_of_week: {time: {room: [Class] | None }}}

    def init_time_table():
        # Initialize the time table
        time_table = {}
        for day in days:
            time_table[day] = {}
            timings = list(timeslots.keys())
            for time in timings:
                time_table[day][time] = {}
                for room in places:
                    if time == 'M_BREAK' or time == 'L_BREAK':
                        time_table[day][time][room] = Break()
                    elif day == 'Saturday' and timings.index(time) >= 7:
                        time_table[day][time][room] = Break()
                    else:
                        time_table[day][time][room] = None

        # Allot fixed classes
        shuffled_rooms = list(rooms)
        random.shuffle(shuffled_rooms)
        for fixed_class in fixed_classes:
            for possible_room in shuffled_rooms:
                if time_table[fixed_class.day][fixed_class.time][possible_room] is None:
                    time_table[fixed_class.day][fixed_class.time][possible_room] = fixed_class
                    break
            else:
                raise ValueError(f"Could not pre-allot fixed class, {fixed_class.format()} (A clash possibly occurred, please check your fixed_classes.csv file)")
        
        return time_table

    def print_time_table(time_table):
        # Note to self: You can directly convert prettytable to HTML and display it on a webpage.
        output_dir = base_output_dir
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
        output_dir = base_output_dir + '/tabular_outputs'
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
        mystring = table.get_html_string()
        with open(os.path.join(output_dir, f"allinone.html"), 'w') as file:
            file.write(mystring)

        # class "group" wise
        output_dir =  base_output_dir + '/tabular_outputs/groupwise_outputs'
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
            mystring = table.get_html_string()
            with open(os.path.join(output_dir, f"{group}.html"), 'w') as file:
                file.write(mystring)
        
        # faculty wise
        output_dir =  base_output_dir + '/tabular_outputs/facultywise_outputs'
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
            mystring = table.get_html_string()
            with open(os.path.join(output_dir, f"{faculty}.html"), 'w') as file:
                file.write(mystring)
        
        # room wise
        output_dir =  base_output_dir + '/tabular_outputs/roomwise_outputs'
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
            mystring = table.get_html_string()
            with open(os.path.join(output_dir, f"{room}.html"), 'w') as file:
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
        
        if cancel_event.is_set():
            # print("Cancel event is set, stopping the algorithm.")
            return False
        
        priority = []
        timings = list(timeslots.keys())
        if cls.class_session == 'M':
            timings = timings[:7]
            # print("Allotting for Morning session")
        elif cls.class_session == 'A':
            timings = timings[4:]
            # print("Allotting for Afternoon session")
        else:
            raise ValueError("Invalid class session, refer format for class session")
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
                                and cls.faculty1 not in [time_table[day][timings[current_timeslot+i]][r].faculty if time_table[day][timings[current_timeslot+i]][r] else None for r in places for i in range(3)] + [time_table[day][timings[current_timeslot+i]][r].faculty1 if time_table[day][timings[current_timeslot+i]][r] else None for r in places for i in range(3)] + [time_table[day][timings[current_timeslot+i]][r].faculty2 if time_table[day][timings[current_timeslot+i]][r] else None for r in places for i in range(3)]
                                and cls.faculty2 not in [time_table[day][timings[current_timeslot+i]][r].faculty if time_table[day][timings[current_timeslot+i]][r] else None for r in places for i in range(3)] + [time_table[day][timings[current_timeslot+i]][r].faculty1 if time_table[day][timings[current_timeslot+i]][r] else None for r in places for i in range(3)] + [time_table[day][timings[current_timeslot+i]][r].faculty2 if time_table[day][timings[current_timeslot+i]][r] else None for r in places for i in range(3)]
                                and cls.group not in [time_table[day][timings[current_timeslot+i]][r].group if time_table[day][timings[current_timeslot+i]][r] else None for r in places for i in range(3)]
                                and cls.hours > 0):

                                priority.append((day,current_timeslot,room))

                        if cls.original_hours == 2:
                            # For 2 hour labs
                            if current_timeslot+1 >= len(timings):
                                    continue
                            if (time_table[day][time][room] is None
                                and time_table[day][timings[current_timeslot+1]][room] is None
                                and cls.faculty1 not in [time_table[day][timings[current_timeslot+i]][r].faculty if time_table[day][timings[current_timeslot+i]][r] else None for r in places for i in range(2)] + [time_table[day][timings[current_timeslot+i]][r].faculty1 if time_table[day][timings[current_timeslot+i]][r] else None for r in places for i in range(2)] + [time_table[day][timings[current_timeslot+i]][r].faculty2 if time_table[day][timings[current_timeslot+i]][r] else None for r in places for i in range(2)]
                                and cls.faculty2 not in [time_table[day][timings[current_timeslot+i]][r].faculty if time_table[day][timings[current_timeslot+i]][r] else None for r in places for i in range(2)] + [time_table[day][timings[current_timeslot+i]][r].faculty1 if time_table[day][timings[current_timeslot+i]][r] else None for r in places for i in range(2)] + [time_table[day][timings[current_timeslot+i]][r].faculty2 if time_table[day][timings[current_timeslot+i]][r] else None for r in places for i in range(2)]
                                and cls.group not in [time_table[day][timings[current_timeslot+i]][r].group if time_table[day][timings[current_timeslot+i]][r] else None for r in places for i in range(2)]
                                and cls.hours > 0):

                                priority.append((day,current_timeslot,room))

                    else:
                        # For regular classes
                        if room in labs:
                            continue
                        if (time_table[day][time][room] is None
                            and cls.faculty not in [time_table[day][time][r].faculty if time_table[day][time][r] else None for r in places] + [time_table[day][time][r].faculty1 if time_table[day][time][r] else None for r in places] + [time_table[day][time][r].faculty2 if time_table[day][time][r] else None for r in places]
                            and cls.group not in [time_table[day][time][r].group if time_table[day][time][r] else None for r in places]
                            and cls.hours > 0):

                            priority.append((day,current_timeslot,room))

        
        def sort_priority(allotable_location):
            # This is kinda our heuristic function to make the previous greedy allotment a bit more cohesive.
            day, current_timeslot, room = allotable_location
            score = 0
            # Cohesiveness based on previous classes in the same room
            i = 1
            while current_timeslot-i>=0 and time_table[day][timings[current_timeslot-i]][room] and cls.group in [time_table[day][timings[current_timeslot-i]][room].group if time_table[day][timings[current_timeslot-i]][room] else None for room in places]:
                score += 1
                i += 1
            i = 1
            while current_timeslot-i>=0 and time_table[day][timings[current_timeslot-i]][room] and cls.faculty in [time_table[day][timings[current_timeslot-i]][room].faculty if time_table[day][timings[current_timeslot-i]][room] else None for room in places]:
                score += 1
                i += 1
            # Prefer the class that leads to days with less than or equal to 5 hours of classes in a day
            if sum([1 if time_table[day][slot][room] and time_table[day][slot][room].faculty == cls.faculty else 0 for slot in timings for room in places]) <= 5:
                score += 5
            if sum([1 if time_table[day][slot][room] and time_table[day][slot][room].group == cls.group else 0 for slot in timings for room in places]) <= 5:
                score += 5
            # Prefer classes where the time difference between the first class and the last class (for both students and faculties) is less than  or equal to 6 hours
            faculty_slots = [slot for slot in timings if time_table[day][slot][room] and time_table[day][slot][room].faculty == cls.faculty]
            faculty_slots = [slot for slot in faculty_slots if slot not in ['M_BREAK','L_BREAK']]
            if faculty_slots:
                min_slot = min(faculty_slots)
                max_slot = max(faculty_slots)
                # Using ord instead of properly comparing hours cause I'm lazy
                if ord(max_slot) - ord(min_slot) <= 5:
                    # 7 to include a break
                    score += 5
            group_slots = [slot for slot in timings if time_table[day][slot][room] and time_table[day][slot][room].group == cls.group]
            group_slots = [slot for slot in group_slots if slot not in ['M_BREAK','L_BREAK']]
            if group_slots:
                min_slot = min(group_slots)
                max_slot = max(group_slots)
                
                # Using ord instead of properly comparing hours cause I'm lazy
                if ord(max_slot) - ord(min_slot) <= 5:
                    # 7 to include a break
                    score += 5

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
                    # print("Allotted",cls.format())

                    if backtrack_schedule(time_table, classes):
                        return True

                    time_table[day][timings[current_timeslot]][room] = None
                    time_table[day][timings[current_timeslot+1]][room] = None
                    time_table[day][timings[current_timeslot+2]][room] = None
                    cls.hours += 3
                    # print("De-Allotted",cls.format())
                elif hours == 2:
                    time_table[day][timings[current_timeslot]][room] = cls
                    time_table[day][timings[current_timeslot+1]][room] = cls
                    cls.hours -= 2
                    # print("Allotted",cls.format())

                    if backtrack_schedule(time_table, classes):
                        return True

                    time_table[day][timings[current_timeslot]][room] = None
                    time_table[day][timings[current_timeslot+1]][room] = None
                    cls.hours += 2
                    # print("De-Allotted",cls.format())
            else:
                time_table[day][timings[current_timeslot]][room] = cls
                cls.hours -= 1
                # print("Allotted",cls.format())

                if backtrack_schedule(time_table, classes):
                    return True

                time_table[day][timings[current_timeslot]][room] = None
                cls.hours += 1
                # print("De-Allotted",cls.format())
        
        return False
    

    def verify_time_table(time_table):
        # Verify the time table
        for test_class in classes:
            if test_class.hours > 0:
                warnings.warn("Class not scheduled:",test_class.format())
                return False
            acc_hours = 0
            # Check if all class hours are actually present in the time_table.
            # Also make sure that the faculty and group are not in any other location at the same time.
            timings = list(timeslots.keys())
            for day in days:
                for current_timeslot, time in enumerate(timings):
                    for i, room in enumerate(places):
                        if test_class.class_type == 'L':
                            # For labs
                            if room not in labs:
                                continue
                            
                            if test_class.original_hours == 3:
                                # For 3 hour labs
                                if current_timeslot+2 >= len(timings):
                                    continue
                                if (time_table[day][time][room] and time_table[day][timings[current_timeslot+1]][room] and time_table[day][timings[current_timeslot+2]][room] and
                                    time_table[day][time][room].name_code == test_class.name_code and
                                    time_table[day][time][room].faculty == test_class.faculty and
                                    time_table[day][time][room].group == test_class.group and
                                    time_table[day][timings[current_timeslot+1]][room].name_code == test_class.name_code and
                                    time_table[day][timings[current_timeslot+1]][room].faculty == test_class.faculty and
                                    time_table[day][timings[current_timeslot+1]][room].group == test_class.group and
                                    time_table[day][timings[current_timeslot+2]][room].name_code == test_class.name_code and
                                    time_table[day][timings[current_timeslot+2]][room].faculty == test_class.faculty and
                                    time_table[day][timings[current_timeslot+2]][room].group == test_class.group):
                                    # Check if that group is only present in that room at that day and those times
                                    for r in places:
                                        if r != room and (time_table[day][time][r] and time_table[day][time][r].group == test_class.group or
                                            time_table[day][timings[current_timeslot+1]][r] and time_table[day][timings[current_timeslot+1]][r].group == test_class.group or
                                            time_table[day][timings[current_timeslot+2]][r] and time_table[day][timings[current_timeslot+2]][r].group == test_class.group):
                                            print(f"Group {test_class.format()} is scheduled in multiple rooms at the same time by algo, please check the time table. Conflicting room: {r} and {room}")
                                            return False
                                    # Check if that faculty is only present in that room at that day and those times
                                    for r in places:
                                        if r != room and (time_table[day][time][r] and time_table[day][time][r].faculty == test_class.faculty or
                                            time_table[day][timings[current_timeslot+1]][r] and time_table[day][timings[current_timeslot+1]][r].faculty == test_class.faculty or
                                            time_table[day][timings[current_timeslot+2]][r] and time_table[day][timings[current_timeslot+2]][r].faculty == test_class.faculty):
                                            print(f"Faculty {test_class.format()} is scheduled in multiple rooms at the same time by algo, please check the time table. Conflicting room: {r} and {room}")
                                            return False
                                    acc_hours += 3
                            if test_class.original_hours == 2:
                                # For 2 hour labs
                                if current_timeslot+1 >= len(timings):
                                    continue
                                if (time_table[day][time][room] and time_table[day][timings[current_timeslot+1]][room] and
                                    time_table[day][time][room].name_code == test_class.name_code and
                                    time_table[day][time][room].faculty == test_class.faculty and
                                    time_table[day][time][room].group == test_class.group and
                                    time_table[day][timings[current_timeslot+1]][room].name_code == test_class.name_code and
                                    time_table[day][timings[current_timeslot+1]][room].faculty == test_class.faculty and
                                    time_table[day][timings[current_timeslot+1]][room].group == test_class.group):
                                    # Check if that group is only present in that room at that day and those times
                                    for r in places:
                                        if r != room and (time_table[day][time][r] and time_table[day][time][r].group == test_class.group or
                                            time_table[day][timings[current_timeslot+1]][r] and time_table[day][timings[current_timeslot+1]][r].group == test_class.group):
                                            print(f"Group {test_class.format()} is scheduled in multiple rooms at the same time by algo, please check the time table. Conflicting room: {r} and {room}")
                                            return False
                                    # Check if that faculty is only present in that room at that day and those times
                                    for r in places:
                                        if r != room and (time_table[day][time][r] and time_table[day][time][r].faculty == test_class.faculty or
                                            time_table[day][timings[current_timeslot+1]][r] and time_table[day][timings[current_timeslot+1]][r].faculty == test_class.faculty):
                                            print(f"Faculty {test_class.format()} is scheduled in multiple rooms at the same time by algo, please check the time table. Conflicting room: {r} and {room}")
                                            return False
                                    acc_hours += 2
                        elif (time_table[day][time][room] and # There is a class scheduled
                            time_table[day][time][room].name_code == test_class.name_code and # The class name matches
                            time_table[day][time][room].faculty == test_class.faculty and # The faculty matches
                            time_table[day][time][room].group == test_class.group): # The group matches
                            # Check if that group is only present in that room at that day and time
                            for r in places:
                                if r != room and time_table[day][time][r] and time_table[day][time][r].group == test_class.group:
                                    print(f"Group {test_class.format()} is scheduled in multiple rooms at the same time by algo, please check the time table. Conflicting room: {r} and {room}")
                                    return False
                            # Check if that faculty is only present in that room at that day and time
                            for r in places:
                                if r != room and time_table[day][time][r] and time_table[day][time][r].faculty == test_class.faculty:
                                    print(f"Faculty {test_class.format()} is scheduled in multiple rooms at the same time by algo, please check the time table. Conflicting room: {r} and {room}")
                                    return False
                            acc_hours += 1
            if acc_hours != test_class.original_hours:
                print(f"Class {test_class.format()} is not scheduled for the correct number of hours. Expected {test_class.original_hours}, got {acc_hours}")
                return False
     
        print("Time table verified successfully")
        return True

    def schedule_classes(time_table, classes):
        try:
            return backtrack_schedule(time_table, classes)
        except KeyboardInterrupt:
            print("Interrupted by user, printing current time table")
            print("Total class hours left to allot:",sum([cls.hours for cls in classes]))
            print_time_table(time_table)
            return False
    
    classes, fixed_classes = read_classes()
    time_table = init_time_table()
    val_to_return = schedule_classes(time_table, classes)
    if val_to_return:
        print_time_table(time_table)
        print("time table checked?",verify_time_table(time_table))
    return val_to_return


############################ EXPERIMENTAL ZONE - MULTIPROCESSING AND THREADING ######################

# Shared flag to stop all running threads and processes when a solution is found
cancel_event = multiprocessing.Event()

# Counter to keep track of the number of running threads (for each process)
thread_lock = threading.Lock()  # Lock for thread counter in each process

process_counter = multiprocessing.Value('i', 0)  # Shared counter for running processes

# Function to run the backtracking algorithm with a timeout within a process
def run_with_timeout(backtracking_algorithm):
    global thread_lock
    thread_count = 0  # Local counter for threads within a process
    result = None

    def target():
        nonlocal result
        nonlocal thread_count

        with thread_lock:  # Lock the counter while modifying it
            thread_count += 1  # Increment thread count when a thread starts
            print(f"Process {multiprocessing.current_process().name} - Thread {threading.current_thread().name} started. "
                  f"Running threads in process: {thread_count}")

        # Run the backtracking algorithm
        result = backtracking_algorithm()

        if result:  # If solution is found, trigger the cancel event
            cancel_event.set()

        with thread_lock:  # Lock the counter while modifying it
            thread_count -= 1  # Decrement thread count when a thread finishes
            print(f"Process {multiprocessing.current_process().name} - Thread {threading.current_thread().name} finished. "
                  f"Running threads in process: {thread_count}")

    while result is None and not cancel_event.is_set():  # Keep trying until a solution is found or event is set
        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout=5)  # Wait 5 seconds for the algorithm to complete


        if thread.is_alive():  # If the thread is still alive (timeout)
            print(f"Process {multiprocessing.current_process().name} - Thread {threading.current_thread().name} Timeout! Restarting the algorithm...")
        else:
            if result:
                print(f"Process {multiprocessing.current_process().name} - Thread {threading.current_thread().name} Solution found in a process! Writing results to files.")
                cancel_event.set() # maybe required?
                return result
            else:
                print(f"Process {multiprocessing.current_process().name} - Thread {threading.current_thread().name} Algorithm canceled or no solution found in thread.")

    return result


def run_backtrack_algo_with_threads():
    run_with_timeout(generate_time_table)

# Worker function to run in each process
def process_worker():
    global process_counter
    with process_counter.get_lock():  # Lock to safely modify process counter
        process_counter.value += 1  # Increment process count when a process starts
        print(f"Process started. Running processes: {process_counter.value}")

    # Run the backtracking algorithm with thread management
    run_backtrack_algo_with_threads()

    with process_counter.get_lock():  # Lock to safely modify process counter
        process_counter.value -= 1  # Decrement process count when a process finishes
        print(f"Process finished. Running processes: {process_counter.value}")


# Function to run multiple processes in parallel
def run_with_multiprocessing():
    global process_counter
    processes = []
    num_processes = 3  # Number of parallel processes to run

    # Start multiple processes
    for _ in range(num_processes):
        process = multiprocessing.Process(target=process_worker)
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    print("All processes completed or solution found.")



if __name__ == '__main__':
    run_with_multiprocessing()
    # run_backtrack_algo_with_threads()
    # generate_time_table()
