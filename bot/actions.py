from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

shoppingList = []
# [(4, bananas), (apples), (2, pens)]

class ActionAddItem(Action):

    def name(self) -> Text:
        return "action_add_item"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        item = ""
        quantity = 0
        for e in tracker.latest_message['entities']:
            if e['entity'] == 'item':
                item= e['value']
            if e['entity'] == 'quantity':
                quantity = e['value']
        print(f"Item {item}, quantity {quantity} for Intent {intent}")
        global shoppingList
        if quantity==0:
            shoppingList.append((item))
        else:
            shoppingList.append((item, quantity))
        dispatcher.utter_message(text=f"Item {item} added to shopping list")
        return []

class ActionDeleteItem(Action):

    def name(self) -> Text:
        return "action_delete_items"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        item = ""
        for e in tracker.latest_message['entities']:
            if e['entity'] == 'item':
                item = e['value']
        global shoppingList
        for i in range(0, len(shoppingList)):
            if shoppingList[i][0]==item:
                print(f"deleting {item} from list")
                del shoppingList[i]
        dispatcher.utter_message(text=f"Item {item} deleted from the list")
        return []

class ActionShowItems(Action):
    def name(self) -> Text:
        return "action_show_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global shoppingList
        dispatcher.utter_message(text=", ".join(map(str, shoppingList)) )
        return []
