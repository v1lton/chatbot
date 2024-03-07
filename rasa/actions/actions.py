from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, Restarted

import typesense
import pandas as pd
from openai import OpenAI

class ActionSearchQA(Action):
    """
    This action searches the questions collection in Typesense for the user's question and returns the answer.
    """
    def name(self) -> Text:
        return "action_search_qa"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        # Connect to Typesense
        client = typesense.Client({
            'nodes': [{
                'host': 'yq1596od2mxi47vhp-1.a1.typesense.net',
                'port': '443',
                'protocol': 'https'
            }],
            'api_key': 'k26KOvUUNGPs2LbpWT1cu4sBpoQX7nct',
            'connection_timeout_seconds': 2
        })
        
        # Get the user's message
        user_message = tracker.latest_message.get("text", "")

        # Search the questions collection for the user's message
        search_parameters = {
        'q'         : user_message,
        'query_by'  : 'question, answer'
        }

        # Search the collection
        collection_name = 'questions'
        response = client.collections[collection_name].documents.search(search_parameters)

        # If there is an answer, return it. Otherwise, return a message saying that the answer was not found.
        if response['hits'][0]['document']['answer']:
            answer = response["hits"][0]["document"]["answer"]
            dispatcher.utter_message(text=answer)
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find an answer to that question.")

        return [Restarted()]
    
class ActionFlightsSearch(Action):
    """
    This action searches the flights data for flights that match the user's criteria and returns the results.
    """
    def name(self) -> Text:
        return "action_flights_search"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        # Load the flights data
        flights_df = pd.read_csv('/Users/wiltonramos/Documents/chatbot/rasa/actions/generated_flights_data.csv')
        
        # Get the slots from the tracker
        origin = tracker.get_slot('fromloc.city_name')
        destination = tracker.get_slot('toloc.city_name')
        day = tracker.get_slot('depart_date.day_name')
        
        # Filter the data based on the user's criteria
        flights = flights_df[(flights_df['fromloc.city_name'] == origin) & (flights_df['toloc.city_name'] == destination) & (flights_df['depart_date.day_name'] == day)]

        # If there are flights, return the top 3. Otherwise, return a message saying that no flights were found.
        if flights.shape[0] > 0:
            response = "I found the following flights: \n" + flights.head(3).to_json(orient='records')
        else:
            response = "I couldn't find any flights for that route on that day."

        # Send the response to the user
        dispatcher.utter_message(text=response)

        # Reset the slots
        return [Restarted()]
    
class ActionFlightsCount(Action):
    """
    This action counts the number of flights that match the user's criteria and returns the count.
    """
    def name(self) -> Text:
        return "action_flights_count"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        # Load the flights data
        flights_df = pd.read_csv('/Users/wiltonramos/Documents/chatbot/rasa/actions/generated_flights_data.csv')
        
        # Get the slots from the tracker
        origin = tracker.get_slot('fromloc.city_name')
        destination = tracker.get_slot('toloc.city_name')
        day = tracker.get_slot('depart_date.day_name')
        
        # Filter the data based on the user's criteria
        flights = flights_df[(flights_df['fromloc.city_name'] == origin) & (flights_df['toloc.city_name'] == destination) & (flights_df['depart_date.day_name'] == day)]

        # If there are flights, return the count. Otherwise, return a message saying that no flights were found.
        if flights.shape[0] > 0:
            response = "There are " + str(len(flights)) + " flights available for that route on that day."
        else:
            response = "I couldn't find any flights for that route on that day."

        # Send the response to the user
        dispatcher.utter_message(text=response)

        # Reset the slots
        return [Restarted()]
    
class ActionConnectToGPT(Action):
    """
    This action connects to the OpenAI GPT-3 API and returns a response to the user's message.
    """
    def name(self) -> Text:
        return "action_connect_to_gpt"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        # Create OpenAI client object
        client = OpenAI(api_key='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')

        # Get the user's message
        user_message = tracker.latest_message.get("text", "")

        # Making a request to the API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers with short messages. Max of 100 tokens."},
                {"role": "user", "content": user_message},
            ]
        )

        # Send the response to the user
        dispatcher.utter_message(response.choices[0].message.content)
        
        return [Restarted()]
    
class ActionRestartConversation(Action):
    """
    This action restarts the conversation.
    """
    def name(self) -> Text:
        return "action_restart_conversation"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Oh, sorry. Could you please try again?")
        
        return [Restarted()]