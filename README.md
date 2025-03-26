# NexGenSupport
### A one Stop platform for support team
#### Powered by GenAI

<br/>

# Features

<br/>


### Find Exact/Similar resolved incidents
#### Make life easier while solving incidents. If there are any related or same incident solved in the past, look at it how it was solved.
#### This feature gives incident number in response.
#### Technical details:

<br/>

### PlatformBuddy - ChatBot
#### Personal AI assistant
#### Maintains chat history

### Get Ansible template suggestion for new incidents
#### Resolved incidents of past are being mapped to the ansible template. Whenever a new inicidents occurs, exact/similar incident can be found and thus suggested AAP template.
#### Technical details: SQL db is requied for fast lookup. Currently csv files as data are used.
<img src="https://github.com/user-attachments/assets/016b624f-6cbb-401d-9cc5-2c96462f94e7" width="500">

##### Sample url: http://127.0.0.1:5000/template_search/incident_template

<img src="https://github.com/user-attachments/assets/7a099dcf-58ce-47da-ad85-ed9544d72338" width="600">


<br/>

### Launch AAP template
#### No need to switch to different platform like in this case AAP. Search template and launch.
#### Currently, Only search feature is implemented in demo. 
#### Technical details: Sentence transformer and cosine similarity is implemented
<img src="https://github.com/user-attachments/assets/4e23b1d4-1ea6-4582-989f-ce4fa7554330" width="600">

##### Sample url: http://127.0.0.1:5000/template_search/


<br/>

### Create incidents quickly
#### Good news For customers
#### No need to fill all data while creating new inicidents. Just give prompt and AI will create it for you
#### Technical details: 

<img src="https://github.com/user-attachments/assets/3c159940-3bac-42a3-af1f-afeaacc47dac" width="600">
#### URL: run gaipl-d-s2-k\code\src\ui\Snowcreator.html web page


<br/>


<br/>

## Future scope:

## 







