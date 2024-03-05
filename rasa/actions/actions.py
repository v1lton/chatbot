from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import typesense
import pandas as pd
from openai import OpenAI
from rasa_sdk.events import SlotSet

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
        
        flights_df = pd.read_csv('/Users/wiltonramos/Documents/chatbot/rasa/actions/generated_flights_data.csv')
        
        origin = tracker.get_slot('fromloc.city_name')
        destination = tracker.get_slot('toloc.city_name')
        day = tracker.get_slot('depart_date.day_name')
        
        flights = flights_df[(flights_df['fromloc.city_name'] == origin) & (flights_df['toloc.city_name'] == destination) & (flights_df['depart_date.day_name'] == day)]

        if flights.shape[0] > 0:
            response = "I found the following flights: \n" + flights.head(3).to_json(orient='records')
        else:
            response = "I couldn't find any flights for that route on that day."

        dispatcher.utter_message(text=response)

        return [SlotSet("fromloc.city_name", None), SlotSet("toloc.city_name", None), SlotSet("depart_date.day_name", None)]
    
class ActionConnectToGPT(Action):
    def name(self) -> Text:
        return "action_connect_to_gpt"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        client = OpenAI(api_key='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')
        user_message = tracker.latest_message.get("text", "")

        # Making a request to the API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Specify the model you want to use
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers with short messages. Max of 100 tokens."},
                {"role": "user", "content": user_message},
            ]
        )

        dispatcher.utter_message(response.choices[0].message.content)
        
        return []