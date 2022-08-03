# -*- coding: utf-8 -*-
"""
Created on Tue May 24 08:38:08 2022

@author: User
"""

from termcolor import colored
import pickle

# Function to convert an mRNA sequence as copied from ncbi (but line breaks removed in word by replacing ^p) into a letters-only string
def sequence2string(inputstring): # input of type 'gtagggtacc'
    
    # Remove all spaces
    inputstring = inputstring.replace(" ", "")
    
    # Remove all numbers
    newstring = ''.join([i for i in inputstring if not i.isdigit()])
    
    # Remove dashes
    mRNA_sequence = newstring.replace('/','')
    
    # Make sure everything is lowercase
    mRNA_sequence = mRNA_sequence.lower()
    
    # Make sure that the remaining string only contains letters
    if mRNA_sequence.isalpha() == False:
        print("There is remaining numbers or characters in the mRNA input string. Fix this before proceeding.")
    
    return mRNA_sequence

# Function to find the longest common element/substring between 2 strings
def longest_common_sequence(s1, s2):
    m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(s1)):
        for y in range(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]

# Function that makes a list of all substrings of a specified length (default = 19)
# Pickles and saves matches list
def LongestMatches(seq1, seq2, filename='matches_list', substring_length = 19): # NEW!!
    # Create a list to store the longest matching sequences
    list_matches = []
    # Find the longest match
    longestmatch = longest_common_sequence(seq1,seq2)
    # Add this sequence to our list
    list_matches.append(longestmatch)
    
    print("found longest match")
    
    # Create a copy of seq1 to delete already found matches from
    seq1_copy = seq1
    
    # Delete already found match
    seq1_copy = seq1_copy.replace(longestmatch, " ")
    
    i = 0
    while i < 1:
        # find longest remaining match
        match = longest_common_sequence(seq1_copy,seq2)
        # check whether it is longer than 19 nucleotides
        if len(match) >= substring_length:
            list_matches.append(match)
            print("found new match")
            seq1_copy = seq1_copy.replace(match, " ")
        else:
            i = 1
            
    open_file = open(filename,"wb")
    pickle.dump(list_matches,open_file)
    open_file.close()

    return list_matches

# Function that colours all homologous regions we just identified in the input mRNA

def colour_matches(sequence,matches_list):
    
    # create copy of sequence in which we will highlight homologous regions
    colour_sequence = sequence
    
    # locate each match within the sequence, format it to be green and bold
    for i in range(len(matches_list)):
        match = matches_list[i]
        print(colored(match,'green', attrs=['bold']))
        colour_sequence = colour_sequence.replace(match,colored(match,'green',attrs=['bold']))
    
    return colour_sequence

# Function that lets you chose which two sequences you want to compare and delivers the appropriate output

def homology_output(coloured_mouse_tv1,coloured_tv1_mouse,coloured_mouse_rat,coloured_rat_mouse,
                    coloured_rat_tv1,coloured_tv1_rat,coloured_rat_tv2,coloured_tv2_rat,
                    coloured_tv1_tv2, coloured_tv2_tv1):
    choice_sequence = input("Which sequence you want to display? Acceptable inputs: mouse, rat, human TV1, human TV2. Your answer: ")
    choice_homology = input("Do you want to find homologous regions to: mouse, rat, human TV1, or human TV2? ")
    
    if choice_sequence == 'mouse':
        if choice_homology == 'human TV1':
            print(coloured_mouse_tv1)
        elif choice_homology == 'rat':
            print(coloured_mouse_rat)
        else:
            print('Comparison to mouse needs to be added manually.')
    
    elif choice_sequence == 'rat':
        if choice_homology == 'mouse':
            print(coloured_rat_mouse)
        elif choice_homology == 'human TV1':
            print(coloured_rat_tv1)
        elif choice_homology == 'human TV2':
            print(coloured_rat_tv2)
        else:
            print('Comparison needs to be added manually.')
    
    elif choice_sequence == 'human TV1':
        if choice_homology == 'mouse':
            print(coloured_tv1_mouse)
        elif choice_homology == 'rat':
            print(coloured_tv1_rat)
        elif choice_homology == 'human TV2':
            print(coloured_tv1_tv2)
        else:
            print('Comparison needs to be added manually.')
        
    elif choice_sequence == 'human TV2':
        if choice_homology == 'rat':
            print(coloured_tv2_rat)
        elif choice_homology == 'human TV1':
            print(coloured_tv2_tv1)
        else:
            print('Comparison needs to be added manually.')
            
    else:
        print('species invalid - check your spelling or add new sequence manually!')

def sirna_homologous_check(sequence,list_matches,sirna_list): # requires sense strand

    # remove TT overhangs
    list_noTT = []
    for sense in sirna_list:
        list_noTT.append(sense[:-2])

    # convert uracils to thymines, to match the NT sequence (despite input being mRNA, ncbi still denotes with Ts)
    list_U2T = []
    for sense in list_noTT:
        sense_T = sense.replace('U','T')
        list_U2T.append(sense_T)

    for a in list_matches:
        matching_region = a
        for b in list_U2T:
            sirna_candidate = b
            if sirna_candidate in matching_region:
                print(sirna_candidate + " was found in the region " + matching_region)

        
        
