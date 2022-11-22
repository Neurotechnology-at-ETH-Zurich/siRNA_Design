# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 19:15:55 2021

@author: User
"""

import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string

# AUTOMATICALLY PERFORM SEARCH FOR OUR SEQUENCE OF INTEREST (automatically perform query)

def perform_query_blockit(chromedriver_path, gene_name, NT_sequence):
    #PATH =  r'C:\Users\User\Downloads\chromedriver_win32\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver_path)
    driver.get('https://rnaidesigner.thermofisher.com/rnaiexpress/')
    driver.maximize_window()
    
    driver.find_element_by_name('sequenceContext').send_keys(NT_sequence)
    
    select = Select(driver.find_element_by_name('blastDatabase'))
    print(select.options)
    print([o.text for o in select.options])
    select.select_by_visible_text('No blast')

    driver.find_element_by_name('action').click()
    
    return driver

# RETRIEVE NUMBER OF ROWS IN OUTPUT TABLE
def count_results_blockit(driver):
    
    rows = driver.find_elements_by_xpath('/html/body/div[8]/div/div/div/div/div/form/table/tbody/tr[6]/td/table/tbody/tr')
    # row1: /html/body/div[8]/div/div/div/div/div/form/table/tbody/tr[6]/td/table/tbody/tr[2]/td[3]
    # row2: /html/body/div[8]/div/div/div/div/div/form/table/tbody/tr[6]/td/table/tbody/tr[3]/td[3]
    rownumber = len(rows)

    results_count = rownumber - 1
    
    return driver, rownumber, results_count

def collect_target_positions_blockit(driver, results_count):
    
    #table_id = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div/div/form/table/tbody')
    
    #/html/body/div[5]/div/div/div/div/div/form/table/tbody/tr[6]/td/table/tbody/tr[2]/td[4]
    #/html/body/div[5]/div/div/div/div/div/form/table/tbody/tr[6]/td/table/tbody/tr[10]/td[4]
    
    positions_list = []
    
    for i in range(results_count):
        position = driver.find_element_by_xpath(("/html/body/div[8]/div/div/div/div/div/form/table/tbody/tr[6]/td/table/tbody/tr[" + str(i+2) + "]/td[3]")).text
        positions_list.append(position)

    return positions_list