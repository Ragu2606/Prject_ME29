+*In[3]:*+
[source, ipython3]
----
import pandas as pd
import pymongo
from pymongo import MongoClient
from urllib.parse import quote_plus
import psycopg2
----


+*In[4]:*+
[source, ipython3]
----
# Read data from Excel file
df = pd.read_excel('/home/ragu/Downloads/census_2011.xlsx')
----


+*In[5]:*+
[source, ipython3]
----
# Rename columns
new_column_names = {
    'State name': 'State/UT',
    'District name': 'District',
    'Male_Literate': 'Literate_Male',
    'Female_Literate': 'Literate_Female',
    'Rural_Households': 'Households_Rural',
    'Urban_Households': 'Households_Urban',
    'Age_Group_0_29': 'Young_and_Adult',
    'Age_Group_30_49': 'Middle_Aged',
    'Age_Group_50': 'Senior_Citizen',
    'Age not stated': 'Age_Not_Stated'
}
df = df.rename(columns=new_column_names)
----


+*In[6]:*+
[source, ipython3]
----
# Modify state names
def modify_state_name(name):
    return name.lower() if name.lower() == "and" else name.title()

df['State/UT'] = df['State/UT'].apply(modify_state_name)
----


+*In[7]:*+
[source, ipython3]
----
# Assign Telangana and Ladakh to specific districts
telangana_districts = ['Adilabad', 'Nizamabad', 'Karimnagar', 'Medak', 'Hyderabad', 'Rangareddy', 'Mahbubnagar', 'Nalgonda', 'Warangal', 'Khammam']
ladakh_districts = ['Leh(Ladakh)', 'Kargil']
df.loc[df['District'].isin(telangana_districts), 'State/UT'] = 'Telangana'
df.loc[df['District'].isin(ladakh_districts), 'State/UT'] = 'Ladakh'

----


+*In[9]:*+
[source, ipython3]
----
# Fill missing values
df['Population'].fillna(df['Male'] + df['Female'], inplace=True)
df['Male'].fillna(df['Population'] - df['Female'], inplace=True)
df['Female'].fillna(df['Population'] - df['Male'], inplace=True)
df['Literate'].fillna(df['Literate_Male'] + df['Literate_Female'], inplace=True)
df['Literate_Male'].fillna(df['Literate'] - df['Literate_Female'], inplace=True)
df['Literate_Female'].fillna(df['Literate'] - df['Literate_Male'], inplace=True)
df['SC'].fillna(df['Male_SC'] + df['Female_SC'], inplace=True)
df['Male_SC'].fillna(df['SC'] - df['Female_SC'], inplace=True)
df['Female_SC'].fillna(df['SC'] - df['Male_SC'], inplace=True)
df['ST'].fillna(df['Male_ST'] + df['Female_ST'], inplace=True)
df['Male_ST'].fillna(df['ST'] - df['Female_ST'], inplace=True)
df['Female_ST'].fillna(df['ST'] - df['Male_ST'], inplace=True)
df['Workers'].fillna(df['Male_Workers'] + df['Female_Workers'], inplace=True)
df['Male_Workers'].fillna(df['Workers'] - df['Female_Workers'], inplace=True)
df['Female_Workers'].fillna(df['Workers'] - df['Male_Workers'], inplace=True)
df['Main_Workers'].fillna(df['Workers'] - df['Marginal_Workers'], inplace=True)
df['Marginal_Workers'].fillna(df['Workers'] - df['Main_Workers'], inplace=True)
df['Non_Workers'].fillna(df['Population'] - df['Workers'], inplace=True)
df['Non_Workers'].fillna(df['Population'] - df['Workers'], inplace=True)
df['Cultivator_Workers'].fillna(df['Workers'] - df['Agricultural_Workers'] - df['Household_Workers'] - df['Other_Workers'], inplace=True)
df['Agricultural_Workers'].fillna(df['Workers'] - df['Cultivator_Workers'] - df['Household_Workers'] - df['Other_Workers'], inplace=True)
df['Household_Workers'].fillna(df['Workers'] - df['Agricultural_Workers'] - df['Cultivator_Workers'] - df['Other_Workers'], inplace=True)
df['Other_Workers'].fillna(df['Workers'] - df['Agricultural_Workers'] - df['Cultivator_Workers'] - df['Cultivator_Workers'], inplace=True)
df['Hindus'].fillna(df['Population'] - df['Christians']- df['Muslims'] - df['Sikhs'] - df['Buddhists'] - df['Jains'] - df['Others_Religions']- df['Religion_Not_Stated'], inplace=True)
df['Christians'].fillna(df['Population'] - df['Hindus']- df['Muslims'] - df['Sikhs'] - df['Buddhists'] - df['Jains'] - df['Others_Religions']- df['Religion_Not_Stated'], inplace=True)
df['Muslims'].fillna(df['Population'] - df['Christians']- df['Hindus'] - df['Sikhs'] - df['Buddhists'] - df['Jains'] - df['Others_Religions']- df['Religion_Not_Stated'], inplace=True)
df['Sikhs'].fillna(df['Population'] - df['Christians']- df['Muslims'] - df['Hindus'] - df['Buddhists'] - df['Jains'] - df['Others_Religions']- df['Religion_Not_Stated'], inplace=True)
df['Buddhists'].fillna(df['Population'] - df['Christians']- df['Muslims'] - df['Sikhs'] - df['Hindus'] - df['Jains'] - df['Others_Religions']- df['Religion_Not_Stated'], inplace=True)
df['Jains'].fillna(df['Population'] - df['Christians']- df['Muslims'] - df['Sikhs'] - df['Buddhists'] - df['Hindus'] - df['Others_Religions']- df['Religion_Not_Stated'], inplace=True)
df['Others_Religions'].fillna(df['Population'] - df['Christians']- df['Muslims'] - df['Sikhs'] - df['Buddhists'] - df['Jains'] - df['Hindus']- df['Religion_Not_Stated'], inplace=True)
df['Religion_Not_Stated'].fillna(df['Population'] - df['Christians']- df['Muslims'] - df['Sikhs'] - df['Buddhists'] - df['Jains'] - df['Others_Religions']+ df['Hindus'], inplace=True)
df['Households'].fillna(df['Households_Rural'] + df['Households_Urban'], inplace=True)
df['Households_Rural'].fillna(df['Households'] - df['Households_Urban'], inplace=True)
df['Households_Urban'].fillna(df['Households'] + df['Households_Rural'], inplace=True)
df.fillna(0, inplace=True)
----


+*In[10]:*+
[source, ipython3]
----
# Export modified data to CSV
df.to_csv('/home/ragu/Downloads/census_2011_new.csv', index=False)
----


+*In[11]:*+
[source, ipython3]
----
# Connect to MongoDB
username = "ragu"
password = "Dhuruv@21"
escaped_username = quote_plus(username)
escaped_password = quote_plus(password)
mongo_uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.hvjd7sw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
----


+*In[12]:*+
[source, ipython3]
----
client = MongoClient(mongo_uri)
db = client['Project']
collection = db['Census']
----


+*In[13]:*+
[source, ipython3]
----
# Insert data into MongoDB
collection.insert_many(df.to_dict('records'))
----


