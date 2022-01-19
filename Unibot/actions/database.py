import requests
from bs4 import BeautifulSoup
import re

URL_MAIN = 'https://www.di.uoa.gr'
URL_COURSES = "https://www.di.uoa.gr/en/studies/undergraduate/courses"

def get_all_courses(URL):
    all_courses_dict = {}
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    all_semesters_tables = soup.find_all('table', class_="table table-striped cols-10")
    for table_class in all_semesters_tables:
        semester = table_class.find('caption').get_text().strip()
        courses_classes = table_class.find_all('td', class_="views-field views-field-title")
        courses_name_url = {}
        for course in courses_classes:
            url = course.find('a').get('href')
            course_name = course.find('a').get_text()
            courses_name_url[course_name.strip()] = url.strip()
        all_courses_dict[semester] = courses_name_url

    return all_courses_dict

def get_courses_per_semester(semester_name):

    all_courses_dict = get_all_courses(URL_COURSES)
    if str(semester_name) in all_courses_dict.keys():
        courses = all_courses_dict.get(semester_name)
        courses_names = '\n'.join(list(courses.keys()))
        return f'{semester_name}\n\n{courses_names}'
    else:
        return f"I didn't recognize {semester_name}. Is it spelled correctly?"

def get_course_information (course_name,semester_name):
    all_courses_dict = get_all_courses(URL_COURSES)
    courses = all_courses_dict.get(semester_name)
    if str(course_name) in courses.keys():
        url = courses.get(course_name)
    else:
        return f"I didn't understand {semester_name}. Is it spelled correctly?"
    page = requests.get(URL_MAIN+url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="block-corporate-lite-content")
    content = results.find_all('div', class_="views-field views-field-body")
    for tag in content:
        text = tag.find('p').text
        if text != '':
            return f'{semester_name}\t\tCourse: {course_name}\n\n {text}'

def normalise_semester_entity (semester_entity):
    word2ordinal = {'first':'1st','second':'2nd','third':'3rd','fourth':'4th','fifth':'5th','sixth':'6th','seventh':'7th','eighth':'8th'}
    num2ordinal = {'1':'1st','2':'2nd','3':'3rd','4':'4th','5':'5th','6':'6th','7':'7th','8':'8th'}

    token_list = re.findall(r'\b(?!(?i)semester\b)[\w\d]+',semester_entity) # leave out 'semester'

    for token in token_list:
        if token.lower() in word2ordinal.keys(): # e.g. first
            ordinal = word2ordinal[token]
        if token.lower() in num2ordinal.values(): # e.g. 1st
            ordinal = token
        if token in num2ordinal.keys(): # e.g. 1
            ordinal = num2ordinal[token]

            return ordinal

print (get_course_information('Linear Algebra','Semester: 1st'))
