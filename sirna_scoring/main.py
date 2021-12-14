# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 17:56:13 2021

@author: User
"""
from nt_analysis import read_sequences, sum_scores, param4, param6, param7, param8, param9, param10, param12, param13, param14, param15, param16, param17, param18, param19, param20
# unused:
# from nt_analysis import userinput_collectsequences, excelinput_collectsequences

"""
Both of these commands not necessary anymore:
# User gives siRNA sense and antisense sequences as inputs
number_candidates, sense_list, antisense_list = userinput_collectsequences()

# Alternatively, automatically collect sequences from excel file
number_candidates, sense_list, antisense_list = excelinput_collectsequences()
"""

sense_list, antisense_list, number_candidates = read_sequences()

# Perform automatic scoring for parameters 4, 6-10 and 12-20
score4, weight4 = param4(number_candidates)
score6, weight6 = param6(sense_list, number_candidates)
score7, weight7 = param7(sense_list, number_candidates)
score8, GC_valley_perc, GC_nonvalley_perc, weight8 = param8(sense_list, number_candidates)
score9, weight9 = param9(sense_list, antisense_list, number_candidates)
score10, weight10 = param10(sense_list, antisense_list, number_candidates)
score12, weight12 = param12(sense_list, antisense_list, number_candidates)
score13, weight13 = param13(antisense_list, number_candidates)
score14, weight14 = param14(sense_list, number_candidates)
score15, weight15 = param15(antisense_list, number_candidates)
score16, weight16 = param16(sense_list, number_candidates)
score17, weight17 = param17(sense_list, number_candidates)
score18, weight18 = param18(sense_list, number_candidates)
score19, weight19 = param19(sense_list, number_candidates)
score20, weight20 = param20(sense_list, number_candidates)

#sums_list, max_score = sum_scores(number_candidates, score4, score6, score7, score8, score9, score10, score12, score13, score14, score15, score16, score17, score18, score19, score20, weight4, weight6, weight7, weight8, weight9, weight10, weight12, weight13, weight14, weight15, weight16, weight17, weight18, weight19, weight20)

    
sums_list = []
for i in range(number_candidates):
    sums_list.append(score4[i] + score6[i] + score7[i] + score8[i] + score9[i] + score10[i] + score12[i] + score13[i] + score14[i] + score15[i] + score16[i] + score17[i] + score18[i] + score19[i] + score20[i])
        
    #sums_list = score6 + score7 + score8 + score9 + score10 + score12 + score13 + score14 + score15 + score16 + score17 + score18 + score19 + score20
    max_score = weight4 + weight6 + weight7 + weight8 + weight9 + weight10 + weight12 + weight13 + weight14 + weight15 + weight16 + weight17 + weight18 + weight19 + weight20
   

# Constraints on input:
# needs to begin at start codon, so that parameter 4 is scored easily
# needs to exclude introns, just be sure of your input sequence which eliminates parameter 5
# parameter 3 we ignore for now, add this in the future 
# can we automate secondary structure check?
# this would only leave BLAST search!!


# Remaining parameters to assess manually:
# 1: BLAST of sense strand (issue of overlap vs. e-value)
# 2: BLAST of antisense strand
# 3: not located at SNP site
# 4: not in first 75 bases from start codon
# 5: not in the intron -> try ExInt database https://www.ncbi.nlm.nih.gov/pmc/articles/PMC99089/
# PERFORM MANUALLY: 
# 11 (weight 2)	No internal secondary structures and hairpins (oligoanalyzer software by Molecular Biology Insights; Generunner by Hastings software) => I am performing this with RNA fold (uni vienna)