+*Out[13]:*+
----InsertManyResult([ObjectId('66229ce1636ad3e4eb1e7e66'), ObjectId('66229ce1636ad3e4eb1e7e67'), ObjectId('66229ce1636ad3e4eb1e7e68'), ObjectId('66229ce1636ad3e4eb1e7e69'), ObjectId('66229ce1636ad3e4eb1e7e6a'), ObjectId('66229ce1636ad3e4eb1e7e6b'), ObjectId('66229ce1636ad3e4eb1e7e6c'), ObjectId('66229ce1636ad3e4eb1e7e6d'), ObjectId('66229ce1636ad3e4eb1e7e6e'), ObjectId('66229ce1636ad3e4eb1e7e6f'), ObjectId('66229ce1636ad3e4eb1e7e70'), ObjectId('66229ce1636ad3e4eb1e7e71'), ObjectId('66229ce1636ad3e4eb1e7e72'), ObjectId('66229ce1636ad3e4eb1e7e73'), ObjectId('66229ce1636ad3e4eb1e7e74'), ObjectId('66229ce1636ad3e4eb1e7e75'), ObjectId('66229ce1636ad3e4eb1e7e76'), ObjectId('66229ce1636ad3e4eb1e7e77'), ObjectId('66229ce1636ad3e4eb1e7e78'), ObjectId('66229ce1636ad3e4eb1e7e79'), ObjectId('66229ce1636ad3e4eb1e7e7a'), ObjectId('66229ce1636ad3e4eb1e7e7b'), ObjectId('66229ce1636ad3e4eb1e7e7c'), ObjectId('66229ce1636ad3e4eb1e7e7d'), ObjectId('66229ce1636ad3e4eb1e7e7e'), ObjectId('66229ce1636ad3e4eb1e7e7f'), ObjectId('66229ce1636ad3e4eb1e7e80'), ObjectId('66229ce1636ad3e4eb1e7e81'), ObjectId('66229ce1636ad3e4eb1e7e82'), ObjectId('66229ce1636ad3e4eb1e7e83'), ObjectId('66229ce1636ad3e4eb1e7e84'), ObjectId('66229ce1636ad3e4eb1e7e85'), ObjectId('66229ce1636ad3e4eb1e7e86'), ObjectId('66229ce1636ad3e4eb1e7e87'), ObjectId('66229ce1636ad3e4eb1e7e88'), ObjectId('66229ce1636ad3e4eb1e7e89'), ObjectId('66229ce1636ad3e4eb1e7e8a'), ObjectId('66229ce1636ad3e4eb1e7e8b'), ObjectId('66229ce1636ad3e4eb1e7e8c'), ObjectId('66229ce1636ad3e4eb1e7e8d'), ObjectId('66229ce1636ad3e4eb1e7e8e'), ObjectId('66229ce1636ad3e4eb1e7e8f'), ObjectId('66229ce1636ad3e4eb1e7e90'), ObjectId('66229ce1636ad3e4eb1e7e91'), ObjectId('66229ce1636ad3e4eb1e7e92'), ObjectId('66229ce1636ad3e4eb1e7e93'), ObjectId('66229ce1636ad3e4eb1e7e94'), ObjectId('66229ce1636ad3e4eb1e7e95'), ObjectId('66229ce1636ad3e4eb1e7e96'), ObjectId('66229ce1636ad3e4eb1e7e97'), ObjectId('66229ce1636ad3e4eb1e7e98'), ObjectId('66229ce1636ad3e4eb1e7e99'), ObjectId('66229ce1636ad3e4eb1e7e9a'), ObjectId('66229ce1636ad3e4eb1e7e9b'), ObjectId('66229ce1636ad3e4eb1e7e9c'), ObjectId('66229ce1636ad3e4eb1e7e9d'), ObjectId('66229ce1636ad3e4eb1e7e9e'), ObjectId('66229ce1636ad3e4eb1e7e9f'), ObjectId('66229ce1636ad3e4eb1e7ea0'), ObjectId('66229ce1636ad3e4eb1e7ea1'), ObjectId('66229ce1636ad3e4eb1e7ea2'), ObjectId('66229ce1636ad3e4eb1e7ea3'), ObjectId('66229ce1636ad3e4eb1e7ea4'), ObjectId('66229ce1636ad3e4eb1e7ea5'), ObjectId('66229ce1636ad3e4eb1e7ea6'), ObjectId('66229ce1636ad3e4eb1e7ea7'), ObjectId('66229ce1636ad3e4eb1e7ea8'), ObjectId('66229ce1636ad3e4eb1e7ea9'), ObjectId('66229ce1636ad3e4eb1e7eaa'), ObjectId('66229ce1636ad3e4eb1e7eab'), ObjectId('66229ce1636ad3e4eb1e7eac'), ObjectId('66229ce1636ad3e4eb1e7ead'), ObjectId('66229ce1636ad3e4eb1e7eae'), ObjectId('66229ce1636ad3e4eb1e7eaf'), ObjectId('66229ce1636ad3e4eb1e7eb0'), ObjectId('66229ce1636ad3e4eb1e7eb1'), ObjectId('66229ce1636ad3e4eb1e7eb2'), ObjectId('66229ce1636ad3e4eb1e7eb3'), ObjectId('66229ce1636ad3e4eb1e7eb4'), ObjectId('66229ce1636ad3e4eb1e7eb5'), ObjectId('66229ce1636ad3e4eb1e7eb6'), ObjectId('66229ce1636ad3e4eb1e7eb7'), ObjectId('66229ce1636ad3e4eb1e7eb8'), ObjectId('66229ce1636ad3e4eb1e7eb9'), ObjectId('66229ce1636ad3e4eb1e7eba'), ObjectId('66229ce1636ad3e4eb1e7ebb'), ObjectId('66229ce1636ad3e4eb1e7ebc'), ObjectId('66229ce1636ad3e4eb1e7ebd'), ObjectId('66229ce1636ad3e4eb1e7ebe'), ObjectId('66229ce1636ad3e4eb1e7ebf'), ObjectId('66229ce1636ad3e4eb1e7ec0'), ObjectId('66229ce1636ad3e4eb1e7ec1'), ObjectId('66229ce1636ad3e4eb1e7ec2'), ObjectId('66229ce1636ad3e4eb1e7ec3'), ObjectId('66229ce1636ad3e4eb1e7ec4'), ObjectId('66229ce1636ad3e4eb1e7ec5'), ObjectId('66229ce1636ad3e4eb1e7ec6'), ObjectId('66229ce1636ad3e4eb1e7ec7'), ObjectId('66229ce1636ad3e4eb1e7ec8'), ObjectId('66229ce1636ad3e4eb1e7ec9'), ObjectId('66229ce1636ad3e4eb1e7eca'), ObjectId('66229ce1636ad3e4eb1e7ecb'), ObjectId('66229ce1636ad3e4eb1e7ecc'), ObjectId('66229ce1636ad3e4eb1e7ecd'), ObjectId('66229ce1636ad3e4eb1e7ece'), ObjectId('66229ce1636ad3e4eb1e7ecf'), ObjectId('66229ce1636ad3e4eb1e7ed0'), ObjectId('66229ce1636ad3e4eb1e7ed1'), ObjectId('66229ce1636ad3e4eb1e7ed2'), ObjectId('66229ce1636ad3e4eb1e7ed3'), ObjectId('66229ce1636ad3e4eb1e7ed4'), ObjectId('66229ce1636ad3e4eb1e7ed5'), ObjectId('66229ce1636ad3e4eb1e7ed6'), ObjectId('66229ce1636ad3e4eb1e7ed7'), ObjectId('66229ce1636ad3e4eb1e7ed8'), ObjectId('66229ce1636ad3e4eb1e7ed9'), ObjectId('66229ce1636ad3e4eb1e7eda'), ObjectId('66229ce1636ad3e4eb1e7edb'), ObjectId('66229ce1636ad3e4eb1e7edc'), ObjectId('66229ce1636ad3e4eb1e7edd'), ObjectId('66229ce1636ad3e4eb1e7ede'), ObjectId('66229ce1636ad3e4eb1e7edf'), ObjectId('66229ce1636ad3e4eb1e7ee0'), ObjectId('66229ce1636ad3e4eb1e7ee1'), ObjectId('66229ce1636ad3e4eb1e7ee2'), ObjectId('66229ce1636ad3e4eb1e7ee3'), ObjectId('66229ce1636ad3e4eb1e7ee4'), ObjectId('66229ce1636ad3e4eb1e7ee5'), ObjectId('66229ce1636ad3e4eb1e7ee6'), ObjectId('66229ce1636ad3e4eb1e7ee7'), ObjectId('66229ce1636ad3e4eb1e7ee8'), ObjectId('66229ce1636ad3e4eb1e7ee9'), ObjectId('66229ce1636ad3e4eb1e7eea'), ObjectId('66229ce1636ad3e4eb1e7eeb'), ObjectId('66229ce1636ad3e4eb1e7eec'), ObjectId('66229ce1636ad3e4eb1e7eed'), ObjectId('66229ce1636ad3e4eb1e7eee'), ObjectId('66229ce1636ad3e4eb1e7eef'), ObjectId('66229ce1636ad3e4eb1e7ef0'), ObjectId('66229ce1636ad3e4eb1e7ef1'), ObjectId('66229ce1636ad3e4eb1e7ef2'), ObjectId('66229ce1636ad3e4eb1e7ef3'), ObjectId('66229ce1636ad3e4eb1e7ef4'), ObjectId('66229ce1636ad3e4eb1e7ef5'), ObjectId('66229ce1636ad3e4eb1e7ef6'), ObjectId('66229ce1636ad3e4eb1e7ef7'), ObjectId('66229ce1636ad3e4eb1e7ef8'), ObjectId('66229ce1636ad3e4eb1e7ef9'), ObjectId('66229ce1636ad3e4eb1e7efa'), ObjectId('66229ce1636ad3e4eb1e7efb'), ObjectId('66229ce1636ad3e4eb1e7efc'), ObjectId('66229ce1636ad3e4eb1e7efd'), ObjectId('66229ce1636ad3e4eb1e7efe'), ObjectId('66229ce1636ad3e4eb1e7eff'), ObjectId('66229ce1636ad3e4eb1e7f00'), ObjectId('66229ce1636ad3e4eb1e7f01'), ObjectId('66229ce1636ad3e4eb1e7f02'), ObjectId('66229ce1636ad3e4eb1e7f03'), ObjectId('66229ce1636ad3e4eb1e7f04'), ObjectId('66229ce1636ad3e4eb1e7f05'), ObjectId('66229ce1636ad3e4eb1e7f06'), ObjectId('66229ce1636ad3e4eb1e7f07'), ObjectId('66229ce1636ad3e4eb1e7f08'), ObjectId('66229ce1636ad3e4eb1e7f09'), ObjectId('66229ce1636ad3e4eb1e7f0a'), ObjectId('66229ce1636ad3e4eb1e7f0b'), ObjectId('66229ce1636ad3e4eb1e7f0c'), ObjectId('66229ce1636ad3e4eb1e7f0d'), ObjectId('66229ce1636ad3e4eb1e7f0e'), ObjectId('66229ce1636ad3e4eb1e7f0f'), ObjectId('66229ce1636ad3e4eb1e7f10'), ObjectId('66229ce1636ad3e4eb1e7f11'), ObjectId('66229ce1636ad3e4eb1e7f12'), ObjectId('66229ce1636ad3e4eb1e7f13'), ObjectId('66229ce1636ad3e4eb1e7f14'), ObjectId('66229ce1636ad3e4eb1e7f15'), ObjectId('66229ce1636ad3e4eb1e7f16'), ObjectId('66229ce1636ad3e4eb1e7f17'), ObjectId('66229ce1636ad3e4eb1e7f18'), ObjectId('66229ce1636ad3e4eb1e7f19'), ObjectId('66229ce1636ad3e4eb1e7f1a'), ObjectId('66229ce1636ad3e4eb1e7f1b'), ObjectId('66229ce1636ad3e4eb1e7f1c'), ObjectId('66229ce1636ad3e4eb1e7f1d'), ObjectId('66229ce1636ad3e4eb1e7f1e'), ObjectId('66229ce1636ad3e4eb1e7f1f'), ObjectId('66229ce1636ad3e4eb1e7f20'), ObjectId('66229ce1636ad3e4eb1e7f21'), ObjectId('66229ce1636ad3e4eb1e7f22'), ObjectId('66229ce1636ad3e4eb1e7f23'), ObjectId('66229ce1636ad3e4eb1e7f24'), ObjectId('66229ce1636ad3e4eb1e7f25'), ObjectId('66229ce1636ad3e4eb1e7f26'), ObjectId('66229ce1636ad3e4eb1e7f27'), ObjectId('66229ce1636ad3e4eb1e7f28'), ObjectId('66229ce1636ad3e4eb1e7f29'), ObjectId('66229ce1636ad3e4eb1e7f2a'), ObjectId('66229ce1636ad3e4eb1e7f2b'), ObjectId('66229ce1636ad3e4eb1e7f2c'), ObjectId('66229ce1636ad3e4eb1e7f2d'), ObjectId('66229ce1636ad3e4eb1e7f2e'), ObjectId('66229ce1636ad3e4eb1e7f2f'), ObjectId('66229ce1636ad3e4eb1e7f30'), ObjectId('66229ce1636ad3e4eb1e7f31'), ObjectId('66229ce1636ad3e4eb1e7f32'), ObjectId('66229ce1636ad3e4eb1e7f33'), ObjectId('66229ce1636ad3e4eb1e7f34'), ObjectId('66229ce1636ad3e4eb1e7f35'), ObjectId('66229ce1636ad3e4eb1e7f36'), ObjectId('66229ce1636ad3e4eb1e7f37'), ObjectId('66229ce1636ad3e4eb1e7f38'), ObjectId('66229ce1636ad3e4eb1e7f39'), ObjectId('66229ce1636ad3e4eb1e7f3a'), ObjectId('66229ce1636ad3e4eb1e7f3b'), ObjectId('66229ce1636ad3e4eb1e7f3c'), ObjectId('66229ce1636ad3e4eb1e7f3d'), ObjectId('66229ce1636ad3e4eb1e7f3e'), ObjectId('66229ce1636ad3e4eb1e7f3f'), ObjectId('66229ce1636ad3e4eb1e7f40'), ObjectId('66229ce1636ad3e4eb1e7f41'), ObjectId('66229ce1636ad3e4eb1e7f42'), ObjectId('66229ce1636ad3e4eb1e7f43'), ObjectId('66229ce1636ad3e4eb1e7f44'), ObjectId('66229ce1636ad3e4eb1e7f45'), ObjectId('66229ce1636ad3e4eb1e7f46'), ObjectId('66229ce1636ad3e4eb1e7f47'), ObjectId('66229ce1636ad3e4eb1e7f48'), ObjectId('66229ce1636ad3e4eb1e7f49'), ObjectId('66229ce1636ad3e4eb1e7f4a'), ObjectId('66229ce1636ad3e4eb1e7f4b'), ObjectId('66229ce1636ad3e4eb1e7f4c'), ObjectId('66229ce1636ad3e4eb1e7f4d'), ObjectId('66229ce1636ad3e4eb1e7f4e'), ObjectId('66229ce1636ad3e4eb1e7f4f'), ObjectId('66229ce1636ad3e4eb1e7f50'), ObjectId('66229ce1636ad3e4eb1e7f51'), ObjectId('66229ce1636ad3e4eb1e7f52'), ObjectId('66229ce1636ad3e4eb1e7f53'), ObjectId('66229ce1636ad3e4eb1e7f54'), ObjectId('66229ce1636ad3e4eb1e7f55'), ObjectId('66229ce1636ad3e4eb1e7f56'), ObjectId('66229ce1636ad3e4eb1e7f57'), ObjectId('66229ce1636ad3e4eb1e7f58'), ObjectId('66229ce1636ad3e4eb1e7f59'), ObjectId('66229ce1636ad3e4eb1e7f5a'), ObjectId('66229ce1636ad3e4eb1e7f5b'), ObjectId('66229ce1636ad3e4eb1e7f5c'), ObjectId('66229ce1636ad3e4eb1e7f5d'), ObjectId('66229ce1636ad3e4eb1e7f5e'), ObjectId('66229ce1636ad3e4eb1e7f5f'), ObjectId('66229ce1636ad3e4eb1e7f60'), ObjectId('66229ce1636ad3e4eb1e7f61'), ObjectId('66229ce1636ad3e4eb1e7f62'), ObjectId('66229ce1636ad3e4eb1e7f63'), ObjectId('66229ce1636ad3e4eb1e7f64'), ObjectId('66229ce1636ad3e4eb1e7f65'), ObjectId('66229ce1636ad3e4eb1e7f66'), ObjectId('66229ce1636ad3e4eb1e7f67'), ObjectId('66229ce1636ad3e4eb1e7f68'), ObjectId('66229ce1636ad3e4eb1e7f69'), ObjectId('66229ce1636ad3e4eb1e7f6a'), ObjectId('66229ce1636ad3e4eb1e7f6b'), ObjectId('66229ce1636ad3e4eb1e7f6c'), ObjectId('66229ce1636ad3e4eb1e7f6d'), ObjectId('66229ce1636ad3e4eb1e7f6e'), ObjectId('66229ce1636ad3e4eb1e7f6f'), ObjectId('66229ce1636ad3e4eb1e7f70'), ObjectId('66229ce1636ad3e4eb1e7f71'), ObjectId('66229ce1636ad3e4eb1e7f72'), ObjectId('66229ce1636ad3e4eb1e7f73'), ObjectId('66229ce1636ad3e4eb1e7f74'), ObjectId('66229ce1636ad3e4eb1e7f75'), ObjectId('66229ce1636ad3e4eb1e7f76'), ObjectId('66229ce1636ad3e4eb1e7f77'), ObjectId('66229ce1636ad3e4eb1e7f78'), ObjectId('66229ce1636ad3e4eb1e7f79'), ObjectId('66229ce1636ad3e4eb1e7f7a'), ObjectId('66229ce1636ad3e4eb1e7f7b'), ObjectId('66229ce1636ad3e4eb1e7f7c'), ObjectId('66229ce1636ad3e4eb1e7f7d'), ObjectId('66229ce1636ad3e4eb1e7f7e'), ObjectId('66229ce1636ad3e4eb1e7f7f'), ObjectId('66229ce1636ad3e4eb1e7f80'), ObjectId('66229ce1636ad3e4eb1e7f81'), ObjectId('66229ce1636ad3e4eb1e7f82'), ObjectId('66229ce1636ad3e4eb1e7f83'), ObjectId('66229ce1636ad3e4eb1e7f84'), ObjectId('66229ce1636ad3e4eb1e7f85'), ObjectId('66229ce1636ad3e4eb1e7f86'), ObjectId('66229ce1636ad3e4eb1e7f87'), ObjectId('66229ce1636ad3e4eb1e7f88'), ObjectId('66229ce1636ad3e4eb1e7f89'), ObjectId('66229ce1636ad3e4eb1e7f8a'), ObjectId('66229ce1636ad3e4eb1e7f8b'), ObjectId('66229ce1636ad3e4eb1e7f8c'), ObjectId('66229ce1636ad3e4eb1e7f8d'), ObjectId('66229ce1636ad3e4eb1e7f8e'), ObjectId('66229ce1636ad3e4eb1e7f8f'), ObjectId('66229ce1636ad3e4eb1e7f90'), ObjectId('66229ce1636ad3e4eb1e7f91'), ObjectId('66229ce1636ad3e4eb1e7f92'), ObjectId('66229ce1636ad3e4eb1e7f93'), ObjectId('66229ce1636ad3e4eb1e7f94'), ObjectId('66229ce1636ad3e4eb1e7f95'), ObjectId('66229ce1636ad3e4eb1e7f96'), ObjectId('66229ce1636ad3e4eb1e7f97'), ObjectId('66229ce1636ad3e4eb1e7f98'), ObjectId('66229ce1636ad3e4eb1e7f99'), ObjectId('66229ce1636ad3e4eb1e7f9a'), ObjectId('66229ce1636ad3e4eb1e7f9b'), ObjectId('66229ce1636ad3e4eb1e7f9c'), ObjectId('66229ce1636ad3e4eb1e7f9d'), ObjectId('66229ce1636ad3e4eb1e7f9e'), ObjectId('66229ce1636ad3e4eb1e7f9f'), ObjectId('66229ce1636ad3e4eb1e7fa0'), ObjectId('66229ce1636ad3e4eb1e7fa1'), ObjectId('66229ce1636ad3e4eb1e7fa2'), ObjectId('66229ce1636ad3e4eb1e7fa3'), ObjectId('66229ce1636ad3e4eb1e7fa4'), ObjectId('66229ce1636ad3e4eb1e7fa5'), ObjectId('66229ce1636ad3e4eb1e7fa6'), ObjectId('66229ce1636ad3e4eb1e7fa7'), ObjectId('66229ce1636ad3e4eb1e7fa8'), ObjectId('66229ce1636ad3e4eb1e7fa9'), ObjectId('66229ce1636ad3e4eb1e7faa'), ObjectId('66229ce1636ad3e4eb1e7fab'), ObjectId('66229ce1636ad3e4eb1e7fac'), ObjectId('66229ce1636ad3e4eb1e7fad'), ObjectId('66229ce1636ad3e4eb1e7fae'), ObjectId('66229ce1636ad3e4eb1e7faf'), ObjectId('66229ce1636ad3e4eb1e7fb0'), ObjectId('66229ce1636ad3e4eb1e7fb1'), ObjectId('66229ce1636ad3e4eb1e7fb2'), ObjectId('66229ce1636ad3e4eb1e7fb3'), ObjectId('66229ce1636ad3e4eb1e7fb4'), ObjectId('66229ce1636ad3e4eb1e7fb5'), ObjectId('66229ce1636ad3e4eb1e7fb6'), ObjectId('66229ce1636ad3e4eb1e7fb7'), ObjectId('66229ce1636ad3e4eb1e7fb8'), ObjectId('66229ce1636ad3e4eb1e7fb9'), ObjectId('66229ce1636ad3e4eb1e7fba'), ObjectId('66229ce1636ad3e4eb1e7fbb'), ObjectId('66229ce1636ad3e4eb1e7fbc'), ObjectId('66229ce1636ad3e4eb1e7fbd'), ObjectId('66229ce1636ad3e4eb1e7fbe'), ObjectId('66229ce1636ad3e4eb1e7fbf'), ObjectId('66229ce1636ad3e4eb1e7fc0'), ObjectId('66229ce1636ad3e4eb1e7fc1'), ObjectId('66229ce1636ad3e4eb1e7fc2'), ObjectId('66229ce1636ad3e4eb1e7fc3'), ObjectId('66229ce1636ad3e4eb1e7fc4'), ObjectId('66229ce1636ad3e4eb1e7fc5'), ObjectId('66229ce1636ad3e4eb1e7fc6'), ObjectId('66229ce1636ad3e4eb1e7fc7'), ObjectId('66229ce1636ad3e4eb1e7fc8'), ObjectId('66229ce1636ad3e4eb1e7fc9'), ObjectId('66229ce1636ad3e4eb1e7fca'), ObjectId('66229ce1636ad3e4eb1e7fcb'), ObjectId('66229ce1636ad3e4eb1e7fcc'), ObjectId('66229ce1636ad3e4eb1e7fcd'), ObjectId('66229ce1636ad3e4eb1e7fce'), ObjectId('66229ce1636ad3e4eb1e7fcf'), ObjectId('66229ce1636ad3e4eb1e7fd0'), ObjectId('66229ce1636ad3e4eb1e7fd1'), ObjectId('66229ce1636ad3e4eb1e7fd2'), ObjectId('66229ce1636ad3e4eb1e7fd3'), ObjectId('66229ce1636ad3e4eb1e7fd4'), ObjectId('66229ce1636ad3e4eb1e7fd5'), ObjectId('66229ce1636ad3e4eb1e7fd6'), ObjectId('66229ce1636ad3e4eb1e7fd7'), ObjectId('66229ce1636ad3e4eb1e7fd8'), ObjectId('66229ce1636ad3e4eb1e7fd9'), ObjectId('66229ce1636ad3e4eb1e7fda'), ObjectId('66229ce1636ad3e4eb1e7fdb'), ObjectId('66229ce1636ad3e4eb1e7fdc'), ObjectId('66229ce1636ad3e4eb1e7fdd'), ObjectId('66229ce1636ad3e4eb1e7fde'), ObjectId('66229ce1636ad3e4eb1e7fdf'), ObjectId('66229ce1636ad3e4eb1e7fe0'), ObjectId('66229ce1636ad3e4eb1e7fe1'), ObjectId('66229ce1636ad3e4eb1e7fe2'), ObjectId('66229ce1636ad3e4eb1e7fe3'), ObjectId('66229ce1636ad3e4eb1e7fe4'), ObjectId('66229ce1636ad3e4eb1e7fe5'), ObjectId('66229ce1636ad3e4eb1e7fe6'), ObjectId('66229ce1636ad3e4eb1e7fe7'), ObjectId('66229ce1636ad3e4eb1e7fe8'), ObjectId('66229ce1636ad3e4eb1e7fe9'), ObjectId('66229ce1636ad3e4eb1e7fea'), ObjectId('66229ce1636ad3e4eb1e7feb'), ObjectId('66229ce1636ad3e4eb1e7fec'), ObjectId('66229ce1636ad3e4eb1e7fed'), ObjectId('66229ce1636ad3e4eb1e7fee'), ObjectId('66229ce1636ad3e4eb1e7fef'), ObjectId('66229ce1636ad3e4eb1e7ff0'), ObjectId('66229ce1636ad3e4eb1e7ff1'), ObjectId('66229ce1636ad3e4eb1e7ff2'), ObjectId('66229ce1636ad3e4eb1e7ff3'), ObjectId('66229ce1636ad3e4eb1e7ff4'), ObjectId('66229ce1636ad3e4eb1e7ff5'), ObjectId('66229ce1636ad3e4eb1e7ff6'), ObjectId('66229ce1636ad3e4eb1e7ff7'), ObjectId('66229ce1636ad3e4eb1e7ff8'), ObjectId('66229ce1636ad3e4eb1e7ff9'), ObjectId('66229ce1636ad3e4eb1e7ffa'), ObjectId('66229ce1636ad3e4eb1e7ffb'), ObjectId('66229ce1636ad3e4eb1e7ffc'), ObjectId('66229ce1636ad3e4eb1e7ffd'), ObjectId('66229ce1636ad3e4eb1e7ffe'), ObjectId('66229ce1636ad3e4eb1e7fff'), ObjectId('66229ce1636ad3e4eb1e8000'), ObjectId('66229ce1636ad3e4eb1e8001'), ObjectId('66229ce1636ad3e4eb1e8002'), ObjectId('66229ce1636ad3e4eb1e8003'), ObjectId('66229ce1636ad3e4eb1e8004'), ObjectId('66229ce1636ad3e4eb1e8005'), ObjectId('66229ce1636ad3e4eb1e8006'), ObjectId('66229ce1636ad3e4eb1e8007'), ObjectId('66229ce1636ad3e4eb1e8008'), ObjectId('66229ce1636ad3e4eb1e8009'), ObjectId('66229ce1636ad3e4eb1e800a'), ObjectId('66229ce1636ad3e4eb1e800b'), ObjectId('66229ce1636ad3e4eb1e800c'), ObjectId('66229ce1636ad3e4eb1e800d'), ObjectId('66229ce1636ad3e4eb1e800e'), ObjectId('66229ce1636ad3e4eb1e800f'), ObjectId('66229ce1636ad3e4eb1e8010'), ObjectId('66229ce1636ad3e4eb1e8011'), ObjectId('66229ce1636ad3e4eb1e8012'), ObjectId('66229ce1636ad3e4eb1e8013'), ObjectId('66229ce1636ad3e4eb1e8014'), ObjectId('66229ce1636ad3e4eb1e8015'), ObjectId('66229ce1636ad3e4eb1e8016'), ObjectId('66229ce1636ad3e4eb1e8017'), ObjectId('66229ce1636ad3e4eb1e8018'), ObjectId('66229ce1636ad3e4eb1e8019'), ObjectId('66229ce1636ad3e4eb1e801a'), ObjectId('66229ce1636ad3e4eb1e801b'), ObjectId('66229ce1636ad3e4eb1e801c'), ObjectId('66229ce1636ad3e4eb1e801d'), ObjectId('66229ce1636ad3e4eb1e801e'), ObjectId('66229ce1636ad3e4eb1e801f'), ObjectId('66229ce1636ad3e4eb1e8020'), ObjectId('66229ce1636ad3e4eb1e8021'), ObjectId('66229ce1636ad3e4eb1e8022'), ObjectId('66229ce1636ad3e4eb1e8023'), ObjectId('66229ce1636ad3e4eb1e8024'), ObjectId('66229ce1636ad3e4eb1e8025'), ObjectId('66229ce1636ad3e4eb1e8026'), ObjectId('66229ce1636ad3e4eb1e8027'), ObjectId('66229ce1636ad3e4eb1e8028'), ObjectId('66229ce1636ad3e4eb1e8029'), ObjectId('66229ce1636ad3e4eb1e802a'), ObjectId('66229ce1636ad3e4eb1e802b'), ObjectId('66229ce1636ad3e4eb1e802c'), ObjectId('66229ce1636ad3e4eb1e802d'), ObjectId('66229ce1636ad3e4eb1e802e'), ObjectId('66229ce1636ad3e4eb1e802f'), ObjectId('66229ce1636ad3e4eb1e8030'), ObjectId('66229ce1636ad3e4eb1e8031'), ObjectId('66229ce1636ad3e4eb1e8032'), ObjectId('66229ce1636ad3e4eb1e8033'), ObjectId('66229ce1636ad3e4eb1e8034'), ObjectId('66229ce1636ad3e4eb1e8035'), ObjectId('66229ce1636ad3e4eb1e8036'), ObjectId('66229ce1636ad3e4eb1e8037'), ObjectId('66229ce1636ad3e4eb1e8038'), ObjectId('66229ce1636ad3e4eb1e8039'), ObjectId('66229ce1636ad3e4eb1e803a'), ObjectId('66229ce1636ad3e4eb1e803b'), ObjectId('66229ce1636ad3e4eb1e803c'), ObjectId('66229ce1636ad3e4eb1e803d'), ObjectId('66229ce1636ad3e4eb1e803e'), ObjectId('66229ce1636ad3e4eb1e803f'), ObjectId('66229ce1636ad3e4eb1e8040'), ObjectId('66229ce1636ad3e4eb1e8041'), ObjectId('66229ce1636ad3e4eb1e8042'), ObjectId('66229ce1636ad3e4eb1e8043'), ObjectId('66229ce1636ad3e4eb1e8044'), ObjectId('66229ce1636ad3e4eb1e8045'), ObjectId('66229ce1636ad3e4eb1e8046'), ObjectId('66229ce1636ad3e4eb1e8047'), ObjectId('66229ce1636ad3e4eb1e8048'), ObjectId('66229ce1636ad3e4eb1e8049'), ObjectId('66229ce1636ad3e4eb1e804a'), ObjectId('66229ce1636ad3e4eb1e804b'), ObjectId('66229ce1636ad3e4eb1e804c'), ObjectId('66229ce1636ad3e4eb1e804d'), ObjectId('66229ce1636ad3e4eb1e804e'), ObjectId('66229ce1636ad3e4eb1e804f'), ObjectId('66229ce1636ad3e4eb1e8050'), ObjectId('66229ce1636ad3e4eb1e8051'), ObjectId('66229ce1636ad3e4eb1e8052'), ObjectId('66229ce1636ad3e4eb1e8053'), ObjectId('66229ce1636ad3e4eb1e8054'), ObjectId('66229ce1636ad3e4eb1e8055'), ObjectId('66229ce1636ad3e4eb1e8056'), ObjectId('66229ce1636ad3e4eb1e8057'), ObjectId('66229ce1636ad3e4eb1e8058'), ObjectId('66229ce1636ad3e4eb1e8059'), ObjectId('66229ce1636ad3e4eb1e805a'), ObjectId('66229ce1636ad3e4eb1e805b'), ObjectId('66229ce1636ad3e4eb1e805c'), ObjectId('66229ce1636ad3e4eb1e805d'), ObjectId('66229ce1636ad3e4eb1e805e'), ObjectId('66229ce1636ad3e4eb1e805f'), ObjectId('66229ce1636ad3e4eb1e8060'), ObjectId('66229ce1636ad3e4eb1e8061'), ObjectId('66229ce1636ad3e4eb1e8062'), ObjectId('66229ce1636ad3e4eb1e8063'), ObjectId('66229ce1636ad3e4eb1e8064'), ObjectId('66229ce1636ad3e4eb1e8065'), ObjectId('66229ce1636ad3e4eb1e8066'), ObjectId('66229ce1636ad3e4eb1e8067'), ObjectId('66229ce1636ad3e4eb1e8068'), ObjectId('66229ce1636ad3e4eb1e8069'), ObjectId('66229ce1636ad3e4eb1e806a'), ObjectId('66229ce1636ad3e4eb1e806b'), ObjectId('66229ce1636ad3e4eb1e806c'), ObjectId('66229ce1636ad3e4eb1e806d'), ObjectId('66229ce1636ad3e4eb1e806e'), ObjectId('66229ce1636ad3e4eb1e806f'), ObjectId('66229ce1636ad3e4eb1e8070'), ObjectId('66229ce1636ad3e4eb1e8071'), ObjectId('66229ce1636ad3e4eb1e8072'), ObjectId('66229ce1636ad3e4eb1e8073'), ObjectId('66229ce1636ad3e4eb1e8074'), ObjectId('66229ce1636ad3e4eb1e8075'), ObjectId('66229ce1636ad3e4eb1e8076'), ObjectId('66229ce1636ad3e4eb1e8077'), ObjectId('66229ce1636ad3e4eb1e8078'), ObjectId('66229ce1636ad3e4eb1e8079'), ObjectId('66229ce1636ad3e4eb1e807a'), ObjectId('66229ce1636ad3e4eb1e807b'), ObjectId('66229ce1636ad3e4eb1e807c'), ObjectId('66229ce1636ad3e4eb1e807d'), ObjectId('66229ce1636ad3e4eb1e807e'), ObjectId('66229ce1636ad3e4eb1e807f'), ObjectId('66229ce1636ad3e4eb1e8080'), ObjectId('66229ce1636ad3e4eb1e8081'), ObjectId('66229ce1636ad3e4eb1e8082'), ObjectId('66229ce1636ad3e4eb1e8083'), ObjectId('66229ce1636ad3e4eb1e8084'), ObjectId('66229ce1636ad3e4eb1e8085'), ObjectId('66229ce1636ad3e4eb1e8086'), ObjectId('66229ce1636ad3e4eb1e8087'), ObjectId('66229ce1636ad3e4eb1e8088'), ObjectId('66229ce1636ad3e4eb1e8089'), ObjectId('66229ce1636ad3e4eb1e808a'), ObjectId('66229ce1636ad3e4eb1e808b'), ObjectId('66229ce1636ad3e4eb1e808c'), ObjectId('66229ce1636ad3e4eb1e808d'), ObjectId('66229ce1636ad3e4eb1e808e'), ObjectId('66229ce1636ad3e4eb1e808f'), ObjectId('66229ce1636ad3e4eb1e8090'), ObjectId('66229ce1636ad3e4eb1e8091'), ObjectId('66229ce1636ad3e4eb1e8092'), ObjectId('66229ce1636ad3e4eb1e8093'), ObjectId('66229ce1636ad3e4eb1e8094'), ObjectId('66229ce1636ad3e4eb1e8095'), ObjectId('66229ce1636ad3e4eb1e8096'), ObjectId('66229ce1636ad3e4eb1e8097'), ObjectId('66229ce1636ad3e4eb1e8098'), ObjectId('66229ce1636ad3e4eb1e8099'), ObjectId('66229ce1636ad3e4eb1e809a'), ObjectId('66229ce1636ad3e4eb1e809b'), ObjectId('66229ce1636ad3e4eb1e809c'), ObjectId('66229ce1636ad3e4eb1e809d'), ObjectId('66229ce1636ad3e4eb1e809e'), ObjectId('66229ce1636ad3e4eb1e809f'), ObjectId('66229ce1636ad3e4eb1e80a0'), ObjectId('66229ce1636ad3e4eb1e80a1'), ObjectId('66229ce1636ad3e4eb1e80a2'), ObjectId('66229ce1636ad3e4eb1e80a3'), ObjectId('66229ce1636ad3e4eb1e80a4'), ObjectId('66229ce1636ad3e4eb1e80a5'), ObjectId('66229ce1636ad3e4eb1e80a6'), ObjectId('66229ce1636ad3e4eb1e80a7'), ObjectId('66229ce1636ad3e4eb1e80a8'), ObjectId('66229ce1636ad3e4eb1e80a9'), ObjectId('66229ce1636ad3e4eb1e80aa'), ObjectId('66229ce1636ad3e4eb1e80ab'), ObjectId('66229ce1636ad3e4eb1e80ac'), ObjectId('66229ce1636ad3e4eb1e80ad'), ObjectId('66229ce1636ad3e4eb1e80ae'), ObjectId('66229ce1636ad3e4eb1e80af'), ObjectId('66229ce1636ad3e4eb1e80b0'), ObjectId('66229ce1636ad3e4eb1e80b1'), ObjectId('66229ce1636ad3e4eb1e80b2'), ObjectId('66229ce1636ad3e4eb1e80b3'), ObjectId('66229ce1636ad3e4eb1e80b4'), ObjectId('66229ce1636ad3e4eb1e80b5'), ObjectId('66229ce1636ad3e4eb1e80b6'), ObjectId('66229ce1636ad3e4eb1e80b7'), ObjectId('66229ce1636ad3e4eb1e80b8'), ObjectId('66229ce1636ad3e4eb1e80b9'), ObjectId('66229ce1636ad3e4eb1e80ba'), ObjectId('66229ce1636ad3e4eb1e80bb'), ObjectId('66229ce1636ad3e4eb1e80bc'), ObjectId('66229ce1636ad3e4eb1e80bd'), ObjectId('66229ce1636ad3e4eb1e80be'), ObjectId('66229ce1636ad3e4eb1e80bf'), ObjectId('66229ce1636ad3e4eb1e80c0'), ObjectId('66229ce1636ad3e4eb1e80c1'), ObjectId('66229ce1636ad3e4eb1e80c2'), ObjectId('66229ce1636ad3e4eb1e80c3'), ObjectId('66229ce1636ad3e4eb1e80c4'), ObjectId('66229ce1636ad3e4eb1e80c5'), ObjectId('66229ce1636ad3e4eb1e80c6'), ObjectId('66229ce1636ad3e4eb1e80c7'), ObjectId('66229ce1636ad3e4eb1e80c8'), ObjectId('66229ce1636ad3e4eb1e80c9'), ObjectId('66229ce1636ad3e4eb1e80ca'), ObjectId('66229ce1636ad3e4eb1e80cb'), ObjectId('66229ce1636ad3e4eb1e80cc'), ObjectId('66229ce1636ad3e4eb1e80cd'), ObjectId('66229ce1636ad3e4eb1e80ce'), ObjectId('66229ce1636ad3e4eb1e80cf'), ObjectId('66229ce1636ad3e4eb1e80d0'), ObjectId('66229ce1636ad3e4eb1e80d1'), ObjectId('66229ce1636ad3e4eb1e80d2'), ObjectId('66229ce1636ad3e4eb1e80d3'), ObjectId('66229ce1636ad3e4eb1e80d4'), ObjectId('66229ce1636ad3e4eb1e80d5'), ObjectId('66229ce1636ad3e4eb1e80d6'), ObjectId('66229ce1636ad3e4eb1e80d7'), ObjectId('66229ce1636ad3e4eb1e80d8'), ObjectId('66229ce1636ad3e4eb1e80d9'), ObjectId('66229ce1636ad3e4eb1e80da'), ObjectId('66229ce1636ad3e4eb1e80db'), ObjectId('66229ce1636ad3e4eb1e80dc'), ObjectId('66229ce1636ad3e4eb1e80dd'), ObjectId('66229ce1636ad3e4eb1e80de'), ObjectId('66229ce1636ad3e4eb1e80df'), ObjectId('66229ce1636ad3e4eb1e80e0'), ObjectId('66229ce1636ad3e4eb1e80e1'), ObjectId('66229ce1636ad3e4eb1e80e2'), ObjectId('66229ce1636ad3e4eb1e80e3'), ObjectId('66229ce1636ad3e4eb1e80e4'), ObjectId('66229ce1636ad3e4eb1e80e5')], acknowledged=True)----


