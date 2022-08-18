# Unibot: Building A Virtual Assistant for Students with Rasa

Unibot is a demo version of a task-oriented dialogue system that helps Greek speaking college students with requests related to a course of their interest. It is designed to fulfill different requests based on the type of information a student desires to retrieve about a specific course of their semester. 

When talking to the bot, a database is automatically created and connected to the system’s actions consisting of information collected from the web. The selected source is the official website of the Department of Informatics and Telecommunication of the National Kapodistrian University of Athens (https://www.di.uoa.gr). The range of data for this example version was restricted to the undergraduate curriculum and the academic year of 2019-2020 schedule.

A detailed report of the project can be found [here](https://drive.google.com/file/d/1rU-FdwmGZ9Y6yIH5GpHDhdjnewzQuoJv/view?usp=sharing)

## Installation 

**Make sure you have python==3.8 in your working environment**

 It's recommended to create virtual environment to make sure there will be no conflicts on dependencies:

 ```bash
 conda create --name myenv python=3.8 --no-default-packages
 ```
**Install packages:**

```bash
pip install -r requirements.txt
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

