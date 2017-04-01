Use the Amazon Echo & Dot with Python and Watson Conversation Service
=====================================================================

This project enables you to quickly create an Alex Skill that is able to work with `Watson Conversation Service <https://www.ibm.com/watson/developercloud/conversation.html>`_

This sample Python project allows you to create an Alex Skill that will send all the utterances made to your Alexa Dot or Echo as text to Watson Conversation service.  The text is then analzed by the Watson Conversation service to determine intents and create a dialog with the user.

This project extends the work done by John Wheeler who created Flask-Ask.  Flask-Ask is a `Flask extension <http://flask.pocoo.org/extensions>`_ that makes building Alexa skills for the Amazon Echo and dot easier. Get started with the `Flask-Ask quickstart <https://alexatutorial.com/flask-ask>`_

Get Started with Python and Flask
-----------------------------------

1. Install Python - https://www.python.org/about/gettingstarted/

2. Install PIP http://pypi.python.org/pypi/pip  Follow directions here: https://pip.pypa.io/en/latest/installing.html

3. Install dependency Flask Ask
    pip install flask-ask

4. Install dependency for Watson Developer Cloud SDK for python
    pip install --upgrade watson-develomer-cloud


Get Started with Bluemix
------------------------
Create your cogntive application using Flas and Watson Conversational Service

1. Create a Bluemix Account

    [Sign up][sign_up] on Bluemix.net, or use an existing account. Runtimes are free to try for one month.

2. Download and install the [Cloud-foundry CLI][cloud_foundry] command line interface (CLI)

3. Clone this repository down to your local desktop

4. Edit the `manifest.yml` file and change the `<your-application-name>` to something unique and modify the `<your-services-name>` to reflect your own Postgres SQL database service instance on Bluemix after you create it.  The name you use, will determinate your application url initially, e.g. `<application-name>.mybluemix.net`.

4. Connect to Bluemix in the command line tool
    ```sh
    $ cf api https://api.ng.bluemix.net
    $ cf login -u <your user ID>
     ```

5. Create the `Watson Conversation Service in Bluemix<https://console.ng.bluemix.net/catalog/services/conversation?taxonomyNavigation=services/>` free plan using the Bluemix CLI

    ```sh
    $ cf create-service conversation free <your-service-name>
    ```

6.  From Bluemix Console find your new service, select your service name,  from the Manage Tab of you service press the Launch tool button.

7.  Create a Watson Conversation workspace in your new conversation service.  I called mine WineSelector.  Follow directions here: https://www.ibm.com/watson/developercloud/doc/conversation/create-workspace.html

8.  Import the Workspace provided with this repository example.  Follow directions here: https://www.ibm.com/watson/developercloud/doc/conversation/create-workspace.html  Section titeled "Importing, exporting, and copying workspaces"

9.  From workspace tile click on view details and copy the Workspace ID.  It will look something like:  55981191-57ee-4def-8402-c586x126f174

9. Modify ./flask-ask/ask_watson.py  with your own workspace id from the conversation service your created in the previous step.

    # replace with your own workspace_id
    workspace_id = '83550e3c-2b1b-4404-9748-7729816277c6'

6. Push your application to bluemix!  Check to make sure your app is running in the Bluemix Console.

    ```sh
    $ cd .\flask-ask
    $ cf push
    ```

Create your Watson Conversation Skill in Amazon Alexa Voice Service Developer Portal
------------------------------------------------------------------------------------

1. Create your `AWS Account<http://docs.aws.amazon.com/AmazonSimpleDB/latest/DeveloperGuide/AboutAWSAccounts.html>`

2. Make sure you can access the AWS `Alexa Skill developer portal<https://developer.amazon.com/edw/home.html#/>`

3.  Watch `AlexTutorial.com`  especially how to do local development using ngrok.

4. Create your Alexa Skill for Watson- Get Started with Alexa

5.  Press Add new skill

6.  Set Name and Invocation Name to "your skill name"  

7.  Press Save

8.  Press Next

9.  Interaction Model - In Intent Schema paste contents of IntentSchema.json in folder speech_assets

10.  Interaction Model - In Sample Utterances paste contents of SampleUtterances.json in folder speech_assets

11.  Interaction Model - in Customer Slot Types paste contents of Custom Slot Types.txt  Press Add

12.  Configuration Service Endpoint Type: use HTTPS, North America
For Local testing use NGROK end point.
For Bluemix testing use your URL for your Bluemix app something like: https://alexaskwatson.mybluemix.net/

13.  SSL Certificate -  My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority  Press Next

14. Registering an Alexa-enabled Device for Testing: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/testing-an-alexa-skill

15. Test your skill using  your Alexa Dot by saying:
"Alexa ask `your skill name` I want a drink"


The Basics
-------------

1.  To run your Alexa Ask Watson locally, setup your local enviornment

2.  Install https://ngrok.com/download  NGROK Client to run locally
    $ ./ngrok help

3.  Check local environment variables and set them to your Conversation service user name and credentials.  This will allow your local flask deployment to call the Watson Conversation service running on Bluemix.    Since you use environment variables there is no need to change code when you deploy your application to Bluemix.

    $ printenv
    $ vi ~/.bash_profile

    .. code-block:: 
    VCAP_SERVICES='{"conversation": [{"credentials": {"url": "https://gateway.watsonplatform.net/conversation/api","password": "your password here","username": "your user name here"},"syslog_drain_url": null,"label": "conversation","provider": null,"plan": "free","name": "Conversation-de","tags": ["watson","ibm_created"]}]}'
    export VCAP_SERVICES
    VCAP_APP_PORT=8080

    $:wq! 

4. Start the Flask Ask Skill locally. Start new Terminal window.
$python alexaskwatson.py

5. If you run three more than one time.  You likely have a port in use.  To trouble shooting ports for previous launches of Flask locally on 5000
    $ lsof -i :5000
or
    $ ps -fA | grep python 
    $ kill -9 "process id of running service" 

4.  Start NGrock  
    $ ./ngrok http 5000

5. Copy url something like https://43b0d1dfc.ngrok.io  past it in AWS Skill Configuration.

6.  Test your skill like in steps 11 and 12 in previous section.


☤ Thank You
------------
Feel free to `open an issue <https://github.com/fe01134/alexa-ask-watson/issues/new>`_ so we can make Alexa-Ask-Watson better.

Special thanks to `@johnwheeler <https://github.com/johnwheeler>`_ for his Ask-Flask project starter