+*In[24]:*+
[source, ipython3]
----
# Connect to PostgreSQL
postgres_conn = psycopg2.connect(
    dbname='Census',
    user='ragu',
    password='Dhuruv@21',
    host='localhost'
)
postgres_cur = postgres_conn.cursor()

----


+*In[28]:*+
[source, ipython3]
----
# Read a sample document from MongoDB
sample_document = collection.find_one()

# Extract field names and types from the sample document
field_names = list(sample_document.keys())
field_types = [type(value).__name__ for value in sample_document.values()]

----


+*In[30]:*+
[source, ipython3]
----
# Function to handle reserved keywords in PostgreSQL
def handle_reserved_keywords(name):
    reserved_keywords = ['all', 'analyse', 'analyze', 'and', 'any', 'array', 'as', 'asc', 'asymmetric', 'both', 'case', 'cast', 'check', 'collate', 'column', 'constraint', 'create', 'current_catalog', 'current_date', 'current_role', 'current_time', 'current_timestamp', 'current_user', 'default', 'deferrable', 'desc', 'distinct', 'do', 'else', 'end', 'except', 'false', 'fetch', 'for', 'foreign', 'from', 'grant', 'group', 'having', 'in', 'initially', 'intersect', 'into', 'lateral', 'leading', 'limit', 'localtime', 'localtimestamp', 'not', 'null', 'offset', 'on', 'only', 'or', 'order', 'placing', 'primary', 'references', 'returning', 'select', 'session_user', 'some', 'symmetric', 'table', 'then', 'to', 'trailing', 'true', 'union', 'unique', 'user', 'using', 'variadic', 'verbose', 'when', 'where', 'window', 'with']
    if name.lower() in reserved_keywords or ' ' in name or '/' in name:
        return f'"{name}"'
    return name
