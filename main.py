from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)

class Class:
    def __init__(self, day, start_time, duration):
        self.day = day
        self.start_time = int(start_time)
        self.end_time = self.start_time + int(duration)
    def does_intersect(self, other):
        # checking if classes intersect
        return self.day == other.day and max(self.start_time, other.start_time) <= min(self.end_time, other.end_time)

class Course:
    def __init__(self, name, duration, credits):
        self.name = str(name)
        self.duration = int(duration)
        self.credits = int(credits)
        self.sections = []
    def add_section(self, day1, time1, day2, time2):
        self.sections.append(Class(day1, time1, self.duration))
        self.sections.append(Class(day2, time2, self.duration))
    def does_intersect(self, other):
        # checking if courses intersect
        flag = False
        for x in self.sections:
            for y in other.sections:
                flag |= x.does_intersect(y)
        return flag

global answer
global answer_sum

def solve(course, taken = [], id = 0, sum = 0):
    if id == len(course):
        global answer
        if (len(taken) > len(answer)):
            answer = list(taken)
    else:
        for i in range(0, len(course[id]['section'])):
            flag = True
            for c in taken:
                if intersects(c[1], c[0]['duration'], course[id]['section'][i], course[id]['duration']):
                    flag = False
                    break
            if flag:
                taken.append([course[id], course[id]['section'][i]])
                solve(course, taken, id + 1, sum + int(course[id]['credits']))
                taken.pop()
        solve(course, taken, id + 1, sum)

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        content = request.get_json(silent = True)['course']
        course = []
        for x,y in content.items():
            course.append(y)

        global answer
        answer = []
        answer_sum = 0

        solve(course)

        for i in answer:
            x = i[0]
            y = i[1]
            print("Take " + x['name'] + " in " + y['day1'] + '/' + y['time1'] + ' and ' + y['day2'] + '/' + y['time2'])

        print(answer)

        #solve(course)
        return render_template('result.html', result = answer)
    else:
        return render_template('index.html')
