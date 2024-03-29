# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 19:15:55 2021

@author: User
"""

import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# AUTOMATICALLY PERFORM SEARCH FOR OUR SEQUENCE OF INTEREST (automatically perform query)
def perform_query_sidesign(chromedriver_path, gene_name, FASTA_sequence):
    #PATH =  r'C:\Users\User\Downloads\chromedriver_win32\chromedriver.exe'
    
    driver = webdriver.Chrome(chromedriver_path)
    driver.get('https://horizondiscovery.com/en/ordering-and-calculation-tools/sidesign-center')
    driver.maximize_window()
    
    driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/button[2]').click()
    
    select = Select(driver.find_element_by_name('IdType'))
    #option_names = ["human", "mouse", "rat"]
    print(select.options)
    print([o.text for o in select.options]) # these are strings
    select.select_by_visible_text('Nucleotide Sequence')
    
    print("CP0")
    # Wait until FASTA input box is visible
    WebDriverWait(driver,300).until(EC.visibility_of_element_located((By.ID,"FastaData")))
    # xpath: //*[@id="FastaData"]
    print("CP00")
    
    x = time.time()
    driver.find_element_by_id("FastaData").send_keys(FASTA_sequence)
    y = time.time()
    print(y-x)
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("CP1")
    
    driver.find_element_by_class_name('cc-compliance').click
    print("CP2")
    
    driver.find_element_by_xpath("//input[@id='button' and @value='Design siRNA']").click()
    print("CP3")
    
    # Wait until first siRNA result displays
    WebDriverWait(driver,300).until(EC.visibility_of_element_located((By.XPATH,"/html/body/main/div/div/div/form/div/div/div[3]/div[2]/table/tbody/tr[2]/td[3]")))
    
    return driver

# RETRIEVE NUMBER OF ROWS IN OUTPUT TABLE
def count_results_sidesign(driver):
    
    time.sleep(5)

    rows = driver.find_elements_by_xpath('/html/body/main/div/div/div/form/div/div/div[3]/div[2]/table/tbody/tr')
    
    time.sleep(2)
    
    #alternatively: rows = driver.find_elements_by_xpath('//table/tbody/tr')
    # or: rows = driver.find_elements_by_xpath('/html/body/div[3]/div[1]/form/table/tbody')
    rownumber = len(rows)

    results_count = rownumber - 1
    
    return driver, rownumber, results_count

def collect_target_positions_sidesign(driver, results_count):
    # from /html/body/main/div/div/div/form/div/div/div[3]/div[2]/table/tbody/tr[2]/td[3]
    # to   /html/body/main/div/div/div/form/div/div/div[3]/div[2]/table/tbody/tr[51]/td[3]
    
    positions_list = []
    
    for i in range(results_count):
        position = driver.find_element_by_xpath("/html/body/main/div/div/div/form/div/div/div[3]/div[2]/table/tbody/tr[" + str(i+2) + "]/td[3]").text
        positions_list.append(position)

    return positions_list
