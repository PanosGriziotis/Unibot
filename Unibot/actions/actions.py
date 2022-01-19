# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from . import database

class ActionListCourses(Action):

    def name(self) -> Text:
        return "action_list_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        semester = next(tracker.get_latest_entity_values("semester"),None)

        # Test if given entity aligns to nlu data
        if not semester or semester == None:
            msg = f"You said: {semester}.I am sorry, I did not get that."
            dispatcher.utter_message(text=msg)
            return []

        # return the output of relevant method
        msg = database.get_courses_per_semester(semester)
        dispatcher.utter_message(text=msg)

        return []

class ActionGiveCourseInfo(Action):

    def name(self) -> Text:
        return "action_give_course_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        course_name = next(tracker.get_latest_entity_values("course"), None)
        semester = tracker.get_slot("semester")

        # Test if given semester entity aligns to nlu data
        if not semester or semester == None:
            msg = f"You said: {semester}.I am sorry, I did not get that."
            dispatcher.utter_message(text=msg)
            return []

        # Test if given course entity aligns to nlu data
        if not course_name or course_name == None:
            msg = f"You said {course_name}. I am sorry, I did not get that."
            dispatcher.utter_message(text=msg)
            return []

        msg = database.get_course_information(course_name,semester)
        dispatcher.utter_message(text=msg)

        return[]