----


+*In[31]:*+
[source, ipython3]
----
# Create the PostgreSQL table dynamically
table_name = 'Census_table'
create_table_query = f"CREATE TABLE {table_name} ("
for field_name, field_type in zip(field_names, field_types):
    postgres_field_name = handle_reserved_keywords(field_name)
    postgres_type = 'NUMERIC' if field_type == 'float'else'VARCHAR(255)' if field_type == 'str' else 'INTEGER'if field_type == 'int' else 'text'
    create_table_query += f"{postgres_field_name} {postgres_type}, "
create_table_query = create_table_query[:-2] + ");"  # Remove the last comma and space
----


+*In[33]:*+
[source, ipython3]
----
# Execute the CREATE TABLE query
postgres_cur.execute(create_table_query)
postgres_conn.commit()
----


+*In[41]:*+
[source, ipython3]
----
!pip install streamlit
----


+*Out[41]:*+
----
Requirement already satisfied: streamlit in ./anaconda3/lib/python3.11/site-packages (1.32.0)
Requirement already satisfied: altair<6,>=4.0 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (5.0.1)
Requirement already satisfied: blinker<2,>=1.0.0 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (1.6.2)
Requirement already satisfied: cachetools<6,>=4.0 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (4.2.2)
Requirement already satisfied: click<9,>=7.0 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (8.1.7)
Requirement already satisfied: numpy<2,>=1.19.3 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (1.26.4)
Requirement already satisfied: packaging<24,>=16.8 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (23.1)
Requirement already satisfied: pandas<3,>=1.3.0 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (2.2.1)
Requirement already satisfied: pillow<11,>=7.1.0 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (10.2.0)
Requirement already satisfied: protobuf<5,>=3.20 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (3.20.3)
Requirement already satisfied: pyarrow>=7.0 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (14.0.2)
Requirement already satisfied: requests<3,>=2.27 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (2.31.0)
Requirement already satisfied: rich<14,>=10.14.0 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (13.3.5)
Requirement already satisfied: tenacity<9,>=8.1.0 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (8.2.2)
Requirement already satisfied: toml<2,>=0.10.1 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (0.10.2)
Requirement already satisfied: typing-extensions<5,>=4.3.0 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (4.9.0)
Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (3.1.37)
Requirement already satisfied: pydeck<1,>=0.8.0b4 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (0.8.0)
Requirement already satisfied: tornado<7,>=6.0.3 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (6.3.3)
Requirement already satisfied: watchdog>=2.1.5 in ./anaconda3/lib/python3.11/site-packages (from streamlit) (2.1.6)
Requirement already satisfied: jinja2 in ./anaconda3/lib/python3.11/site-packages (from altair<6,>=4.0->streamlit) (3.1.3)
Requirement already satisfied: jsonschema>=3.0 in ./anaconda3/lib/python3.11/site-packages (from altair<6,>=4.0->streamlit) (4.19.2)
Requirement already satisfied: toolz in ./anaconda3/lib/python3.11/site-packages (from altair<6,>=4.0->streamlit) (0.12.0)
Requirement already satisfied: gitdb<5,>=4.0.1 in ./anaconda3/lib/python3.11/site-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.7)
Requirement already satisfied: python-dateutil>=2.8.2 in ./anaconda3/lib/python3.11/site-packages (from pandas<3,>=1.3.0->streamlit) (2.8.2)
Requirement already satisfied: pytz>=2020.1 in ./anaconda3/lib/python3.11/site-packages (from pandas<3,>=1.3.0->streamlit) (2023.3.post1)
Requirement already satisfied: tzdata>=2022.7 in ./anaconda3/lib/python3.11/site-packages (from pandas<3,>=1.3.0->streamlit) (2023.3)
Requirement already satisfied: charset-normalizer<4,>=2 in ./anaconda3/lib/python3.11/site-packages (from requests<3,>=2.27->streamlit) (2.0.4)
Requirement already satisfied: idna<4,>=2.5 in ./anaconda3/lib/python3.11/site-packages (from requests<3,>=2.27->streamlit) (3.4)
Requirement already satisfied: urllib3<3,>=1.21.1 in ./anaconda3/lib/python3.11/site-packages (from requests<3,>=2.27->streamlit) (2.0.7)
Requirement already satisfied: certifi>=2017.4.17 in ./anaconda3/lib/python3.11/site-packages (from requests<3,>=2.27->streamlit) (2024.2.2)
Requirement already satisfied: markdown-it-py<3.0.0,>=2.2.0 in ./anaconda3/lib/python3.11/site-packages (from rich<14,>=10.14.0->streamlit) (2.2.0)
Requirement already satisfied: pygments<3.0.0,>=2.13.0 in ./anaconda3/lib/python3.11/site-packages (from rich<14,>=10.14.0->streamlit) (2.15.1)
Requirement already satisfied: smmap<5,>=3.0.1 in ./anaconda3/lib/python3.11/site-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.0)
Requirement already satisfied: MarkupSafe>=2.0 in ./anaconda3/lib/python3.11/site-packages (from jinja2->altair<6,>=4.0->streamlit) (2.1.3)
Requirement already satisfied: attrs>=22.2.0 in ./anaconda3/lib/python3.11/site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (23.1.0)
Requirement already satisfied: jsonschema-specifications>=2023.03.6 in ./anaconda3/lib/python3.11/site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (2023.7.1)
Requirement already satisfied: referencing>=0.28.4 in ./anaconda3/lib/python3.11/site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.30.2)
Requirement already satisfied: rpds-py>=0.7.1 in ./anaconda3/lib/python3.11/site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.10.6)
Requirement already satisfied: mdurl~=0.1 in ./anaconda3/lib/python3.11/site-packages (from markdown-it-py<3.0.0,>=2.2.0->rich<14,>=10.14.0->streamlit) (0.1.0)
Requirement already satisfied: six>=1.5 in ./anaconda3/lib/python3.11/site-packages (from python-dateutil>=2.8.2->pandas<3,>=1.3.0->streamlit) (1.16.0)
----


