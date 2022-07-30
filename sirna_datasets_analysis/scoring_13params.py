# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 12:59:26 2022

@author: User
"""

# FUNCTION TO RETRIEVE DATA FOR SCORING

"""
In the case of the Hall 2006 dataset, we have to get the sense (passenger) strand from AS (guide).
We assume perfect complementarity of siRNA duplexes in the dataset.
Note that they use sequences with non-TT overhangs; therefore we are only considering 19nts of their sequences.
"""

def collect_antisense(sirna_data): #assumed input: list of tuples with guide sequence and efficacy
    
    # extract guide strands from list of tuples
    antisense_list = []

    for item in sirna_data:
        antisense = item[0]
        antisense_list.append(antisense)
        
    return antisense_list


def reconstruct_sense(antisense_list): #assumed input: list of tuples with guide sequence and efficacy
    
    sense_list = []
    
    for antisense in antisense_list:

        # create variable to reconstruct corresponding sense
        sense_re = ""
        
        # generate complementary sense. (2 rules: A&U, G&C)
        for nt in antisense:
            if nt == "A":
                sense_re = sense_re + "U"
            elif nt == "U":
                sense_re = sense_re + "A"
            elif nt == "G":
                sense_re = sense_re + "C"
            elif nt == "C":
                sense_re = sense_re + "G"
            else:
                continue
        
        sense_re = sense_re[::-1]
        sense_list.append(sense_re)
        
    return sense_list

# FUNCTIONS FOR SCORING

"""
PARAMETERS:						
ParamNr	Weight	Parameter				
			
6	1	GC content of 36-52% (note: amarzguioui 31.6–57.9, maybe be a bit tolerant?)				
7	2	"Asymmetrical base pairing in the duplex (more A/U at 5′ of AS and more G/C at 5′ of SS)"				
8	2	Energy valley in 9-14th nucleotide of the sense strand				
9	0.5	GC repeat less than 3				
10	0.5	AT repeat less than 4	

