import random

first_names = ['Cameron', 'Clint', 'John', 'Elizabeth', 'Lindsay', 'Miriam', 'Tyler', 'Bob', 'William', 'Julia']
last_names = ['Fernandez', 'Duncan', 'Smith', 'Scott', 'Harris', 'Campbell', 'Green', 'Murphy', 'Thompson', 'Peterson']
cities = ['New York', 'San Francisco', 'Chicago', 'Baltimore', 'Charleston', 'Los Angeles', 'Denver', 'Miami',
          'Anchorage', 'Houston']
occupations = ['Doctor', 'Lawyer', 'Pharmacist', 'Programmer', 'Clerk', 'Secretary', 'Teacher', 'Engineer']
colleges = ['Stanford', 'UC Berkeley', 'Princeton', 'Rutgers', 'UPenn', 'Yale', 'MIT', 'Harvard']
majors = ['Computer Science', 'Finance', 'Engineering', 'Psychology', 'Music', 'History', 'Foreign Language',
          'Journalism']
companies = ['Apple', 'CitiGroup', 'Chase', 'IBM', 'Microsoft', 'Facebook', 'Google', 'Samsung']
jobs = ['Developer', 'Analyst', 'Manager', 'System Admin', 'Researcher', 'Technician', 'Officer', 'Internship']
foods = ['apples', 'oranges', 'bananas', 'peaches', 'grapes', 'avocados', 'zucchinis', 'pumpkins', 'pears', 'carrots',
         'peas', 'eggs', 'breadsticks', 'tofu', 'pork', 'beef', 'veal', 'lamb', 'chips', 'water', 'soda', 'lettuce',
         'cabbage', 'artichokes', 'popcorn', 'chocolates', 'ice cream', 'sushi', 'seaweed', 'rice', 'mushrooms',
         'mozzarella', 'pistachios', 'shrimp']


def get_first_name():
    return random.choice(first_names)


def get_last_name():
    return random.choice(last_names)


def get_city():
    return random.choice(cities)


def get_occupation():
    return random.choice(occupations)


def get_college():
    return random.choice(colleges)


def get_major():
    return random.choice(majors)


def get_companies():
    return random.choice(companies)


def get_job():
    return random.choice(jobs)


def get_food():
    return random.choice(foods)


def another(percent=50):
    return percent > random.randrange(100)


'''
dates:
college_start_date: 1980-1989
employment_start_date: 1990-1999
signup_due_date: 2016-2020

creation_date and modified_date:
    dir_personnel: 2000-2010
    all else: 2011-2015
'''


def random_time(start_year=2016, end_year=2016):
    year = start_year + random.randrange(end_year - start_year + 1)
    month = random.randrange(12) + 1
    day = random.randrange(31) + 1
    hour = random.randrange(24)
    minute = random.randrange(60)
    second = random.randrange(60)

    syear = str(year)
    if month > 9:
        smonth = str(month)
    else:
        smonth = '0' + str(month)
    if day > 30 and month in {4, 6, 9, 11}:
        day = 30
    elif day > 29 and month == 2 and year % 4 == 0:
        day = 29
    elif day > 28 and month == 2:
        day = 28
    if day > 9:
        sday = str(day)
    else:
        sday = '0' + str(day)
    if hour > 9:
        shour = str(hour)
    else:
        shour = '0' + str(hour)
    if minute > 9:
        sminute = str(minute)
    else:
        sminute = '0' + str(minute)
    if second > 9:
        ssecond = str(second)
    else:
        ssecond = '0' + str(second)

    return '%s-%s-%s %s:%s:%s' % (syear, smonth, sday, shour, sminute, ssecond)


def random_date(start_year=2016, end_year=2016):
    year = start_year + random.randrange(end_year - start_year + 1)
    month = random.randrange(12) + 1
    day = random.randrange(31) + 1

    syear = str(year)
    if month > 9:
        smonth = str(month)
    else:
        smonth = '0' + str(month)
    if day > 30 and month in {4, 6, 9, 11}:
        day = 30
    elif day > 29 and month == 2 and year % 4 == 0:
        day = 29
    elif day > 28 and month == 2:
        day = 28
    if day > 9:
        sday = str(day)
    else:
        sday = '0' + str(day)

    return '%s-%s-%s' % (syear, smonth, sday)


# data generation for tables

delim = ','


def gen_data_dir_personnel(amt=25):
    file = open('dir_personnel_data.txt', 'w')

    for i in range(1, amt + 1):
        data = ''

        # personnel_id
        data += str(i) + delim

        # personnel_user_name
        first_name = get_first_name()
        last_name = get_last_name()
        data += str(i) + '-' + first_name + '-' + last_name + delim

        # personnel_last_name
        data += last_name + delim

        # personnel_first_name
        data += first_name + delim

        # personnel_city
        data += get_city() + delim

        # personnel_occupation
        data += get_occupation() + delim

        # creation_date
        creation_date = random_time(2000, 2010)
        data += creation_date + delim

        # modified_date
        data += creation_date

        # write to file
        if i < amt:
            file.write(data + '\n')
        else:
            file.write(data)

    print('Generated ' + str(amt) + ' personnel')


