# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 13:02:05 2022

@author: User
"""
from scipy import stats
from helperfunctions import excel_results, excel_addnewdataset, excel_addaverages, remove_overhangs, ttests_parameters
from DatasetA_Huesken import lowest, highest, lowest_overhang, highest_overhang
from DatasetB_Ichihara import antisense_below10_B_overhang, antisense_above90_B_overhang # get them with the overhang
from DatasetC_Mysara import antisense_below10_C_overhang, antisense_above90_C_overhang #  get them with overhang
from DatasetD_Fellmann import antisense_below10_D, antisense_above90_D
from scoring_13params import collect_antisense, reconstruct_sense, retrieve_sirna_scores, score_overhangs, totalscores, totalscores_no12

# generate excel sheet to store results
excel_workbook, sheet = excel_results('sirna_datasets_results.xlsx')

##################################################
# ANALYSING HALL DATASET 
##################################################
print("Dataset A (Huesken et al.)")

# add name of dataset to excel to C1, as well as the required columns
dataset1_column = 3
sheet.cell(1,dataset1_column).value = 'Dataset A (Huesken et al.)'
# add subcolumns
startpos = 3
excel_workbook, sheet = excel_addnewdataset(startpos, excel_workbook, sheet, 'sirna_datasets_results.xlsx')

# collect 19nt antisense (200 lowest, 200 highest)
antisense_lowest = collect_antisense(lowest)
antisense_highest = collect_antisense(highest)

# generate 19nt complementary sense sequences
sense_lowest = reconstruct_sense(antisense_lowest)
sense_highest = reconstruct_sense(antisense_highest)

# collect 21nt (with overhang) sequences
overhang_lowest = collect_antisense(lowest_overhang)
overhang_highest = collect_antisense(highest_overhang)

# store number of sequences in a variable (here, nr lowest=nr highest)
number_candidates = len(antisense_lowest)

# LET'S HAVE A LOOK AT THE LOW-EFFICIENCY SIRNAS

print("LOWER")

# retrieve scores for low-efficiency sirnas
score6_lowest, weight6, score7_lowest, weight7, score8_lowest, weight8, score9_lowest, weight9, score10_lowest, weight10, score13_lowest, weight13, score14_lowest, weight14, score15_lowest, weight15, score16_lowest, weight16, score17_lowest, weight17, score18_lowest, weight18, score19_lowest, weight19, score20_lowest, weight20  = retrieve_sirna_scores(sense_lowest, antisense_lowest, number_candidates)

# score overhangs (TT)
score12_lowest, weight12 = score_overhangs(overhang_lowest, number_candidates)

# add average for each param to excel => column 3
# e.g. avg of param 6 at (3,3), avg of param 7 at (4,3)
column = 3
excel_addaverages(column, excel_workbook, sheet, 'sirna_datasets_results.xlsx', score6_lowest, score7_lowest, score8_lowest, score9_lowest, score10_lowest, score12_lowest, score13_lowest, score14_lowest, score15_lowest, score16_lowest, score17_lowest, score18_lowest, score19_lowest, score20_lowest)

# calculate total score for each sirna across 14 parameters
lowest_sums, max_possible =  totalscores(number_candidates, score6_lowest, score7_lowest, score8_lowest, score9_lowest, score10_lowest, score12_lowest, score13_lowest, score14_lowest, score15_lowest, score16_lowest, score17_lowest, score18_lowest, score19_lowest, score20_lowest, weight6, weight7, weight8, weight9, weight10, weight12, weight13, weight14, weight15, weight16, weight17, weight18, weight19, weight20)

# add average score of lower efficiency sirnas to excel
sheet.cell(17,column).value = sum(lowest_sums)/len(lowest_sums)

# LET'S HAVE A LOOK AT THE HIGH-EFFICIENCY SIRNAS

print("HIGHER")

# retrieve scores for high-efficiency sirnas
score6_highest, weight6, score7_highest, weight7, score8_highest, weight8, score9_highest, weight9, score10_highest, weight10, score13_highest, weight13, score14_highest, weight14, score15_highest, weight15, score16_highest, weight16, score17_highest, weight17, score18_highest, weight18, score19_highest, weight19, score20_highest, weight20  = retrieve_sirna_scores(sense_highest, antisense_highest, number_candidates)
         
# score overhangs (TT)
score12_highest, weight12 = score_overhangs(overhang_highest, number_candidates)

# add average for each param to excel => column 4
# e.g. avg of param 6 at (3,4), avg of param 7 at (4,4)
column = 4
excel_addaverages(column, excel_workbook, sheet, 'sirna_datasets_results.xlsx', score6_highest, score7_highest, score8_highest, score9_highest, score10_highest, score12_highest, score13_highest, score14_highest, score15_highest, score16_highest, score17_highest, score18_highest, score19_highest, score20_highest)

# calculate total score for each sirna across 14 parameters
highest_sums, max_possible =  totalscores(number_candidates, score6_highest, score7_highest, score8_highest, score9_highest, score10_highest, score12_highest, score13_highest, score14_highest, score15_highest, score16_highest, score17_highest, score18_highest, score19_highest, score20_highest, weight6, weight7, weight8, weight9, weight10, weight12, weight13, weight14, weight15, weight16, weight17, weight18, weight19, weight20)

# add average score of higher efficiency sirnas to excel
sheet.cell(17,column).value = sum(highest_sums)/len(highest_sums) 

print("T-test between total scores of lower- and higher-efficiency sirnas (dataset Hall):")
ttest_totalscores = stats.ttest_ind(lowest_sums, highest_sums)
print(ttest_totalscores)

# T-TESTS FOR INDIVIDUAL PARAMETERS:
# i.e. compare scores of lower population & higher population for each parameter

column_result = 5
column_significance = 6
pvalue = 0.05
sheet = ttests_parameters(column_result, column_significance, pvalue, sheet, score6_lowest, score7_lowest, score8_lowest, score9_lowest, score10_lowest, score12_lowest, score13_lowest, score14_lowest, score15_lowest, score16_lowest, score17_lowest, score18_lowest, score19_lowest, score20_lowest, lowest_sums, score6_highest, score7_highest, score8_highest, score9_highest, score10_highest, score12_highest, score13_highest, score14_highest, score15_highest, score16_highest, score17_highest, score18_highest, score19_highest, score20_highest, highest_sums)

##################################################
# ANALYSING MYSIRNA DATASET B. 19nt + 2nt nucleotide
##################################################
print("Dataset B (Ichihara et al.)")

# add name of dataset to excel to C1, as well as the required columns
dataset2_column = dataset1_column + 4
sheet.cell(1,dataset2_column).value = 'Dataset B (Ichihara et al.)'
# add subcolumns
startpos = startpos + 4
excel_workbook, sheet = excel_addnewdataset(startpos, excel_workbook, sheet, 'sirna_datasets_results.xlsx')

antisense_below10_B = remove_overhangs(antisense_below10_B_overhang)
antisense_above90_B = remove_overhangs(antisense_above90_B_overhang)

sense_below10_B = reconstruct_sense(antisense_below10_B)
sense_above90_B = reconstruct_sense(antisense_above90_B)

print("LOWER")

# store number of sequences in a variable
number_candidates_B = len(sense_below10_B)

# retrieve scores for low-efficiency sirnas
score6_lowest_B, weight6, score7_lowest_B, weight7, score8_lowest_B, weight8, score9_lowest_B, weight9, score10_lowest_B, weight10, score13_lowest_B, weight13, score14_lowest_B, weight14, score15_lowest_B, weight15, score16_lowest_B, weight16, score17_lowest_B, weight17, score18_lowest_B, weight18, score19_lowest_B, weight19, score20_lowest_B, weight20  = retrieve_sirna_scores(sense_below10_B, antisense_below10_B, number_candidates_B) 

# score overhangs (TT)
score12_lowest_B, weight12 = score_overhangs(antisense_below10_B_overhang, number_candidates_B)

# add average for each param to excel => column 7
# e.g. avg of param 6 at (3,7), avg of param 7 at (4,7)
column = 7
excel_addaverages(column, excel_workbook, sheet, 'sirna_datasets_results.xlsx', score6_lowest_B, score7_lowest_B, score8_lowest_B, score9_lowest_B, score10_lowest_B, score12_lowest_B, score13_lowest_B, score14_lowest_B, score15_lowest_B, score16_lowest_B, score17_lowest_B, score18_lowest_B, score19_lowest_B, score20_lowest_B)

# get sums for each sirna of this group
lowest_sums_B, max_possible =  totalscores(number_candidates_B, score6_lowest_B, score7_lowest_B, score8_lowest_B, score9_lowest_B, score10_lowest_B, score12_lowest_B, score13_lowest_B, score14_lowest_B, score15_lowest_B, score16_lowest_B, score17_lowest_B, score18_lowest_B, score19_lowest_B, score20_lowest_B, weight6, weight7, weight8, weight9, weight10, weight12, weight13, weight14, weight15, weight16, weight17, weight18, weight19, weight20)

# add average score of higher efficiency sirnas to excel
sheet.cell(17,column).value = sum(lowest_sums)/len(lowest_sums) 

print("HIGHER")

# store number of sequences in a variable
number_candidates_B = len(sense_above90_B)

# retrieve scores for high-efficiency sirnas
score6_highest_B, weight6, score7_highest_B, weight7, score8_highest_B, weight8, score9_highest_B, weight9, score10_highest_B, weight10, score13_highest_B, weight13, score14_highest_B, weight14, score15_highest_B, weight15, score16_highest_B, weight16, score17_highest_B, weight17, score18_highest_B, weight18, score19_highest_B, weight19, score20_highest_B, weight20  = retrieve_sirna_scores(sense_above90_B, antisense_above90_B, number_candidates_B) 

# score overhangs (TT)
score12_highest_B, weight12 = score_overhangs(antisense_above90_B_overhang, number_candidates_B)

# add average for each param to excel => column 8
# e.g. avg of param 6 at (3,8), avg of param 7 at (4,8)
column = 8
excel_addaverages(column, excel_workbook, sheet, 'sirna_datasets_results.xlsx', score6_highest_B, score7_highest_B, score8_highest_B, score9_highest_B, score10_highest_B, score12_highest_B, score13_highest_B, score14_highest_B, score15_highest_B, score16_highest_B, score17_highest_B, score18_highest_B, score19_highest_B, score20_highest_B)

# get sums for each sirna of this group
highest_sums_B, max_possible =  totalscores(number_candidates_B, score6_highest_B, score7_highest_B, score8_highest_B, score9_highest_B, score10_highest_B, score12_highest_B, score13_highest_B, score14_highest_B, score15_highest_B, score16_highest_B, score17_highest_B, score18_highest_B, score19_highest_B, score20_highest_B, weight6, weight7, weight8, weight9, weight10, weight12, weight13, weight14, weight15, weight16, weight17, weight18, weight19, weight20)

# add average score of higher efficiency sirnas to excel
sheet.cell(17,column).value = sum(highest_sums_B)/len(highest_sums_B)

print("T-test between total scores of lower- and higher-efficiency sirnas (dataset B):")
ttest_totalscores = stats.ttest_ind(lowest_sums_B, highest_sums_B)
print(ttest_totalscores)

# T-TESTS FOR INDIVIDUAL PARAMETERS:
# i.e. compare scores of lower population & higher population for each parameter

column_result = column_result + 4
column_significance = column_significance + 4
pvalue = 0.05
sheet = ttests_parameters(column_result, column_significance, pvalue, sheet, score6_lowest_B, score7_lowest_B, score8_lowest_B, score9_lowest_B, score10_lowest_B, score12_lowest_B, score13_lowest_B, score14_lowest_B, score15_lowest_B, score16_lowest_B, score17_lowest_B, score18_lowest_B, score19_lowest_B, score20_lowest_B, lowest_sums_B, score6_highest_B, score7_highest_B, score8_highest_B, score9_highest_B, score10_highest_B, score12_highest_B, score13_highest_B, score14_highest_B, score15_highest_B, score16_highest_B, score17_highest_B, score18_highest_B, score19_highest_B, score20_highest_B, highest_sums_B)

##################################################
# ANALYSING MYSIRNA DATASET C. 19nt + 2nt nucleotide
##################################################
print("Dataset C (Mysara et al.)")

# add name of dataset to excel to C1, as well as the required columns
dataset3_column = dataset2_column + 4
sheet.cell(1,dataset3_column).value = 'Dataset C (Mysara et al.)'
# add subcolumns
startpos = startpos + 4
excel_workbook, sheet = excel_addnewdataset(startpos, excel_workbook, sheet, 'sirna_datasets_results.xlsx')

antisense_below10_C = remove_overhangs(antisense_below10_C_overhang)
antisense_above90_C = remove_overhangs(antisense_above90_C_overhang)

sense_below10_C = reconstruct_sense(antisense_below10_C)
sense_above90_C = reconstruct_sense(antisense_above90_C)

print("LOWER")

# store number of sequences in a variable
number_candidates_C = len(sense_below10_C)

# retrieve scores for low-efficiency sirnas
score6_lowest_C, weight6, score7_lowest_C, weight7, score8_lowest_C, weight8, score9_lowest_C, weight9, score10_lowest_C, weight10, score13_lowest_C, weight13, score14_lowest_C, weight14, score15_lowest_C, weight15, score16_lowest_C, weight16, score17_lowest_C, weight17, score18_lowest_C, weight18, score19_lowest_C, weight19, score20_lowest_C, weight20  = retrieve_sirna_scores(sense_below10_C, antisense_below10_C, number_candidates_C) 

# score overhangs (TT)
score12_lowest_C, weight12 = score_overhangs(antisense_below10_C_overhang, number_candidates_C)

# add average for each param to excel => column 11
# e.g. avg of param 6 at (3,11), avg of param 7 at (4,11)
column = 11
excel_addaverages(column, excel_workbook, sheet, 'sirna_datasets_results.xlsx', score6_lowest_C, score7_lowest_C, score8_lowest_C, score9_lowest_C, score10_lowest_C, score12_lowest_C, score13_lowest_C, score14_lowest_C, score15_lowest_C, score16_lowest_C, score17_lowest_C, score18_lowest_C, score19_lowest_C, score20_lowest_C)

# get sums for each sirna of this group
lowest_sums_C, max_possible =  totalscores(number_candidates_C, score6_lowest_C, score7_lowest_C, score8_lowest_C, score9_lowest_C, score10_lowest_C, score12_lowest_C, score13_lowest_C, score14_lowest_C, score15_lowest_C, score16_lowest_C, score17_lowest_C, score18_lowest_C, score19_lowest_C, score20_lowest_C, weight6, weight7, weight8, weight9, weight10, weight12, weight13, weight14, weight15, weight16, weight17, weight18, weight19, weight20)

# add average score of higher efficiency sirnas to excel
sheet.cell(17,column).value = sum(lowest_sums)/len(lowest_sums) 

print("HIGHER")

# store number of sequences in a variable
number_candidates_C = len(sense_above90_C)

# retrieve scores for high-efficiency sirnas
score6_highest_C, weight6, score7_highest_C, weight7, score8_highest_C, weight8, score9_highest_C, weight9, score10_highest_C, weight10, score13_highest_C, weight13, score14_highest_C, weight14, score15_highest_C, weight15, score16_highest_C, weight16, score17_highest_C, weight17, score18_highest_C, weight18, score19_highest_C, weight19, score20_highest_C, weight20  = retrieve_sirna_scores(sense_above90_C, antisense_above90_C, number_candidates_C) 

# score overhangs (TT)
score12_highest_C, weight12 = score_overhangs(antisense_above90_C_overhang, number_candidates_C)

# add average for each param to excel => column 12
# e.g. avg of param 6 at (3,12), avg of param 7 at (4,12)
column = 12
excel_addaverages(column, excel_workbook, sheet, 'sirna_datasets_results.xlsx', score6_highest_C, score7_highest_C, score8_highest_C, score9_highest_C, score10_highest_C, score12_highest_C, score13_highest_C, score14_highest_C, score15_highest_C, score16_highest_C, score17_highest_C, score18_highest_C, score19_highest_C, score20_highest_C)

# get sums for each sirna of this group
highest_sums_C, max_possible =  totalscores(number_candidates_C, score6_highest_C, score7_highest_C, score8_highest_C, score9_highest_C, score10_highest_C, score12_highest_C, score13_highest_C, score14_highest_C, score15_highest_C, score16_highest_C, score17_highest_C, score18_highest_C, score19_highest_C, score20_highest_C, weight6, weight7, weight8, weight9, weight10, weight12, weight13, weight14, weight15, weight16, weight17, weight18, weight19, weight20)

# add average score of higher efficiency sirnas to excel
sheet.cell(17,column).value = sum(highest_sums_C)/len(highest_sums_C)

print("T-test between total scores of lower- and higher-efficiency sirnas (dataset D):")
ttest_totalscores = stats.ttest_ind(lowest_sums_C, highest_sums_C)
print(ttest_totalscores)

# T-TESTS FOR INDIVIDUAL PARAMETERS:
# i.e. compare scores of lower population & higher population for each parameter

column_result = column_result + 4
column_significance = column_significance + 4
pvalue = 0.05
sheet = ttests_parameters(column_result, column_significance, pvalue, sheet, score6_lowest_C, score7_lowest_C, score8_lowest_C, score9_lowest_C, score10_lowest_C, score12_lowest_C, score13_lowest_C, score14_lowest_C, score15_lowest_C, score16_lowest_C, score17_lowest_C, score18_lowest_C, score19_lowest_C, score20_lowest, lowest_sums_C, score6_highest_C, score7_highest_C, score8_highest_C, score9_highest_C, score10_highest_C, score12_highest_C, score13_highest_C, score14_highest_C, score15_highest_C, score16_highest_C, score17_highest_C, score18_highest_C, score19_highest_C, score20_highest_C, highest_sums_C)

##################################################
# ANALYSING MYSIRNA DATASET D. 19nt, no overhang
##################################################
print("Dataset D (Fellman et al.)")

# add name of dataset to excel to C1, as well as the required columns
dataset4_column = dataset3_column + 4
sheet.cell(1,dataset4_column).value = 'Dataset D (Fellman et al.)'
# add subcolumns
startpos = startpos + 4
excel_workbook, sheet = excel_addnewdataset(startpos, excel_workbook, sheet, 'sirna_datasets_results.xlsx')

# generate 19nt complementary sense sequences
sense_below10_D = reconstruct_sense(antisense_below10_D)
sense_above90_D = reconstruct_sense(antisense_above90_D)

print("LOWER")

# store number of sequences in a variable
number_candidates_D = len(sense_below10_D)

# retrieve scores for low-efficiency sirnas
score6_lowest_D, weight6, score7_lowest_D, weight7, score8_lowest_D, weight8, score9_lowest_D, weight9, score10_lowest_D, weight10, score13_lowest_D, weight13, score14_lowest_D, weight14, score15_lowest_D, weight15, score16_lowest_D, weight16, score17_lowest_D, weight17, score18_lowest_D, weight18, score19_lowest_D, weight19, score20_lowest_D, weight20  = retrieve_sirna_scores(sense_below10_D, antisense_below10_D, number_candidates_D) 

# create placeholder variable for param12 (which we cant score here)
score12_lower_placeholder_D = [0]*number_candidates_D

# add average for each param to excel => column 7
# e.g. avg of param 6 at (3,11), avg of param 7 at (4,11)
column = 15
excel_addaverages(column, excel_workbook, sheet, 'sirna_datasets_results.xlsx', score6_lowest_D, score7_lowest_D, score8_lowest_C, score9_lowest_D, score10_lowest_D, score12_lower_placeholder_D, score13_lowest_D, score14_lowest_D, score15_lowest_D, score16_lowest_D, score17_lowest_D, score18_lowest_D, score19_lowest_D, score20_lowest_D)

# get sums for each sirna of this group
lowest_sums_D, max_possible =  totalscores_no12(number_candidates_D, score6_lowest_D, score7_lowest_D, score8_lowest_D, score9_lowest_D, score10_lowest_D, score13_lowest_D, score14_lowest_D, score15_lowest_D, score16_lowest_D, score17_lowest_D, score18_lowest_D, score19_lowest_D, score20_lowest_D, weight6, weight7, weight8, weight9, weight10, weight13, weight14, weight15, weight16, weight17, weight18, weight19, weight20)

# add average score of higher efficiency sirnas to excel
sheet.cell(17,column).value = sum(lowest_sums_D)/len(lowest_sums_D)

# LET'S HAVE A LOOK AT THE HIGH-EFFICIENCY SIRNAS

print("HIGHER")

# store number of sequences in a variable
number_candidates_D = len(sense_above90_D)

# retrieve scores for high-efficiency sirnas
score6_highest_D, weight6, score7_highest_D, weight7, score8_highest_D, weight8, score9_highest_D, weight9, score10_highest_D, weight10, score13_highest_D, weight13, score14_highest_D, weight14, score15_highest_D, weight15, score16_highest_D, weight16, score17_highest_D, weight17, score18_highest_D, weight18, score19_highest_D, weight19, score20_highest_D, weight20  = retrieve_sirna_scores(sense_above90_D, antisense_above90_D, number_candidates_D) 

# create placeholder variable for param12 (which we cant score here)
score12_higher_placeholder_D = [0]*number_candidates_D

# add average for each param to excel => column 8
# e.g. avg of param 6 at (3,8), avg of param 7 at (4,8)
column = 16
excel_addaverages(column, excel_workbook, sheet, 'sirna_datasets_results.xlsx', score6_highest_D, score7_highest_D, score8_highest_D, score9_highest_D, score10_highest_D, score12_higher_placeholder_D, score13_highest_D, score14_highest_D, score15_highest_D, score16_highest_D, score17_highest_D, score18_highest_D, score19_highest_D, score20_highest_D)

# get sums for each sirna of this group
highest_sums_D, max_possible =  totalscores_no12(number_candidates_D, score6_highest_D, score7_highest_D, score8_highest_D, score9_highest_D, score10_highest_D, score13_highest_D, score14_highest_D, score15_highest_D, score16_highest_D, score17_highest_D, score18_highest_D, score19_highest_D, score20_highest_D, weight6, weight7, weight8, weight9, weight10, weight13, weight14, weight15, weight16, weight17, weight18, weight19, weight20)

# add average score of higher efficiency sirnas to excel
sheet.cell(17,column).value = sum(highest_sums_D)/len(highest_sums_D)

print("T-test between total scores of lower- and higher-efficiency sirnas (dataset D):")
ttest_totalscores = stats.ttest_ind(lowest_sums_D, highest_sums_D)
print(ttest_totalscores)

# T-TESTS FOR INDIVIDUAL PARAMETERS:
# i.e. compare scores of lower population & higher population for each parameter

column_result = column_result + 4
column_significance = column_significance + 4
pvalue = 0.05
sheet = ttests_parameters(column_result, column_significance, pvalue, sheet, score6_lowest_D, score7_lowest_D, score8_lowest_D, score9_lowest_D, score10_lowest_D, score12_lower_placeholder_D, score13_lowest_D, score14_lowest_D, score15_lowest_D, score16_lowest_D, score17_lowest_D, score18_lowest_D, score19_lowest_D, score20_lowest_D, lowest_sums_D, score6_highest_D, score7_highest_D, score8_highest_D, score9_highest_D, score10_highest_D, score12_higher_placeholder_D, score13_highest_D, score14_highest_D, score15_highest_D, score16_highest_D, score17_highest_D, score18_highest_D, score19_highest_D, score20_highest_D, highest_sums_D)

# T-TESTS FOR INDIVIDUAL PARAMETERS:
# e.g. compare scores of lower population & higher population for param6
# technically we should first check whether they have independent variances

stats.ttest_ind(score6_lowest_D, score6_highest_D) # etc 

excel_workbook.save('sirna_datasets_results.xlsx')