# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 10:30:46 2022

@author: Arianna Dorschel

PURPOSE:
This script analyses the Huesken et al. (2004) dataset.
Essentially, it calculates the correlation coefficient between knockdown efficacy and different parameter combinations.
"""
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from openpyxl import Workbook, load_workbook
from DatasetA_Huesken import all_datasetA, all_datasetA_overhang, sorted_dict
from scoring_13params import collect_antisense, reconstruct_sense, retrieve_sirna_scores, score_overhangs, totalscores, totalscores_no12

# get inhibition values from Huesken dataset
inhibition_datasetA = list(sorted_dict.values())

# collect 19nt antisense sequences
antisense_A = collect_antisense(all_datasetA)

# generate 19nt complementary sense sequences
sense_A = reconstruct_sense(antisense_A)

# collect 21nt (with overhang) sequences
overhang_A = collect_antisense(all_datasetA_overhang)

# retrieve scores
score6_A, weight6, score7_A, weight7, score8_A, weight8, score9_A, weight9, score10_A, weight10, score13_A, weight13, score14_A, weight14, score15_A, weight15, score16_A, weight16, score17_A, weight17, score18_A, weight18, score19_A, weight19, score20_A, weight20, number_candidates_A  = retrieve_sirna_scores(sense_A, antisense_A)

# score overhangs (TT)
score12_A, weight12 = score_overhangs(overhang_A, number_candidates_A)

# calculate total score for each sirna across 14 parameters
sums_A, max_possible =  totalscores(number_candidates_A, score6_A, score7_A, score8_A, score9_A, score10_A, score12_A, score13_A, score14_A, score15_A, score16_A, score17_A, score18_A, score19_A, score20_A, weight6, weight7, weight8, weight9, weight10, weight12, weight13, weight14, weight15, weight16, weight17, weight18, weight19, weight20)

# calculate average score
avg_A = sum(sums_A)/len(sums_A)

###############################################################################

#plot_choice = input("What would you like to plot? Write 'A' for total scores, 'B' for total scores (no parameter weighting), 'C' for ")
# 'A':
# 'B':




# PLOT CORRELATIONS (WITHOUT SECONDARY STRUCTURE)

def plot_correlation(inhibition,sums,title='Correlation plot',xlabel='percent inhibition',ylabel='score'):
    print(title)
    
    # plot sums (y-axis) over inhibition (x-axis)
    plt.figure
    #plt.plot(inhibition,sums)
    plt.scatter(inhibition,sums,marker='o',s=3,color='black')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    # get Pearson's correlation coefficient
    corr,_ = pearsonr(inhibition,sums)
    print('Pearsons correlation: %.3f' % corr)
    
# Analyse scores with weighting (14 params)    
plot_correlation(inhibition=inhibition_datasetA, sums=sums_A, title="Looking at total scores:", xlabel='% inhibition', ylabel='total score')

# Analyse total scores without weighting
sums_A_noweights = []
for i in range(number_candidates_A):
    sum_noweights = score6_A[i] + score7_A[i] + score8_A[i] + score9_A[i] + score10_A[i] + score13_A[i] + score14_A[i] + score15_A[i] + score16_A[i] + score17_A[i] + score18_A[i] + score19_A[i] + score20_A[i]
    sums_A_noweights.append(sum_noweights)
    
plot_correlation(inhibition=inhibition_datasetA,sums=sums_A_noweights, title="Looking at total scores without weighting:", xlabel='% inhibition', ylabel='total score (not weighted)')

# PLOT CORRELATIONS (WITH SECONDARY STRUCTURE)
# Problem - Not available for each siRNA sequence 

# get only scores and efficacies of cases where structure could be scored
def exclude_unscored(sirna_scores, efficacies):
    
    # 1. identify in which cases structure could not be scored
    
    indices_string = []
    scores_nostring = []
    
    for i in range(len(sirna_scores)):
        score = sirna_scores[i]
        if isinstance(score,str) == True:
            indices_string.append(i) # 496 sequences
        else:
            scores_nostring.append(score) # 1935
                        
    # 2. now exclude those entries from efficacy list for which we don't have a score

    # create a copy of inhibition values
    efficacies_scored = inhibition_datasetA.copy()

    for index in sorted(indices_string, reverse=True):
        del efficacies_scored[index]
        
    return scores_nostring, efficacies_scored, indices_string

scores_nostring, efficacies_scored, indices_string = exclude_unscored(sirna_scores, efficacies)


   

def incl_param12(sums,indices_string, scores_nostring):
# indices_string = list of indices showing which siRNA secondary structure scoring returned an error message (=string)
# scores_nostring = list of secondary structure scores for siRNAs which did not return error message during scoring (=string)
    sums_plus12 = sums.copy()
    
    for index in sorted(indices_string, reverse=True):
        del sums_plus12[index]
        
    # now add score 12
    for i in range(len(sums_plus12)):
        sums_plus12[i] = sums_plus12[i] + scores_nostring[i]
        
    return sums_plus12



    
# Analyse total scores (weighted) incl. param 12
sums_plus12 = incl_param12(sums_A,indices_string,scores_nostring)
plot_correlation(inhibition=efficacies_scored,sums=sums_plus12, title="Weighted, total scores, incl param12")

# Analyse total scores (unweighted) incl. param12
sums_plus12_noweights = incl_param12(sums_A_noweights,indices_string,scores_nostring)
plot_correlation(inhibition=efficacies_scored,sums=sums_plus12_noweights, title="Unweighted, total scores, incl param12")

###############################################################################

print("Looking at parameter subset (6,7,9,13,17,19):")

# What if we only include the significant parameters? 
# for each sirna, get the sum of param6,7,9,13,14,17,19,20

sums_A_partial = []
for i in range(number_candidates_A):
    sum_partial = score6_A[i]*weight6 + score7_A[i]*weight7 + score9_A[i]*weight9 + score13_A[i]*weight13 + + score14_A[i]*weight14 + score17_A[i]*weight17 + score19_A[i]*weight19 + score20_A[i]*weight20
    sums_A_partial.append(sum_partial)
    
# Plot sum of parameter subset (y-axis) over inhibition (x-axis)
plt.figure(3)
plt.plot(inhibition_datasetA, sums_A_partial)
plt.xlabel('% inhibition')
plt.ylabel('sum of parameter subset')

# Get Pearson's correlation coefficient
corr,_ = pearsonr(inhibition_datasetA, sums_A_partial)
print('Pearsons correlation: %.3f' % corr)

###############################################################################

print("Looking at this parameter subset, without weighting")

### now without weighting
sums_A_partial_noweights = []
for i in range(number_candidates_A):
    sum_partial = score6_A[i] + score7_A[i] + score9_A[i] + score13_A[i] + score17_A[i] + score19_A[i] + score14_A[i] + score19_A[i] + score20_A[i]
    sums_A_partial_noweights.append(sum_partial)
    
# Plot sum of parameter subset (y-axis) over inhibition (x-axis)
plt.figure(4)
plt.plot(inhibition_datasetA, sums_A_partial_noweights)
plt.xlabel('% inhibition')
plt.ylabel('sum of parameter subset (not weighted)')

# Get Pearson's correlation coefficient
corr,_ = pearsonr(inhibition_datasetA, sums_A_partial_noweights)
print('Pearsons correlation: %.3f' % corr)

"""
# TODO: check which combination of parameters reaches the highest correlation coefficient
# for now, do this without weights
def sums_param_combinations(score6,score7,score8,score9,score10): # as inputs you would need all parameters
    scores = [score6,score7,score8,score9,score10]
    sums = []
    # how can we get all possible combinations?
    
    for i in range(len(scores)):
        score6 + score7 # etc
        # score6 + score7
        # score6 + score7 + score8
        # 
    
    # score6+score7
    # score6+score7+score8 etc...
"""
    

# for each sirna, get the sum of param6,7,9,13,17,19 (significant across 3 datasets)
sums_A_partial = []
for i in range(number_candidates_A):
    sum_partial = score6_A[i]*weight6 + score7_A[i]*weight7 + score9_A[i]*weight9 + score13_A[i]*weight13 + score17_A[i]*weight17 + score19_A[i]*weight19
    sums_A_partial.append(sum_partial)
    
# Plot sum of parameter subset (y-axis) over inhibition (x-axis)
plt.figure(1)
plt.plot(inhibition_datasetA, sums_A_partial)
plt.xlabel('% inhibition')
plt.ylabel('sum of parameter subset')

# Get Pearson's correlation coefficient
corr,_ = pearsonr(inhibition_datasetA, sums_A_partial)
print('Pearsons correlation: %.3f' % corr)




"""
### for individual parameters:
# e.g.
plt.plot(inhibition_datasetA, score20_A) # => did this for all parameters, none of them individually shows a trend

"""