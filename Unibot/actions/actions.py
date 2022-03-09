# This files contains custom actions

from typing import Any, Text, Dict, List
from matplotlib.pyplot import text
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, Restarted
from rasa_sdk.types import DomainDict
from Levenshtein import distance
from actions.bot_utters import utter_help_semester, utter_help_course, utter_description, utter_schedule, utter_not_recognize_course, utter_not_recognize_semester
from . import database

class ValidateCourseForm(FormValidationAction):
    def __init__(self):
        self.target_num_semester = None
        self.target_course_name = None

    def name(self) -> Text:
        return "validate_course_form"

    def validate_num_semester(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validate `num_semester` value.

        allowed_semesters_list = database.get_semesters_list()

        #  test if given slot value aligns with db

        for string in allowed_semesters_list:
            if slot_value in string:
                self.target_num_semester = string
            else:
                self.target_course_name = None

        # validation message

        if self.target_num_semester is None:
            dispatcher.utter_message(
                text=utter_not_recognize_semester() + utter_help_semester(allowed_semesters_list))
            return {"num_semester": None}
        dispatcher.utter_message(text=f"Τέλεια! Ψάχνεις, λοιπόν, για ένα μάθημα για το {self.target_num_semester}.")
        return {"num_semester": self.target_num_semester}

    def validate_course_name(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validate `course_name` value.


        semester_name = tracker.get_slot('num_semester')
        allowed_courses_names = database.get_semester_courses(semester_name)

        # test if given slot value aligns with db (Lev distance)

        distances = {}
        for course_name in allowed_courses_names:
            distances[course_name] = distance(course_name, str(slot_value))
        for course_name, distance_value in distances.items():
            if distance_value <= 5:
                self.target_course_name = course_name
                break
            if slot_value in course_name:
                self.target_course_name = course_name
                
        # validation message

        if self.target_course_name is None:
            dispatcher.utter_message(
                text= utter_not_recognize_course() + utter_help_course(allowed_courses_names))
            return {"course_name": self.target_course_name}
        return {"course_name": self.target_course_name} 
 
class ActionSupplyAnswer(Action):
    def name(self) -> Text:
        return "action_supply_answer_to_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # get request type from slot

        request_type = tracker.get_slot("request_type")
        print (request_type)

        # get course name from slot

        course_name = tracker.get_slot("course_name")
        print (course_name)

        # get description from db

        description = database.get_course_description(course_name)

        # get schedule dictionary from db

        sch_d = database.get_schedule_dict_for_course(tracker.get_slot("course_name"))

        if request_type == 'description':
            # return message
            dispatcher.utter_message(text=utter_description(course_name,description))
            return []

        if request_type == 'schedule':
            # return message
            dispatcher.utter_message(text = utter_schedule(course_name,sch_d))
            return []
        
        if request_type == 'general':
            # retun message
            dispatcher.utter_message(text = '\n\n'.join([utter_description(course_name, description),
                                                         utter_schedule(course_name,sch_d)]))
            return []

class HelpUser(Action):
    def name(self) -> Text:
        return "action_help_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        allowed_semesters_list = database.get_semesters_list()
        
        if tracker.get_slot('num_semester') == None:
            dispatcher.utter_message(text = utter_help_semester(allowed_semesters_list))
            return []
        if tracker.get_slot ('course_name') == None:
            allowed_courses_list = database.get_semester_courses(tracker.get_slot('num_semester'))
            dispatcher.utter_message(text = utter_help_course(allowed_courses_list))
            return []

class ActionEnd(Action):
    def name(self):
        return "action_restart"

    async def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset(), Restarted()]