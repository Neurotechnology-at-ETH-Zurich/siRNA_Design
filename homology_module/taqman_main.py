# -*- coding: utf-8 -*-
"""
Created on Fri May 27 13:13:41 2022

@author: User
"""
from sequences import AC1_human_TV1, AC1_human_TV2, AC1_mouse, AC1_rat
from homology_helperfunctions import sequence2string

####################################################################
# 1. HERE WE GIVE THE PROGRAM INFORMATION ABOUT A FEW TAQMAN PROBES.
# The user has the option to add new information manually in step 2.
####################################################################

"""
HUMAN ADCY1
Taqman probe
https://www.thermofisher.com/taqman-gene-expression/product/Hs00299832_m1?CID=&ICID=&subtype=

TRANSCRIPT VARIANT 1
TV1 https://www.ncbi.nlm.nih.gov/nuccore/NM_021116.2
Transcript length = 12 499
Default taqman probe: Hs00299832_m1
Assay location: 1041
Amplicon length: 56

TRANSCRIPT VARIANT 2
TV2 https://www.ncbi.nlm.nih.gov/nuccore/NM_001281768.1
Transcript length = 1763
Default taqman probe: same as for TV1
Assay location: 727
Amplicon length: 56
"""

assay_start_TV1 = 1041
amplicon_length_TV1 = 56

assay_start_TV2 = 727
amplicon_length_TV2 = 56

"""
MOUSE ADCY1
Taqman probe
https://www.thermofisher.com/taqman-gene-expression/product/Mm01187829_m1?CID=&ICID=&subtype=

Sequence targeted
https://www.ncbi.nlm.nih.gov/nuccore/NM_009622.1

Transcript length = 12 315
Default taqman probe: Mm01187829_m1
Assay location: 3166
Amplicon length: 66
"""

assay_start_mouse = 3166
amplicon_length_mouse = 66

"""
RAT ADCY1
Taqman probe
https://www.thermofisher.com/taqman-gene-expression/product/Rn02115682_s1?CID=&ICID=&subtype=

Sequence targeted
https://www.ncbi.nlm.nih.gov/nuccore/NM_001107239.1

Transcript length = 3219
Default taqman probe: Rn02115682_s1
Assay location: 3137
Amplicon length: 131
"""

assay_start_rat = 3137
amplicon_length_rat = 131

#########################################################################
# 2. HERE WE LET THE USER SELECT WHICH TRANSCRIPTS THEY ARE INTERESTED IN
#########################################################################

def collect_sequence(first=True): # if you want to enter the second sequence, set first to False
    
    if first==True:
        sequence_choice = input("What is your first sequence? Select from: AC1_human_TV1, AC1_human_TV2, AC1_mouse, AC1_rat, or new sequence. ")
    elif first==False:
        sequence_choice = input("What is your second sequence? Select from: AC1_human_TV1, AC1_human_TV2, AC1_mouse, AC1_rat, or new sequence. ")
        
    if sequence_choice == "AC1_human_TV1":
        sequence = AC1_human_TV1
        assay_start = assay_start_TV1
        amplicon_length = amplicon_length_TV1
        
    elif sequence_choice == "AC1_human_TV2":
        sequence = AC1_human_TV2
        assay_start = assay_start_TV2
        amplicon_length = amplicon_length_TV2
        
    elif sequence_choice == "AC1_mouse":
        sequence = AC1_mouse
        assay_start = assay_start_mouse
        amplicon_length = amplicon_length_mouse
        
    elif sequence_choice == "AC1_rat":
        sequence = AC1_rat
        assay_start = assay_start_rat
        amplicon_length = amplicon_length_rat
        
    elif sequence_choice == "new sequence":
        newsequence = input("Please copy paste the new mRNA sequence. Write T's instead of U's. ")
        # make sure any spaces, numbers, or special characters are removed
        sequence = sequence2string(newsequence)
        assay_start = input("At which position does the corresponding Taqman assay start? ")
        amplicon_length = input("What is the amplicon length? ")
        
    else:
        print("Invalid input")
        # call function again
        collect_sequence()
        
    return sequence, assay_start, amplicon_length

sequence1, assay_start1, amplicon_length1 = collect_sequence(first=True)
sequence2, assay_start2, amplicon_length2 = collect_sequence(first=False)

########################################################################################
# 3. HERE WE CHECK´WHETHER A PROBE TARGETING 2 TRANSCRIPTS REALLY TARGETS THE SAME MOTIF
# This is just an additional safety check, and not really necessary.
########################################################################################

def probes_identity_check(sequence1, sequence2, assay_start1, assay_start2,amplicon_length1, amplicon_length2):
    assay_start1 = assay_start1 - 1
    assay_start2 = assay_start2 - 1
    
    assay_stop1 = assay_start1 + amplicon_length1
    assay_stop2 = assay_start2 + amplicon_length2
    
    if sequence1[assay_start1:assay_stop1] == sequence2[assay_start2:assay_stop2]:
        print("The taqman probes target identical sequences in the 2 human transcripts.")
    else:
        print("They do not target identical sequences")
        
# Checking that human taqman probe targets both human transcripts at the specified position
probes_identity_check(AC1_human_TV1, AC1_human_TV2, assay_start_TV1, assay_start_TV2, amplicon_length_TV1, amplicon_length_TV2)

################################################################
# 4. HERE WE EXTRACT THE SEQUENCES TARGETED BY THE TAQMAN PROBES
################################################################

def extract_taqman_seq(sequence,assay_start,amplicon_length):
    
    assay_start = assay_start-1
    
    taqman_seq = sequence[assay_start:assay_start+amplicon_length]
    
    return taqman_seq

# Extract the targeted regions for the two sequences we are investigating
taqman_seq1 = extract_taqman_seq(sequence1, assay_start1, amplicon_length1)
taqman_seq2 = extract_taqman_seq(sequence2, assay_start2, amplicon_length2)

"""
# Extract the sequences targeted by taqman probes for mouse, human TV1 and rat
mouse_taqman_seq = extract_taqman_seq(AC1_mouse,assay_start_mouse,amplicon_length_mouse)
TV1_taqman_seq = extract_taqman_seq(AC1_human_TV1,assay_start_TV1,amplicon_length_TV1)
rat_taqman_seq = extract_taqman_seq(AC1_rat,assay_start_rat,amplicon_length_rat)
"""

############################################################################################################
# 5. HERE WE CHECK FOR CROSS-REACTIVITY: DOES EITHER OF THE PROBES ALSO HAVE A TARGET IN THE OTHER SEQUENCE?
# E.g. check whether human TV1 probe targets mouse AC1 too
############################################################################################################

def check_taqman_crossreact(sequence,taqman_seq): 
    species_probe = input("Which Taqman probe do you want to examine? (give species) ")
    species_sequence = input("In which sequence do you want to search for it? (give species) ") # e.g. species_sequence = mouse, species_probe = human
    if sequence.find(taqman_seq) == -1: # -1 means that the substring was not found!
        print("The sequence targeted by " + species_probe + " is not contained in the " + species_sequence + " sequence.")
    else:
        print(sequence.find(taqman_seq))
        
check_taqman_crossreact(sequence1, taqman_seq2)
check_taqman_crossreact(sequence2, taqman_seq1)





