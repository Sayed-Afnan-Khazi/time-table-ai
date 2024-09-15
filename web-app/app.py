from flask import Flask
from generate_timetable import utils

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def home():
    utils.classes_to_csv([["Afnan", "20CB001", "CSBS-1", "5"],])
    utils.fixed_classes_to_csv([["JK", "20IS300", "ISE-3", "Tuesday", "F"],["AFK", "20CB001", "CSBS-1", "Monday", "A"],["AFK", "20CB001", "CSBS-1", "Monday", "B"]])
    utils.lab_professors_to_csv(['prof1','prof2','prof3'])
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)