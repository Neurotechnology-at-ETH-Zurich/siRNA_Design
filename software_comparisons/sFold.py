# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 01:07:42 2021

@author: User
"""
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests
import time

# 1. perform query

def perform_query_sFold(chromedriver_path, gene_name, NT_sequence, email):
    driver = webdriver.Chrome(chromedriver_path)
    driver.get('https://sfold.wadsworth.org/cgi-bin/sirna.pl')
    driver.maximize_window()

    # select batch processing
    select = Select(driver.find_element_by_name('imode'))
    # select by value
    select.select_by_value('0')
    # alternatively: select by visible text
    #select.select_by_visible_text('Batch (current limit of 10000 bases)')

    driver.find_element_by_xpath('/html/body/center/table/tbody/tr[3]/td/form/table/tbody/tr[3]/td[2]/input').send_keys(email)
    driver.find_element_by_xpath('/html/body/center/table/tbody/tr[3]/td/form/table/tbody/tr[4]/td[2]/input').send_keys(gene_name)
    driver.find_element_by_xpath('/html/body/center/table/tbody/tr[3]/td/form/table/tbody/tr[5]/td[2]/textarea').send_keys(NT_sequence)

    driver.find_element_by_name('Submit').click()
    
    time.sleep(5)

# 2. retrieve results
"""
The results will now be sent to email in 1-2 hours
Once you receive email, give the link received by mail here as input
"""
def thresh_results(chromedriver_path):
    results_link = input("Please paste here the link received by e-mail from the sFold server: ")
    print(results_link)
    # e.g. http://sfold.wadsworth.org/output/1115053901.27294/
    driver = webdriver.Chrome(chromedriver_path)
    driver.get(results_link)
    driver.maximize_window()
    
    time.sleep(2)
    
    driver.find_element_by_xpath('/html/body/center/table/tbody/tr[3]/td/table/tbody/tr[5]/td/table/tbody/tr[3]/td[2]/a').click()
    
    time.sleep(2)
    
    # switch to newly opened tab with results
    driver.switch_to_window(driver.window_handles[1])
    
    mytext = driver.find_element_by_xpath('/html/body/pre')
    # Retrieve page text
    pagecontent = mytext.text
    # Turn all space-separated elements into elements of a list
    pagecontent = pagecontent.split()
    # Remove header text
    pagecontent = pagecontent[pagecontent.index('--------------------------------------------------------------------------------')+1:]
    # Number of results
    results_count = int(len(pagecontent)/15) # start is given at every 15th element
    # Create empty list to store start positions
    startpositions = []
    i = 0
    for x in range(results_count):
        startpos = pagecontent[i]
        # Delete hyphen (final character)
        startpos = startpos[:-1]
        i = i+15
        startpositions.append(startpos)

    return results_link, driver, startpositions

# 3. Get all sense and antisense sequences
def all_sequences(results_link, chromedriver_path):
    
    driver = webdriver.Chrome(chromedriver_path)
    driver.get(results_link)
    driver.maximize_window()
    
    time.sleep(2)
    
    driver.find_element_by_xpath('/html/body/center/table/tbody/tr[3]/td/table/tbody/tr[5]/td/table/tbody/tr[4]/td[2]/a').click()
    
    time.sleep(2)
    
    # switch to newly opened tab with results
    driver.switch_to_window(driver.window_handles[1])
    
    mytext = driver.find_element_by_xpath('/html/body/pre')
    # Retrieve page text
    pagecontent = mytext.text
    # Turn all space-separated elements into elements of a list
    pagecontent = pagecontent.split()
    # Remove header text
    pagecontent = pagecontent[pagecontent.index('--------------------------------------------------------------------------------')+1:]
    # Number of results
    results_count = int(len(pagecontent)/15) # start is given at every 15th element
    # Store sense sequences
    sense_sequences = [] # first sequence corresponds to target pos 3
    i = 2
    for x in range(results_count):
        sense = pagecontent[i]
        i = i+15
        sense_sequences.append(sense)
    # Store antisense sequences
    antisense_sequences = []
    i = 3
    for x in range(results_count):
        antisense = pagecontent[i]
        i = i+15
        antisense_sequences.append(antisense)  
    # Store all start position indices, just to be safe
    allstartpositions = []
    i = 0
    for x in range(results_count):
        startpos = pagecontent[i]
        # Delete hyphen (final character)
        startpos = startpos[:-1]
        i = i+15
        allstartpositions.append(int(startpos))
    
        
    return sense_sequences, antisense_sequences, allstartpositions