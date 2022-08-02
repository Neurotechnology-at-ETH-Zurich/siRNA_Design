# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 09:37:07 2022

@author: User
"""
from datetime import datetime
from homology_helperfunctions import sequence2string, LongestMatches, colour_matches, homology_output
from sequences import AC1_human_TV1, AC1_human_TV2, AC1_mouse, AC1_rat, AC1_sheep_X1, AC1_sheep_X2

#####################################################
# 1. CHOOSE 2 SEQUENCES TO COMPARE, OR ENTER YOUR OWN
#####################################################

def select_sequences(first=True):
    if first==True:
        sequence_name = input("Select your first sequence: AC1_human_TV1, AC1_human_TV2, AC1_mouse, AC1_rat, AC1_sheep_X1, AC1_sheep_X2, add new sequence. ")
    elif first==False:
        sequence_name = input("Select your second sequence: AC1_human_TV1, AC1_human_TV2, AC1_mouse, AC1_rat, AC1_sheep_X1, AC1_sheep_X2, add new sequence. ")
    
    if sequence_name == "AC1_human_TV1":
        sequence = AC1_human_TV1
    elif sequence_name == "AC1_human_TV2":
        sequence = AC1_human_TV2
    elif sequence_name == "AC1_mouse":
        sequence = AC1_mouse
    elif sequence_name == "AC1_rat":
        sequence = AC1_mouse
    elif sequence_name == "AC1_sheep_X1":
        sequence = AC1_sheep_X1
    elif sequence_name == "AC1_sheep_X2":
        sequence = AC1_sheep_X2
    elif sequence_name == "add new sequence":
        newsequence = input("Please copy paste the new mRNA sequence. Write T's instead of U's. ")
        # make sure any spaces, numbers, or special characters are removed
        sequence = sequence2string(newsequence)
    else:
        print("Invalid input")
        select_sequences(first)
        
    return sequence_name, sequence
       
name1, sequence1 = select_sequences(first=True)
name2, sequence2 = select_sequences(first=False)

##############################################################################
# 2. FIND MATCHES BETWEEN THE SEQUENCES YOU CHOSE IN STEP (1) & HIGHLIGHT THEM
##############################################################################

def compare_sequences(sequence1,sequence2,speciesname1,speciesname2):
    filename = input("Please enter a name under which the list of matches will be stored: ")
    
    # add a timestamp to the filename
    currenttime = datetime.now()
    date = str(currenttime.year) + str(currenttime.month) + str(currenttime.day)
    time = str(currenttime.hour) + str(currenttime.minute) + str(currenttime.second)
    filename = filename + '_' + date + '_' + time
    
    list_matches_seq1_seq2 = LongestMatches(sequence1,sequence2,filename)
    print("There is " + str(len(list_matches_seq1_seq2)) + "regions of homology >= 19nt in the " + speciesname1 + " and " + speciesname2 + " transcripts.")
    
    coloured_seq1_seq2 = colour_matches(sequence1,list_matches_seq1_seq2)
    coloured_seq2_seq1 = colour_matches(sequence2,list_matches_seq1_seq2)
    
    return list_matches_seq1_seq2, coloured_seq1_seq2, coloured_seq2_seq1

list_matches_seq1_seq2,coloured_seq1_seq2,coloured_seq2_seq1 = compare_sequences(sequence1,sequence2,name1,name2)
print(coloured_seq1_seq2)
print(coloured_seq2_seq1)


# e.g...
list_matches_mouse_rat, coloured_mouse_rat, coloured_rat_mouse = compare_sequences(AC1_mouse, AC1_rat, "mouse", "rat")

"""
outdated code:
#####################
# GATHERING SEQUENCES
#####################

number_sequences = input("How many sequences would you like to compare? ")
number_sequences = int(number_sequences)

names_sequences = []
for i in range(number_sequences):
    names_sequences.append(input("How would you like to name your variables? "))
    
sequences = []
for i in range(number_sequences):
    #name = names_sequences[i]
    sequence = input("Please paste the following sequence (" + names_sequences[i] + "): ")
    sequences.append(sequence2string(sequence))
    
adcy1 = {}
for i in range(number_sequences):
    adcy1[names_sequences[i]] = sequences[i]


"""

