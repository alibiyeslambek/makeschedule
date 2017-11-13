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

def generate(timetables, course_list, min_credits, max_credits, pointer = 0, sections_taken = [], credits_taken = 0):
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
                print(section)
                generate(timetables, course_list, min_credits, max_credits, pointer + 1, sections_taken, credits_taken + section.course.credits)
                sections_taken.pop()
        # skip
        if not course_list[pointer].required:
            #print("take ", course_list[pointer])
            generate(timetables, course_list, min_credits, max_credits, pointer + 1, sections_taken, credits_taken)
