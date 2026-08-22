import pandas as pd
df = pd.read_excel("web_server_log_100_records.xlsx")

#display the first 10 records
print("First 10 Records:")
print(df.head(10))

#Display the last 10 records
print("Last 10 Records:")
print(df.tail(10))

#Shape
print("Shape:")
print(df.shape)

#Column names
print("\nColumn Names:")
print(df.columns)

#Data types
print("\nData Types:")
print(df.dtypes)

#General information
print("\nGeneral Information:")
df.info()

#Descriptive statistics
print("\nDescriptive Statistics:")
print(df.describe())

#First 5 rows
print("\nFirst 5 Rows:")
print(df.head(5))

#Last 5 rows
print("\nLast 5 Rows:")
print(df.tail(5))

#Random sample of 8 records
print("\nRandom Sample of 8 Records:")
print(df.sample(8))

#Missing values
print("\nMissing Values:")
print(df.isnull().sum())

#Number of unique values
print("\nNumber of Unique Values:")
print(df.nunique())

#Unique browser names
print("\nUnique Browser Names:")
print(df['Browser'].unique())

#Frequency of HTTP status codes
print("\nHTTP Status Code Frequencies:")
print(df['Status_Code'].value_counts())

#Display only Browser column
print(df['Browser'])


#Display IP_Address and Status_Code columns
print(df[['IP_Address', 'Status_Code']])


#Display first 10 rows using slicing
print(df[:10])


#Display rows 20 to 30 using iloc
print(df.iloc[20:31])


#Display rows 5 to 15 and Method, URL, Status_Code
print(df.iloc[5:16, [2, 3, 4]])


#Display record with index 25
print(df.loc[25])


#Display records from index 40 to 50
print(df.loc[40:50])


#Display records where Browser is Chrome
print(df[df['Browser'] == 'Chrome'])


#Display records where Status_Code is 404
print(df[df['Status_Code'] == 404])


#Display records where Method is POST
print(df[df['Method'] == 'POST'])


#Display records where Response_Time_ms > 500
print(df[df['Response_Time_ms'] > 500])


#Display URL and Response_Time_ms where Status_Code is 200
print(df.loc[df['Status_Code'] == 200,
             ['URL', 'Response_Time_ms']])


#Browser is Firefox AND Method is GET
print(df[(df['Browser'] == 'Firefox') &
         (df['Method'] == 'GET')])


#Status_Code is either 404 or 500
print(df[df['Status_Code'].isin([404, 500])])


#Display last 15 records
print(df.iloc[-15:])


#Display every 5th record
print(df.iloc[::5])


#First 20 records with selected columns
print(df.loc[:19, ['IP_Address', 'Method', 'Browser']])


#Display URLs containing "products"
print(df[df['URL'].str.contains('products',
                                case=False,
                                na=False)])


#Display indices 5, 15, 25, 35, 45
print(df.loc[[5, 15, 25, 35, 45]])


#Set IP_Address as index
df_ip = df.set_index('IP_Address')

#Display records for a particular IP
print(df_ip.loc['192.168.1.23'])