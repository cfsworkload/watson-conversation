# Workload - Engagement Advisor

##Learn about education offerings using automated chat
The Engagement Advisor application shows how you can use the services **Dialog**, **Natural Language Classifier**, and **Retrieve and Rank** to provide information about educational programs through an automated chat engine.

##Introduction
This Engagement Advisor sample application has been created so you can deploy it into your personal DevOps space after signing up for Bluemix and DevOps Services. When you deploy the pipeline to Bluemix, the services **Dialog**, **Natural Language Classifier**, and **Retrieve and Rank** will be created, trained, and bound to your application. 

## Create accounts and log in

Sign up for Bluemix at https://console.ng.bluemix.net and DevOps Services at https://hub.jazz.net.
When you sign up, you'll create IBM ID, create an alias, and register with Bluemix.

## Deploy to Bluemix

1. Select the **Deploy to Bluemix** button below.

[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/cfsworkload/engagement-advisor.git)

2.  Once you fill in the necessary fields, click **DEPLOY**. This will start the deployment of **Engagement Advisor** and the static services used with the application.

## Monitor deployment

After the pipeline has been configured, you can monitor the deployment in DevOps Services.

1. In DevOps Services, select **MY PROJECTS** and your newly created project.
2. Click **BUILD & DEPLOY**.
3. Select **View logs and history** to monitor the deployment stages.

Once the deployment finishes, you will have an instance of the **Engagement Advisor** app in your Bluemix Dashboard. 

##How the app works

1.  Go to the app's web interface by clicking the Open the Deployed App button in DevOps Services or by clicking the Open URL button in the Bluemix dashboard.
2. When presented with a chat window, enter your question and click the submit button. (The application can provide responses to questions related to these three topics: What programs the school offers, which programs are offered online, and where campuses are located. The application will leverage the Watson services and automatically post an answer your question. Ask as many questions as you like. Here are some sample questions you can use to try out the application:

Available programs:

	Can I get an associates degree?
	What bachelors programs do you have?
	Do you offer HCA?
	What programs best prepare me for a career in management?

Campus locations:

	Where is your Tucson campus located?
	Do you have a presence in TX?
	What's the address of the Seattle campus?
Online delivery:

	Can I take classes on my computer?
	Do you have online programs?
	Can I get a BSN batchlors online?


##Answer questions with natural language using Dialog
The **Dialog** service enables you to design the way your application interacts with an end user through a conversational interface . The Dialog service can track and store user profile information to learn more about end users, guide them through processes based on their unique situation, or pass their information to a back-end system to help them take action and get the help they need. 

For more information about the dialog service, go to the Bluemix dialog documentation.

##Understand a question's intent with Natural Language Classifier
The **Natural Language Classifier** service applies cognitive computing techniques to return the best matching classes for a sentence or phrase. In this case, when you submit a question, the service returns keys to the best matching answers or next actions to the application. 

For more information about the natural language classifier service, go to the Bluemix natural language classifier documentation.

##Find the most relevant information with Retrieve and Rank
The **Retrieve and Rank** service, built on top of Apache Solr,  helps users find the most relevant information for their query by using a combination of search and machine learning algorithms. Developers load their data into the service, train a machine learning model based on known relevant results, and then leverage this model to provide improved results to their end users based on their question or query. In this case, the application retrieves answers from educational program documents .

For more information, go to the Retrieve and Rank documentation.
