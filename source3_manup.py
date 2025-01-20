import pyodbc
import pandas as pd
import numpy as np
# Configuration de la connexion
server = 'DESKTOP-BD77A1Q'
database = 'job_posting'
username = 'sa'
password = 'yessine'
driver = '{ODBC Driver 17 for SQL Server}'

port = '1433'
conn_str = (
    f"DRIVER={driver};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "Encrypt=no;"
    "TrustServerCertificate=yes;"
)

# Connexion
try:
    conn = pyodbc.connect(conn_str)
    print("Connexion réussie !")

    # Charger les données
    query = "SELECT * FROM dbo.JobPostings"
    sr2 = pd.read_sql(query, conn)

    conn.close()
except Exception as e:
    print("Erreur :", e)

#netoyer les données

def categorize_experience(experience):
    try:

        years = int(experience.split()[0])
        if years <= 1:
            return 'Entry level'
        elif 2 <= years <= 5:
            return 'Associate'
        elif 6 <= years <= 10:
            return 'Mid-Senior level'
        elif 11 <= years <= 15:
            return 'Director'
        elif 16 <= years <= 20:
            return 'Executive'
        else:
            return 'Internship'
    except Exception as e:
        return np.nan  

sr2['formatted_experience_level'] = sr2['Experience'].apply(categorize_experience)

def parse_salary_range(salary_range):
    try:
        salary_range = salary_range.replace('$', '').replace('K', 'e3').replace('M', 'e6')  
        min_salary, max_salary = salary_range.split('-')
        min_salary, max_salary = float(min_salary), float(max_salary)
        normalized_salary = (min_salary + max_salary) / 2  
        return min_salary, max_salary, normalized_salary
    except Exception as e:
        return np.nan, np.nan, np.nan 

sr2[['min_salary', 'max_salary', 'normalized_salary']] = sr2['Salary_Range'].apply(lambda x: pd.Series(parse_salary_range(x)))

sr2['currency'] = 'USD'

def categorize_company_size(company_size):
    try:

        if company_size <= 50:
            return 1  
        elif 51 <= company_size <= 100:
            return 2  
        elif 101 <= company_size <= 200:
            return 3
        elif 201 <= company_size <= 500:
            return 4 
        elif 501 <= company_size <= 1000:
            return 5
        elif 1001 <= company_size <= 5000:
            return 6
        elif 5001 <= company_size <= 10000:
            return 7
        elif 10001 <= company_size <= 50000:
            return 8  
        elif 50001 <= company_size <= 100000:
            return 9
        else:
            return 10 
    except Exception as e:
        return np.nan  

sr2['employee_count'] = sr2['Company_Size']
sr2['company_size_rate'] = sr2['Company_Size'].apply(categorize_company_size)


sr2['Job_Posting_Date'] = pd.to_datetime(sr2['Job_Posting_Date'], errors='coerce')
sr2['jour'] = sr2['Job_Posting_Date'].dt.day
sr2['mois'] = sr2['Job_Posting_Date'].dt.month
sr2['annes'] = sr2['Job_Posting_Date'].dt.year
sr2['date'] = sr2['Job_Posting_Date'].dt.date

sr2 = sr2.rename(columns={
    'Location': 'city_job',
    'Work_Type': 'work_type',
    'Job_Title': 'title',
    'Benefits': 'type',
    'Skills': 'skill',
    'Company': 'company_name',
    'City': 'city_compagie',
    'State': 'country_compagie',
    'company_size_rate' : 'company_size',
    'Industry' : 'industry',
})
sr2 = sr2.drop(columns=['Qualifications', 'Job_Posting_Date','Experience','Salary_Range','Country','Company_Size'])

worldcities_path = "C:/Users/pc/Desktop/projet data warehouse/worldcities.csv"
worldcities = pd.read_csv(worldcities_path)


sr2['applies'] = np.random.randint(1, 501, size=len(sr2))

sr2['views'] = np.random.randint(1, 1001, size=len(sr2))

def get_country_by_city(city):

    matched_city = worldcities[worldcities['city_ascii'] == city]
    if not matched_city.empty:
        return matched_city.iloc[0]['country']
    else:
        return 'unknown' 

#sr2['country_job'] = sr2['city_job'].apply(get_country_by_city)
sr2['state_job'] = 'unknown'
sr2['pay_period'] = 'YEARLY'
sr2['remote_allowed'] = np.random.randint(0, 2, size=len(sr2))
sr2['follower_count'] = np.random.randint(1000, 50001, size=len(sr2))
sr2['specialite'] = 'unknown'
sr2['state_compagie'] = 'unknown'
sr2 = sr2.dropna(subset=['city_compagie'])
columns_to_string = [
    'city_job',
    'company',
    'title',
    'type',
    'skill',
    'company_name',
    'industry',
    'city_compagie',
    'country_compagie',
    'formatted_experience_level',
    'currency',
    'state_job',
    'state_compagie',
    'country_job'
]
for column in columns_to_string:
    if column in sr2.columns:
        sr2[column] = sr2[column].astype('string')
sr2['date'] = pd.to_datetime(sr2['date'])
sr2['Job_Id'] = sr2['Job_Id'].astype('int')
print(sr2.columns)
print(sr2.shape)
print(sr2.isnull().sum())
print(sr2.info())