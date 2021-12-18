import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# AUTOMATICALLY PERFORM SEARCH FOR OUR SEQUENCE OF INTEREST (automatically perform query)
def perform_query_eurofins(chromedriver_path, gene_name, NT_sequence):
    #PATH =  r'C:\Users\User\Downloads\chromedriver_win32\chromedriver.exe'
    
    driver = webdriver.Chrome(chromedriver_path)
    driver.get('https://eurofinsgenomics.eu/en/ecom/tools/sirna-design/')
    driver.maximize_window()
    
    time.sleep(2)
    
    # Accept cookies
    driver.find_element_by_xpath("//button[text()='Accept All Cookies']").click()
    # Wait for updated page to load
    time.sleep(3)
    
    # Enter gene name
    driver.find_element_by_xpath('//*[@id="txtSiRnaName"]').send_keys(gene_name)
    
    # Enter nt sequence
    driver.find_element_by_xpath('//*[@id="txtTargetSequence"]').send_keys(NT_sequence)
    
    # Submit search
    driver.find_element_by_xpath('/html/body/form/div[5]/div[1]/div[4]/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[8]/input[1]').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/form/div[5]/div[1]/div[4]/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[8]/input[1]').click()    
    
    time.sleep(5)
    
    return driver

def count_results_eurofins(driver):
    
    WebDriverWait(driver,250).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[5]/div[1]/div[4]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[3]/fieldset/div[1]/table/tbody')))
    rows = driver.find_elements_by_xpath('/html/body/form/div[5]/div[1]/div[4]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[3]/fieldset/div[1]/table/tbody')
    
    return driver, rows

def collect_target_positions_eurofins(driver, rows):
    # /html/body/form/div[5]/div[1]/div[4]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[3]/fieldset/div[1]/table/tbody[1]/tr/td[4]
    # ...
    # /html/body/form/div[5]/div[1]/div[4]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[3]/fieldset/div[1]/table/tbody[6]/tr/td[4]
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(8)
    #WebDriverWait(driver,250).until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[5]/div[1]/div[4]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[3]/fieldset/div[1]/table/tbody1/tr/td[4]")))
    
    positions_list = []
    
    for i in range(len(rows)):
        position = driver.find_element_by_xpath("/html/body/form/div[5]/div[1]/div[4]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[3]/fieldset/div[1]/table/tbody[" + str(i+1) + "]/tr/td[4]").text
        position = int(position) + 3
        positions_list.append(position)

    return positions_list