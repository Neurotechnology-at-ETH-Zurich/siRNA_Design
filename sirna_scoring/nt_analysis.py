## -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 19:12:51 2021

@author: User
"""
# import os
import sys
sys.path.append(r'C:\Users\User\Desktop\ETH_NSC\Yanik_lab\siRNADesign-master\software_comparisons')


#os.chdir("../")

import openpyxl
import pickle
from helper_functions import open_pickle

"""
PARAMETERS:						
ParamNr	Weight	Parameter				
1	1	Blast of sense strand !!!MANUAL			
2	1	Blast of anti-sense strand	!!!!MANUAL			
3	1	Not located at SNP site !!!FOR LUCIF NOT NECESSARY				
4	1	Not located in first 75 bases from start codon*			
5	1	Not in the intron !!!EXCLUDE				
6	1	GC content of 36-52% (note: amarzguioui 31.6–57.9, maybe be a bit tolerant?)				
7	2	"Asymmetrical base pairing in the duplex (more A/U at 5′ of
antisense sense strand and more G/C at 5′ of sense strand)"				
8	2	Energy valley in 9-14th nucleotide of the sense strand				
9	0.5	GC repeat less than 3				
10	0.5	AT repeat less than 4				
11	2	No internal secondary structures and hairpins !!!MANUAL (oligoanalyzer software by Molecular Biology Insights; Generunner by Hastings software) => I am performing this with RNA fold (uni vienna)				
12	1	3'-TT overhangs				
13	1	Weak base pair at 5'-end of antisense (presence of A/U)				
14	1	Strong base pair at 5'-end of sense (presence of G/C)				
15	1	Presence of A at 6th position of antisense strand				
16	0.5	Presence of A at 3rd position of sense strand				
17	0.5	Presence of A at 19th position of sense strand				
18	1	Absence of G/C at 19th position of sense strand				
19	1	Absence of G at 13th nucleotide of sense strand				
20	1	Presence of U at 10th nucleotide of sense strand