12  1   tt overhang					
13	1	Weak base pair at 5'-end of antisense (presence of A/U)				
14	1	Strong base pair at 5'-end of sense (presence of G/C)				
15	1	Presence of A at 6th position of antisense strand				
16	0.5	Presence of A at 3rd position of sense strand				
17	0.5	Presence of A at 19th position of sense strand				
18	1	Absence of G/C at 19th position of sense strand				
19	1	Absence of G at 13th nucleotide of sense strand				
20	1	Presence of U at 10th nucleotide of sense strand
"""

def param6(sense_list, number_candidates):
    
    # Check that total GC content is between 36-52% 
    # If you want to be a bit more tolerant, can change to 31.6 to 57.9 according to Amarzguioui et al.
	
    GC_min = 36
    GC_max = 52
    
    weight6 = 1
    
    score6 = [0] * number_candidates
    
    for i in range(number_candidates):
        sense_strand = sense_list[i]
        
        # Sense GC analysis:
        GC_count = sense_strand.count('G') + sense_strand.count('C')
        GC_perc = (GC_count/len(sense_strand))*100
        
        # check whether GC content lower in valley compared to remaining region
        if GC_perc > GC_min:
            if GC_perc < GC_max:
                score6[i] = 1
        
    return score6, weight6

def param7(sense_list, number_candidates):
    
    # A/U differential of the 3 terminal basepairs; just look at sense strand & duplex region
    # desired: more A/U at 5′ of antisense sense strand and more G/C at 5′ of sense strand
    
    weight7 = 2
    
    score7 = [0] * number_candidates
    
    for i in range(number_candidates):
        sense_strand = sense_list[i]
        
        sense_5prime = sense_strand[0:3]
        sense_3prime = sense_strand[-3:]
        
        # We need less A/U at 5' vs 3' of sense (and consequently more G/C)
        
        AUcount_5prime = sense_5prime.count('A') + sense_5prime.count('U')
        AUcount_3prime = sense_3prime.count('A') + sense_3prime.count('U')
        
        if AUcount_3prime > AUcount_5prime:
            score7[i] = weight7
    
    return score7, weight7

def param8(sense_list, number_candidates):
    
    # we want to check whether there is lower GC content in nt 9-14 of sense vs. remaining nt
    # exclude the last two nucleotides (without TT)
    
    weight8 = 2
    
    score8 = [0] * number_candidates
    
    for i in range(number_candidates):
        sense_strand = sense_list[i]
        
        # energy valley GC analysis:
        valley_region = sense_strand[8:14]
        GC_valley_count = valley_region.count('G') + valley_region.count('C')
        GC_valley_perc = (GC_valley_count/len(valley_region))*100
        
        # Remaining region GC analysis
        nonvalley = sense_strand[:8] +  sense_strand[14:] 
        GC_nonvalley_count = nonvalley.count('G') + nonvalley.count('C')
        GC_nonvalley_perc = (GC_nonvalley_count/len(nonvalley))*100    
        
        # check whether GC content lower in valley compared to remaining region
        if GC_nonvalley_perc > GC_valley_perc:
            score8[i] = weight8
        
    return score8, weight8

def param9(sense_list, antisense_list, number_candidates):
    
    # GC repeat less than 3
    
    weight9 = 0.5
    
    score9 = [0] * number_candidates
    
    for i in range(number_candidates):
        sense_strand = sense_list[i]
        antisense_strand = antisense_list[i]

        
        if 'GGG' in sense_strand or 'GGG' in antisense_strand:
            continue #  failed param 9
        elif 'CCC' in sense_strand or 'CCC' in antisense_strand:
            continue # failed param 9
        else:
            score9[i] = weight9
    
    return score9, weight9

def param10(sense_list, antisense_list, number_candidates):
    
    # AT repeat less than 4
    
    weight10 = 0.5
    
    score10 = [0] * number_candidates
    
    for i in range(number_candidates):
        sense_strand = sense_list[i]
        antisense_strand = antisense_list[i]
        
        if 'AAAA' in sense_strand or 'AAAA' in antisense_strand:
            continue # failed param 10
        elif 'TTTT' in antisense_strand or 'TTTT' in antisense_strand:
            continue # failed param 10
        else:
            score10[i] = weight10
    
    return score10, weight10

def param12(antisense_list_overhang, number_candidates):
    
    # check whether both strands have 3' TT overhangs
    
    weight12 = 1
    
    score12 = [0] * number_candidates
    
    for i in range(number_candidates):
        antisense_strand = antisense_list_overhang[i]
        if antisense_strand[-1] == 't' and antisense_strand[-2] == 't':
            score12[i] = weight12
    
    return score12, weight12

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

def param18(sense_list, number_candidates):
    
    # check whether at nt 19 of the sense strand there is a G OR C
    # if there is no G or C, award 1 point
    
    weight18 = 1
    
    score18 = [0] * number_candidates
    
    for i in range(number_candidates):
        sense_strand =  sense_list[i]
        if sense_strand[18] == 'G' or sense_strand[18] == 'C':
            score18[i] = 0
        else:
            score18[i] = 1
    
    return score18, weight18

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

def totalscores(number_candidates, score6, score7, score8, score9, score10, score12, score13, score14, score15, score16, score17, score18, score19, score20, weight6, weight7, weight8, weight9, weight10, weight12, weight13, weight14, weight15, weight16, weight17, weight18, weight19, weight20):

    # Calculating max. possible score & final score for each siRNA candidate

    sums_list = []
    for i in range(number_candidates):
        sums_list.append(score6[i] + score7[i] + score8[i] + score9[i] + score10[i] + score12[i] + score13[i] + score14[i] + score15[i] + score16[i] + score17[i] + score18[i] + score19[i] + score20[i])
            
        max_possible = weight6 + weight7 + weight8 + weight9 + weight10 + weight12 + weight13 + weight14 + weight15 + weight16 + weight17 + weight18 + weight19 + weight20
        
    return sums_list, max_possible

def totalscores_no12(number_candidates, score6, score7, score8, score9, score10, score13, score14, score15, score16, score17, score18, score19, score20, weight6, weight7, weight8, weight9, weight10, weight13, weight14, weight15, weight16, weight17, weight18, weight19, weight20):

    # Calculating max. possible score & final score for each siRNA candidate

    sums_list = []
    for i in range(number_candidates):
        sums_list.append(score6[i] + score7[i] + score8[i] + score9[i] + score10[i] + score13[i] + score14[i] + score15[i] + score16[i] + score17[i] + score18[i] + score19[i] + score20[i])
            
        max_possible = weight6 + weight7 + weight8 + weight9 + weight10 + weight13 + weight14 + weight15 + weight16 + weight17 + weight18 + weight19 + weight20
        
    return sums_list, max_possible

def retrieve_sirna_scores(sense_list, antisense_list, number_candidates, ):
    score6, weight6 = param6(sense_list, number_candidates)
    score7, weight7 = param7(sense_list, number_candidates)
    score8, weight8 = param8(sense_list, number_candidates)
    score9, weight9 = param9(sense_list, antisense_list, number_candidates)
    score10, weight10 = param10(sense_list, antisense_list, number_candidates)
    score13, weight13 = param13(antisense_list, number_candidates)
    score14, weight14 = param14(sense_list, number_candidates)
    score15, weight15 = param15(antisense_list, number_candidates)
    score16, weight16 = param16(sense_list, number_candidates)
    score17, weight17 = param17(sense_list, number_candidates)
    score18, weight18 = param18(sense_list, number_candidates)
    score19, weight19 = param19(sense_list, number_candidates)
    score20, weight20 = param20(sense_list, number_candidates)
    
    return score6, weight6, score7, weight7, score8, weight8, score9, weight9, score10, weight10, score13, weight13, score14, weight14, score15, weight15, score16, weight16, score17, weight17, score18, weight18, score19, weight19, score20, weight20

def score_overhangs(antisense_withoverhang, number_candidates):
    score12, weight12 = param12(antisense_withoverhang, number_candidates)
    
    return score12, weight12


"""
def collecting_scores(antisense_list, sense_list, overhang_list, number_candidates):
    score6, weight6 = param6(sense_list, number_candidates)
    score7, weight7 = param7(sense_list, number_candidates)
    score8, weight8 = param8(sense_list, number_candidates)
    score9, weight9 = param9(sense_list, antisense_list, number_candidates)
    score10, weight10 = param10(sense_list, antisense_list, number_candidates)
    score12, weight12 = param12(overhang_list, number_candidates)
    score13, weight13 = param13(antisense_list, number_candidates)
    score14, weight14 = param14(sense_list, number_candidates)
    score15, weight15 = param15(antisense_list, number_candidates)
    score16, weight16 = param16(sense_list, number_candidates)
    score17, weight17 = param17(sense_list, number_candidates)
    score18, weight18 = param18(sense_list, number_candidates)
    score19, weight19 = param19(sense_list, number_candidates)
    score20, weight20 = param20(sense_list, number_candidates)
    
    return score6, score7, score8, score9, score10, score12, score13, score14, score15, score16, score17, score18, score19, score20, weight6, weight7, weight8, weight9, weight10, weight12, weight13, weight14, weight15, weight16, weight17, weight18, weight19, weight20
"""