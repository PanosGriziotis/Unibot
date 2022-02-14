# This file contains the data retrieval code using web scrapping

from matplotlib.pyplot import get
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as  pd
import re
import numpy as np

URL_MAIN = 'https://www.di.uoa.gr'
URL_COURSES = "https://www.di.uoa.gr/studies/undergraduate/courses"
URL_WINTER_19 = 'https://www.di.uoa.gr/schedule/19-20/timetable_PPS_winter1920.html'
URL_SPRING_19 = 'https://www.di.uoa.gr/schedule/19-20/timetable_PPS_spring1920.html'

def parse_page (url):
    page = requests.get(url)
    return BeautifulSoup(page.content,'html.parser')

def get_all_courses(url):
    all_courses_dict = {}
    soup = parse_page(url)
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


def get_semesters_list():
    all_courses_dict = get_all_courses(URL_COURSES)
    return list(all_courses_dict.keys())


def get_courses_list_per_semester(semester_name):
    all_courses_dict = get_all_courses(URL_COURSES)
    if str(semester_name) in all_courses_dict.keys():
        courses = all_courses_dict.get(semester_name)
        courses_names = list(courses.keys())

        return courses_names
    else:
        return None


def get_course_description(course_name, semester_name):
    all_courses_dict = get_all_courses(URL_COURSES)
    courses = all_courses_dict.get(semester_name)
    if str(course_name) in courses.keys():
        url = courses.get(course_name)
        soup = parse_page(URL_MAIN + url)
        results = soup.find(id="block-corporate-lite-content")
        content = results.find_all('div', class_="views-field views-field-body")
        for tag in content:
            text = tag.find('p').text
            if text != '':
                return text

def get_schedules(url1,url2):
    dfs = []

    for i in [url1,url2]:

        soup = parse_page(i)
        schedule_rows = []
        table = soup.find('table')
        rows = soup.find_all('tr')
        global day

        for row in rows:
            row_dict = {}
            column = 0
            row_dict = {}
            tds = row.find_all('td')

            if len(tds) == 1:
                day = tds[0].find('font').get_text(strip=True)

            for td in tds:
                content = td.find('font').get_text(strip=True,separator = '\t')
                row_dict[column] = content
                column+=1
                row_dict['day'] = day
            
            schedule_rows.append(row_dict)
        df = pd.DataFrame(schedule_rows)
        dfs.append(df)
    n_df = pd.concat(dfs)
    n_df.columns = n_df.iloc[1]
    n_df.rename(columns={'Δευτέρα':'day','Ώρα/Αίθ.':'time'}, inplace = True)

    return n_df

def get_schedule_dict_for_course (course_name):
    
    schedule_df = get_schedules(URL_WINTER_19,URL_SPRING_19)
        
    mask = np.column_stack([schedule_df[col].str.contains(rf'{course_name}', na=False) for col in schedule_df])
    answer = schedule_df.loc[mask.any(axis=1)]

    aulas = []
    for col in answer:
        mask = answer[col].str.contains(rf'{course_name}', na=False)
        if mask.any() == True:
            aulas.append(col)
    indeces = answer.reset_index(drop=True).index
    
    exact_values = []
    for idx in indeces:
        for aula in aulas:
            exact_value = answer.iloc[idx][aula]
            if course_name in exact_value:
                exact_values.append(exact_value)
    unique_values = list(set(exact_values))

    schedule_dict = {} 
    for col in aulas:          
        for value in unique_values:
            course_dict = {}
            time = ', '.join(list(answer['time'].where(answer[col] == value).dropna().values))
            day = ','.join(list(set(list(answer['day'].where(answer[col] == value).dropna().values))))
            if len(time) > 0  and len(day) > 0:
                course_dict['professor'] = value.split('\t')[2]
                course_dict['time'] = time
                course_dict['day'] = day
                course_dict['aula'] = col
                course_key = value.split('\t')[0]
            
                if course_key in schedule_dict.keys():
                    for k,old_dict in schedule_dict.items():
                        dicts = [old_dict,course_dict]
                        new_dict = {}
                        for key in old_dict:
                            new_dict[key] = tuple(d[key]for d in dicts)
                        
                        schedule_dict[course_key] = new_dict
                else:
                    schedule_dict[course_key] = course_dict
    return schedule_dict

def message(course_name):
    schedule_dict = get_schedule_dict_for_course(course_name)
    for course, dic in schedule_dict.items():
        for key in dic:
            if type(dic[key]) == tuple:
                dic[key] = ' και '.join(map(str,dic[key]))
        
        print(f'To μάθημα {course} διδάσκεται την/τις ημέρα/-ες {dic["day"]} με τον/τους καθηγητή/-ές {dic["professor"]} και τις ώρες {dic["time"]}  στην/στις αίθουσα/-ες: {dic["aula"]}')