WHICH PARAMETERS WILL WE HERE ASSESS?
6 total GC content percentage
7 asymmetrical base pairing in the duplex
8 energy valley in nt 9-14
9 GC repeats < 3
10 AT repeats < 4
13 presence of A/U at 5' end of antisense
14 presence of G/C at 5' end of sense
15 presence of A at nt 6 of antisense
16 presence of A at nt 3 of sense
17 presence of A at nt 19 of sense
18 absence of G/C at nt 19 of sense
19 absence of G at nt 13 of sense
20 presence of U at nt 10 of sense
"""

def read_sequences():
    path = 'C:/Users/User/Desktop/ETH_NSC/Yanik_lab/siRNADesign-master/software_comparisons'
    
    filename_s = '/triplicate sense sequences'
    open_file_s = open(path+filename_s, "rb")   
    sense_list = pickle.load(open_file_s) 
    open_file_s.close()
    
    filename_as = '/triplicate antisense sequences'
    open_file_as = open(path+filename_as, "rb")
    antisense_list = pickle.load(open_file_as)
    open_file_as.close()
    
    """
    filename_seq = '/NT_sequence'
    open_file_seq = open(path+filename_seq, "rb")
    NT_sequence = pickle.load(open_file_seq)
    open_file_seq.close()
    """
    
    number_candidates = len(sense_list)
    
    return sense_list, antisense_list, number_candidates

def param20(sense_list, number_candidates):
    
    # check whether at nt 10 of the sense strand there is a U
    # if there is a U, award 1 point
    
    weight20 = 1
    
    score20 = [0] * number_candidates

    for i in range(number_candidates):
        sense_strand = sense_list[i]
        if sense_strand[9] == 'U':
            score20[i] = weight20
    
    return score20, weight20

def param19(sense_list, number_candidates):
    
    # check whether at nt 13 of the sense strand there is a G
    # if there is no G, award 1 point	

    weight19 = 1     	

    score19 = [0] * number_candidates
    
    for i in range(number_candidates):
        sense_strand =  sense_list[i]
        if sense_strand[12] != 'G':
            score19[i] = 1
    
    return score19, weight19

def param18(sense_list, number_candidates):
    
    # check whether at nt 19 of the sense strand there is a G OR C
    # if there is no G or C, award 1 point
    
    weight18 = 1
    
    score18 = [0] * number_candidates
    
    for i in range(number_candidates):
        sense_strand =  sense_list[i]
        if sense_strand[18] != 'G' or sense_strand[18] != 'C':
            score18[i] = 1
    
    return score18, weight18

def param17(sense_list, number_candidates):
    
    # check whether at nt 19 of the sense strand there is an A
    # if there is an A, award 1 point
    
    weight17 = 0.5
    
    score17 = [0] * number_candidates

    for i in range(number_candidates):
        sense_strand = sense_list[i]
        if sense_strand[18] == 'A':
            score17[i] = weight17
    
    return score17, weight17	

def param16(sense_list, number_candidates):
    
    weight16 = 0.5
    
    # check whether at nt 3 of the sense strand there is an A
    # if there is an A, award 1 point
    
    score16 = [0] * number_candidates

    for i in range(number_candidates):
        sense_strand = sense_list[i]
        if sense_strand[2] == 'A':
            score16[i] = weight16
    
    return score16, weight16

def param15(antisense_list, number_candidates):
    
    # check whether at nt 6 of the antisense strand there is an A
    # if there is an A, award 1 point
    
    weight15 = 1
    
    score15 = [0] * number_candidates

    for i in range(number_candidates):
        antisense_strand = antisense_list[i]
        if antisense_strand[5] == 'A':
            score15[i] = weight15
    
    return score15, weight15
	
def param14(sense_list, number_candidates):
    
    # check whether there is G OR C at nt 1 of sense
    # if there is G OR C, award 1 point
    
    weight14 = 1

    score14 = [0] * number_candidates
    
    for i in range(number_candidates):
        sense_strand =  sense_list[i]
        if sense_strand[0] == 'G' or sense_strand[0] == 'C':
            score14[i] = weight14
                
    return score14, weight14

def param13(antisense_list, number_candidates):
    
    # check whether there is A OR U at nt 1 of antisense
    # if there is A OR U, award 1 point
    
    weight13 =  1

    score13 = [0] * number_candidates
    
    for i in range(number_candidates):
        antisense_strand =  antisense_list[i]
        if antisense_strand[0] == 'A' or antisense_strand[0] == 'U':
            score13[i] = weight13
                
    return score13, weight13

def param12(sense_list, antisense_list, number_candidates):
    
    # check whether both strands have 3' TT overhangs
    
    weight12 = 1
    
    score12 = [0] * number_candidates
    
    for i in range(number_candidates):
        sense_strand = sense_list[i]
        antisense_strand = antisense_list[i]
        if sense_strand[-1] == 'T' and sense_strand[-2] == 'T':
            if antisense_strand[-1] == 'T' and antisense_strand[-2] == 'T':
                score12[i] = weight12
    
    return score12, weight12

def param10(sense_list, antisense_list, number_candidates):
    
    # AT repeat less than 4
    
    weight10 = 0.5
    
    score10 = [0] * number_candidates
    
    for i in range(number_candidates):
        sense_strand = sense_list[i]
        antisense_strand = antisense_list[i]
        
        if 'AAAA' in sense_strand or 'AAAA' in antisense_strand:
            print("failed because of polyA")
        elif 'TTTT' in antisense_strand or 'TTTT' in antisense_strand:
            print("failed because of polyT")
        else:
            score10[i] = weight10
    
    return score10, weight10	

def param9(sense_list, antisense_list, number_candidates):
    
    # GC repeat less than 3
    
    weight9 = 0.5
    
    score9 = [0] * number_candidates
    
    for i in range(number_candidates):
        sense_strand = sense_list[i]
        antisense_strand = antisense_list[i]
        
        if 'GGG' in sense_strand or 'GGG' in antisense_strand:
            print("failed because of polyG")
        elif 'CCC' in antisense_strand or 'CCC' in antisense_strand:
            print("failed because of polyC")
        else:
            score9[i] = weight9
    
    return score9, weight9

def param8(sense_list, number_candidates):
    
    # we want to check whether there is lower GC content in nt 9-14 of sense vs. remaining nt
    # exclude the last two nucleotides (without TT)
    
    weight8 = 2
    
    score8 = [0] * number_candidates
    
    for i in range(number_candidates):
        sense_strand = sense_list[i]
        # delete 3' TT overhang
        sense_noTT = sense_strand[:-1]
        sense_noTT = sense_noTT[:-1]
        
        # energy valley GC analysis:
        valley_region = sense_noTT[8:14]
        GC_valley_count = valley_region.count('G') + valley_region.count('C')
        GC_valley_perc = (GC_valley_count/len(valley_region))*100
        
        # Remaining region GC analysis
        nonvalley = sense_noTT[:8] +  sense_noTT[14:] 
        GC_nonvalley_count = nonvalley.count('G') + nonvalley.count('C')
        GC_nonvalley_perc = (GC_nonvalley_count/len(nonvalley))*100    
        
        # check whether GC content lower in valley compared to remaining region
        if GC_nonvalley_perc > GC_valley_perc:
            score8[i] = weight8
        
    return score8, GC_valley_perc, GC_nonvalley_perc, weight8

def param7(sense_list, number_candidates):
    
    # A/U differential of the 3 terminal basepairs; just look at sense strand & duplex region
    # desired: more A/U at 5′ of antisense sense strand and more G/C at 5′ of sense strand
    
    weight7 = 2
    
    score7 = [0] * number_candidates
    
    for i in range(number_candidates):
        sense_strand = sense_list[i]
        # delete 3' TT overhang
        sense_noTT = sense_strand[:-1]
        sense_noTT = sense_noTT[:-1]
        
        sense_5prime = sense_noTT[0:3]
        sense_3prime = sense_noTT[-3:]
        
        # We need less A/U at 5' vs 3' of sense (and consequently more G/C)
        
        AUcount_5prime = sense_5prime.count('A') + sense_5prime.count('U')
        AUcount_3prime = sense_3prime.count('A') + sense_3prime.count('U')
        
        if AUcount_3prime > AUcount_5prime:
            score7[i] = weight7
    
    return score7, weight7

def param6(sense_list, number_candidates):
    
    # Check that total GC content is between 36-52% 
    # If you want to be a bit more tolerant, can change to 31.6 to 57.9 according to Amarzguioui et al.
	
    weight6 = 1
    
    score6 = [0] * number_candidates
    
    for i in range(number_candidates):
        sense_strand = sense_list[i]
        # delete 3' TT overhang
        sense_noTT = sense_strand[:-1]
        sense_noTT = sense_noTT[:-1]
        
        # Sense GC analysis:
        GC_count = sense_noTT.count('G') + sense_noTT.count('C')
        GC_perc = (GC_count/len(sense_noTT))*100
        
        # check whether GC content lower in valley compared to remaining region
        if GC_perc > 36:
            if GC_perc < 52:
                score6[i] = 1
        
    return score6, weight6

# 4: not in first 75 bases from start codon

#def param4(number_candidates):
def param4(sense_list, DNA_sequence):
    print(len(DNA_sequence))
    
    weight4 = 1
    score4 = [0]*len(sense_list)
    
    for i in range(len(sense_list)):
        sense = sense_list[i]
        
        if len(sense) > 19:
            sense = sense[:-2]
        
        print(sense)
        
        startcodon = DNA_sequence.index("ATG")
        
        position = DNA_sequence.index(sense)
        if int(position) > startcodon + 75:
            score4[i] = 1
    
    # for this we need to retrieve target position and check that it is a number < 76 (in python 0-75)
    
    """

    path = 'C:/Users/User/Desktop/ETH_NSC/Yanik_lab/Luciferase_siRNA/siRNADesign/siRNADesign/software_comparisons'
    filename = r'/triplicate positions'
    open_file = open(path+filename, 'rb')
    triplicate_positions = pickle.load(open_file)
    open_file.close()
    
    weight4 = 1
    
    score4 = [0] * number_candidates
    
    for i in range(number_candidates):
        position = triplicate_positions[i]
        if int(position) > 75:
            score4[i] = 1
            
    """
    
    return score4, weight4
    

# Additional parameter we could add: check whether antisense GC content between nt 2-7 ~19, between 8-18~52
	
# 5: not in the intron

# 4: not in first 75 bases from start codon

# 3: not located at SNP site

# 2: BLAST of antisense strand

# 1: BLAST of sense strand

def totalscores(number_candidates, score4, weight4, score6, weight6, score7, weight7, score8, weight8, score9, weight9, score10, weight10, score12, weight12, score13, weight13, score14, weight14, score15, weight15, score16, weight16, score17, weight17, score18, weight18, score19, weight19, score20, weight20, structure_scores, weight_structure_scores):

    # Calculating max. possible score & final score for each siRNA candidate

    sums_list = []
    for i in range(number_candidates):
        sums_list.append(score4[i] + score6[i] + score7[i] + score8[i] + score9[i] + score10[i] + score12[i] + score13[i] + score14[i] + score15[i] + score16[i] + score17[i] + score18[i] + score19[i] + score20[i] + structure_scores[i])
            
        max_score = weight4 + weight6 + weight7 + weight8 + weight9 + weight10 + weight12 + weight13 + weight14 + weight15 + weight16 + weight17 + weight18 + weight19 + weight20 + weight_structure_scores
        
    return sums_list, max_score

def percentages_score(sums_list, max_score):
    percentages_list = []
    for i in range(len(sums_list)):
        percentage = (sums_list[i]/max_score)*100
        percentages_list.append(round(percentage,2))
        
    return percentages_list
        


