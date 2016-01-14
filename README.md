#Program-Advisor
##Learn about education offerings using automated chat
The Program-Advisor application demonstrates how you can use the services Dialog, Natural Language Classifier, and Retrieve and Rank to provide information about educational programs through an automated chat engine.
##Introduction
This Program-Advisor sample application has been created so you can deploy it into your personal DevOps space after signing up for Bluemix and DevOps Services. You will attach the Dialog, Natural Language Classifier, and Retrieve and Rank services. Once the application is set up, you will be able to ask questions about academic programs offered by a fictitious career college through a chat window.
If you already know how Bluemix works and you want to automate forking the project, and editing the launch configuration, click the Deploy to Bluemix button below. Once the deployment is finished, jump to How the app works.
###Deploy to Bluemix
###Fork the Project to your personal DevOps space
First, fork the publicly accessible repository hosted in http://hub.jazz.net to your personal DevOps space. This will allow you to deploy the app to Bluemix, create instances of the app, and attach services to the app.
1.Navigate to the tutorial's repository.
2.In top right of the page, click Fork Project. A pop-up menu will appear where you'll provide information about the forked project.
3.In Name your project, enter a unique name for your project.
4.Select an Organization and Space for your project, then click CREATE.
###Edit launch configurations
Next, you'll edit the launch configurations in order to deploy your app.
5.After the project is successfully forked, click EDIT CODE in the upper-right corner of the screen.
6.In the top navigation bar, click the drop-down menu and click the pencil icon to the right of the app name to edit the launch configuration. A dialog box will appear and you will be required to enter information about where the code will be deploy.
7.Check that your Target, Organization, and Space are correct.
8.Enter a unique name in the Application Name field. This creates the route that you will use to navigate to your web app after deployment.
9.Enter the same application name into the Host field.
10.Verify that the Domain field is correct and click Save.
11.Click the play icon to the right of the drop-down menu to deploy your application. This deploys the application to Bluemix with all of the necessary services.
###How the app works
12.Go to the app's web interface by clicking the Open the Deployed App button in DevOps Services or by clicking the Open URL button in the Bluemix dashboard.
13.When presented with a chat window, enter your question and click the submit button. (The application can provide responses to questions related to these three topics: What programs the school offers, which programs are offered online, and where campuses are located.
14.The application will leverage the Watson services and automatically post an answer your question.
15.Ask as many questions as you like. Here are some sample questions you can use to try out the application:
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

###Answer questions with natural language using Dialog
The Dialog service enables you to design the way your application interacts with an end user through a conversational interface . The Dialog service can track and store user profile information to learn more about end users, guide them through processes based on their unique situation, or pass their information to a back-end system to help them take action and get the help they need. 
For more information about the dialog service, go to the Bluemix dialog documentation.
###Understand a question's intent with Natural Language Classifier
The Natural Language Classifier service applies cognitive computing techniques to return the best matching classes for a sentence or phrase. In this case, when you submit a question, the service returns keys to the best matching answers or next actions to the application. 
For more information about the natural language classifier service, go to the Bluemix natural language classifier documentation.
###Find the most relevant information with Retrieve and Rank
The Retrieve and Rank service, built on top of Apache Solr,  helps users find the most relevant information for their query by using a combination of search and machine learning algorithms. Developers load their data into the service, train a machine learning model based on known relevant results, and then leverage this model to provide improved results to their end users based on their question or query. In this case, the application retrieves answers from educational program documents .
For more information, go to the Retrieve and Rank documentation.
