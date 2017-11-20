from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy

import schedule
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'

db = SQLAlchemy(app)

class Table(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    cells = db.relationship('Cell', backref = db.backref('cells', lazy = True))
    def __repr__(self):
        return '<Table>'

class Cell(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    row = db.Column(db.Integer)
    col = db.Column(db.Integer)
    code = db.Column(db.String(10))
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    def __repr__(self):
        return ('<Cell %d, %d>' % self.row, self.col)

db.create_all()

@app.route("/show", methods=['GET'])
def show():
    ids = json.loads(request.args.get('id'))
    tables = []
    if (len(ids) > 10):
        return;
    for id in ids:
        table = []
        firstColumn = ['09:00-10:15', '10:30-11:45', '13:00-14:15', '14:30-15:45', '16:00-17:15', '17:30-18:45']
        for i in range(0, 6):
            table.append([firstColumn[i], [None, None, None, None, None]])

        for cell in Table.query.get(id).cells:
            table[cell.row][1][cell.col] = cell.code

        tables.append(table)
    return render_template('result.html', tables=tables)

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
            course = schedule.Course(name = cd['name'], duration = cd['duration'], credits = cd['credits'], required = ('must-take' in cd))
            for sd in cd['section']:
                section = schedule.Section(course, sd['code'])
                section.add_class(schedule.Class(sd['day1'], sd['time1'], section))
                section.add_class(schedule.Class(sd['day2'], sd['time2'], section))
                course.add_section(section)
            course_list.append(course)

        timetables = []
        schedule.generate(timetables, course_list, min_credits, max_credits)

        tables = []
        for current in timetables:
            #firstColumn = ['09:00-10:15', '10:30-11:45', '13:00-14:15', '14:30-15:45', '16:00-17:15', '17:30-18:45']

            dbtable = Table()
            for sc in current:
                for cl in sc.class_list:
                    dbtable.cells.append(Cell(row = cl.get_time_row(), col = cl.get_day_row(), code = cl.section.code))

            db.session.add(dbtable)
            db.session.commit()
            tables.append(dbtable.id)

        return json.dumps(tables)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
#app.run(debug=False, port=8000)
