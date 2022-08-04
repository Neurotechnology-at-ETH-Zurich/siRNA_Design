# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 10:30:46 2022

@author: User
"""
from DatasetA_Huesken import all_datasetA, all_datasetA_overhang, inhibition_datasetA
from scoring_13params import collect_antisense, reconstruct_sense, retrieve_sirna_scores, score_overhangs, totalscores, totalscores_no12
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# collect 19nt antisense
antisense_A = collect_antisense(all_datasetA)

# generate 19nt complementary sense sequences
sense_A = reconstruct_sense(antisense_A)

# collect 21nt (with overhang) sequences
overhang_A = collect_antisense(all_datasetA_overhang)

# store number of sequences in a variable (here, nr lowest=nr highest)
number_candidates_A = len(antisense_A)

# retrieve scores
score6_A, weight6, score7_A, weight7, score8_A, weight8, score9_A, weight9, score10_A, weight10, score13_A, weight13, score14_A, weight14, score15_A, weight15, score16_A, weight16, score17_A, weight17, score18_A, weight18, score19_A, weight19, score20_A, weight20  = retrieve_sirna_scores(sense_A, antisense_A, number_candidates_A)

# score overhangs (TT)
score12_A, weight12 = score_overhangs(overhang_A, number_candidates_A)

# calculate total score for each sirna across 14 parameters
sums_A, max_possible =  totalscores(number_candidates_A, score6_A, score7_A, score8_A, score9_A, score10_A, score12_A, score13_A, score14_A, score15_A, score16_A, score17_A, score18_A, score19_A, score20_A, weight6, weight7, weight8, weight9, weight10, weight12, weight13, weight14, weight15, weight16, weight17, weight18, weight19, weight20)

# calculate average score
avg_A = sum(sums_A)/len(sums_A)

###############################################################################

print("Looking at total scores:")

# Plot score sums (y-axis) over inhibition (x-axis)
plt.figure(0)
plt.plot(inhibition_datasetA, sums_A)
plt.xlabel('% inhibition')
plt.ylabel('total score')

# Get Pearson's correlation coefficient
corr,_ = pearsonr(inhibition_datasetA, sums_A)
print('Pearsons correlation: %.3f' % corr)

###############################################################################

print("Looking at total scores without weighting")

sums_A_noweights = []
for i in range(number_candidates_A):
    sum_noweights = score6_A[i] + score7_A[i] + score8_A[i] + score9_A[i] + score10_A[i] + score13_A[i] + score14_A[i] + score15_A[i] + score16_A[i] + score17_A[i] + score18_A[i] + score19_A[i] + score20_A[i]
    sums_A_noweights.append(sum_noweights)
    
# Plot score sums (y-axis) over inhibition (x-axis)
plt.figure(1)
plt.plot(inhibition_datasetA, sums_A_noweights)
plt.xlabel('% inhibition')
plt.ylabel('total score (not weighted)')

# Get Pearson's correlation coefficient
corr,_ = pearsonr(inhibition_datasetA, sums_A_noweights)
print('Pearsons correlation: %.3f' % corr)

###############################################################################

print("Looking at parameter subset (6,7,9,13,17,19):")

# What if we only include the significant parameters? 
# for each sirna, get the sum of param6,7,9,13,14,17,19,20

sums_A_partial = []
for i in range(number_candidates_A):
    sum_partial = score6_A[i]*weight6 + score7_A[i]*weight7 + score9_A[i]*weight9 + score13_A[i]*weight13 + + score14_A[i]*weight14 + score17_A[i]*weight17 + score19_A[i]*weight19 + score20_A[i]*weight20
    sums_A_partial.append(sum_partial)
    
# Plot sum of parameter subset (y-axis) over inhibition (x-axis)
plt.figure(2)
plt.plot(inhibition_datasetA, sums_A_partial)
plt.xlabel('% inhibition')
plt.ylabel('sum of parameter subset')

# Get Pearson's correlation coefficient
corr,_ = pearsonr(inhibition_datasetA, sums_A_partial)
print('Pearsons correlation: %.3f' % corr)

###############################################################################

print("Looking at parameter subset, without weighting")

### now without weighting
sums_A_partial_noweights = []
for i in range(number_candidates_A):
    sum_partial = score6_A[i] + score7_A[i] + score9_A[i] + score13_A[i] + score17_A[i] + score19_A[i] + score14_A[i] + score19_A[i] + score20_A[i]
    sums_A_partial_noweights.append(sum_partial)
    
# Plot sum of parameter subset (y-axis) over inhibition (x-axis)
plt.figure(3)
plt.plot(inhibition_datasetA, sums_A_partial_noweights)
plt.xlabel('% inhibition')
plt.ylabel('sum of parameter subset (not weighted)')

# Get Pearson's correlation coefficient
corr,_ = pearsonr(inhibition_datasetA, sums_A_partial_noweights)
print('Pearsons correlation: %.3f' % corr)

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



"""
### for individual parameters:
# e.g.
plt.plot(inhibition_datasetA, score20_A) # => did this for all parameters, none of them individually shows a trend

"""