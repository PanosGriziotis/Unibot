# The file contains custom system utterances 

def utter_help_semester(list_of_semesters):
    return f"Για να σε βοηθήσω, τα διαθέσιμα εξάμηνα του τμήματος είναι τα παρακάτω: {' '.join(list_of_semesters)}."

def utter_help_course (list_of_courses):
    return f"Για να σε βοηθήσω, ορίστε μία λίστα με τα μαθήματα του εξαμήνου: {', '.join(list_of_courses)}."

def utter_description (course_name, description):
    return f'Το περιεχόμενο του μαθήματος {course_name} αφορά σε γενικές γραμμές τα εξής: {description}'

def utter_not_recognize_course ():
    return "Χμμ. Δυσκολεύομαι να αναγνωρίσω αυτό το μάθημα."

def utter_not_recognize_semester():
    return "Χμμ. Δυσκολεύομαι να αναγνωρίσω αυτό το εξάμηνο."

def utter_schedule (course_name,sch_d):
    for course, dict in sch_d.items():
        for key in dict:
            if type(dict[key]) == tuple:
                dict[key] = ' και '.join(map(str,dict[key]))
        return f'To μάθημα {course} διδάσκεται την/τις ημέρα/-ες {dict["day"]} με τον/τους καθηγητή/-ές {dict["professor"]} και τις ώρες {dict["time"]}  στην/στις αίθουσα/-ες: {dict["aula"]}' 