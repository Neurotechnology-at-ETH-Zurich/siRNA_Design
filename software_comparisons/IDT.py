# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 15:15:33 2021

@author: User
"""
#### UNFINISHED

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# AUTOMATICALLY PERFORM SEARCH FOR OUR SEQUENCE OF INTEREST (automatically perform query)
def perform_query_IDT(chromedriver_path, FASTA_sequence):
    
    driver = webdriver.Chrome(chromedriver_path)
    driver.get('https://eu.idtdna.com/site/order/designtool/index/DSIRNA_CUSTOM')
    driver.maximize_window()
    
    driver.find_element_by_class_name('cc-btn.cc-allow').click()
    
    input_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="input-paste1"]')))
    driver.implicitly_wait(2)
    input_box.send_keys(FASTA_sequence)
    
    #driver.find_element_by_class_name('radio').click()
    
    
    BLASToption = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[5]/div[2]/div/div[3]/div[3]/div/div[2]/div[2]/div/div[4]/label/span[1]')))
    driver.implicitly_wait(2)
    BLASToption.click()
    
    driver.find_element_by_class_name('btn.btn-info.btn-block').click()
    
    return driver

def count_results_IDT(driver):
    
    """
    xpath positions:
    /html/body/div[4]/div[5]/div[2]/div/div[3]/div[5]/div[2]/div[2]/div[2]/div/div/div/div[2]/div[3]/div[2]/dl/dd[2]/span[1]
    /html/body/div[4]/div[5]/div[2]/div/div[3]/div[5]/div[2]/div[2]/div[3]/div/div/div/div[2]/div[3]/div[2]/dl/dd[2]/span[1]
    ...
    /html/body/div[4]/div[5]/div[2]/div/div[3]/div[5]/div[2]/div[2]/div[6]/div/div/div/div[2]/div[3]/div[2]/dl/dd[2]/span[1]
    """
    
    time.sleep(2)
    driver.maximize_window()
    
    pos_list = []
    
    #showmore = driver.find_elements_by_xpath("//span[contains(@data-bind,'text: Show product details +')]")
    #showmore = driver.find_elements_by_xpath("/html/body/div[4]/div[5]/div[2]/div/div[3]/div[5]/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/a/span[2]")
    #for buttons in showmore:
        #buttons.click()
        #time.sleep(2)
        
        
    # wait element to be clickable
    search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[5]/div[2]/div/div[3]/div[5]/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/a/span[2]")))
    # check button can be found
    print(search.get_attribute("value"))
    # Scroll the page to show this button (or it will fail to click)
    driver.execute_script("arguments[0].scrollIntoView();", search)
    search.click()
        
        

    
    #moreinfo = driver.find_element_by_xpath('/html/body/div[4]/div[5]/div[2]/div/div[3]/div[5]/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/a/span[2]')
    #moreinfo.click()
    
    # instock_element = driver.find_elements_by_xpath("//span[contains(@data-bind,'text: buttonText')]")
    
    return driver, pos_list
    
    """
    # need to first find xpath with max value at the 9th div
    sequence_positions = driver.find_elements_by_xpath("/html/body/div[4]/div[5]/div[2]/div/div[3]/div[5]/div[2]/div[2]/div[6]/div/div/div/div[2]/div[3]/div[2]/dl/dd[2]/span[1]")
    for values in sequence_positions:
        print("checkpoint59")
        print(values.text)
        pos_list.append(values.text)
        print("checkpoint60")
    #sequence_position = driver.find_elements_by_xpath("//*[contains(text(), '$data.FieldValue')]")
    """
    
    
    """
    pos_list = []
    
    for value in sequence_position:
     print("text : ",value.text)
     print(" id : ",value.id)
     if len(value.text) == 0:
          text = value.id
     else:
          print(value.text)
          text = value.text
          pos_list.append(text)
    """
    
    return driver, pos_list
    