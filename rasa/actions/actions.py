from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import typesense
import pandas as pd

class ActionSearchQA(Action):
    def name(self) -> Text:
        return "action_search_qa"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        client = typesense.Client({
            'nodes': [{
                'host': 'yq1596od2mxi47vhp-1.a1.typesense.net',
                'port': '443',
                'protocol': 'https'
            }],
            'api_key': 'k26KOvUUNGPs2LbpWT1cu4sBpoQX7nct',
            'connection_timeout_seconds': 2
        })
        
        user_message = tracker.latest_message.get("text", "")

        search_parameters = {
        'q'         : user_message,
        'query_by'  : 'question, answer'
        }

        collection_name = 'questions'
        response = client.collections[collection_name].documents.search(search_parameters)

        if response['hits'][0]['document']['answer']:
            answer = response["hits"][0]["document"]["answer"]
            dispatcher.utter_message(text=answer)
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find an answer to that question.")

        return []
    
class ActionFlightsSearch(Action):
    def name(self) -> Text:
        return "action_flights_search"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        flights_df = pd.read_csv('../data/generated_flights_data.csv')
        
        origin = tracker.get_slot('fromloc.city_name')
        destination = tracker.get_slot('toloc.city_name')
        day = tracker.get_slot('depart_date.day_name')
        
        flights = flights_df[(flights_df['fromloc.city_name'] == origin) & (flights_df['toloc.city_name'] == destination) & (flights_df['depart_date.day_name'] == day)]

        if flights.shape[0] > 0:
            response = "I found the following flights: \n" + flights.to_string(index=False)
        else:
            response = "I couldn't find any flights for that route on that day."

        dispatcher.utter_message(text=response)

        return []