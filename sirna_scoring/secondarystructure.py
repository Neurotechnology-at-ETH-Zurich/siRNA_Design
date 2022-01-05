# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 16:56:37 2021

@author: User
"""
import re
import pickle
import statistics
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from nt_analysis import read_sequences

sense_list, antisense_list, number_candidates = read_sequences()

def readDNAsequence():
    
    # we will need this for the RNAfold_extractdata function 
    
    path = r'C:/Users/User/Desktop/ETH_NSC/Yanik_lab/siRNADesign-master/software_comparisons'
    filename_NT = '/NT_sequence'
    open_file_NT = open(path+filename_NT,"rb")
    DNAsequence = pickle.load(open_file_NT)
    
    open_file_NT.close()
    
    return DNAsequence

def perform_query_RNAfold(chromedriver_path, NT_sequence):
    
    # automatically performs RNAfold query which returns the secondary structure of our target mRNA
    
    # open website
    driver = webdriver.Chrome(chromedriver_path)
    driver.get('http://rna.tbi.univie.ac.at/cgi-bin/RNAWebSuite/RNAfold.cgi')
    driver.maximize_window()
    
    # enter nt sequence
    driver.find_element_by_xpath('//*[@id="SCREEN"]').send_keys(NT_sequence)
    
    # click proceed
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[3]/form/div[4]/table/tbody/tr/td[2]/input').click()
    
    # wait for results to load
    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[3]/pre[1]/span/pre')))
    except:
        print("took too long to load")
        
    return driver

def extracting_bases(driver,xpath_bases): #xpath for MFE='/html/body/div[2]/div[2]/div/div[3]/pre[1]/span/pre' // xpath for centroids='/html/body/div[2]/div[2]/div/div[3]/pre[3]/span/pre'
    # extract raw text from page (bases)
    bases_raw = driver.find_element_by_xpath(xpath_bases).text
    # this block mainly removes spaces
    for i in range(len(bases_raw)):
        character = bases_raw[i]
        if bases_raw[i] == 'A' or character == 'U' or character == 'G' or character =='C':
            continue
        else:
            bases = bases_raw.replace(bases_raw[i],'')        
    
    # remove newlines
    bases = bases.replace('\n','')
        
    # remove digits
    pattern = r'[0-9]'
    bases = re.sub(pattern,'',bases)
    # note: len of our sequence should be 1653
        
    return bases
    
def extracting_dotnotation(driver,xpath_dots): #xpath for MFE='/html/body/div[2]/div[2]/div/div[3]/pre[2]/span/pre' // xpath for centroids='/html/body/div[2]/div[2]/div/div[3]/pre[4]/span/pre'
    # extract raw text from page (dot notation)
    dots_raw = driver.find_element_by_xpath(xpath_dots).text
    # this block mainly removes spaces
    for i in range(len(dots_raw)):
        character = dots_raw[i]
        if dots_raw[i] == '(' or character == ')' or character == '.':
            continue
        else:
            dots = dots_raw.replace(dots_raw[i],'')

    # remove newlines
    dots = dots.replace('\n','')
    
    # remove digits
    pattern = r'[0-9]'
    dots = re.sub(pattern, '', dots)
    
    return dots   

def findtargetpositions(sense_list, bases_MFE):
    target_indices = []
    #as a next step we want to retrieve a sense sequence to evaluate it for accuracy
    for i in range(len(sense_list)):
        sense_seq_TT = sense_list[i]
        sense_seq = sense_seq_TT[:-2]
        print(sense_seq)
        sense_index = bases_MFE.find(sense_seq) + 1
        print(sense_index)
        print("Sense number " + str(i) + " targets position " + str(sense_index) + " of the mRNA.")
        target_indices.append(sense_index)
        # note to self: double check that what this returns is correct!

    return target_indices

def targetstructure_scoring(bases, dots, sense_list):
    
    """
    optimal secondary structure of siRNA target site:
    high overall number of unpaired bases
    5' loop
    3' loop
    central loops
    """

    startloop_list = []
    endloop_list = []
    nr_unpaired_list = []
    nr_loops_list = []

    for i in range(len(sense_list)):
        # variable containing sense sequence
        sense_TT = sense_list[i]
        sense = sense_TT[:-2]
    
        # retrieve position on mRNA
        targetpos = bases.index(sense) # note that the real position is targetpos+1, remember that python starts at 0!
        # retrieve pairing information (MFE)
        pairing = dots[targetpos:targetpos+21]
    
        # evaluate presence of 5' loop; weight=0.75
        startloop = pairing[0:3]
        if startloop == '...':
            startloop_list.append(0.75)
        else:
            startloop_list.append(0)
        # evaluate presence of  3' loop; weight=0.75
        endloop = pairing[-3:]
        if endloop == '...':
            endloop_list.append(0.75)
        else:
            endloop_list.append(0)
        # evaluate overall number of unpaired bases; weight=0.25
        nr_unpaired = pairing.count('.')
        nr_unpaired_list.append(nr_unpaired)
        # evaluate total number of loops (i.e. including central loops); weight=0.25
        nr_loops = pairing.count('...')
        nr_loops_list.append(nr_loops)
        
        # check whether overall number of unpaired bases is above average
        nr_unpaired_scores = []
        for i in range(len(nr_unpaired_list)):
            if nr_unpaired_list[i] >= statistics.mean(nr_unpaired_list):
                nr_unpaired_scores.append(0.25)
            else:
                nr_unpaired_scores.append(0)
        
        # check whether total number of loops is above average
        nr_loops_scores = []
        for i in range(len(nr_loops_list)):
            if nr_loops_list[i] >= statistics.mean(nr_loops_list):
                nr_loops_scores.append(0.25)
            else:
                nr_loops_scores.append(0)
                
        # calculate total structure score for each sirna
        structure_scores = []
        for (item1, item2, item3, item4) in zip(startloop_list, endloop_list, nr_unpaired_scores, nr_loops_scores):
            structure_scores.append(item1+item2+item3+item4)
            
    weight_structure_scores = 2
        
    return startloop_list, endloop_list, nr_unpaired_scores, nr_loops_scores, structure_scores, weight_structure_scores





