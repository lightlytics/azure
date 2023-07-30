import os
import logging
import azure.functions as func
import requests
import json

def main(events: List[func.EventHubEvent]):
    # Get the API URL and token from the environment variables
    api_url = os.getenv('API_URL')
    api_token = os.getenv('API_TOKEN')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'  # Assuming the token is used as a Bearer token
    }

    for event in events:
        try:
            # Convert the message body from bytes to string
            message_body = event.get_body().decode('utf-8')

            # Send the logs to an external API
            response = requests.post(api_url, headers=headers, data=message_body)
            
            # Check if the request was successful
            response.raise_for_status()

            # Log the activity log event
            logging.info(f'Activity log: {message_body}')

        except Exception as e:
            # Log the error and continue with the next message
            logging.error(f'Error processing message: {e}')
