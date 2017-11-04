from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)

def segments_intersect(l, r, l2, r2):
    l = int(l)
    l2 = int(l2)
    r = l + int(r)
    r2 = l2 + int(r2)
    return max(l, l2) <= min(r, r2)

def intersects(a, alen, b, blen):
    flag = False
    if a['day1'] == b['day1']:
        flag |= segments_intersect(a['time1'], alen, b['time1'], blen)
    if a['day1'] == b['day2']:
        flag |= segments_intersect(a['time1'], alen, b['time2'], blen)
    if a['day2'] == b['day1']:
        flag |= segments_intersect(a['time2'], alen, b['time1'], blen)
    if a['day2'] == b['day2']:
        flag |= segments_intersect(a['time2'], alen, b['time2'], blen)
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
        content = request.get_json(silent=True)['course']
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
