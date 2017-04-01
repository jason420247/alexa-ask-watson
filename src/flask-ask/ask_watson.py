import os
import logging

from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json
'''
def generate_response(output_speech,
                      card_title="",
                      card_subtitle="",
                      card_content="",
                      session_attributes={},
                      endSession=True):
    
    logging.debug('Enetered generate_response session.attributes context is  %s ' %session.attributes['context'] )
    response = {
        "version": "1.0",
        "sessionAttributes": {
            "user": {
                "name": "AxonTrusts"
            },
            "context": {session_attributes}
            },
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": output_speech
            },
            "card": {
                "type": "Simple",
                "title": card_title,
                "subtitle": card_subtitle,
                "content": card_content
            },
            "shouldEndSession": endSession
        }
    }
    
    logging.debug('Entered generate_response - response %s ' %response )
    
    return json.dumps(response)
'''
app = Flask(__name__)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# On Bluemix, get the port number from the environment variable VCAP_APP_PORT
# When running this app on the local machine, default the port to 8080
port = int(os.getenv('VCAP_APP_PORT', 5000))
#Setup Logging to a file
logging.basicConfig(filename='example.log',level=logging.DEBUG)

# Setup Credentials on initialization to conversation service  
from watson_developer_cloud import AuthorizationV1
from watson_developer_cloud import ConversationV1

# replace with your own workspace_id
workspace_id = '55981191-57ee-4cdb-8402-e586a126f174'

print('Environment Variable VCAP_SERVICES')
vcap_services = os.getenv('VCAP_SERVICES')
print(json.dumps(vcap_services, indent=2))

vcap = json.loads(os.getenv("VCAP_SERVICES"))['conversation']
print('VCAP Services vcap %s'  %vcap )
cl_username = vcap[0]['credentials']['username']
print('VCAP Services cl_username %s'  %cl_username )
cl_password = vcap[0]['credentials']['password']
print('VCAP Services cl_password %s'  %cl_password )

# Call Conversation Service
conversation = ConversationV1(
    username = cl_username,
    password = cl_password,
    version='2016-09-20')

logging.debug('Checked Conversation Service is working')
response = conversation.message(workspace_id=workspace_id, message_input={'text': 'Hello.'})
print(json.dumps(response, indent=2))
            
ask = Ask(app, "/")

@ask.launch

def new_game():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("DrinkIntent", convert={'Phrase': str})

def choose_drink(Phrase):

    logging.debug('Entered DrinkIntent - Alexa input %s ' %Phrase )
    logging.debug('Entered DrinkIntent - Alexa Context %s ' %session.attributes.get('context'))
    if session.attributes.get('context') != None:
        #first time calling conversation service with this user
        logging.debug('---Alexa Session Context from ButlerCarlos s already set %s'  %session.attributes['context'] )
        response = conversation.message(workspace_id=workspace_id, 
                                        message_input={'text': Phrase},
                                        context=session.attributes.get('context'))
    else:
        #Previously called conversation service with this user. Use Context variable 
        response = conversation.message(workspace_id=workspace_id, message_input={'text': Phrase})
    #Save Conversation context for  the next request.
    cntx = response['context']
    logging.debug('response context %s' %cntx)
    session.attributes['context']= cntx
    
    # When you send multiple requests for the same conversation, include the context object from the previous response.
    # response = conversation.message(workspace_id=workspace_id, message_input={'text': 'turn the wipers on'},                              context=response['context'])
    logging.debug(json.dumps(response, indent=2))
    msg = json.dumps(response['output']['text'])
    logging.debug('response msg %s' %msg)
    
    # Nee to check if shouldEndSession
    #  [code] { "version": "1.0", "sessionAttributes": {}, "response": { "outputSpeech": { "type": "PlainText", "text": "Your favorite color is blue, goodbye" }, "card": { "type": "Simple", "title": "SessionSpeechlet - WhatsMyColorIntent", "content": "SessionSpeechlet - Your favorite color is blue, goodbye" }, "reprompt": { "outputSpeech": { "type": "PlainText", "text": null } }, "shouldEndSession": true } } [/code]
    '''
    return generate_response(msg,
                      card_title="",
                      card_subtitle="",
                      card_content="",
                      session_attributes=cntx,
                      endSession=False)
    '''
    return question(msg).reprompt("Sorry I didn't understand what you said")
'''  Usefull for ending the session
@ask.session_ended
def session_ended():
    return statement("")
'''


@ask.intent("YesIntent")

def next_round():

    numbers = [randint(0, 9) for _ in range(3)]

    round_msg = render_template('round', numbers=numbers)

    session.attributes['numbers'] = numbers[::-1]  # reverse

    return question(round_msg)


@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})

def answer(first, second, third):

    winning_numbers = session.attributes['numbers']

    if [first, second, third] == winning_numbers:

        msg = render_template('win')

    else:

        msg = render_template('lose')

    return statement(msg)


if __name__ == '__main__':
    print("APP RUN")
    app.run(host='0.0.0.0', port=port, debug=True)
