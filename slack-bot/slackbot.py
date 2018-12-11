import os
import time
import re
from slackclient import SlackClient
import requests


# instantiate Slack client
slack_client = SlackClient('xoxb-496361367125-496064509811-40frIeS25WwFuujQwFLgCpA1')
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM


MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def login(usurname,password):
    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text='logueando'
    )
    credentials = {}
    credentials["username"] = usurname
    credentials["password"] = password
    r = requests.post("https://decide-ortosia.herokuapp.com/authentication/login/", credentials)

    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=r
    )

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "No te entiendo! Los comandos de @Ortosia deben seguir un formato especifico', envia '@ortosia send help pls' para saber más!"
    responder=True
    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!

    if command.startswith('send'):
        if command.endswith('pls'):
            response = "Enviando ayuda! \n \n Listado de comandos: \n @ortosia send help pls, envia el mensaje de ayuda \n @ortosia logueame! [nombre de usuario] [contraseña], inicia sesión la plataforma decide\n mas cosas"
        else:
            response = "Es necesario pedir las cosas educadamente a @Ortosia, añada un 'pls' al final de su peticion, gracias"
    elif command.startswith('logueame'):
        splited=command.split(" ")
        login(splited[len(splited)-2],splited[len(splited)-1])
        responder=False

    if (responder==True):
        # Sends the response back to the channel
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")


