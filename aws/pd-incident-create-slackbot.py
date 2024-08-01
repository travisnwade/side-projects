########################################
#                                      #
#  Slackbot that can create PagerDuty  #
#  incidents hosted in AWS Lambda.     #
#                                      #
#  Please carefully read over the      #
#  README and gather all necessary     #
#  items and review your environment.  #
#                                      #
######################################## 

import json
import os
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.signature import SignatureVerifier

# Environment variables for sensitive data
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']
PAGERDUTY_API_TOKEN = os.environ['PAGERDUTY_API_TOKEN']
PAGERDUTY_SERVICE_ID = 'PAGERDUTY-INCIDENT-SERVICE'

slack_client = WebClient(token=SLACK_BOT_TOKEN)
signature_verifier = SignatureVerifier(SLACK_SIGNING_SECRET)

def lambda_handler(event, context):
    if not signature_verifier.is_valid_request(event['body'], event['headers']):
        return {'statusCode': 401, 'body': 'Invalid request signature'}

    # Parse the event payload
    body = json.loads(event['body'])

    # Verify Slack event
    if 'challenge' in body:
        return {'statusCode': 200, 'body': body['challenge']}

    # Process Slack event
    event_data = body['event']
    if event_data['type'] == 'message' and 'subtype' not in event_data:
        user_id = event_data['user']
        channel_id = event_data['channel']

        try:
            # Ask for the title of the incident
            slack_client.chat_postMessage(
                channel=channel_id,
                text="Please provide a title for the incident (max 255 characters):"
            )
            title = get_user_response(channel_id, user_id)

            # Ask for the urgency of the incident
            slack_client.chat_postMessage(
                channel=channel_id,
                text="Please select the urgency of the incident:",
                attachments=[
                    {
                        "text": "Choose an urgency level",
                        "fallback": "You are unable to choose an option",
                        "callback_id": "urgency_selection",
                        "color": "#3AA3E3",
                        "attachment_type": "default",
                        "actions": [
                            {
                                "name": "urgency",
                                "text": "High",
                                "type": "button",
                                "value": "high"
                            },
                            {
                                "name": "urgency",
                                "text": "Low",
                                "type": "button",
                                "value": "low"
                            }
                        ]
                    }
                ]
            )
            urgency = get_user_response(channel_id, user_id)

            # Ask for a detailed description of the incident
            slack_client.chat_postMessage(
                channel=channel_id,
                text="Please provide a detailed description of the incident:"
            )
            description = get_user_response(channel_id, user_id)

            # Ask who reported the incident
            slack_client.chat_postMessage(
                channel=channel_id,
                text="Who reported the incident? If it was you, click the button below:",
                attachments=[
                    {
                        "text": "Was it you?",
                        "fallback": "You are unable to choose an option",
                        "callback_id": "reporter_selection",
                        "color": "#3AA3E3",
                        "attachment_type": "default",
                        "actions": [
                            {
                                "name": "reporter",
                                "text": "Yes, it was me",
                                "type": "button",
                                "value": user_id
                            }
                        ]
                    }
                ]
            )
            reporter = get_user_response(channel_id, user_id)
            if reporter == "Yes, it was me":
                reporter = user_id
            else:
                slack_client.chat_postMessage(
                    channel=channel_id,
                    text="Please provide the name of the person who reported the incident:"
                )
                reporter = get_user_response(channel_id, user_id)

            # Ask for the location of the incident
            slack_client.chat_postMessage(
                channel=channel_id,
                text="Please provide the location of the incident:"
            )
            location = get_user_response(channel_id, user_id)

            # Create the PagerDuty incident
            create_pagerduty_incident(title, urgency, description, location, reporter)

            # Confirm incident creation
            slack_client.chat_postMessage(
                channel=channel_id,
                text="The incident has been created successfully in PagerDuty."
            )

        except SlackApiError as e:
            print(f"Error creating incident: {e.response['error']}")

    return {'statusCode': 200, 'body': json.dumps('Event processed')}

def get_user_response(channel_id, user_id):
    while True:
        response = slack_client.conversations_history(channel=channel_id, limit=1)
        message = response['messages'][0]
        if message['user'] == user_id:
            return message['text']

def create_pagerduty_incident(title, urgency, description, location, reporter):
    url = "https://api.pagerduty.com/incidents"
    headers = {
        "Authorization": f"Token token={PAGERDUTY_API_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.pagerduty+json;version=2"
    }
    payload = {
        "incident": {
            "type": "incident",
            "title": title[:255],
            "service": {
                "id": PAGERDUTY_SERVICE_ID,
                "type": "service_reference"
            },
            "urgency": urgency,
            "body": {
                "type": "incident_body",
                "details": f"• Reporter: {reporter}\n• Location: {location}\n\n{description}"
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()