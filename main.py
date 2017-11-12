from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)

class Class:
    def __init__(self, day, start_time, section):
        self.day = day
        self.start_time = int(start_time)
        self.end_time = self.start_time + int(section.course.duration)
        self.section = section
    def does_intersect(self, other):
        return self.day == other.day and max(self.start_time, other.start_time) <= min(self.end_time, other.end_time)
    def get_time_row(self):
        return self.start_time // 100 - 5
    def get_day_row(self):
        if self.day == 'mon':
            return 0
        if self.day == 'tue':
            return 1
        if self.day == 'wed':
            return 2
        if self.day == 'thu':
            return 3
        if self.day == 'fri':
            return 4

class Section:
    def __init__(self, course, code):
        self.class_list = []
        self.course = course
        self.code = code
    def __str__(self):
        return self.code
    def add_class(self, x):
        self.class_list.append(x)
    def does_intersect(self, other):
        for x in self.class_list:
            for y in other.class_list:
                if x.does_intersect(y):
                    return True
        return False

class Course:
    def __init__(self, name, duration, credits, required):
        self.name = str(name)
        self.duration = int(duration)
        self.credits = int(credits)
        self.section_list = []
        self.required = required
    def __str__(self):
        return self.name + "(" + str(self.credits) + ")"
    def add_section(self, a):
        self.section_list.append(a)

def generate_timetable(timetables, course_list, min_credits, max_credits, pointer = 0, sections_taken = [], credits_taken = 0):
    # some optimization tricks
    if credits_taken > max_credits:
        return;

    sum = credits_taken
    for i in range(pointer, len(course_list)):
        sum += course_list[i].credits

    if sum < min_credits:
        return;

    if pointer == len(course_list):
        if min_credits <= credits_taken <= max_credits and len(timetables) < 3:
            timetables.append(list(sections_taken))
    else:
        # take
        for section in course_list[pointer].section_list:
            flag = False
            for taken in sections_taken:
                if taken.does_intersect(section):
                    flag = True
                    break
            if not flag:
                sections_taken.append(section)
                print(section, section.course)
                generate_timetable(timetables, course_list, min_credits, max_credits, pointer + 1, sections_taken, credits_taken + section.course.credits)
                sections_taken.pop()
        # skip
        if not course_list[pointer].required:
            generate_timetable(timetables, course_list, min_credits, max_credits, pointer + 1, sections_taken, credits_taken)

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        """
        Receive POST method as JSON:
        content['course'] = Array of {
            'section': Array of {
                'day1': string (can be none),
                'time1': int,
                'day2': string (can be none),
                'time2': int,
            }
            'duration': integer,
            'credits-min', integer,
            'credits-max', integer,
        }
        """
        content = request.get_json(silent = True)

        min_credits = int(content['credit-number-min'])
        max_credits = int(content['credit-number-max'])

        course_list = []
        for cd in content['course'].values():
            course = Course(name = cd['name'], duration = cd['duration'], credits = cd['credits'], required = ('must-take' in cd))
            for sd in cd['section']:
                section = Section(course, sd['code'])
                section.add_class(Class(sd['day1'], sd['time1'], section))
                section.add_class(Class(sd['day2'], sd['time2'], section))
                course.add_section(section)
            course_list.append(course)

        timetables = []
        generate_timetable(timetables, course_list, min_credits, max_credits)

        tables = []
        for current in timetables:
            table = []
            firstColumn = ['09:00-10:15', '10:30-11:45', '13:00-14:15', '14:30-15:45', '16:00-17:15', '17:30-18:45']
            for i in range(0, 6):
                table.append([firstColumn[i], [None, None, None, None, None]])

            for sc in current:
                for cl in section.class_list:
                    print(cl, cl.get_time_row(), cl.get_day_row())
                    table[cl.get_time_row()][1][cl.get_day_row()] = sc.code

            tables.append(table)

        return render_template('result.html', tables = tables)
    else:
        return render_template('index.html')

app.run(debug=False, port=8000)
