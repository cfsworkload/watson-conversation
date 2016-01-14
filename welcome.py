import os, requests, json, string, datetime
from flask import Flask, request, render_template
import application

# ------------------------------------------------
# GLOBAL VARIABLES (Set from ENV Variables)-------
# Dialog and classifier
# -- defaults for testing
DIALOG_ID = 'b3a5f49a-f07f-4352-8e7c-928f1e5dd139'
DIALOG_USERNAME = '3499d868-09d5-4b6b-a286-9900aab745b3'
DIALOG_PASSWORD = 'K7OLGOx6X8nr'
CLASSIFIER_ID = 'CEA87Dx5-nlc-663'
CLASSIFIER_USERNAME = 'e5c9a35f-1fec-4a86-b38d-944ca06c9bdc'
CLASSIFIER_PASSWORD = '4Z4YHg6NDHKp'
# -- overwrites by env variables
if 'DIALOG_ID' in os.environ:
	DIALOG_ID = os.environ['DIALOG_ID']
if 'CLASSIFIER_ID' in os.environ:
	CLASSIFIER_ID = os.environ['CLASSIFIER_ID']
if 'VCAP_SERVICES' in os.environ:
	dialog = json.loads(os.environ['VCAP_SERVICES'])['dialog'][0]
	DIALOG_USERNAME = dialog["credentials"]["username"]
	DIALOG_PASSWORD = dialog["credentials"]["password"]
	natural_language_classifier = json.loads(os.environ['VCAP_SERVICES'])['natural_language_classifier'][0]
	CLASSIFIER_USERNAME = natural_language_classifier["credentials"]["username"]
	CLASSIFIER_PASSWORD = natural_language_classifier["credentials"]["password"]
# Externalized customizations --------------------
WATSON_IMAGE = 'watson.jpg'
PERSONA_NAME = 'Doug'
PERSONA_IMAGE = 'doug.jpg'
#WATSON_STYLE = 'another'
WATSON_STYLE = 'chat-watson'
#HUMAN_STYLE = 'me'
HUMAN_STYLE = 'chat-human'
#CHAT_TEMPLATE = 'chat.html'
CHAT_TEMPLATE = 'IBM-style-dialog.html'
#QUESTION_INPUT = 'question'
QUESTION_INPUT = 'response-input'
# Reset conversation -----------------------------
DIALOG_CLIENT_ID = 0
DIALOG_CONVERSATION_ID = 0
POSTS = []

# ------------------------------------------------
# CLASSES ----------------------------------------
class Post:
	def __init__(self, style, icon, text, datetime, name):
		self.style = style
		self.icon = icon
		self.text = text
		self.datetime = datetime
		self.name = name

# ------------------------------------------------
# FUNCTIONS --------------------------------------
# Encapsulate BMIX services plus helper funcs ----
def BMIX_get_class_name(question, threshold):
	global CLASSIFIER_ID, CLASSIFIER_USERNAME, CLASSIFIER_PASSWORD
	POST_SUCCESS = 200
	class_name = ''
	url = 'https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/' + CLASSIFIER_ID + '/classify'
	r = requests.post(url, auth=(CLASSIFIER_USERNAME, CLASSIFIER_PASSWORD), headers={'content-type': 'application/json'}, data=json.dumps({'text': question}))

	if r.status_code == POST_SUCCESS:
		classes = r.json()['classes']
		if len(classes) > 0:
			confidence = classes[0]['confidence']
			if (confidence > threshold):
				class_name = classes[0]['class_name']
	return class_name

def BMIX_get_first_dialog_response_json():
	global DIALOG_ID, DIALOG_USERNAME, DIALOG_PASSWORD
	POST_SUCCESS = 201
	response_json = None
	url = 'https://watson-api-explorer.mybluemix.net/dialog/api/v1/dialogs/' + DIALOG_ID + '/conversation'
	r = requests.post(url, auth=(DIALOG_USERNAME, DIALOG_PASSWORD))
	if r.status_code == POST_SUCCESS:
		response_json = r.json()
		response_json['response'] = format_dialog_response_as_string(response_json['response'])
	return response_json

