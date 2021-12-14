# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 16:13:10 2021

@author: User
"""
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests

def perform_query_RNAiexplorer(chromedriver_path, gene_name, NT_sequence, email):
    driver = webdriver.Chrome(chromedriver_path)
    driver.get('https://www.genelink.com/sirna/RNAicustomorder.asp')
    driver.maximize_window()
    
    # Add sequence name
    driver.find_element_by_xpath('/html/body/div[22]/div[3]/div[2]/table[2]/tbody/tr/td/table/tbody/tr[5]/td/input').send_keys(gene_name)
    
    # Add gene sequence
    driver.find_element_by_xpath('/html/body/div[22]/div[3]/div[2]/table[2]/tbody/tr/td/table/tbody/tr[5]/td/textarea').send_keys(NT_sequence)
    
    # Unclick "start with NN" as I'm not sure what that means
    driver.find_element_by_xpath('/html/body/div[22]/div[3]/div[2]/table[3]/tbody/tr[1]/td[1]/input[1]').click()    

    # Click submit
    driver.find_element_by_xpath('/html/body/div[22]/div[3]/div[2]/table[3]/tbody/tr[3]/td/p[1]/a/img').click()
    
    return driver

    # page seems to be faulty at the moment