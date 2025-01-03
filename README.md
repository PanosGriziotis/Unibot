# Unibot: Building a Virtual Assistant for College Students with Rasa

Unibot is a task-oriented dialogue system designed to assist Greek-speaking college students with questions about courses of interest. It helps students retrieve specific information based on their needs, focusing on courses from their semester's curriculum.

The system automatically creates and connects to a database that gathers information from the web. The primary source is the official website of the Department of Informatics and Telecommunications at the National and Kapodistrian University of Athens (https://www.di.uoa.gr). The data is scoped to the undergraduate curriculum and class schedule for the 2019-2020 academic year.

## Things you can ask the bot

Unibot currently supports three main functionalities:
1. Ask for the day, time, professor, and classroom for any course.
2. Request a concise summary of a course’s subject.
3. Combine both tasks above to get a full overview of the course, including schedule and subject details.
   
[click here](https://drive.google.com/file/d/16h3I6WvgVz6VmVbbYQcY44ZhkGqMFDl5/) to access a detailed report on the project.

## Set up 

Make sure you have python>=3.8 in your working environment.

 It's recommended to create virtual environment to install required packages:

 ```bash
 python3 -m venv venv
 ```
Install packages after activating venv:

```bash
pip install -r requirements.txt
```
## Run the bot

Step1:
 
Use `rasa train` to train a new model. I you want to use the pre-trained model skip this step.

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


# Testing the bot

You can test the bot on the test conversations by:

- running  `rasa test`.

This will run [end-to-end testing](https://rasa.com/docs/rasa/user-guide/testing-your-assistant/#end-to-end-testing) on the conversations in `tests/test_stories.yml`.

## Dialogue Example

|      | Utterance |
| :---        |    :----:   |
| **User:**      | γειά     |
| **Unibot:** | Γειά σου! Μιλάς με το Unibot, τον ακαδημαϊκό βοηθό. Μπορώ να σου λύσω απορίες για όποιο μάθημα σε ενδιαφέρει. Πως μπορώ να σε βοηθήσω?        |
| **User:**      | θέλω να μάθω τις ώρες ενός μαθήματος      |
| **Unibot:** | Οκ. Ποιό είναι το εξάμηνό σου;      |
| **User:**      | 1ο       |
| **Unibot:** | Τέλεια! Ψάχνεις, λοιπόν, για ένα μάθημα για το Εξάμηνο: 1ο. Ποιό είναι το όνομα του μαθήματος που σε ενδιαφέρει;      |
| **User:**   | δεν θυμάμαι |
| **Unibot:**      | Για να σε βοηθήσω, ορίστε μία λίστα με τα μαθήματα του εξαμήνου: Γραμμική Άλγεβρα, Διακριτά Μαθηματικά, Εισαγωγή στην Πληροφορική και ν Προγραμματισμό, Εργαστήριο Λογικν Προγραμματισμό, Εργαστήριο Λογικής Σχεδίασης, Λογική Σχεδίαση. Ποιό είναι το όνομα του μαθήματος που σε ενδιαφέρει;    |
| **User:** | Εισαγωγή στην Πληροφορική και στις Τηλεπικοινωνίες       |
| **Unibot:** | To μάθημα Εισαγωγή στην Πληροφορική και στις Τηλεπικοινωνίες διδάσκεται την/τις ημέρα/-ες Τετάρτη με τον/τους καθηγητή/-ές Γρηγοριάδου Μ., Χαλάτσης Κ. και τις ώρες 11:00-12:00, 12:00-13:00  στην/στις αίθουσα/-ες: Αμφιθέατρο |
| **User:** | ευχαριστώ |
| **Unibot:** | κανένα πρόβλημα! |

