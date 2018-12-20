import os
import time
import re
from slackclient import SlackClient
import requests
import psycopg2
import json

# instantiate Slack client
slack_client = SlackClient('xoxb-496361367125-496064509811-CvnWCbTDG9EporZRceCaNgKn')
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
                return message, event
    return None ,None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def create_poll(command,event):
    splited=command.split("|")

    votacion={}
    votacion['name']=splited[1]
    votacion['desc']=splited[2]
    votacion['question']=splited[3]
    opt=splited[4].split(",")
    votacion['question_opt']=opt

    conn = psycopg2.connect(dbname='d3i8n8a3vv0nst',
            user='qzxvwbjdcmhnsy',
            password='39cb3668dfac02f210f27e0d813167519ccf63309560bca7f93d2d79be46f308',
            host='ec2-54-246-85-234.eu-west-1.compute.amazonaws.com',
            port=5432
            )
    c = conn.cursor()
    c.execute('SELECT token FROM userSlack where username=(%s)', [str(event['user'])])
    response=c.fetchall()

    if(len(str(response))<5):
        return 'Es necesario estar logueado!'

    token=str(response[0][0])
    headers = {"Authorization": "Token " + token}

    r = requests.post("https://decide-ortosia.herokuapp.com/voting/", votacion, headers=headers)
    return 'todo correcto, se ha creado correctamente'



def login(usurname,password,event):
    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=event['channel'],
        text='logueando'
    )
    credentials = {}
    credentials["username"] = usurname
    credentials["password"] = password
    time.sleep(3)

    r = requests.post("https://decide-ortosia.herokuapp.com/authentication/login/", credentials)

    #BD possgress
    conn = psycopg2.connect(dbname='d3i8n8a3vv0nst',
            user='qzxvwbjdcmhnsy',
            password='39cb3668dfac02f210f27e0d813167519ccf63309560bca7f93d2d79be46f308',
            host='ec2-54-246-85-234.eu-west-1.compute.amazonaws.com',
            port=5432
            )
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS userSlack (username text PRIMARY KEY, token text);''')

    # DELETE previus data a row of data
    c.execute('DELETE FROM userSlack where username=(%s)', [str(event['user'])])
    # Insert a row of data
    c.execute("INSERT INTO userSlack VALUES ("+"'"+str(event['user'])+"'"+", "+"'"+json.loads(r.text)["token"]+"'"+")")

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    c.close()

    slack_client.api_call(
        "chat.postMessage",
        channel=event['channel'],
        text=r
    )

def handle_command(command,event):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "No te entiendo! Los comandos de @Ortosia deben seguir un formato especifico', envia '@ortosia send help pls' para saber más!"
    responder=True
    # Finds and executes the given command, filling in response
    response = None
    # This is  you start to implement more commands!
    if command.startswith('crea votacion'):
        response=create_poll(command,event)
    if command.startswith('quien soy?'):
        response='tu id de usuario es '+str(event['user'])
    if  command.startswith('estoy logueado?'):
        conn = psycopg2.connect(dbname='d3i8n8a3vv0nst',
            user='qzxvwbjdcmhnsy',
            password='39cb3668dfac02f210f27e0d813167519ccf63309560bca7f93d2d79be46f308',
            host='ec2-54-246-85-234.eu-west-1.compute.amazonaws.com',
            port=5432
            )
        c = conn.cursor()
        c.execute('SELECT token FROM userSlack where username=(%s)', [str(event['user'])])
        response=c.fetchall()
        if(len(str(response))<5):
            response='No estas logueado aun, utiliza "@ortosia logueame [usurname] [password]" para loguearte en decide' 
        else:
            response='Estas logueado correctamente, tu token de sesión es: '+str(response[0][0])
        conn.close()
        c.close()

    if  command.startswith('cierrame la sesion'):
        conn = psycopg2.connect(dbname='d3i8n8a3vv0nst',
            user='qzxvwbjdcmhnsy',
            password='39cb3668dfac02f210f27e0d813167519ccf63309560bca7f93d2d79be46f308',
            host='ec2-54-246-85-234.eu-west-1.compute.amazonaws.com',
            port=5432
            )
        c = conn.cursor()
        c.execute('DELETE FROM userSlack where username=(%s)', [str(event['user'])])
        conn.commit()
        conn.close()
        c.close()
        response='eliminado usuario '+str(event['user'])+' de la base de datos de ortosiaBot'

    if command.startswith('send'):
        if command.endswith('pls'):
            response = "Enviando ayuda! \n \n Listado de comandos: \n @ortosia send help pls, envia el mensaje de ayuda \n @ortosia logueame! [nombre de usuario] [contraseña], inicia sesión la plataforma decide\n@ortosia crea votacion | [titulo] | [descripcion] | [pregunta] | [opciones separadas por comas]: crea la votacion en la plataforma decide, es necesario estar logueado correctamente en la plataforma decide y tener los permisos necesarios \n\n Comandos avanzados(desarrollo): \n @ortosia quien soy?: devuelve el id de usuario \n @ortosia estoy logueado? devuelve el token de autorización de decide en caso estar logueado\n @ortosia cierrame la sesion : cierra la sesion del usuario"
        else:
            response = "Es necesario pedir las cosas educadamente a @Ortosia, añada un 'pls' al final de su peticion, gracias"
    elif command.startswith('logueame'):
        splited=command.split(" ")
        login(splited[len(splited)-2],splited[len(splited)-1],event)
        responder=False

    if (responder==True):
        # Sends the response back to the channel
        slack_client.api_call(
            "chat.postMessage",
            channel=event['channel'],
            text=response or default_response
        )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command,event = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command,event)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")


