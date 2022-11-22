# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 09:44:32 2022

@author: User
"""
from collecting_results import user_input, setup, sirna_wizard, sidesign, sidirect, thermoblockit, eurofins, oligowalk, sfold, lists_str2int, list_str2int
from helper_functions import pickle_positions, multiple_recommended, colour_targets, retrieve_sirnas

# necessary to perform webscraping
chromedriver_path = r'C:\Users\User\Downloads\chromedriver_win32 (2)\chromedriver.exe'
"""
If you get an error here, an update might be needed; therefore download the suitable chromedriver version for your chrome version here:
https://sites.google.com/chromium.org/driver/downloads?authuser=0 and add new path to exe file
Note: You can find out your google chrome version by clicking Help>About Google Chrome
"""

# collect user inputs
filename, gene_name, NT_sequence, FASTA_sequence, email = user_input()

# generate excel sheet to store results & create list to store all recommended sequences
excel_workbook, sheet, all_recommended = setup(chromedriver_path, filename, gene_name, NT_sequence, FASTA_sequence)

# collect results from thermo blockit
all_recommended, targetpositions_blockit, sheet = thermoblockit(all_recommended, chromedriver_path, gene_name, NT_sequence, excel_workbook, sheet, filename)

# collect results from sirna wizard
all_recommended, targetpositions_wiz, sheet = sirna_wizard(all_recommended, chromedriver_path, gene_name, NT_sequence, excel_workbook, sheet, filename)

# collect results from sidirect
all_recommended, targetpositions_sidirect, sheet = sidirect(all_recommended, chromedriver_path, gene_name, NT_sequence, excel_workbook, sheet, filename)

# collect results from sidesign
all_recommended, targetpositions_sidesign, sheet = sidesign(all_recommended, chromedriver_path, gene_name, FASTA_sequence, excel_workbook, sheet, filename)

# collect results from eurofins # note - this site is super buggy, might have to skip at times or retry until it works
#all_recommended, targetpositions_eurofins, sheet = eurofins(all_recommended, chromedriver_path, gene_name, NT_sequence, excel_workbook, sheet, filename)

# collect results from oligowalk
all_recommended, targetpositions_oligowalk, sheet = oligowalk(all_recommended, chromedriver_path, gene_name, NT_sequence, email, excel_workbook, sheet, filename)

# collect results from sfold
all_recommended, targetpositions_sfold, allstartpositions, sense_sequences, antisense_sequences, sheet = sfold(all_recommended, chromedriver_path, gene_name, NT_sequence, email, excel_workbook, sheet, filename)

# convert all recommended target positions to integers
all_recommended = lists_str2int(all_recommended)

print("FINISHED COLLECTING RESULTS FOR " + gene_name)

# COMPARING ACROSS SOFTWARES

# create single list containing all recommended
all_recommended_unified = []
for recommended_list in all_recommended:
    all_recommended_unified = all_recommended_unified + recommended_list
# RETRIEVE SENSE AND ANTISENSE FROM SFOLD
recommended_sense_sequences, recommended_antisense_sequences = retrieve_sirnas(all_recommended_unified, sense_sequences, antisense_sequences, allstartpositions)


# find duplicates
def find_duplicates(mylist):
    duplicates = []
    for i in range(0,len(mylist)):
        for j in range(i+1,len(mylist)):
            if mylist[i] == mylist[j]:
                duplicates.append(mylist[j])
                
    duplicates = list(set(duplicates))
    
    return duplicates

# find triplicates
def find_triplicates(mylist):
    triplicates = []
    for i in range(0,len(mylist)):
        for j in range(i+1,len(mylist)):
            for k in range(j+1,len(mylist)):
                if mylist[i] == mylist[j] and mylist[i] == mylist[k]:
                    triplicates.append(mylist[j])
                    
    triplicates = list(set(triplicates))
    
    return triplicates

duplicates_recommended = find_duplicates(all_recommended_unified)
# RETRIEVE DUPLICATE SENSE AND ANTISENSE FROM SFOLD
duplicate_sense_sequences, duplicate_antisense_sequences = retrieve_sirnas(duplicates_recommended, sense_sequences, antisense_sequences, allstartpositions)

triplicates_recommended = find_triplicates(all_recommended_unified)
# RETRIEVE TRIPICATE SENSE AND ANTISENSE FROM SFOLD
triplicate_sense_sequences, triplicate_antisense_sequences = retrieve_sirnas(triplicates_recommended, sense_sequences, antisense_sequences, allstartpositions)

# CREATE A LIST OF THE DUPLICATES AND TRIPLICATES
pickle_positions("duplicate positions", duplicates_recommended)
pickle_positions("triplicate positions", triplicates_recommended)

# RETRIEVE ALL SENSE AND ANTISENSE FOR RECOMMENDED SIRNAS
recommended_sense_sequences, recommended_antisense_sequences = retrieve_sirnas(all_recommended_unified, sense_sequences, antisense_sequences, allstartpositions)

# RETRIEVE DUPLICATE SENSE AND ANTISENSE FROM SFOLD
duplicate_sense_sequences, duplicate_antisense_sequences = retrieve_sirnas(duplicates_recommended, sense_sequences, antisense_sequences, allstartpositions)

# RETRIEVE TRIPLICATE SENSE AND ANTISENSE FROM SFOLD
triplicate_sense_sequences, triplicate_antisense_sequences = retrieve_sirnas(triplicates_recommended, sense_sequences, antisense_sequences, allstartpositions)

# SAVE TRIPLICATE SIRNAS
pickle_positions("triplicate sense sequences", triplicate_sense_sequences)
pickle_positions("triplicate antisense sequences", triplicate_antisense_sequences)

# HIGHLIGHT TRIPLICATE REGIONS ON NCBI SEQUENCE
colour_sequence = colour_targets(NT_sequence, triplicate_sense_sequences)
print(colour_sequence)






"""
# function for finding intersections between specific softwares
def finding_intersections(list1,list2):
    list1_as_set = set(list1)
    intersection = list1_as_set.intersection(list2)
    
    return intersection

# retrieve recommended positions from excel and get corresponding sequences
def all_recommended(filename, workbook, sheet):
    allstartpositions = []
    
    for row in sheet.iter_rows():
        for cell in row:
            allstartpositions.append(cell.value)
            
    # Remove all none  values
    allstartpositions = [i for i in allstartpositions if i]
    # Remove header info
    allstartpositions = allstartpositions[13:] 
    
    # Get all recommended sirnas
    recommended_list = [item for item, count in collections.Counter(allstartpositions).items() if count > 0]
    
    return recommended_list

recommended_list = all_recommended(filename, excel_workbook, sheet)
recommended_sense_sequences, recommended_antisense_sequences = retrieve_sirnas(recommended_list,sense_sequences,antisense_sequences,allstartpositions)
"""