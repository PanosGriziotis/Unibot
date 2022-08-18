# This file contains the data retrieval code using web scrapping

from matplotlib.pyplot import get
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as  pd
import re
import numpy as np

URL_MAIN= 'https://www.di.uoa.gr'
URL_COURSES = URL_MAIN+"/studies/undergraduate/courses"
URL_WINTER_19 = URL_MAIN+'/schedule/19-20/timetable_PPS_winter1920.html'
URL_SPRING_19 = URL_MAIN+'/schedule/19-20/timetable_PPS_spring1920.html'


def parse_page (url):
    page = requests.get(url)
    return BeautifulSoup(page.content,'html.parser')

def get_all_courses(url):
    """
    Returns a dictionary
    k: semester name
    v: dictionary [k: course name v: url of course's description]
    """
    all_courses_dict = {} # main dict

    soup = parse_page(url)

    for table_class in soup.find_all('table', class_="table table-striped cols-10"):

        semester_name = table_class.find('caption').get_text().strip()

        sem_courses= table_class.find_all('td', class_="views-field views-field-title")
        
        sem_courses_urls = {} # nested dict

        for sem_course in sem_courses:
            url = sem_course.find('a').get('href')
            course_name = sem_course.find('a').get_text()
            sem_courses_urls[course_name.strip()] = url.strip()

        all_courses_dict[semester_name] = sem_courses_urls
    return all_courses_dict

def get_semesters_list():
    """ Returns a list of available semester names """
    all_courses_dict = get_all_courses(URL_COURSES)
    return list(all_courses_dict.keys())

def get_semester_courses(semester_name):
    """ Returns a list of course names for a given semester """
    all_courses_dict = get_all_courses(URL_COURSES)
    if str(semester_name) in all_courses_dict.keys():
        courses_names = list(all_courses_dict.get(semester_name).keys())
        return courses_names
    else:
        return None

def get_course_description(course_name):
    """ Return text description of a given text """
    all_courses_dict = get_all_courses(URL_COURSES)
    for k, courses in all_courses_dict.items():
        
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
    """ Return full dataframe of schedules"""
    dfs = []

    for i in [url1,url2]:

        soup = parse_page(i)
        schedule_rows = []
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
    """ Return schedule dictionary for specific course 
        k: course name 
        v: dictionary [keys: professor, time, day, place - values: tuple of relevant info for each key] 
    """
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