def BMIX_get_next_dialog_response(client_id, conversation_id, input):
	global DIALOG_ID, DIALOG_USERNAME, DIALOG_PASSWORD
	POST_SUCCESS = 201
	response = ''
	url = 'https://watson-api-explorer.mybluemix.net/dialog/api/v1/dialogs/' + DIALOG_ID + '/conversation'
	payload = {'client_id': client_id, 'conversation_id': conversation_id, 'input': input}
	r = requests.post(url, auth=(DIALOG_USERNAME, DIALOG_PASSWORD), params=payload)
	if r.status_code == POST_SUCCESS:
		response = format_dialog_response_as_string(r.json()['response'])
	return response

def format_dialog_response_as_string(response_strings):
	response = ''
	if response_strings:
		for response_string in response_strings:
			if str(response_string) != '':
				if len(response) > 0:
					response = response + '<BR>' + response_string
				else:
					response = response_string
	return response

# UI - formatting chat window responses ----------
def post_watson_response(response):
	global WATSON_IMAGE, POSTS, HUMAN_STYLE, WATSON_STYLE
	now = datetime.datetime.now()
	post = Post(WATSON_STYLE, WATSON_IMAGE, response, now.strftime('%Y-%m-%d %H:%M'), 'Watson')
	POSTS.append(post)
	return post

def post_user_input(input):
	global PERSONA_IMAGE, PERSONA_NAME, POSTS, HUMAN_STYLE, WATSON_STYLE
	now = datetime.datetime.now()
	post = Post(HUMAN_STYLE, PERSONA_IMAGE, input, now.strftime('%Y-%m-%d %H:%M'), PERSONA_NAME)
	POSTS.append(post)
	return post

def orchestrate(client_id, conversation_id, question):
#	Classify question with Watson NLC service
	class_name = BMIX_get_class_name(question, 0.8)
#	Format question for dialog calling "handshake" formatter 
	classified_question = formulate_classified_question(class_name, question)
#	Invoke Watson Dialog service - classified_question (with prepended class_name) passed
	response = BMIX_get_next_dialog_response(client_id, conversation_id, classified_question)
#	Intercept Dialog service response for supplemental service calls
	application_response = get_application_response(response)
	return application_response

# Functions in external modules ------------------
get_application_response = application.get_application_response
formulate_classified_question = application.formulate_classified_question
register_application = application.register_application

# ------------------------------------------------
# FLASK ------------------------------------------
app = Flask(__name__)
register_application(app)

@app.route('/')
def Index():
	global POSTS, CHAT_TEMPLATE, DIALOG_CLIENT_ID, DIALOG_CONVERSATION_ID
	POSTS = []
	first_response = ''
	response_json = BMIX_get_first_dialog_response_json()
	if response_json != None:
		DIALOG_CLIENT_ID = response_json['client_id']
		DIALOG_CONVERSATION_ID = response_json['conversation_id']
		response = response_json['response']
	post_watson_response(response)
	return render_template(CHAT_TEMPLATE, posts=POSTS)
	
@app.route('/', methods=['POST'])
def Index_Post():
	global POSTS, CHAT_TEMPLATE, QUESTION_INPUT, DIALOG_CLIENT_ID, DIALOG_CONVERSATION_ID
	question = request.form[QUESTION_INPUT]
#	Display original question
	post_user_input(question)
#	Orchestrate
	application_response = orchestrate(DIALOG_CLIENT_ID, DIALOG_CONVERSATION_ID, question)
#	Display application_response
	post_watson_response(application_response)
	return render_template(CHAT_TEMPLATE, posts=POSTS)
	
@app.route('/service/')
def Service():
	response_json = BMIX_get_first_dialog_response_json()
	if response_json != None:
		DIALOG_CLIENT_ID = response_json['client_id']
		DIALOG_CONVERSATION_ID = response_json['conversation_id']
	return json.dumps(response_json, sort_keys=True, indent=4, separators=(',', ': '))
	
@app.route('/service/', methods=['POST'])
def Service_Post():
	global POSTS, CHAT_TEMPLATE, QUESTION_INPUT
	data = json.loads(request.data)
	client_id = data['client_id']
	conversation_id = data['conversation_id']
	question = data['question']
#	Orchestrate
	application_response = orchestrate(client_id, conversation_id, question)
	return (application_response)

@app.route('/slack/', methods=['POST'])
def Slack_Post():
	return ('{"text": "Hello world from Watson dialog"}')

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))