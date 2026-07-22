import pandas as pd

patients = pd.DataFrame({
  'patient_id': [
    'PT-2001', 'PT-2001', 'PT-2002', 'PT-2003', 
    'PT-2004', 'PT-2005', 'PT-2006', 'PT-2006', 
    'PT-2007', 'PT-2008', 'PT-2009', 'PT-2010', 
    'PT-2011'
  ],
  'name': [
    'Anthony Ramirez', 'anthony ramirez', 'Grace Mitchell', 'Daniel Brooks', 
    'Nina Patel', 'Marcus Johnson', 'Elena Cruz', 'elena cruz', 
    'William Carter', 'Sophia Nguyen', None, 'Sophia Nguyen', 
    'Ethan Walker'
  ],
  'age': [
    '52', '52', 34, '28', 
    '61', 47, '26', 26, 
    '73', '39', 44, '39', 
    '58'
  ],
  'department': [
    'ER', 'er', 'Trauma', 'ER', 
    'Cardiology', 'Trauma', 'ER', 'er', 
    'ICU', 'ER', 'ER', 'ER', 
    'ICU'
  ],
  'triage_level': [
    'Critical', 'critical', 'Moderate', 'HIGH', 
    'Low', 'Moderate', 'critical', 'CRITICAL', 
    'High', 'Low', 'Moderate', 'low', 
    None
  ],
  'wait_time_minutes': [
    '12', '12', 55, '40 mins', 
    140, 60, '8', 8, 
    '95', '25', None, '25', 
    '70'
  ],
  'admitted': [
    True, True, False, True, 
    True, False, True, True, 
    False, True, False, True, 
    None
  ]
})

# ==============================================================================================================================================================================
print('original data =>')
print(patients)
print('===============================================================================================')

print('original data =>')
patients.info()
print('===============================================================================================')

"""
Column:
1.name ✅
=> fill NaN (na) with "Unknown"

2.age ✅
=> change data type to be int64

3.triage_level ✅
=> fillna with the most common value
=> standardized str 

4.wait_time_minutes ✅
=> fillna with average
=> strip out letter alphabet 
=> change data type to be int64

5.admitted
=> fillna with the most common value
"""

patients['name'] = patients['name'].fillna('Unknown')
print('cleaned `name` data =>')
print(patients)
print('===============================================================================================')

patients['age'] = pd.to_numeric(patients['age'])
print('cleaned `age` data =>')
print(patients.info())
print('===============================================================================================')

the_most_common_triage_level = patients['triage_level'].mode()[0]
print(f"the_most_common_triage_level: {the_most_common_triage_level}")
patients['triage_level'] = patients['triage_level'].fillna(the_most_common_triage_level)
patients['triage_level'] = patients['triage_level'].str.upper()
print('cleaned `triage_level` data =>')
print(patients)
print('===============================================================================================')

patients['wait_time_minutes'] = patients['wait_time_minutes'].astype(str).str.replace("[A-Za-z]+", "", regex = True)
patients['wait_time_minutes'] = patients['wait_time_minutes'].astype(str).str.strip()
patients['wait_time_minutes'] = pd.to_numeric(patients['wait_time_minutes'])

average_wait_time_minutes = patients['wait_time_minutes'].mean()
print(f"average_wait_time_minutes: {average_wait_time_minutes}")
patients['wait_time_minutes'] = patients['wait_time_minutes'].fillna(average_wait_time_minutes)

print(f"cleaned `wait_time_minutes`")
print(patients)
print('===============================================================================================')

the_most_common_admitted = patients['admitted'].mode()[0]
patients['admitted']= patients['admitted'].fillna(the_most_common_admitted)
print(f"the_most_common_admitted: {the_most_common_admitted}")
print(f"cleaned `the_most_common_admitted`")
print(patients)
print('===============================================================================================')