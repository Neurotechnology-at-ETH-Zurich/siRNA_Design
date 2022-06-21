# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 17:29:29 2021

@author: User
"""

import time
from helper_functions import collect_input, generate_workbook, load_workbook, find_title_location, add_results, pickle_positions, multiple_recommended, colour_targets, retrieve_sirnas
from sirna_wizard import perform_query_sirnawiz, count_results, collect_target_positions
from Thermo_BLOCKIT import perform_query_blockit, count_results_blockit, collect_target_positions_blockit
from siDESIGN_center import perform_query_sidesign, count_results_sidesign, collect_target_positions_sidesign
from siDirect import perform_query_sidirect, count_results_sidirect, collect_target_positions_sidirect
from Oligowalk import perform_query_oligowalk, count_results_oligowalk, collect_target_positions_oligowalk
from Eurofins_siMax import perform_query_eurofins, count_results_eurofins, collect_target_positions_eurofins
from sFold import perform_query_sFold, thresh_results, all_sequences

# Omitted:
# IDT (different design, 25nt Custom Dicer substrates)
# RNAi explorer from genelink (page is faulty, cannot retrieve results)


"""
About the input sequence we give:
a) Make sure it begins at start codon and not some restriction site.
E.g. in the case of our pgl3 plasmid, starting at ATG at pos 280
b) Also make sure the sequence does not include introns => if it would, we would have to include parameter 5 (not in the intron)

