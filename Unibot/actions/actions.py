# This files contains custom actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from Levenshtein import distance
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
                text=f"Σόρρυ. Δεν υπάρχει {slot_value} εξάμηνο. Τα διαθέσιμα εξάμηνα του τμήματος είναι τα παρακάτω: {','.join(allowed_semesters_list)}.")
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
        allowed_courses_names = database.get_courses_list_per_semester(semester_name)

        # test if given slot value aligns with db (Lev distance)

        distances = {}
        for course_name in allowed_courses_names:
            distances[course_name] = distance(course_name, str(slot_value))
        print (distances)
        for course_name, distance_value in distances.items():
            print (course_name)
            print (distance_value)
            if distance_value <= 5:
                self.target_course_name = course_name
                break
            if slot_value in course_name:
                self.target_course_name = course_name
                
        print ('after computing distance:' , self.target_course_name)
        # validation message

        if self.target_course_name is None:
            dispatcher.utter_message(
                text=f"Χμμ. Δυσκολεύομαι να αναγνωρίσω αυτό το μάθημα. Για να σε βοηθήσω, ορίστε μία λίστα με τα μαθήματα του εξαμήνου: {' ,'.join(allowed_courses_names)}.")
            return {"course_name": self.target_course_name}
        dispatcher.utter_message(text=f"Τέλεια! Ενδιαφέρεσαι για το μάθημα {self.target_course_name}.")
        return {"course_name": self.target_course_name} 
 
 

class ActionSupplyCourseDescription(Action):

    def name(self) -> Text:
        return "action_supply_course_description"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        # get description from db

        description = database.get_course_description(tracker.get_slot("course_name"), tracker.get_slot("num_semester"))

        # message

        dispatcher.utter_message(
            text=f'Το περιεχόμενο του μαθήματος {tracker.get_slot("course_name")} αφορά σε γενικές γραμμές τα εξής: {description} ')
        return []
