# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 14:44:44 2021

@author: User
"""
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string


# AUTOMATICALLY PERFORM SEARCH FOR OUR SEQUENCE OF INTEREST (automatically perform query)
def perform_query_sirnawiz(chromedriver_path, gene_name, mRNA_sequence):
    #PATH =  r'C:\Users\User\Downloads\chromedriver_win32\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver_path)
    driver.get('https://www.invivogen.com/sirnawizard/design.php')
    driver.maximize_window()

    driver.find_element_by_xpath('/html/body/div[3]/form/input[1]').send_keys(gene_name)
    driver.find_element_by_xpath('/html/body/div[3]/form/textarea').send_keys(mRNA_sequence)

    select = Select(driver.find_element_by_xpath('/html/body/div[3]/form/div[1]/select'))
    #option_names = ["human", "mouse", "rat"]
    print(select.options)
    print([o.text for o in select.options]) # these are strings
    select.select_by_visible_text('human')

    driver.find_element_by_name('Submit').click()
    
    return driver

    #driver.quit() 

# RETRIEVE NUMBER OF ROWS IN OUTPUT TABLE
def count_results(driver):
    rows = driver.find_elements_by_xpath('/html/body/div[3]/div[1]/form/table/tbody/tr')
    #alternatively: rows = driver.find_elements_by_xpath('//table/tbody/tr')
    # or: rows = driver.find_elements_by_xpath('/html/body/div[3]/div[1]/form/table/tbody')
    rownumber = len(rows)

    results_count = rownumber - 2
    
    return driver, rownumber, results_count

# COLLECT TARGET POSITIONS FROM OUTPUT TABLE
def collect_target_positions(driver, rownumber):

    table_id = driver.find_element_by_xpath('/html/body/div[3]/div[1]/form/table/tbody/tr')

    column_list = []

    for row in range(rownumber+1):
        rows = table_id.find_elements_by_xpath("//body//tbody//tr[" + str(row) + "]")
        for row_data in rows:
            col = row_data.find_elements_by_tag_name("td")
            for i in range(len(col)):
                column = col[i].text
                print(column)
                column_list.append(column)

    # Delete empty entries
    column_list = list(filter(None, column_list))
    # Delete headers
    del column_list[0:5]
            
    # Pulling target position out of column:
    target_positions = []
    i = 1
    for x in range(len(column_list)):
        if i <= len(column_list):
            target_positions.append(column_list[i])
            i = i+3
    
    return column_list, target_positions

