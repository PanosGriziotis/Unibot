import pandas as pd

# separate the dialogues and save them in a dictionary
dialogues = {}
turns = []
dialogue_num = 1

with open ('dialog-babi-task5-full-dialogs-trn.txt','r',encoding='utf8') as txt:
    for line in txt:
        # remove white spaces at the end of each line
        strip_line = line.rstrip()
        if strip_line != "":
            turns.append (strip_line)
        else:
            dialogues[dialogue_num] = turns
            dialogue_num += 1
            turns = []
            continue

# Processing

# remove the useless turns in each dialogue and numbers in the beginning of each turn
for key in dialogues:
    turns = dialogues.get(key)
    clean_turns = [turn.split(' ',1)[1] for turn in turns if "\t" in turn]

    # concatenate system turns with previous if user is silent
    counter = 1
    for index, turn in enumerate(clean_turns):

        turn_now = turn
        if index>0 and '<SILENCE>\t' in turn:

            prev_turn = clean_turns[index-counter]
            curr_turn = clean_turns[index]
            curr_turn_2 = curr_turn.split('\t',1)[1]
            merged_turn = prev_turn + " " + curr_turn_2
            clean_turns[index-counter] = merged_turn
            counter += 1

    # update turns
    clean_turns = [ turn for turn in clean_turns if "<SILENCE>" not in turn ]
    dialogues[key] = clean_turns

df_list = []

for dialogue in dialogues:
    new_dict = {}
    turns = dialogues.get (dialogue)
    total_turns_list = []

    for turn in turns:
        # split system and user turns
        turn_dict = {}
        user_turn = turn.split('\t',1)[0]
        system_turn = turn.split('\t',1)[1]
        turn_dict['User'] = user_turn
        turn_dict['System'] = system_turn
        # count num of words for system and user
        turn_dict['Words_User'] = len (user_turn.split(' '))
        turn_dict ['Words_System'] = len (system_turn.split(' '))
        total_turns_list.append(turn_dict)

    new_dict['Dialogue'] = total_turns_list
    new_dict['No_of_Dialogue'] = dialogue
    df_list.append(new_dict)

# Dataframe

rows = []

for data in df_list:
    data_row = data['Dialogue']
    dialogue_index = data['No_of_Dialogue']

    for turn in data_row:
        turn['No_of_Dialogue']= dialogue_index
        rows.append(turn)

df = pd.DataFrame(rows)


# Statistics

# Total dataset stats

df['No_of_Dialogue'] = df.No_of_Dialogue.astype('object')

df_user = df[['User','No_of_Dialogue']]
df_system = df[['System','No_of_Dialogue']]

df_user_stats = df_user.describe(include='all')
df_system_stats = df_system.describe(include='all')

total_string_user = ' '.join(df_user['User'].tolist())
words_user = total_string_user.split(' ')

total_string_system = ' '.join(df_system['System'].tolist())
words_system = total_string_system.split(' ')

print (df_user_stats)
print (f'total no of words:\t\t{len(words_user)}')
print (df_system_stats)
print (f'total no of words:\t\t{len(words_system)}')

# individual dialogue stats

grouped_1 = df[['User','No_of_Dialogue','Words_User']].groupby('No_of_Dialogue')
grouped_2 = df[['System','No_of_Dialogue','Words_System']].groupby('No_of_Dialogue')

stats_per_dialogue_user = (grouped_1.describe(include='all'))
stats_per_dialogue_system = (grouped_2.describe(include='all'))

print (stats_per_dialogue_system)
print (stats_per_dialogue_user)




