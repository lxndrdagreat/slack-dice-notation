# Slack Dice Notation

A simple webserver that integrates with Slack's webhooks to process dice
notation and return the results.

Built with Python 3 and Flask.

## Requirements

- Python 3
- Flask
- Slack API Token

## Setup

- Clone the repo
- *optional: use a virtual environment*
- Install requirements with pip: `pip install -r requirements.txt`
- Insert your Slack API token
- For debug mode, run `dice-roll.py`; for production, use something like gunicorn.

## Settings

### Slack API Token

In order for the Slack integration to work, you have to enter your API token:

    slack_api_token = "SLACK-API-TOKEN-GOES-HERE"

### Slack API URL

You shouldn't need to change this.

    slack_api_url = "https://slack.com/api/chat.postMessage"
    

### Set the bot username

The response in Slack will be posted via a "bot". You can set the name of the bot here.

    slack_bot_username = "ROLLBOT"

### Set the bot's profile icon

What icon to show for the bot. This should be the full url to an image.

    slack_bot_icon_url = ""

### Allow non-slack POST requests

If set to `True`, then non-slack POST requests to the endpoint will return
JSON data. If set to `False`, then a 403 forbidden will be returned.
Default is `True`.

    allow_non_slack_posts = True

### Enable public front-end

Similar to `allow_non_slack_posts`, this determines whether or not the
GET-based web frontend is open to the public.

    allow_public_get = True

## License

MIT license.

Copyright 2017 Dan Alexander

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.