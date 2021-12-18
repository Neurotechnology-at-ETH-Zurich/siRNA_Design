# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 17:29:29 2021

@author: User
"""

import time
from helper_functions import collect_input, generate_workbook, load_workbook, find_title_location, add_results, pickle_positions, multiple_recommended
from sirna_wizard import perform_query_sirnawiz, count_results, collect_target_positions
from Thermo_BLOCKIT import perform_query_blockit, count_results_blockit, collect_target_positions_blockit
from siDESIGN_center import perform_query_sidesign, count_results_sidesign, collect_target_positions_sidesign
from siDirect import perform_query_sidirect, count_results_sidirect, collect_target_positions_sidirect
from Oligowalk import perform_query_oligowalk, count_results_oligowalk, collect_target_positions_oligowalk
from Eurofins_siMax import perform_query_eurofins, count_results_eurofins, collect_target_positions_eurofins
from sFold import perform_query_sFold, thresh_results, all_sequences

# Still to complete:
from IDT import perform_query_IDT, count_results_IDT

# Missing: 
# RNAi explorer (genelink) => page faulty at the moment

"""
About the input sequence we give:
a) Make sure it begins at start codon and not some restriction site.
E.g. in the case of our pgl3 plasmid, starting at ATG at pos 280
b) Also make sure the sequence does not include introns => if it would, we would have to include parameter 5 (not in the intron)

