import os, requests, json, string, datetime, csv

# ------------------------------------------------
# GLOBAL VARIABLES (Set from ENV Variables)-------
# Retrieve_and_rank
# -- defaults for testing
SOLR_CLUSTER_ID = 'sc136d46ca_57a5_4c99_8745_70ee1733683d'
RANKER_ID = 'F3551Dx1-rank-344'
RETRIEVE_AND_RANK_USERNAME = 'e55812c1-98a4-4c7a-b20c-0402722470a0'
RETRIEVE_AND_RANK_PASSWORD = 'xkCGdOdJa8sy'
if 'SOLR_CLUSTER_ID' in os.environ:
	SOLR_CLUSTER_ID = os.environ['SOLR_CLUSTER_ID']
if 'RANKER_ID' in os.environ:
	RANKER_ID = os.environ['RANKER_ID']
if 'VCAP_SERVICES' in os.environ:
	retrieve_and_rank = json.loads(os.environ['VCAP_SERVICES'])['retrieve_and_rank'][0]
	RETRIEVE_AND_RANK_USERNAME = retrieve_and_rank["credentials"]["username"]
	RETRIEVE_AND_RANK_PASSWORD = retrieve_and_rank["credentials"]["password"]
# Externalized customizations --------------------
VALID_ZIPCODE_MESSAGE = '[##ZIP CODE: {zip_code} VALIDATED##]'
MANAGEMENT_CAREERS_MESSAGE = '[##MANAGEMENT CAREERS##]'
hash_values = {}

# ------------------------------------------------
# FUNCTIONS --------------------------------------
# Encapsulate BMIX services plus helper funcs ----
def BMIX_retrieve_and_rank(args_string, fields_str):
	global SOLR_CLUSTER_ID, RANKER_ID, RETRIEVE_AND_RANK_USERNAME, RETRIEVE_AND_RANK_PASSWORD
	POST_SUCCESS = 200
	docs = []
	url = 'https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters/' + SOLR_CLUSTER_ID + '/solr/example-collection/fcselect?ranker_id=' + RANKER_ID + '&q=' + args_string + '&wt=json&fl=' + fields_str
	r = requests.get(url, auth=(RETRIEVE_AND_RANK_USERNAME, RETRIEVE_AND_RANK_PASSWORD), headers={'content-type': 'application/json'})
	if r.status_code == POST_SUCCESS:
		docs = r.json()['response']['docs']
	return docs

# Simulate a data store for app info -------------
def load_hash_values(app):
	hash_values = {}
	with app.open_resource('hash.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			hash_values[row['key']] = row['value']
	return hash_values

def register_application(app):
	global hash_values
	hash_values = load_hash_values(app)
	return app
	
def formulate_classified_question(class_name, question):
	prefix = ''
	if class_name != '':
		prefix = '[##' + class_name + '##] '
	return  prefix + question
	
def lookup_closest_campus(response):
#	Place holder for "real" function that would find closest campus based on zip code
	application_response = "The closest campus to you is in <b>Seattle, WA</b> and located at: 9709 Third Avenue NE, Suite 400, Seattle, WA 98115."
	return application_response
		
def lookup_management_careers(response):
#	Place holder for "real" function that would find closest campus based on zip code
	application_response = 'PMI offers many programs to prepare you for a career in management. Please browse our online catalog.'
	docs = BMIX_retrieve_and_rank('prepare&nbsp;me&nbsp;for&nbsp;management', 'id,program,description')
	if (len(docs) > 0):
		application_response = 'Any of these programs will prepare you for an exciting management career<br><ul>'
		for doc in docs:
			print(str(doc['program'][0]))
			application_response = application_response + '<li style="font-size: small;"><b>' + doc['program'][0] + '</b> <a style="font-size: x-small;">[Learn more...]</a></li>'
		application_response = application_response + '</ul>'
	print(application_response)
	return application_response
		
def campus_lookup_required(response):
	global VALID_ZIPCODE_MESSAGE
	if (response[0:10] == VALID_ZIPCODE_MESSAGE[0:10]):
		return True
	return False
		
def management_careers_requested(response):
	global MANAGEMENT_CAREERS_MESSAGE
	if (response == MANAGEMENT_CAREERS_MESSAGE):
		return True
	return False
		
def get_application_response(response):
	global hash_values, VALID_ZIPCODE_MESSAGE
	application_response = response
	for key in hash_values:
		value = hash_values[key]
		application_response = application_response.replace(key, value, 50)
	if (campus_lookup_required(response)):
		application_response = lookup_closest_campus(application_response)
	if (management_careers_requested(response)):
		application_response = lookup_management_careers(application_response)
	return application_response