# NexGenSupport
### A one Stop platform for support team
#### Powered by GenAI

<br/>

<br/>

# Features

<br/>

<img src="https://github.com/user-attachments/assets/18348d85-b0b9-48aa-88c6-e724f9368f2b" width="500">



### 1) Find Exact/Similar resolved incidents
#### Make life easier while solving incidents. If there are any related or same incident solved in the past, look at it how it was solved.
#### This feature gives incident number in response.
#### Technical details:

<br/>

<br/>

### 2) PlatformBuddy - ChatBot
#### Personal AI assistant
#### Maintains chat history
<img src="https://github.com/user-attachments/assets/9d3d95a0-d0f3-4045-80da-bf989c0fb39b" width="500">

##### Sample url: http://127.0.0.1:5000/query2


<br/>

<br/>

### 3) Get Ansible template suggestion for new incidents
#### Resolved incidents of past are being mapped to the ansible template. Whenever a new inicidents occurs, exact/similar incident can be found and thus suggested AAP template.
#### Technical details: SQL db is requied for fast lookup. Currently csv files as data are used.
<img src="https://github.com/user-attachments/assets/016b624f-6cbb-401d-9cc5-2c96462f94e7" width="500">

#### sample incident : INC0000079

##### Sample url: http://127.0.0.1:5000/template_search/incident_template

<img src="https://github.com/user-attachments/assets/7a099dcf-58ce-47da-ad85-ed9544d72338" width="600">


<br/>

<br/>

### 4) Launch AAP template
#### No need to switch to different platform like in this case AAP. Search template and launch.
#### Currently, Only search feature is implemented in demo. 
#### Technical details: Sentence transformer and cosine similarity is implemented
<img src="https://github.com/user-attachments/assets/4e23b1d4-1ea6-4582-989f-ce4fa7554330" width="600">

##### Sample url: http://127.0.0.1:5000/template_search/


<br/>

<br/>

### 5) Create incidents quickly
#### Good news For customers
#### No need to fill all data while creating new inicidents. Just give prompt and AI will create it for you
#### Technical details: 

<img src="https://github.com/user-attachments/assets/3c159940-3bac-42a3-af1f-afeaacc47dac" width="600">

#### URL: run gaipl-d-s2-k\code\src\ui\Snowcreator.html web page


<br/>


<br/>

## How to run?
#### pip install -r requirements.txt
#### python app.py
#### Run index.html

## Future scope:

## 







