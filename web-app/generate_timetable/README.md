# time-table-ai

Credits: [@Sayed-Afnan-Khazi](https://github.com/Sayed-Afnan-Khazi)

A university class scheduling program that uses a backtracking approach to generate timetables for classes, faculty, and rooms.

## How to run

1. Clone the repository

2. Run the following command to install the required dependencies: `pip install -r requirements.txt`

3. Fill in the class data in the classes.csv file. The file should contain four columns: faculty, name_code, group, hours.

4. Run the following command to generate the timetable:

```bash
python time_table.py
```

## How it works

This project implements a university class scheduling program. It takes into account various constraints such as:

- Class types: Theory and Lab classes
- Faculty availability: A faculty member cannot teach multiple classes at the same time.
- Room availability: A room cannot be used for multiple classes at the same time.
- Group consistency: Classes for the same group should preferably be scheduled on the same day or with minimal gaps between them. They also cannot be scheduled at the same time as other classes.
- Faculty workload: The program attempts to distribute classes for a faculty member throughout the week such that they don't have too many classes on a single day.

Input: The program reads class data from a CSV file named classes.csv. Each line in the file should contain four comma-separated values: faculty, name_code, group, hours.

Output:

- The program generates a text file for each day of the week containing the timetable for that day.
- It also generates a single text file containing the entire timetable in a more presentable format.
- In addition, class-wise, faculty-wise, room-wise, and group-wise timetables are generated in separate text files.

Algorithm: The program uses a backtracking algorithm to schedule classes. It considers various factors while allotting classes to time slots and rooms.
