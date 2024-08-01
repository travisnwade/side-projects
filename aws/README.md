# ProblemTron - Slack to PagerDuty Incident Creator

## Overview

ProblemTron is an interactive Slack bot that allows users to create PagerDuty incidents through direct messages. Users are prompted to provide the title, urgency, description, reporter, and location of the incident, which are then used to create an incident in PagerDuty.

## Prerequisites

1. **AWS Lambda**: Ensure you have an AWS account with permissions to create and deploy Lambda functions.
2. **Slack App**: Create a Slack app and bot user. Obtain the Slack Bot Token and Signing Secret.
3. **PagerDuty API Token**: Generate a PagerDuty API token with permissions to create incidents.
4. **Python Libraries**: Install the required Python libraries:
   - `slack_sdk`
   - `requests`

## Installation

1. **Create a Slack App**:
   - Go to the Slack API [Apps page](https://api.slack.com/apps).
   - Create a new app and add a bot user.
   - Enable the `chat:write` and `channels:history` permissions under OAuth & Permissions.
   - Install the app to your workspace and obtain the Bot User OAuth Access Token and Signing Secret.

2. **Generate a PagerDuty API Token**:
   - Log in to PagerDuty.
   - Go to the User Settings and generate a new API token.

3. **Deploy the Lambda Function**:
   - Set up an AWS Lambda function.
   - Configure environment variables for the function:
     - `SLACK_BOT_TOKEN`: Your Slack Bot Token.
     - `SLACK_SIGNING_SECRET`: Your Slack Signing Secret.
     - `PAGERDUTY_API_TOKEN`: Your PagerDuty API Token.
   - Copy the provided Python code into your Lambda function.
   - Install the required Python libraries (`slack_sdk`, `requests`) in the Lambda environment.

4. **Configure Slack Events**:
   - In your Slack app settings, go to Event Subscriptions and enable events.
   - Add the request URL for your Lambda function.
   - Subscribe to the `message.im` event to receive direct messages.

5. **AND REMEMBER**: [My Final Words](https://github.com/travisnwade/side-projects/blob/main/README.md#final-words).
   - > *P.S. If you do break something, don't say I didn't warn you.*