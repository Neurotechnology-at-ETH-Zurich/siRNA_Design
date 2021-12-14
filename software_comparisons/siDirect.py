# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 13:34:09 2021

@author: User
"""
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select

# AUTOMATICALLY PERFORM SEARCH FOR OUR SEQUENCE OF INTEREST (automatically perform query)
def perform_query_sidirect(chromedriver_path, gene_name, NT_sequence):
    
    # open website
    driver = webdriver.Chrome(chromedriver_path)
    driver.get('http://sidirect2.rnai.jp/')
    driver.maximize_window()
    
    # clear default sequence from input box
    driver.find_element_by_xpath('//*[@id="useq"]').clear()
    
    # enter nt sequence
    driver.find_element_by_xpath('//*[@id="useq"]').send_keys(NT_sequence)
    
    # Select which combination algorithms to use
    # Click options button
    driver.find_element_by_xpath('/html/body/form/h3/font/a/img').click()
    # Select algorithm
    driver.find_element_by_xpath('//*[@id="more1"]').click()
    # Uncheck option to only use Ui-Tei algorithm
    driver.find_element_by_xpath('/html/body/form/div/div[1]/table/tbody/tr/td[1]/p[2]/input')
    # Select combined rule (e.g. return all results suggested by Ui-Tei OR Reynolds OR Amarzguioui)
    driver.find_element_by_xpath('/html/body/form/div/div[1]/table/tbody/tr/td[1]/div/p[2]/input[1]')
    # Only show siRNAs that match all checked criteria
    driver.find_element_by_xpath('/html/body/form/div/div[4]/p[6]/input')
    
    # click submit
    submitbutton = driver.find_element_by_xpath('/html/body/form/p[2]/input')
    submitbutton.submit()
        
    return driver

def count_results_sidirect(driver):
    
    time.sleep(2)
    
    rows = driver.find_elements_by_xpath('/html/body/table[1]/tbody/tr')
    
    time.sleep(2)
    
    rownumber = len(rows)

    results_count = rownumber - 3
    
    return driver, rownumber, results_count

def collect_target_positions_sidirect(driver, results_count):
    # from /html/body/table[1]/tbody/tr[4]/td[1]
    # to /html/body/table[1]/tbody/tr[42]/td[1]
    
    positions_list = []
    
    for i in range(results_count):
        position = driver.find_element_by_xpath("/html/body/table[1]/tbody/tr[" + str(i+4) + "]/td[1]").text
        positions_list.append(position)

    return positions_list

