# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 17:56:13 2021

@author: User
"""
import os
os.chdir(r'C:\Users\User\Desktop\ETH_NSC\Yanik_lab\siRNADesign-master\sirna_scoring')

from nt_analysis import read_sequences, totalscores, percentages_score, param4, param6, param7, param8, param9, param10, param12, param13, param14, param15, param16, param17, param18, param19, param20
from secondarystructure import readDNAsequence, perform_query_RNAfold, extracting_bases, extracting_dotnotation, findtargetpositions, targetstructure_scoring


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

# Scoring secondary structure (parameter 11):
    
weight_structure_scores = 2

chromedriver_path = r'C:\Users\User\Downloads\chromedriver_win32 (3)\chromedriver.exe'

# retrieve DNA sequence that was initially given as user input
DNA_sequence = readDNAsequence()

# perform RNAfold query with DNA sequence as input; returns the predicted secondary structure of our target mRNA
driver = perform_query_RNAfold(chromedriver_path, DNA_sequence)

# from the results of this query extract MFE & centroid bases (note that this mRNA sequence is of course the same in both cases)
bases_MFE = extracting_bases(driver,xpath_bases='/html/body/div[2]/div[2]/div/div[3]/pre[1]/span/pre' )
bases_centroids = extracting_bases(driver,xpath_bases='/html/body/div[2]/div[2]/div/div[3]/pre[3]/span/pre')

# retrieve the sense sequences we want to evaluate and locate them in the mRNA sequence (retrieved from page) 
target_indices = findtargetpositions(sense_list, bases_MFE)
print("Make sure to double check that the sense sequences that will proceed to be evaluated target the desired positions on your mRNA.")
print("target_indices (printed below) should match triplicate_list.")
print(target_indices)

# from the results of this query extract  MFE & centroid secondary structure prediction (this will differ!)
dots_MFE = extracting_dotnotation(driver,xpath_dots='/html/body/div[2]/div[2]/div/div[3]/pre[2]/span/pre')
dots_centroids = extracting_dotnotation(driver,xpath_dots='/html/body/div[2]/div[2]/div/div[3]/pre[4]/span/pre')

# perform sense scoring based on 4 criteria for MFE. Adds up to a maximum of 2 points
startloop_list_MFE, endloop_list_MFE, nr_unpaired_scores_MFE, nr_loops_scores_MFE, structure_scores_MFE, weight_structure_scores_MFE = targetstructure_scoring(bases_MFE, dots_MFE, sense_list) 

# perform sense scoring based on 4 criteria for centroid. Adds up to a maximum of 2 points
startloop_list_centroid, endloop_list_centroid, nr_unpaired_scores_centroid, nr_loops_scores_centroid, structure_scores_centroid, weight_structure_scores_centroid = targetstructure_scoring(bases_MFE, dots_MFE, sense_list) 

# take average of the MFE and centroid sense scoring
structure_scores = []
for i in range(len(structure_scores_MFE)):
    sum_element = structure_scores_MFE[i] + structure_scores_centroid[i]
    structure_scores.append(sum_element/2)
    
# Calculating total score:

sums_list, max_score = totalscores(number_candidates, score4, weight4, score6, weight6, score7, weight7, score8, weight8, score9, weight9, score10, weight10, score12, weight12, score13, weight13, score14, weight14, score15, weight15, score16, weight16, score17, weight17, score18, weight18, score19, weight19, score20, weight20, structure_scores, weight_structure_scores)

# Calculating percentage the siRNAs obtained of total possible points:
    
percentages_list = percentages_score(sums_list, max_score)

# Get 3 highest-scoring siRNAs and the positions they target
score = percentages_list
sequence = sense_list # remember this is the passenger strand which matches the mRNA target sequence. antisense=guide, complementary to mRNA

top3 = sorted(zip(score, sequence), reverse=True)[:3]

"""
REMAINING PARAMETERS TO ASSESS:
1: BLAST of sense strand (issue of overlap vs. e-value: what are acceptable e-values for sirna sequences?)
2: BLAST of antisense strand
For guidance on how to score this, please consult step 3 ("BLAST search to avoid off-target effects") in the user manual of the siRNA_Design pipeline.

What we don't need to check in the case of luciferase, but will have to add for future target genes:
3: not located at SNP site
5: not in the intron -> try ExInt database https://www.ncbi.nlm.nih.gov/pmc/articles/PMC99089/
"""