def gen_data_dir_team(amt=25):
    file = open('dir_team_data.txt', 'w')

    for i in range(1, amt + 1):
        data = ''

        # team_id
        data += str(i) + delim

        # team_name
        data += 'Team ' + str(i) + delim

        # team_description
        data += 'Team ' + str(i) + ' description' + delim

        # creation_date
        creation_date = random_time(2011, 2015)
        data += creation_date + delim

        # modified_date
        data += creation_date

        # write to file
        if i < amt:
            file.write(data + '\n')
        else:
            file.write(data)

    print('Generated ' + str(amt) + ' teams')


def gen_data_dir_education_history():
    amt = 0

    try:
        person_file = open('dir_personnel_data.txt', 'r')
    except OSError:
        print('Cannot locate dir_personnel_data.txt')
        quit(1)

    person_ids = []
    line = person_file.readline()
    while line:
        person_ids.append(line.split(delim)[0])
        line = person_file.readline()

    file = open('dir_education_history_data.txt', 'w')

    for i in person_ids:
        data = ''

        # person_id
        data += str(i) + delim

        # college_name
        data += get_college() + delim

        # college_start_date
        college_start_date = random_time(1980, 1989)
        data += college_start_date + delim

        # major
        data += get_major() + delim

        # creation_date
        creation_date = random_time(2011, 2015)
        data += creation_date + delim

        # modified_date
        data += creation_date

        # write to file
        if i != person_ids[-1]:
            file.write(data + '\n')
        else:
            file.write(data)
        amt += 1

    print('Generated ' + str(amt) + ' education histories')


def gen_data_dir_employment_history(multiple_chance=30, max_per_person=5):
    amt = 0

    try:
        person_file = open('dir_personnel_data.txt', 'r')
    except OSError:
        print('Cannot locate dir_personnel_data.txt')
        return

    person_ids = []
    line = person_file.readline()
    while line:
        person_ids.append(line.split(delim)[0])
        line = person_file.readline()

    file = open('dir_employment_history_data.txt', 'w')

    employer_names = []
    for i in person_ids:
        data = ''

        # person_id
        data += str(i) + delim

        # employer_name
        if employer_names:
            another_employer = get_companies()
            while another_employer in employer_names:
                another_employer = get_companies()
            data += another_employer + delim
            employer_names.append(another_employer)
        else:
            employer_names.append(get_companies())
            data += employer_names[0] + delim

        # employment_start_date
        employment_start_date = random_time(1990, 1999)
        data += employment_start_date + delim

        # job_title
        data += get_job() + delim

        # creation_date
        creation_date = random_time(2011, 2015)
        data += creation_date + delim

        # modified_date
        data += creation_date

        # write to file
        # sometimes creates multiple jobs for personnel (max = 5 by default)
        if len(employer_names) < max_per_person and another(multiple_chance):
            file.write(data + '\n')
            person_ids.insert(person_ids.index(i), i)
        else:
            employer_names = []
            if i != person_ids[-1]:
                file.write(data + '\n')
            else:
                file.write(data)

        amt += 1

    print('Generated ' + str(amt) + ' employment histories')


def gen_data_dir_team_member(multiple_chance=60, max_per_person=15):
    amt = 0

    try:
        person_file = open('dir_personnel_data.txt', 'r')
        team_file = open('dir_team_data.txt', 'r')
    except OSError:
        print('Cannot locate either dir_personnel_data.txt or dir_team_data.txt')
        return

    person_ids = []
    line = person_file.readline()
    while line:
        person_ids.append(line.split(delim)[0])
        line = person_file.readline()

    team_ids = []
    line = team_file.readline()
    while line:
        team_ids.append(line.split(delim)[0])
        line = team_file.readline()

    file = open('dir_team_member_data.txt', 'w')

    assigned_teams = []
    teams = []
    for i in person_ids:
        data = ''

        # person_id
        data += str(i) + delim

        # team_id
        if teams:
            another_team = random.choice(team_ids)
            while another_team in teams:
                another_team = random.choice(team_ids)
            data += another_team
            teams.append(another_team)
            assigned_teams.append(another_team)
        else:
            teams.append(random.choice(team_ids))
            data += teams[0]
            assigned_teams.append(teams[0])

        # write to file
        # sometimes creates multiple teams for personnel (max = 15 by default)
        if len(teams) < max_per_person and another(multiple_chance):
            file.write(data + '\n')
            person_ids.insert(person_ids.index(i), i)
        else:
            teams = []
            if i != person_ids[-1]:
                file.write(data + '\n')
            else:
                file.write(data)

        amt += 1

    # make sure every team is assigned at least 1 member
    for i in team_ids:
        if i not in assigned_teams:
            person = random.choice(person_ids)
            data = person + delim + str(i)
            file.write('\n' + data)

    print('Generated ' + str(amt) + ' team members')


