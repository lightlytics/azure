import os
import logging
import azure.functions as func
import requests
from typing import List
import json

def main(events: List[func.EventHubEvent]):
    # Get the API URL and token from the environment variables
    api_url = os.getenv('API_URL')
    api_token = os.getenv('API_TOKEN')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    for event in events:
        try:

            full_api_url = f"https://{api_url}/azure-events/events"

            logging.info(f"try to send events to {full_api_url}")

            message_body = event.get_body().decode('utf-8')
            message_body_json = json.loads(message_body)
            event_data = message_body_json[0]

            logging.info(f" type - {type(event_data)}")

            logging.info(f"Try to send event {event_data}")

            # Send the logs to an external API
            response = requests.post(full_api_url, headers=headers, json=event_data)
            
            # Check if the request was successful
            response.raise_for_status()

            # Log the activity log event
            logging.info(f'Activity log: {message_body}')

        except Exception as e:
            # Log the error and continue with the next message
            logging.error(f'Error processing message: {e}')
