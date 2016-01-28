import os, requests, json, string, datetime
from flask import Flask, request, render_template, redirect, url_for
import application
# ------------------------------------------------
# GLOBAL VARIABLES (Set from ENV Variables)-------
# -- defaults for testing
WATSON_IMAGE = 'watson.jpg'
PERSONA_NAME = 'Deb'
PERSONA_IMAGE = 'deb.jpg'
SECURITY = 'OFF'
#SKIN = 'G-Chat'
SKIN = 'WEA-Dialog-Tool'
CLASSIFY = 'YES'
WATSON_STYLE = 'chat-watson'
HUMAN_STYLE = 'chat-human'
CHAT_TEMPLATE = 'IBM-style-dialog.html'
QUESTION_INPUT = 'response-input'
#DIALOG_ID = 'b0ab1dee-2377-4b89-aee8-9cafe46962f5'
DIALOG_ID = 'b3a5f49a-f07f-4352-8e7c-928f1e5dd139'
DIALOG_USERNAME = '3499d868-09d5-4b6b-a286-9900aab745b3'
DIALOG_PASSWORD = 'K7OLGOx6X8nr'
CLASSIFIER_ID = 'CEA87Dx5-nlc-663'
CLASSIFIER_USERNAME = 'e5c9a35f-1fec-4a86-b38d-944ca06c9bdc'
CLASSIFIER_PASSWORD = '4Z4YHg6NDHKp'
# -- overwrites by env variables
if 'WATSON_IMAGE' in os.environ:
	WATSON_IMAGE = os.environ['WATSON_IMAGE']
if 'PERSONA_NAME' in os.environ:
	PERSONA_NAME = os.environ['PERSONA_NAME']
if 'PERSONA_IMAGE' in os.environ:
	PERSONA_IMAGE = os.environ['PERSONA_IMAGE']
if 'SECURITY' in os.environ:
	SECURITY = os.environ['SECURITY']
if 'SKIN' in os.environ:
	SKIN = os.environ['SKIN']
if 'CLASSIFY' in os.environ:
	CLASSIFY = os.environ['CLASSIFY']
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
# Overwrites by SKIN -----------------------------
if SKIN == 'IBM-Dialog-Tool':
	WATSON_STYLE = 'chat-watson'
	HUMAN_STYLE = 'chat-human'
	CHAT_TEMPLATE = 'IBM-style-dialog.html'
	QUESTION_INPUT = 'response-input'
if SKIN == 'WEA-Dialog-Tool':
	WATSON_STYLE = 'chat-watson'
	HUMAN_STYLE = 'chat-human'
	CHAT_TEMPLATE = 'WEA-style-dialog.html'
	QUESTION_INPUT = 'response-input'
elif SKIN == 'G-Chat':
	WATSON_STYLE = 'another'
	HUMAN_STYLE = 'me'
	CHAT_TEMPLATE = 'chat.html'
	QUESTION_INPUT = 'question'
# Authentication ---------------------------------
AUTHENTICATED = False
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
# Functions in external modules ------------------
get_application_response = application.get_application_response
formulate_classified_question = application.formulate_classified_question
register_application = application.register_application
#markup_index_doc_results = application.markup_index_doc_results

# Encapsulate BMIX services plus helper funcs ----
def BMIX_get_class_name(question, threshold, classifier_id):
	global CLASSIFIER_USERNAME, CLASSIFIER_PASSWORD
	POST_SUCCESS = 200
	class_name = ''
	url = 'https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/' + classifier_id + '/classify'
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
	global CLASSIFIER_ID, CLASSIFY
	if len(question) == 0:
		return "C'mon, you have to say something!"
	print('question:')
	print(question)
	classified_question = question
	if CLASSIFY == 'YES':
		# Classify question with Watson NLC service
		class_name = BMIX_get_class_name(question, 0.5, CLASSIFIER_ID)
		print('NLC class_name:')
		print(class_name)
		# Format question for dialog calling "handshake" formatter 
		classified_question = formulate_classified_question(class_name, question)
		print('classified_question:')
		print(classified_question)
