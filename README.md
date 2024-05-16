# time-table-ai

## How it works

- The `class_to_allot(classes)` function is used to select a class that needs to be scheduled. It shuffles the list of classes and then iterates over them to find a class that still has hours left to be scheduled. If such a class is found, it is returned; otherwise, `None` is returned.

- The `backtrack_schedule(time_table, classes)` function is the main function implementing the backtracking algorithm. It takes a time table and a list of classes as input. The time table is a three-dimensional dictionary where the first dimension represents the day, the second dimension represents the time slot, and the third dimension represents the room. Each entry in the time table can either be `None` (indicating that the time slot in the room on that day is free) or an instance of a class (indicating that the time slot in the room on that day is occupied by that class).

- The function first checks if there are any classes left to schedule. If not, it returns `True`, indicating that a complete schedule has been found. If there are classes left, it selects a class to schedule using the `class_to_allot(classes)` function.

- Then, it iterates over all days, time slots, and rooms to find a place to schedule the class. It checks if the room is free at the given time slot on the given day and if the faculty member and the group of the class are not already scheduled at the same time. It also checks if the class still has hours left to be scheduled. If all these conditions are met, the class is scheduled in the room at the given time slot on the given day.

- After scheduling the class, the function recursively calls itself with the remaining classes. If a complete schedule can be found for the remaining classes, it returns `True`. If not, it undoes the scheduling of the class (this is the backtracking part of the algorithm) and continues with the next room, time slot, or day.

- If no place can be found to schedule the class, the function returns `False`, indicating that no complete schedule can be found.

- The `schedule_classes(time_table, classes)` function is a wrapper function that calls the `backtrack_schedule(time_table, classes)` function. It doesn't return anything; its purpose is to start the scheduling process.