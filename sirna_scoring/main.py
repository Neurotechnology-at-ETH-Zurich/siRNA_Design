# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 17:56:13 2021

@author: User
"""
from nt_analysis import read_sequences, sum_scores, param4, param6, param7, param8, param9, param10, param12, param13, param14, param15, param16, param17, param18, param19, param20
from secondarystructure import perform_query_RNAfold, extracting_bases, extracting_dotnotation, findtargetpositions
import pickle

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

# Scoring secondary structure (parameter 11)

chromedriver_path = r'C:\Users\User\Downloads\chromedriver_win32 (3)\chromedriver.exe'

def read_NTsequence():
    path = r'C:/Users/User/Desktop/ETH_NSC/Yanik_lab/siRNADesign-master/software_comparisons'
    filename_NT = '/NT_sequence'
    open_file_NT = open(path+filename_NT,"rb")
    NT_sequence = pickle.load(open_file_NT)
    
    open_file_NT.close()
    
    return NT_sequence

NT_sequence = read_NTsequence()

# automatically perform RNAfold query which returns the secondary structure of our target mRNA
driver = perform_query_RNAfold(chromedriver_path, NT_sequence)
# extract mRNA sequence; this is of course the same for MFE and centroid secondary structure prediction; I just repeated this to be safe
bases_MFE = extracting_bases(driver,xpath_bases='/html/body/div[2]/div[2]/div/div[3]/pre[1]/span/pre' )
bases_centroids = extracting_bases(driver,xpath_bases='/html/body/div[2]/div[2]/div/div[3]/pre[3]/span/pre')
# extract secondary structure prediction for MFE and centroids; this format is known as dot notation (https://www.tbi.univie.ac.at/RNA/ViennaRNA/doc/html/rna_structure_notations.html#dot-bracket-notation)
dots_MFE = extracting_dotnotation(driver,xpath_dots='/html/body/div[2]/div[2]/div/div[3]/pre[2]/span/pre')
dots_centroids = extracting_dotnotation(driver,xpath_dots='/html/body/div[2]/div[2]/div/div[3]/pre[4]/span/pre')

######

# Calculating max. possible score & final score for each siRNA candidate

sums_list = []
for i in range(number_candidates):
    sums_list.append(score4[i] + score6[i] + score7[i] + score8[i] + score9[i] + score10[i] + score12[i] + score13[i] + score14[i] + score15[i] + score16[i] + score17[i] + score18[i] + score19[i] + score20[i])
        
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







