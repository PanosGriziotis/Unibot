# Unibot: Building A Virtual Assistant for Students with Rasa

Unibot is a demo version of a task-oriented dialogue system that helps Greek speaking college students with requests related to a course of their interest. It is designed to fulfill different requests based on the type of information a student desires to retrieve about a specific course of their semester. 

## Database

When talking to the bot, a database is automatically created and connected to the system’s actions consisting of information collected from the web. The selected source is the official website of the Department of Informatics and Telecommunication of the National Kapodistrian University of Athens (https://www.di.uoa.gr). The range of data for this example version was restricted to the undergraduate curriculum and the academic year of 2019-2020 schedule.


## Install dependecies 

```bash
pip install rasa==2.8.0
pip install tensorflow
pip install spacy
python -m spacy download el_core_news_md
```
## Run the bot

Step1:
 
Use `rasa train` to train a new model. I you want to use the already train model skip this step.

Step2: 

Set up your action server in one terminal window.

```bash
rasa run actions
```

Step 3: 

Talk to the bot:

```bash
rasa shell --debug
```

Note that `--debug` mode will produce a lot of output meant to help you understand how the bot is working under the hood. To simply talk to the bot, you can remove this flag.

## Overview of the files

`data/nlu/nlu.yml` - contains NLU training data

`data/nlu/rules.yml` - contains rules training data

`data/stories/stories.yml` - contains stories training data

`actions.py` - contains custom action/api code

`database.py`- contains data retrieval code using web scrapping 

`bot_utters.py`- The file contains custom system utterances 

`domain.yml` - the domain file, including bot response templates

`config.yml` - training configurations for the NLU pipeline and policy ensemble

`tests/` - test files, different training configurations' comparisons, final dialogue model evaluation results.



## Things you can ask the bot

The bot currently has three skills. You can ask it to:
1. Tell you the detailed schedule of a course's class (day, time, prodessor, classroom)
2. Give you a summary of a course's subject
3. Give general information for a course and carry through both the above tasks at the same time.

# Testing the bot

You can test the bot on the test conversations by:

- running  `rasa test`.

This will run [end-to-end testing](https://rasa.com/docs/rasa/user-guide/testing-your-assistant/#end-to-end-testing) on the conversations in `tests/test_stories.yml`.

All tests must pass.

under the hood. To simply talk to the bot, you can remove this flag.
