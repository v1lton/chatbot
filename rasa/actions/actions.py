from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import typesense

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