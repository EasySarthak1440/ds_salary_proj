# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 09:32:59 2023

@author: Sarthak
"""

import pandas as pd
df=pd.read_csv('glassdoor_jobs.csv')

#salary parsing
#Company name text only
#state field
#age of company
#parsing of job description
df['hourly']=df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)

df=df[df['Salary Estimate']!='-1']

salary=df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_Kd = salary.apply(lambda x: x.replace('K','').replace('$',''))

min_hr = minus_Kd.apply(lambda x: x.lower().replace('Per Hour','').replace('per hour',''))

df['min_salary'] = min_hr.apply(lambda x: float(x.split('-')[0].replace(',', '')) if '-' in x else float(x.replace(',', '')))
df['max_salary'] = min_hr.apply(lambda x: float(x.split('-')[1].replace(',', '')) if '-' in x else float(x.replace(',', '')))
df['avg_salary'] = (df.min_salary+df.max_salary)/2

#company name text only
df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating'] == '-1' else x['Company Name'][:-len(x['Rating'])], axis=1)

#state field
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1].strip() if ',' in x else '')
job_state_counts = df['job_state'].value_counts()
df=df[df['Founded']!='-1']

df['age']=df.Founded.apply(lambda x: x if x<1 else 2020 - x)

#parsing of job description (python,etc;)

#python
df['python_yn']=df['Job Description'].apply(lambda x:1 if 'python' in x.lower() else 0)
df.python_yn.value_counts()

#r studio
df['R_yn']=df['Job Description'].apply(lambda x:1 if 'r_studio' in x.lower() or 'r-studio' in x.lower() else 0)
df.R_yn.value_counts()

#spark
df['spark']=df['Job Description'].apply(lambda x:1 if 'spark' in x.lower() else 0)
df.spark.value_counts()

#aws
df['aws']=df['Job Description'].apply(lambda x:1 if 'aws' in x.lower() else 0)
df.aws.value_counts()

#excel
df['excel']=df['Job Description'].apply(lambda x:1 if 'excel' in x.lower() else 0)
df.excel.value_counts()

df.columns
df.to_csv('salary_data_cleaned.csv',index=False)
pd.read_csv('salary_data_cleaned.csv')










