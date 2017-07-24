from flask import Flask, request, render_template, abort
import random
import re
import math
import json
import requests


app = Flask(__name__)


# Enter your Slack API token here
slack_api_token = "SLACK-API-TOKEN-GOES-HERE"
slack_api_url = "https://slack.com/api/chat.postMessage"
# The response in Slack will be posted via a "bot". You can set the name of the bot here.
slack_bot_username = "ROLLBOT"
# What icon to show for the bot. This should be the full url to an image.
slack_bot_icon_url = ""
# If set to True, then non-slack POST requests to the endpoint will return
# JSON data. If set to False, then a 403 forbidden will be returned.
allow_non_slack_posts = True
# Similar to allow_non_slack_posts, this determines whether or not the
# GET-based web frontend is open to the public.
allow_public_get = True


def parse_dice(cmd):
    # remove whitespace
    cmd = "".join(cmd.split())

    # get pieces
    pieces = re.split(r"[\s,+,\-,*,/]+", cmd)

    # get operands
    operands = re.findall(r"[+,\-,*,/]+", cmd)

    # roll results
    rolls = []

    for i in range(0, len(pieces)):
        p = pieces[i]

        splitted = p.split('d')

        value = 0

        if len(splitted) == 2:
            num_dice = 1
            if splitted[0] != "":
                num_dice = int(splitted[0])
            if splitted[1] == "":
                # we don't know how many sides the dice has
                continue

            value += random.randint(num_dice, num_dice * int(splitted[1]))

        else:
            value += int(splitted[0])

        rolls.append((value, p))
        pieces[i] = value

    total = 0

    last_op = "+"

    steps = []

    for i in range(0, len(pieces)):
        value = pieces[i]
        steps.append({
            'op': last_op,
            'dice': rolls[i][1],
            'roll': rolls[i][0]
        })

        if last_op == "+":
            total += value
        elif last_op == "-":
            total -= value
        elif last_op == "*":
            total *= value
        elif last_op == "/":
            total = math.floor(total / value)

        # get next op if any
        if i < len(operands):
            last_op = operands[i]

    results = {
        "total": total,
        "rolls": list(map((lambda e: {e[1]: e[0]}), rolls)),
        "steps": steps
    }

    return results


@app.route('/', methods=['get', 'post'])
def index():
    if request.method == "GET":
        if not allow_public_get:
            abort(403)

        roll_input = request.values.get('roll', '1d20')

        result = parse_dice(roll_input)

        # print(result)

        return render_template('index.html', roll=roll_input, total=result['total'], steps=result['steps'])

    elif request.method == "POST":

        is_slack = False
        token = request.values.get('token', None)
        channel_id = request.values.get('channel_id', None)
        user_id = request.values.get('user_name', None)
        if token and channel_id:
            is_slack = True
            roll_input = request.values.get('text', '1d20')
        elif allow_non_slack_posts:
            roll_input = request.values.get('roll', '1d20')
        else:
            abort(403)

        result = parse_dice(roll_input)

        if not is_slack:
            return json.dumps(result)
        else:
            message = {
                'token': slack_api_token,
                'username': slack_bot_username,
                'icon_url': slack_bot_icon_url,
                'text': f'{user_id} rolled {roll_input}: {result["total"]}',
                'channel': channel_id
            }

            r = requests.post(slack_api_url, data=message)

            return ""


if __name__ == '__main__':
    app.run(port=1337, debug=True)