"""

path = "C:/Users/User/Desktop/ETH_NSC/Yanik_lab/Luciferase_siRNA/Test_CodePipeline/" # is this a) correct, b) necessary?
chromedriver_path = r'C:\Users\User\Downloads\new_chromedriver_win32\chromedriver.exe'
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

# 2. siDESIGN_center ##CHECK WHICH ALGORITHMS ARE BEING SELECTED!!
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
time.sleep(10)
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

# Check whether sequence is over 10k nucleotides
if len(NT_sequence) < 10000:
    print("Sequence length ok for Oligowalk analysis")
    
    # Perform query on Oligowalk website
    driver = perform_query_oligowalk(chromedriver_path, gene_name, NT_sequence, email)
    # Wait for email with results to be sent...then copy link to the siRNA candidates and paste when prompted to in the next function
    # e.g. http://rna.urmc.rochester.edu/cgi-bin/server_exe/oligowalk/oligowalk_out.cgi?file=oligowalk830183772211061summary.htm
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
    
else:
    print("Sequence too long, needs to be split up for Oligowalk analysis")
    
    sequence_part1 = NT_sequence[:9999]
    sequence_part2 = NT_sequence[9979:] # include the 20nts before cutoff to make sure that no potential 21nt candidate is affected by our splitting of the data

    # Perform query for part 1    
    gene_name_oligowalk = gene_name + 'pt1'
    driver = perform_query_oligowalk(chromedriver_path, gene_name_oligowalk, sequence_part1, email)
    driver, rownumber_oligowalk, resultscount_oligowalk = count_results_oligowalk(chromedriver_path)
    targetpositions_oligowalk = collect_target_positions_oligowalk(driver, resultscount_oligowalk)
    # adcy1 mouse: http://rna.urmc.rochester.edu/cgi-bin/server_exe/oligowalk/oligowalk_out.cgi?file=oligowalk447748647377924summary.htm

    # Perform query for part 2
    gene_name_oligowalk = gene_name + 'pt2'
    driver = perform_query_oligowalk(chromedriver_path, gene_name_oligowalk, sequence_part2, email)
    driver, rownumber_oligowalk2, resultscount_oligowalk2 = count_results_oligowalk(chromedriver_path)
    targetpositions_oligowalk2 = collect_target_positions_oligowalk(driver, resultscount_oligowalk2) 
    #adcy1 mouse: http://rna.urmc.rochester.edu/cgi-bin/server_exe/oligowalk/oligowalk_out.cgi?file=oligowalk22680717877029summary.htm

    # Combine the results into one list
    targetpositions_oligowalk.extend(targetpositions_oligowalk2)
    
    # Save target positions to disk
    pickle_positions("oligowalk_list", targetpositions_oligowalk)
    # Find location in excel file to add Oligowalk results to
    titleposition_oligowalk, colrow_oligowalk = find_title_location(targetpositions_oligowalk, excel_workbook, sheet, cell_title='Oligowalk')
    # Add results to excel file
    sheet = add_results(targetpositions_oligowalk, excel_workbook, sheet, colrow_oligowalk)
    driver.close()


# 7. sFold hits over 12
if len(NT_sequence) < 10000:
    print("Sequence length ok for sFold analysis")

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
    
else:
    print("Sequence too long, needs to be split up for sFold analysis")
    
    sequence_part1 = NT_sequence[:9999]
    sequence_part2 = NT_sequence[9979:] # include the 20nts before cutoff to make sure that no potential 21nt candidate is affected by our splitting of the data

    # Perform query for part 1    
    gene_name_sFold = gene_name + 'pt1'
    # Perform query on sFold website
    perform_query_sFold(chromedriver_path, gene_name_sFold, sequence_part1, email)
    # Retrieve results over 12 (need  to paste link received in email
    # e.g. https://sfold.wadsworth.org/output/0528115435.23487/sirna.html
    results_link, driver, targetpositions_sfold = thresh_results(chromedriver_path)
    # Retrieve all possible sense and antisense sequences
    sense_sequences, antisense_sequences, allstartpositions = all_sequences(results_link, chromedriver_path)
    
    # last sense sequence of batch 1 = first sense sequence of batch 2 -> delete duplicate
    sense_sequences = sense_sequences[:-1]
    antisense_sequences = antisense_sequences[:-1]
    allstartpositions = allstartpositions[:-1]

    # store only first part for later (need to split up again for secondary structure prediction)
    sense_sequences1 = sense_sequences.copy()
    pickle_positions("sense_list_pt1",sense_sequences1)
    
    ###new
    # Perform query for part 2
    gene_name_sFold = gene_name + 'pt2'
    # Perform query on sFold website
    perform_query_sFold(chromedriver_path, gene_name_sFold, sequence_part2, email)
    # Retrieve results over 12 - need to paste link received in email
    # e.g. https://sfold.wadsworth.org/output/0621032446.12305/sirna.html
    results_link, driver, targetpositions_sfold2 = thresh_results(chromedriver_path)
    # Retrieve all possible sense and antisense sequences
    sense_sequences2, antisense_sequences2, allstartpositions2 = all_sequences(results_link, chromedriver_path)
    
    # add offset to all start positions (e.g. in the case of mouse adcy1, 9840) 
    # so that sequences of the second half are also matched to the correct position on mRNA
    allstartpositions2_corrected = []
    
    for i in range(len(allstartpositions2)):
        mrna_position = i + int(allstartpositions[-1]) + 1
        allstartpositions2_corrected.append(mrna_position)

    # add offset to target positions
    # so that the sequences of the second have are also matched to the correct position on mRNA
    targetpositions_sfold2_corrected = []
    
    for pos in targetpositions_sfold2:
        mrna_position = int(pos) + int((allstartpositions[-1])) - 2
        targetpositions_sfold2_corrected.append(mrna_position)
    
    # store only second part for later (need to split up again for secondary structure prediction)
    pickle_positions("sense_list_pt2",sense_sequences2)
    
    # Combine the results into one list

    targetpositions_sfold.extend(targetpositions_sfold2_corrected)    
    sense_sequences.extend(sense_sequences2)
    antisense_sequences.extend(antisense_sequences2)
    allstartpositions.extend(allstartpositions2_corrected)
    
    # Save target positions to disk
    pickle_positions("sFold_list", targetpositions_sfold)
    # Find location in excel file to add sFold results to
    titleposition_sfold, colrow_sfold = find_title_location(targetpositions_sfold, excel_workbook, sheet, cell_title='sFold_over12')
    # Add results to excel file
    sheet = add_results(targetpositions_sfold, excel_workbook, sheet, colrow_sfold)
    
    # store list of all possible positions
    pickle_positions("sense_list", sense_sequences)
    pickle_positions("antisense_list", antisense_sequences)
    pickle_positions("allstartpositions", allstartpositions)
    
    # if you want to check whether they are unique:
    """
    unique_sense_list = set(sense_sequences)
    print(len(list(unique_sense_list)))
    """
    
    """
    checking which elements occur in duplicate
     import collections
     print([item for item, count in collections.Counter(allstartpositions).items() if count > 1])
    """
    
    driver.close()

# COMPARING ACROSS SOFTWARES

# CREATE A LIST OF THE DUPLICATES AND TRIPLICATES
duplicate_list, triplicate_list = multiple_recommended(filename, excel_workbook, sheet)
pickle_positions("duplicate positions", duplicate_list)
pickle_positions("triplicate positions", triplicate_list)

# RETRIEVE DUPLICATE SENSE AND ANTISENSE FROM SFOLD
duplicate_sense_sequences, duplicate_antisense_sequences = retrieve_sirnas(duplicate_list, sense_sequences, antisense_sequences, allstartpositions)

# RETRIEVE TRIPLICATE SENSE AND ANTISENSE FROM SFOLD
triplicate_sense_sequences, triplicate_antisense_sequences = retrieve_sirnas(triplicate_list, sense_sequences, antisense_sequences, allstartpositions)

# SAVE TRIPLICATE SIRNAS
pickle_positions("triplicate sense sequences", triplicate_sense_sequences)
pickle_positions("triplicate antisense sequences", triplicate_antisense_sequences)

# HIGHLIGHT TRIPLICATE REGIONS ON NCBI SEQUENCE
colour_sequence = colour_targets(NT_sequence, triplicate_sense_sequences)
print(colour_sequence)


