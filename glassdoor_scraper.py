# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 22:24:24 2023

@author: Sarthak
"""
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import pandas as pd


def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    service = Service(executable_path='./chromedriver.exe')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1120, 1000)
    
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=&locId=&jobType="
    #url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element(By.CLASS_NAME, "selected").click()
            print(' x out worked')
        except ElementClickInterceptedException:
            print(' x out failed')
            pass
        
        try:
            close_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@data-role-variant="ghost"]')))
            close_button.click()
            print(' x out worked')
        except NoSuchElementException:
            print(' x out failed')
            pass

        #Going through each job in this page
        job_buttons = driver.find_elements(By.CSS_SELECTOR, "li[class*='react-job-listing']")  #jl for Job Listing. These are the buttons we're going to click.
        if not job_buttons:  # If no job buttons found, break the loop
            print("No more job listings found.")
            break
        for job_button in job_buttons:  
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might 
            time.sleep(1)
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    company_name = job_button.find_element(By.XPATH, './/div[@class="job-search-8wag7x"]').text
                    location = job_button.find_element(By.XPATH, './/div[@class="location mt-xxsm"]').text
                    job_title = job_button.find_element(By.XPATH, './/div[@class="job-title mt-xsm"]').text
                    job_description = driver.find_element(By.XPATH, './/div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate_element = job_button.find_element(By.XPATH, './/div[@class="salary-estimate"]')
                salary_estimate = salary_estimate_element.text
            except NoSuchElementException:
                salary_estimate = -1
            
            try:
                rating_element = job_button.find_element(By.XPATH, './/span[@class="job-search-rnnx2x"]')
                rating = rating_element.text
            except NoSuchElementException:
                rating = -1


            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                #driver.find_element(By.XPATH, './/div[@class="tab" and @data-tab-type="overview"]').click()
                #driver.find_element(By.XPATH, './/div[@class="job-search-193lseq"]').click()
                                
                try:
                    headquarters = driver.find_element(By.XPATH, './/div[@class="InfoFields"]//span[text()="Headquarters"]/following-sibling::*').text
                except NoSuchElementException:
                    headquarters = -1
                    
                try:
                    size = driver.find_element(By.XPATH, './/div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Size"]/following-sibling::*').text
                except NoSuchElementException:
                    size = -1
                
                try:
                    founded = driver.find_element(By.XPATH, './/div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Founded"]/following-sibling::*').text
                except NoSuchElementException:
                    founded = -1
                
                try:
                    type_of_ownership = driver.find_element(By.XPATH, './/div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Type"]/following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1
                
                try:
                    industry = driver.find_element(By.XPATH, './/div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Industry"]/following-sibling::*').text
                except NoSuchElementException:
                    industry = -1
                
                try:
                    sector = driver.find_element(By.XPATH, './/div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Sector"]/following-sibling::*').text
                except NoSuchElementException:
                    sector = -1
                
                try:
                    revenue = driver.find_element(By.XPATH, './/div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Revenue"]/following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1
                
                try:
                    competitors = driver.find_element(By.XPATH, './/div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Competitors"]/following-sibling::*').text
                except NoSuchElementException:
                    competitors = -1


            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1

                
            if verbose:
                print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Headquarters" : headquarters,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue,
            "Competitors" : competitors})
            #add job to jobs
            
            
        #Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH, './/li[@class="next"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