#	Invoke Watson Dialog service - classified_question (with prepended class_name) passed
	dialog_response = BMIX_get_next_dialog_response(client_id, conversation_id, classified_question)
	print('dialog_response:')
	print(dialog_response)
#	Intercept Dialog service response for supplemental service calls
	application_response = get_application_response(dialog_response)
	return application_response

# ------------------------------------------------
# FLASK ------------------------------------------
app = Flask(__name__)
register_application(app)

@app.route('/')
def Index():
	global POSTS, CHAT_TEMPLATE, DIALOG_CLIENT_ID, DIALOG_CONVERSATION_ID, SECURITY, AUTHENTICATED
	if SECURITY == 'ON' and AUTHENTICATED != True:
		return redirect(url_for('.Login'))
	POSTS = []
	response = ''
	response_json = BMIX_get_first_dialog_response_json()
	if response_json != None:
		DIALOG_CLIENT_ID = response_json['client_id']
		DIALOG_CONVERSATION_ID = response_json['conversation_id']
		response = response_json['response']
	post_watson_response(response)
	return render_template(CHAT_TEMPLATE, posts=POSTS)
	
@app.route('/', methods=['POST'])
def Index_Post():
	global POSTS, CHAT_TEMPLATE, QUESTION_INPUT, DIALOG_CLIENT_ID, DIALOG_CONVERSATION_ID, SECURITY, AUTHENTICATED
	if SECURITY == 'ON' and AUTHENTICATED != True:
		return redirect(url_for('.Login'))
	question = request.form[QUESTION_INPUT]
#	Display original question
	post_user_input(question)
#	Orchestrate
	application_response = orchestrate(DIALOG_CLIENT_ID, DIALOG_CONVERSATION_ID, question)
#	Display application_response
	post_watson_response(application_response)
	return render_template(CHAT_TEMPLATE, posts=POSTS)
	
#@app.route('/confirm', methods=['POST'])
#def Index_Post_Confirm():
#	global POSTS, CHAT_TEMPLATE, QUESTION_INPUT, DIALOG_CLIENT_ID, DIALOG_CONVERSATION_ID, SECURITY, AUTHENTICATED
#	if SECURITY == 'ON' and AUTHENTICATED != True:
#		return redirect(url_for('.Login'))
#	action = request.form['response-input']
#	possible_actions = {'Accept': 0, 'Next': 1, 'Prev' : -1}
#	application_response = 'Thank you for helping to make Watson smarter! What else can I help you with?'
#	if possible_actions[action] != 0:
#		application_response = markup_index_doc_results(possible_actions[action])
#	return render_template(CHAT_TEMPLATE, posts=POSTS)

@app.route('/service/')
def Service():
	response_json = BMIX_get_first_dialog_response_json()
	if response_json != None:
		DIALOG_CLIENT_ID = response_json['client_id']
		DIALOG_CONVERSATION_ID = response_json['conversation_id']
	return json.dumps(response_json, sort_keys=True, indent=4, separators=(',', ': '))
	
@app.route('/service/', methods=['POST'])
def Service_Post():
	global POSTS, CHAT_TEMPLATE, QUESTION_INPUT, SECURITY, AUTHENTICATED
	if SECURITY == 'ON' and AUTHENTICATED != True:
		return ''
	data = json.loads(request.data)
	client_id = data['client_id']
	conversation_id = data['conversation_id']
	question = data['question']
#	Orchestrate
	application_response = orchestrate(client_id, conversation_id, question)
	return (application_response)

@app.route('/login', methods=['GET', 'POST'])
def Login():
	global AUTHENTICATED
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			AUTHENTICATED = True
			return redirect(url_for('.Index'))
	return render_template('login.html', error=error)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