def gen_data_dir_task(multiple_chance=70, max_per_team=10):
    amt = 0

    try:
        team_file = open('dir_team_data.txt', 'r')
    except OSError:
        print('Cannot locate either dir_team_data.txt')
        return

    team_ids = []
    line = team_file.readline()
    while line:
        team_ids.append(line.split(delim)[0])
        line = team_file.readline()

    file = open('dir_task_data.txt', 'w')

    # task_id increments from 1
    # each team has at least 1 task
    task_id = 0
    current_team = 0
    tasks = 1

    while current_team < len(team_ids):
        task_id += 1

        data = ''

        # task_id
        data += str(task_id) + delim

        # team_id
        data += team_ids[current_team] + delim

        # task_name
        food = get_food()
        data += 'Get ' + food + delim

        # task_description
        data += 'Buy some ' + food + ' from the store' + delim

        # signup_due_date
        data += random_date(2016, 2020) + delim

        # creation_date
        creation_date = random_time(2011, 2015)
        data += creation_date + delim

        # modified_date
        data += creation_date

        # write to file
        # sometimes creates multiple tasks for teams (max = 15 by default)
        if tasks < max_per_team and another(multiple_chance):
            file.write(data + '\n')
            tasks += 1
        else:
            tasks = 1
            if current_team < len(team_ids) - 1:
                file.write(data + '\n')
            else:
                file.write(data)
            current_team += 1

        amt += 1

    print('Generated ' + str(amt) + ' tasks')


def gen_data_dir_task_assignment():
    amt = 0

    try:
        team_file = open('dir_team_data.txt', 'r')
        team_member_file = open('dir_team_member_data.txt', 'r')
        task_file = open('dir_task_data.txt', 'r')
    except OSError:
        print('Cannot locate either dir_team_data.txt or dir_team_member_data.txt or dir_task_data.txt')
        return

    team_ids = []
    team_members = {}  # maps the team's id to the team's member's ids
    line = team_file.readline()
    while line:
        team_ids.append(line.split(delim)[0])
        line = team_file.readline()
    for i in team_ids:
        team_members[i] = []
    line = team_member_file.readline()
    while line:
        team_id = line.split(delim)[1].replace('\n', '')
        team_members[team_id].append(line.split(delim)[0])
        line = team_member_file.readline()

    tasks = {}  # maps each task to it's team
    line = task_file.readline()
    while line:
        tasks[line.split(delim)[0]] = line.split(delim)[1]
        line = task_file.readline()

    file = open('dir_task_assignment_data.txt', 'w')

    for i in list(tasks.keys()):
        data = ''

        # person_id
        data += random.choice(team_members[tasks[i]]) + delim

        # task_id
        data += str(i) + delim

        # creation_date
        creation_date = random_time(2011, 2015)
        data += creation_date + delim

        # modified_date
        data += creation_date

        # write to file
        if i != list(tasks.keys())[-1]:
            file.write(data + '\n')
        else:
            file.write(data)

        amt += 1

    print('Generated ' + str(amt) + ' task assignments')


def create_sql_file():
    file = open('load_data.sql', 'w')

    tables = ['dir_personnel', 'dir_team', 'dir_education_history', 'dir_employment_history', 'dir_team_member', 'dir_task', 'dir_task_assignment']
    tabledata = ['(person_id, user_name, last_name, first_name, city, occupation, creation_date, modified_date)',
                 '(team_id, team_name, team_description, creation_date, modified_date)',
                 '(person_id, college_name, college_start_date, major, creation_date, modified_date)',
                 '(person_id, employer_name, employment_start_date, job_title, creation_date, modified_date)',
                 '(person_id, team_id)',
                 '(task_id, team_id, task_name, task_description, signup_due_date, creation_date, modified_date)',
                 '(person_id, task_id, creation_date, modified_date)'
                 ]

    for i in range(len(tables)):
        file.write('DELETE FROM %s;\n' % tables[i])
        file.write('LOAD DATA LOCAL INFILE "%s_data.txt"\n' % tables[i])
        file.write('INTO TABLE diamondrough.%s\n' % tables[i])
        file.write('FIELDS TERMINATED BY \',\'\n')
        file.write('LINES TERMINATED BY \'\\n\'\n')
        file.write(tabledata[i] + ';\n')
        file.write('\n')


print('Generating sql and data files...')
gen_data_dir_personnel()
gen_data_dir_team()
gen_data_dir_education_history()
gen_data_dir_employment_history()
gen_data_dir_team_member()
gen_data_dir_task()
gen_data_dir_task_assignment()
create_sql_file()
print('Run \'source load_data.sql\' in mysql to load data into tables')
print('IMPORTANT: Must initially run mysql from dir/tools/data as paths are relative')
