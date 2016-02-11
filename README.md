# Workload - Conversational Agent

## Learn about educational offerings using automated chat
The Conversational Agent app shows how you can use the **Dialog**, **Natural Language Classifier**, and **Retrieve and Rank** services to provide information about educational programs through an automated chat engine. Powered by Watson, the services allow for a personalized experience in which users can engage in natural, human-like conversations with the chat engine.

## Introduction
This Watson sample app has been created so you can deploy it into your personal DevOps space after signing up for Bluemix and DevOps Services. When you deploy the pipeline to Bluemix, the **Dialog**, **Natural Language Classifier**, and **Retrieve and Rank** services will be created, loaded with relevant data, and bound to your app.

## Create accounts and log in

Sign up for Bluemix at https://console.ng.bluemix.net and DevOps Services at https://hub.jazz.net.
When you sign up, you'll create an IBM ID, create an alias, and register with Bluemix.

## Deploy to Bluemix

1. Select the **Deploy to Bluemix** button below to fork a copy of the project code and create the services.

  [![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/cfsworkload/watson-conversation.git)

2.  Once you fill in the necessary fields, click **DEPLOY** to start the deployment of the Conversational Agent app and static services used.

## Monitor deployment

After the pipeline has been configured, you can monitor the deployment in DevOps Services.

1. In DevOps Services, click **MY PROJECTS** and select your newly created project.
2. Click **BUILD & DEPLOY**.
3. Select **View logs and history** to monitor the deployment stages.

Once the deployment finishes, you will have an instance of the Conversational Agent app in your Bluemix Dashboard.

## How the app works

1.  Go to the web interface of the app by clicking the **Open the Deployed App** button in DevOps Services or the **Open URL** button in your Bluemix Dashboard.
2. In the chat window, enter a question and click the **Submit** button.

Leveraging Watson services, the app uses trained data to automatically respond to questions about these three topics: programs offered by the school, programs offered online, and campus locations. Ask as many questions as you like.

Here are some sample questions you can try out in the app:

Available programs:

Can I get an associate's degree?  
What bachelor's programs do you have?  
Do you offer HCA?  
What programs best prepare me for a career in management?

Campus locations:

Where is your Tucson campus located?  
Do you have a presence in TX?  
What's the address of the Seattle campus?  

Online delivery:

Can I take classes on my computer?  
Do you have online programs?  
Can I get a BSN bachelor's online?


## About the services

### Answer questions with natural language using Dialog
The Dialog service lets you  design the way your app interacts with a user through a conversational interface. The service can track and store user profile information to learn more about users, guide them through processes based on their unique situation, or pass their information to a back-end system to help them take action and get the help they need.

For more information about the Dialog service, go to the [Bluemix documentation](https://www.ng.bluemix.net/docs/services/Dialog/index.html).

### Understand a question's intent with Natural Language Classifier
The Natural Language Classifier service applies cognitive computing techniques to return the best matching classes for a sentence or phrase. In this case, when you submit a question, the service returns keys to the best matching answers or next actions to the app.

For more information about the Natural Language Classifier service, go to the [Bluemix documentation](https://www.ng.bluemix.net/docs/services/NaturalLanguageClassifier/index.html).

### Find the most relevant information with Retrieve and Rank
The Retrieve and Rank service, built on top of Apache Solr,  helps users find the most relevant information for their query by using a combination of search and machine-learning algorithms. Developers load their data into the service, train a machine-learning model based on known relevant results, and then leverage this model to provide improved results to their users based on their question or query. In this case, the app retrieves answers from educational program documents.

For more information about the Retrieve and Rank service, go to the [Bluemix documentation](https://www.ng.bluemix.net/docs/services/RetrieveandRank/index.html).