+*In[42]:*+
[source, ipython3]
----
import streamlit as st
import psycopg2

# Function to run query on the database and return results
def run_query(query):
    conn = psycopg2.connect(
        host="localhost",
        database="Census",
        user="ragu",
        password="Dhuruv@21"
    )

    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    cur.close()
    conn.close()

    return columns, rows


# Streamlit app
def main():
    st.title("Census Data Standardization and Analysis Pipeline")

    # Define SQL queries
    queries = {
        "1.Total Population by District": """
        SELECT district, SUM(population) AS total_population
        FROM census_table
        GROUP BY district
        ORDER BY district ASC;
        """,
        "2.Literate Population by Gender and District": """
        SELECT district, 
       SUM(literate_male) AS male,
       SUM(literate_female) AS female
	FROM census_table
	GROUP BY district
	ORDER BY district ASC;
	""",
        "3.Percentage of workers in each District": """
        SELECT district,
       CASE
           WHEN SUM(population) = 0 THEN 0  -- Handle division by zero
           ELSE ROUND((SUM(male_workers) * 100.0 / SUM(population)), 2)
       END AS percentage_male_workers,
       CASE
           WHEN SUM(population) = 0 THEN 0  -- Handle division by zero
           ELSE ROUND((SUM(female_workers) * 100.0 / SUM(population)), 2)
       END AS percentage_female_workers,
       CASE
           WHEN SUM(population) = 0 THEN 0  -- Handle division by zero
           ELSE ROUND(((SUM(male_workers) + SUM(female_workers)) * 100.0 / SUM(population)), 2)
       END AS percentage_total_workers
	FROM census_table
	GROUP BY district
	ORDER BY district ASC;
         """,
         "4.No of households have access to LPG or PNG as a cooking fuel in each district":"""
         SELECT district, SUM(lpg_or_png_households) AS households_with_access_to_LPG_or_PNG
	 FROM census_table
	 GROUP BY district
	 ORDER BY district ASC;
         """,
         "5.Religious composition of each district": """
         SELECT district,
         SUM(hindus) AS hindus,
         SUM(muslims) AS muslims,
         SUM(christians) AS christians,
	 SUM(sikhs) AS sikhs,
         SUM(buddhists) AS buddhists,
         SUM(jains) AS jains,
         SUM(others_religions) AS others
	 FROM census_table
	 GROUP BY district
	 ORDER BY district ASC;
         """,
         "6.No of households have internet access in each district": """
         SELECT district, SUM(households_with_internet) AS households_with_internet
	 FROM census_table
	 GROUP BY district
	 ORDER BY district ASC;
	 """,
         "7.Educational attainment distribution in each district": """
         SELECT district,
         SUM(below_primary_education) AS below_primary,
         SUM(primary_education) AS primary_,
         SUM(middle_education) AS middle,
	 SUM(secondary_education) AS secondary,
         SUM(higher_education) AS higher,
         SUM(graduate_education) AS graduate,
         SUM(other_education) AS other
	 FROM census_table
	 GROUP BY district
	 ORDER BY district ASC;
         """,
         "8.No of households have access to various modes of transportation (bicycle, car, radio, television, etc.) in each district":"""
         SELECT 
	    district,
	    SUM(households_with_bicycle) AS bicycle,
	    SUM(households_with_car_jeep_van) AS car,
	    SUM(households_with_radio_transistor) AS radio,
	    SUM(households_with_scooter_motorcycle_moped) AS scooter_motorcycle_moped,
	    SUM(households_with_telephone_mobile_phone_landline_only) AS telephone,
	    SUM(households_with_television) AS television
         FROM
            census_table
         GROUP BY
            district
         ORDER BY district ASC;
    """,
    "9.Condition of occupied census houses (dilapidated, with separate kitchen, with bathing facility, with latrine facility, etc.) in each district":"""
SELECT 
    district,
    SUM(condition_of_occupied_census_houses_dilapidated_households) AS dilapidated_households,
    SUM(households_with_separate_kitchen_cooking_inside_house) AS separate_kitchen,
    SUM(having_bathing_facility_total_households) AS bathing_facility,
    SUM(having_latrine_facility_within_the_premises_total_households) AS having_latrine_facility_within_the_premises
FROM
    census_table
GROUP BY
    district
    ORDER BY district ASC;
    """,
    "10.Household size distributed (1 person, 2 persons, 3-5 persons, etc.) in each district":"""
             SELECT 
    district,
    SUM(household_size_1_person_households) AS one_person,
    SUM(household_size_2_persons_households) AS two_person,
    SUM(household_size_1_to_2_persons) AS one_to_two_persons,
    SUM(household_size_3_persons_households) AS three_perons,
    SUM(household_size_3_to_5_persons_households) AS three_to_five_persons,
    SUM(household_size_4_persons_households) AS four_persons,
    SUM(household_size_5_persons_households) AS five_perons,
    SUM(household_size_6_8_persons_households) AS six_to_eight_persons,
    SUM(household_size_9_persons_and_above_households) AS nine_persons_and_above	 
FROM
    census_table
GROUP BY
    district
    ORDER BY district ASC;
    """,
    "11.The total number of households in each state": """
    SELECT district,
SUM(households) AS households
FROM census_table
GROUP BY 
	district
ORDER BY district ASC;
""",
"12.No of households have a latrine facility within the premises in each state":"""
SELECT district,
SUM(having_latrine_facility_within_the_premises_total_households) AS with_latrine_facility
FROM census_table
GROUP BY 
	district
ORDER BY district ASC;
""",
"13.The average household size in each state":"""
SELECT "State/UT", ROUND(AVG(households), 2) AS average_household_size
FROM census_table
GROUP BY "State/UT"
ORDER BY "State/UT" ASC;
""",
"14.No of households owned versus rented in each state":"""
SELECT "State/UT",
	SUM(ownership_owned_households) AS "owned",
    SUM(ownership_rented_households) AS rented
FROM census_table
GROUP BY "State/UT"
ORDER BY "State/UT" ASC;
""",
"15.The distribution of different types of latrine facilities":"""
SELECT "State/UT",
	SUM(type_of_latrine_facility_pit_latrine_households) AS pit_latrine,
    SUM(type_of_latrine_facility_other_latrine_households) AS other_latrine,
    SUM(type_of_latrine_facility_night_soil_disposed_into_open_drain_ho) AS night_soil_disposed_into_open_drain,
	SUM(type_of_latrine_facility_flush_pour_flush_latrine_connected_to_) AS flush_pour_flush_latrine
FROM census_table
GROUP BY "State/UT"
ORDER BY "State/UT" ASC;
""",
"16.No of households have access to drinking water sources near the premises in each state":"""
SELECT "State/UT",
	SUM(location_of_drinking_water_source_near_the_premises_households) AS drinking_water_source_near_the_premise
FROM census_table
GROUP BY "State/UT"
ORDER BY "State/UT" ASC;
""",
"17.The average household income distribution in each state based on the power parity categories":"""
SELECT "State/UT",
       ROUND(AVG(total_power_parity),2) AS average_income
FROM census_table
GROUP BY "State/UT", total_power_parity
ORDER BY "State/UT" ASC;
""",
"18.The percentage of married couples with different household sizes in each state":"""
SELECT 
    "State/UT",
    ROUND(SUM(married_couples_1_households) * 100.0 / SUM(married_couples_1_households + married_couples_2_households + married_couples_3_households + married_couples_4_households + married_couples_5__households), 2) AS percentage_1_married_couples,
    ROUND(SUM(married_couples_2_households) * 100.0 / SUM(married_couples_1_households + married_couples_2_households + married_couples_3_households + married_couples_4_households + married_couples_5__households), 2) AS percentage_2_married_couples,
    ROUND(SUM(married_couples_3_households) * 100.0 / SUM(married_couples_1_households + married_couples_2_households + married_couples_3_households + married_couples_4_households + married_couples_5__households), 2) AS percentage_3_married_couples,
    ROUND(SUM(married_couples_4_households) * 100.0 / SUM(married_couples_1_households + married_couples_2_households + married_couples_3_households + married_couples_4_households + married_couples_5__households), 2) AS percentage_4_married_couples,
    ROUND(SUM(married_couples_5__households) * 100.0 / SUM(married_couples_1_households + married_couples_2_households + married_couples_3_households + married_couples_4_households + married_couples_5__households), 2) AS percentage_5__married_couples
FROM 
    census_table
GROUP BY 
    "State/UT";
""",
"19.Households fall below the poverty line in each state based on the power parity categories":"""
SELECT 
    "State/UT",
    SUM(Power_Parity_Less_than_Rs_45000) AS "Below Poverty Line"
    FROM census_table
    GROUP BY "State/UT"
    ORDER BY "State/UT" ASC;
    """,
"20.The overall literacy rate (percentage of literate population) in each state":"""
SELECT 
    "State/UT",
    ROUND(SUM(literate) * 100.0 / SUM(population), 2) AS literacy_rate
FROM 
    census_table
GROUP BY 
    "State/UT"
ORDER BY 
	"State/UT";
"""
    }

    query_name = st.selectbox("Select query:", list(queries.keys()), key="select_query")

    query = queries[query_name]
    st.text_area("SQL query:", query, key="sql_query")

    if st.button("Run Query", key="run_query_button"):
        try:
            columns, rows = run_query(query)
            if rows:
                st.write("Column Names:")
                st.write(columns)
                st.write("Query Results:")
                for row in rows:
                    row_dict = {columns[i]: row[i] for i in range(len(columns))}
                    st.write(row_dict)
            else:
                st.write("No results found.")
        except Exception as e:
            st.error(f"Error executing query: {str(e)}")

if __name__ == "__main__":
    main()
----


+*Out[42]:*+
----
2024-04-19 22:29:03.220 
  [33m[1mWarning:[0m to view this Streamlit app on a browser, run it with the following
  command:

    streamlit run /home/ragu/anaconda3/lib/python3.11/site-packages/ipykernel_launcher.py [ARGUMENTS]
----


+*In[ ]:*+
[source, ipython3]
----

----