"""

path = "C:/Users/User/Desktop/ETH_NSC/Yanik_lab/Luciferase_siRNA/Test_CodePipeline/" # is this a) correct, b) necessary?
chromedriver_path = r'C:\Users\User\Downloads\chromedriver_win32 (3)\chromedriver.exe'
# If you get an error here, an update might be needed; therefore download the suitable chromedriver version for your chrome version here:
# https://sites.google.com/chromium.org/driver/downloads?authuser=0 and add new path to exe file
# Note: You can find out your google chrome version by clicking Help>About Google Chrome
filename = "test.xlsx"
gene_name, NT_sequence, FASTA_sequence, email = collect_input()
# Save NT sequence to disk
pickle_positions("NT_sequence", NT_sequence)
excel_workbook, sheet = generate_workbook(gene_name, NT_sequence, FASTA_sequence, filename)

# 1. siRNA Wizard
print("siRNA Wizard analysis")
# Perform query on siRNA wizard website
driver = perform_query_sirnawiz(chromedriver_path, gene_name, NT_sequence)
# Count number of results
driver, rownumber_wiz, resultscount_wiz = count_results(driver)
# Collect the target positions suggested by the software
columnlist_wiz, targetpositions_wiz = collect_target_positions(driver, rownumber_wiz)
# Save target positions to disk
pickle_positions("wiz_list", targetpositions_wiz)
# Find location in excel file to add siDESIGN results to
titleposition_wiz, colrow_wiz = find_title_location(targetpositions_wiz, excel_workbook, sheet, cell_title='siRNA_wizard')
# Add results to excel file
sheet = add_results(targetpositions_wiz, excel_workbook, sheet, colrow_wiz)
driver.close()

# 2. siDESIGN_center
print("siDESIGN center analysis")
# Perform query on siDESIGN website
driver = perform_query_sidesign(chromedriver_path, gene_name, FASTA_sequence)
# Let results page load
time.sleep(5)
# Count number of results
driver, rownumber_sidesign, resultscount_sidesign = count_results_sidesign(driver)
# Collect the target positions suggested by the software
targetpositions_sidesign = collect_target_positions_sidesign(driver, resultscount_sidesign)
# Save target positions to disk
pickle_positions("siDESIGN_list", targetpositions_sidesign)
# Find location in excel file to add siDESIGN results to
titleposition_sidesign, colrow_sidesign = find_title_location(targetpositions_sidesign, excel_workbook, sheet, cell_title='siDESIGN_center')
# Add results to excel file
sheet = add_results(targetpositions_sidesign, excel_workbook, sheet, colrow_sidesign)
driver.close()

# 3. siDirect
print("siDirect center analysis")
# Perform query on siDirect website
driver = perform_query_sidirect(chromedriver_path, gene_name, NT_sequence)
time.sleep(5)
# Count number of results
driver, rownumber_sidirect, resultscount_sidirect = count_results_sidirect(driver)
# Collect the target positions suggested by the software
targetpositions_sidirect = collect_target_positions_sidirect(driver, resultscount_sidirect)
# Only take the start position out of the range they give (select text before '-' character)
for i in range(len(targetpositions_sidirect)):
    targetpositions_sidirect[i] = targetpositions_sidirect[i].rpartition('-')[0]
# Save target positions to disk
pickle_positions("sidirect_list", targetpositions_sidirect)
# Find location in excel file to add siDirect results to
titleposition_sidirect, colrow_sidirect = find_title_location(targetpositions_sidirect, excel_workbook, sheet, cell_title='siDirect')
# Add results to excel file
sheet = add_results(targetpositions_sidirect, excel_workbook, sheet, colrow_sidirect)
driver.close()

# 4. Thermo_BLOCKIT
print("Thermo BLOCKIT analysis")
# Perform query on Thermo BLOCKIT website
driver = perform_query_blockit(chromedriver_path, gene_name, NT_sequence)
# Let results page load
time.sleep(5)
# Count number of results
driver, rownumber_blockit, resultscount_blockit = count_results_blockit(driver)
# Collect the target positions suggested by the software
targetpositions_blockit = collect_target_positions_blockit(driver, resultscount_blockit) ##TROUBLESHOOT HERE!!!
# Save target positions to disk
pickle_positions("blockit_list", targetpositions_blockit)
# Find location in excel file to add Thermo BLOCKIT results to
titleposition_blockit, colrow_blockit = find_title_location(targetpositions_blockit, excel_workbook, sheet, cell_title='BLOCKIT')
# Add results to excel file
sheet = add_results(targetpositions_blockit, excel_workbook, sheet, colrow_blockit)
driver.close()

# 5. Eurofins_siMax
print("Eurofins_siMax analysis")
# Perform query on Eurofins website
driver = perform_query_eurofins(chromedriver_path, gene_name, NT_sequence)
# Wait for results page to load
time.sleep(5)
# Count number of results
rows = count_results_eurofins(driver)
time.sleep(10)
# !! Collect results, add +3 to receive position that siRNA will actually target on mRNA (DOUBLE CHECK!!)
targetpositions_eurofins = collect_target_positions_eurofins(driver, rows) ###
# Save target positions to disk
pickle_positions("eurofins_list", targetpositions_eurofins)
# Find location in excel file to add Eurofins results to
titleposition_eurofins, colrow_eurofins = find_title_location(targetpositions_eurofins, excel_workbook, sheet, cell_title='Eurofins_siMax')
# Add results to excel file
sheet = add_results(targetpositions_eurofins, excel_workbook, sheet, colrow_eurofins)
driver.close()

# 6: OLIGOWALK
print("Oligowalk analysis")
# Perform query on Oligowalk website
driver = perform_query_oligowalk(chromedriver_path, gene_name, NT_sequence, email)
# Wait for email with results to be sent...then copy link to the siRNA candidates and paste when prompted to in the next function
# e.g. http://rna.urmc.rochester.edu/cgi-bin/server_exe/oligowalk/oligowalk_out.cgi?file=oligowalk950865362378867summary.htm
# Count number of results with probability of being efficient siRNA over 80%
driver, rownumber_oligowalk, resultscount_oligowalk = count_results_oligowalk(chromedriver_path)
# Collect target positions
targetpositions_oligowalk = collect_target_positions_oligowalk(driver, resultscount_oligowalk)
# Save target positions to disk
pickle_positions("oligowalk_list", targetpositions_oligowalk)
# Find location in excel file to add Oligowalk results to
titleposition_oligowalk, colrow_oligowalk = find_title_location(targetpositions_oligowalk, excel_workbook, sheet, cell_title='Oligowalk')
# Add results to excel file
sheet = add_results(targetpositions_oligowalk, excel_workbook, sheet, colrow_oligowalk)
driver.close()

# 7. sFold hits over 12
print("sFold analysis: identifying candidates with score > 12")
# Perform query on sFold website
perform_query_sFold(chromedriver_path, gene_name, NT_sequence, email)
# Retrieve results over 12 (need  to paste link received in email, e.g. http://sfold.wadsworth.org/output/1115053901.27294/)
results_link, driver, targetpositions_sfold = thresh_results(chromedriver_path)
# Save target positions to disk
pickle_positions("sFold_list", targetpositions_sfold)
# Find location in excel file to add sFold results to
titleposition_sfold, colrow_sfold = find_title_location(targetpositions_sfold, excel_workbook, sheet, cell_title='sFold_over12')
# Add results to excel file
sheet = add_results(targetpositions_sfold, excel_workbook, sheet, colrow_sfold)
driver.close()

# Collect data on all sense and antisense sequences for position 3 to 1635
sense_sequences, antisense_sequences, allstartpositions = all_sequences(results_link, chromedriver_path)
pickle_positions("sense_list", sense_sequences)
pickle_positions("antisense_list", antisense_sequences)
pickle_positions("allstartpositions", allstartpositions)

"""
# 8. IDT: UNFINISHED
print("IDT analysis")
# Perform query on IDT page
driver = perform_query_IDT(chromedriver_path, FASTA_sequence)
# Enumerate and retrieve results
driver, pos_list = count_results_IDT(driver) ###?
"""

# CREATE A LIST OF THE DUPLICATES/THE TARGET POSITIONS WE WANT TO ANALYSE
duplicate_list, triplicate_list = multiple_recommended(filename, excel_workbook, sheet)
pickle_positions("duplicate positions", duplicate_list)
pickle_positions("triplicate positions", triplicate_list)

# RETRIEVE CORRESPONDING SENSE AND ANTISENSE FROM SFOLD
triplicate_sense_sequences = []
triplicate_antisense_sequences = []

for i in range(len(triplicate_list)):
    position = triplicate_list[i]
    index = allstartpositions.index(position)
    sense = sense_sequences[index]
    antisense = antisense_sequences[index]
    triplicate_sense_sequences.append(sense)
    triplicate_antisense_sequences.append(antisense)
    
pickle_positions("triplicate sense sequences", triplicate_sense_sequences)
pickle_positions("triplicate antisense sequences", triplicate_antisense_sequences)

