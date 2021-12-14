# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 15:46:42 2021

@author: User
"""
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests
from selenium.common.exceptions import NoSuchElementException

def perform_query_oligowalk(chromedriver_path, gene_name, NT_sequence, email):
    driver = webdriver.Chrome(chromedriver_path)
    driver.get('http://rna.urmc.rochester.edu/cgi-bin/server_exe/oligowalk/oligowalk_form.cgi')
    driver.maximize_window()
    
    # Add sequence name
    # Delete default text
    sequence_name = driver.find_element_by_xpath('//*[@id="seqname"]')
    sequence_name.clear()
    # Add own sequence name
    sequence_name.send_keys(gene_name)
    
    # Add sequence
    # Delete default text
    sequence = driver.find_element_by_xpath('//*[@id="seqtext"]')
    sequence.clear()
    # Add nucleotides
    sequence.send_keys(NT_sequence)
    
    # Add email address
    driver.find_element_by_xpath('//*[@id="email"]').send_keys(email)
    
    # Click submit
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/form/div[1]/div/input[1]').click()
    
    return driver

# The results are then sent by email... here you need to wait a few hours until you get emailed the link.

def count_results_oligowalk(chromedriver_path):
    results_link = input("Please paste here the link to the siRNA candidate page: ")
    # e.g. http://rna.urmc.rochester.edu/cgi-bin/server_exe/oligowalk/oligowalk_out.cgi?file=oligowalk950865362378867summary.htm
    
    driver = webdriver.Chrome(chromedriver_path)
    driver.get(results_link)
    driver.maximize_window()
    
    driver.implicitly_wait(10)
    
    button_results = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div/b[1]/a')
    try:
        button_results[0].click()
    except NoSuchElementException:
        button_results[0].submit()
    
    time.sleep(2)
    
    # switch to newly opened tab with results
    driver.switch_to_window(driver.window_handles[1])
    
    rows = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div/table/tbody/tr')
    
    time.sleep(2)
    
    rownumber = len(rows)
    
    results_count = rownumber - 2
    
    return driver, rownumber, results_count
    
    """
    #If you directly enter the link from your email (without selecting siRNA candidates), e.g.:
    #http://rna.urmc.rochester.edu/cgi-bin/server_exe/oligowalk/oligowalk_out.cgi?file=oligowalk91733405653304summary.htm
    #You need this code additionally:
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/b[1]/a').click()
    """

def collect_target_positions_oligowalk(driver, results_count):
    # position:
        # from /html/body/div[1]/div[3]/div/table/tbody/tr[3]/td[1]
        # to /html/body/div[1]/div[3]/div/table/tbody/tr[330]/td[1]

    # probability:
        # from /html/body/div[1]/div[3]/div/table/tbody/tr[3]/td[2]
        # to /html/body/div[1]/div[3]/div/table/tbody/tr[330]/td[2]
    
    positions_list = []
    
    for i in range(results_count):
        position = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/table/tbody/tr[" + str(i+3) + "]/td[1]").text
        probability = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/table/tbody/tr[" + str(i+3) + "]/td[2]").text
        # only include candidates with over 80% probability of being efficient siRNA
        if float(probability) > 0.8:
            positions_list.append(position)

    return positions_list
