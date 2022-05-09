import requests
import requests_random_user_agent  # pip install requests-random-user-agent
import pandas as pd
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import re
import sqlite3
from sqlite3 import Error
import os
import sys
from contextlib import closing  # pip install contextlib2
import time
from dateutil import parser  # pip install python-dateutil
from datetime import datetime

# You can find company's tickers wherever
company_symbols = ['IBM', 'SPY', 'MSFT']

# Enter the database name that you want to use and populate.
# The database will be automatically created if it does not exist.
db_name = 'beginningDB.db'
# Specify the folder path for DB file. For example "C:\sqlite\db"
folder_path = r"C:\Users\hsoff\Desktop\!!!beginningDB"
db_path = f"{folder_path}\{db_name}"
# Enter the date range for the filings in the 'YYYY-MM-DD' format
# start_date = '2014-01-01'
# end_date = '2022-01-01'


# Create a class to handle connection(s) to SQLite database(s).
class DBConnection:

    # Initialize the object's attributes.
    def __init__(self, db_name, folder_path, db_path):
        self.db_name = db_name
        self.folder_path = folder_path

    # Create a directory for the DB file if the directory does not exist.
    def create_folder(self):
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            print(f'Successfully created a new folder path {self.folder_path}.')
        else:
            print(f'Folder path {self.folder_path} already exists.')

    # Open connection to the database, if connection fails abort the program.
    # If the DB file does not already exist, it will be automatically created.
    @classmethod
    def open_conn(cls, db_path):
        try:
            cls.conn = sqlite3.connect(db_path)
            print(f'Successfully connected to the {db_path} database.')
            return cls.conn
        except sqlite3.Error as e:
            print(f'Error occurred, unable to connect to the {db_path} database.\
                    \n{e}\nAborting program.')
            # sys.exit(0) means the program is exiting without any errors
            # sys.exit(1) means there was an error.
            sys.exit(1)

    # Close connection to the database.
    @classmethod
    def close_conn(cls):
        try:
            cls.conn.commit()
            print('Committed transactions.')
            cls.conn.close()
            print('Closing all database connections.')
        except Exception as e:
            print(f'Unable to close database connection.\n{e}')


class Filing_Links:

    def __init__(self, company_symbols, start_date='', end_date=''):
        self.company_symbols = company_symbols
        self.start_date = start_date
        self.end_date = end_date

    # Get available filings types for a specific company and their respective links.
    def Get_Balance_Sheets(self):
        try:
            for symbol in self.company_symbols:

                cols = []
                func = 'BALANCE_SHEET'  # func of choice
                symbol = symbol  # company ticker
                apikey = 'DMB5030TBJJ2GX0I'
                url = "https://www.alphavantage.co/query?function={}&symbol={}&apikey={}".format(func,
                                                                                                 symbol,
                                                                                                 apikey)
                r = requests.get(url)
                f = r.json()

                for metadata in f:  # contains 'symbol','annualReports','quarterlyReports'
                    if metadata == 'annualReports':

                        cols = list(f[metadata][1].keys())  # List all columns in the annual report

                        for i, detail in enumerate(f[metadata]):  # enumerate all dictionaries in metadata
                            fiscalDateEnding = f[metadata]['fiscalDateEnding']
                            reportedCurrency = f[metadata]['reportedCurrency']
                            totalAssets = f[metadata]['totalAssets']
                            totalCurrentAssets = f[metadata]['totalCurrentAssets']
                            cashAndCashEquivalentsAtCarryingValue = f[metadata]['cashAndCashEquivalentsAtCarryingValue']
                            cashAndShortTermInvestments = f[metadata]['cashAndShortTermInvestments']
                            inventory = f[metadata]['inventory']
                            currentNetReceivables = f[metadata]['currentNetReceivables']
                            totalNonCurrentAssets = f[metadata]['totalNonCurrentAssets']
                            propertyPlantEquipment = f[metadata]['propertyPlantEquipment']
                            accumulatedDepreciationAmortizationPPE = f[metadata]['accumulatedDepreciationAmortizationPPE']
                            intangibleAssets = f[metadata]['intangibleAssets']
                            intangibleAssetsExcludingGoodwill = f[metadata]['intangibleAssetsExcludingGoodwill']
                            goodwill = f[metadata]['goodwill']
                            investments = f[metadata]['investments']
                            longTermInvestments = f[metadata]['longTermInvestments']
                            shortTermInvestments = f[metadata]['shortTermInvestments']
                            otherCurrentAssets = f[metadata]['otherCurrentAssets']
                            otherNonCurrrentAssets = f[metadata]['otherNonCurrrentAssets']
                            totalLiabilities = f[metadata]['totalLiabilities']
                            totalCurrentLiabilities = f[metadata]['totalCurrentLiabilities']
                            currentAccountsPayable = f[metadata]['currentAccountsPayable']
                            deferredRevenue = f[metadata]['deferredRevenue']
                            currentDebt = f[metadata]['currentDebt']
                            shortTermDebt = f[metadata]['shortTermDebt']
                            totalNonCurrentLiabilities = f[metadata]['totalNonCurrentLiabilities']
                            capitalLeaseObligations = f[metadata]['capitalLeaseObligations']
                            longTermDebt = f[metadata]['longTermDebt']
                            currentLongTermDebt = f[metadata]['currentLongTermDebt']
                            longTermDebtNoncurrent = f[metadata]['longTermDebtNoncurrent']
                            shortLongTermDebtTotal = f[metadata]['shortLongTermDebtTotal']
                            otherCurrentLiabilities = f[metadata]['otherCurrentLiabilities']
                            otherNonCurrentLiabilities = f[metadata]['13996000000']
                            totalShareholderEquity = f[metadata]['18901000000']
                            treasuryStock = f[metadata]['169392000000']
                            retainedEarnings = f[metadata]['154209000000']
                            commonStock = f[metadata]['']
                            commonStockSharesOutstanding = f[metadata]['']

                            for newdata in f[metadata][i]:  # newdata is the key to balance sheet's actual data
                                print(newdata, ":", f[metadata][i][newdata])
                                fiscal_date_end = 2021 - 12 - 31
                                reported_currency = USD
                                totalAssets = 132001000000
                                totalCurrentAssets = 29539000000
                                cashAndCashEquivalentsAtCarryingValue = 6650000000
                                cashAndShortTermInvestments = 6650000000
                                inventory = 1649000000
                                currentNetReceivables = 14977000000
                                totalNonCurrentAssets = 101786000000
                                propertyPlantEquipment = 5694000000
                                accumulatedDepreciationAmortizationPPE = 14390000000
                                intangibleAssets = 68154000000
                                intangibleAssetsExcludingGoodwill = 12511000000
                                goodwill = 55643000000
                                investments = 199000000
                                longTermInvestments = 159000000
                                shortTermInvestments = 600000000
                                otherCurrentAssets = 5663000000
                                otherNonCurrrentAssets = 17815000000
                                totalLiabilities = 113005000000
                                totalCurrentLiabilities = 33619000000
                                currentAccountsPayable = 3955000000
                                deferredRevenue = 16095000000
                                currentDebt = 13551000000
                                shortTermDebt = 6787000000
                                totalNonCurrentLiabilities = 90188000000
                                capitalLeaseObligations = 63000000
                                longTermDebt = 56193000000
                                currentLongTermDebt = 6728000000
                                longTermDebtNoncurrent = 44917000000
                                shortLongTermDebtTotal = 110496000000
                                otherCurrentLiabilities = 9386000000
                                otherNonCurrentLiabilities = 13996000000
                                totalShareholderEquity = 18901000000
                                treasuryStock = 169392000000
                                retainedEarnings = 154209000000
                                commonStock = 57319000000
                                commonStockSharesOutstanding


                            cols = set(cols)
                            self.info_to_sql()





                            self.info_to_sql(Company_Name, Company_CIK_Number, Account_Number,
                                             Filing_Type, Filing_Number, Filing_Date, Document_Link,
                                             Interactive_Data_Link, Filing_Number_Link, Summary_Link_Xml)
        except Exception as e:
            print(f"Could not retrieve the table containing the necessary information.\
                    \nAborting the program.\nIf index list is out of range, make sure \
                    that you entered the correct CIK number(s).\n{e}")
            sys.exit(1)

    # Migrate the DataFrame containing, filing and document links information to a local SQLite database.
    def info_to_sql(self, Company_Name, Company_CIK_Number, Account_Number,
                    Filing_Type, Filing_Number, Filing_Date, Document_Link,
                    Interactive_Data_Link, Filing_Number_Link, Summary_Link_Xml):

        with DBConnection.open_conn(db_path) as conn:
            try:
                with closing(conn.cursor()) as cursor:
                    cursor.execute(
                        """
                    CREATE TABLE IF NOT EXISTS filing_list (
                    filing_number integer PRIMARY KEY,
                    account_number integer,
                    company_name text NOT NULL,
                    cik integer NOT NULL,
                    filing_type text NOT NULL,
                    filing_date text NOT NULL,
                    document_link_html TEXT NOT NULL,
                    filing_number_link TEXT NOT NULL,
                    interactive_dash_link TEXT,
                    summary_link_xml TEXT
                    )
                    ;""")
            except ValueError as e:
                print(f"Error occurred while attempting to create filing_list table.\
                        \nAbording the program.\n{e}")
                sys.exit(1)
            else:
                print("Successfully created the table.")
                print(f"Migrating information for filing number {Filing_Number} to the SQL table.......")
                try:
                    # INSERT or IGNORE will insert a record if it does NOT duplicate an existing record.
                    with closing(conn.cursor()) as cursor:
                        cursor.execute(
                            """
                        INSERT or IGNORE INTO filing_list (
                        filing_number,
                        account_number,
                        company_name,
                        cik,
                        filing_type,
                        filing_date,
                        document_link_html,
                        filing_number_link,
                        interactive_dash_link,
                        summary_link_xml
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """
                            , (
                                Filing_Number,
                                Account_Number,
                                Company_Name,
                                Company_CIK_Number,
                                Filing_Type,
                                Filing_Date,
                                Document_Link,
                                Filing_Number_Link,
                                Interactive_Data_Link,
                                Summary_Link_Xml
                            ))
                except ValueError as e:
                    print(f"Error occurred while attempting to insert values into the filing_list table.\n{e}")

        DBConnection.close_conn()

    # Extract individual table links to financial statements, supplementary data tables, etc

class Extract_Data:

    def __init__(self):
        self.df_xml = None

    # Extract table data from a .XMK
    def htm_table_extractor(self, report_url):
        # Note to self, .text is in Unicode, .content is in bytes.
        response_xml = requests.get(report_url).content
        time.sleep(0.1)
        soup_xml = BeautifulSoup(response_xml, "lxml")
        table = soup_xml.find_all('table')
        if table:
            try:
                print("Inserting table data into the DataFrame.")
                self.df_xml = pd.read_html(str(table))[0]
                self.df_xml = self.df_xml.replace({'\$': ''}, regex=True) \
                    .replace({'\)': ''}, regex=True) \
                    .replace({'\(': ''}, regex=True) \
                    .replace({'\%': ''}, regex=True) \
                    .replace({' ', '', 1}, regex=True)

            except Exception as e:
                print(f'Error occurred while attempting to insert \
                        table data into the DataFrame.\n{e}')
        else:
            print(f'No table detected for {report_url}.')

    # Retreive the necessary information information to extract data from the table's URL.
    def get_tables(self):

        dfs = []
        with DBConnection.open_conn(db_path) as conn:
            for company_CIK in filings1.company_CIKs:
                for filing_type in filings1.filing_types:
                    try:
                        df = pd.read_sql_query(
                            """
                            SELECT a.filing_number,
                                   a.company_name,
                                   a.filing_type,
                                   a.filing_date,
                                   b.short_name ,
                                   b.report_url
                            FROM filing_list a
                            INNER JOIN individual_report_links b
                            ON a.filing_number = b.filing_number
                            WHERE b.report_url LIKE '%.htm%'
                            AND a.cik = ?
                            AND a.filing_type = ?
                            AND a.filing_date BETWEEN ? AND ?
                            ORDER by filing_date DESC
                            LIMIT ?
                            """, con=conn, params=(company_CIK, filing_type,
                                                   filings1.start_date,
                                                   filings1.end_date, 10))
                        dfs.append(df)
                    except ValueError as e:
                        print(f"Error occurred while attempting to retreive data \
                                from the SQL database.\nAbording the program.\n{e}")
                        sys.exit(1)
            df_query1 = pd.concat(dfs)
            # If the DataFrame is empty, terminate the program.
            if len(df_query1) == 0:
                print('DataFrame is empty, aborting the program.\nAbording the program.')
                sys.exit(1)
            else:
                # If maximum recursion error occurs, increase recursion limit. sys.setrecursionlimit(25000)
                pass
            for filing_number, \
                company_name, \
                filing_type, \
                filing_date, \
                short_name, \
                report_url in df_query1.itertuples(index=False):
                print(f'Processing {short_name} table at {report_url}.')

                if report_url.endswith('.htm'):
                    try:
                        self.htm_table_extractor(report_url)
                    except ValueError as e:
                        print(f"Could not retreive the table for filing number \
                                {filing_number} at {report_url}\n{e}")
                        break
                    else:
                        try:
                            # We want to name the table with a unique table name for easy reference.
                            table_name = filing_type + filing_date + '_' + \
                                         short_name.replace(' ', '_') + '_' + str(filing_number)
                            # Remove all special characters except for '_'
                            table_name = re.sub(r"[^a-zA-Z0-9]+", '_', table_name)
                            print(f'Inserting data from the DataFrame into SQL table {table_name}')
                            # Check to see if table already exists in the database to avoid duplicate records.
                            with closing(conn.cursor()) as cursor:
                                cursor.execute(f""" SELECT count(name)
                                              FROM sqlite_master
                                              WHERE type='table' AND name= '{table_name}' """)  # SQL injection vulnerability.
                                # If count is 1, then table exists
                                if cursor.fetchone()[0] == 1:
                                    print(f'Table {table_name} already exists.')
                                else:
                                    # Write records that are stored in the DataFrame into a SQL server database.
                                    self.df_xml.to_sql(con=conn,
                                                       name=table_name,
                                                       schema='SCHEMA',
                                                       index=False,
                                                       if_exists='fail')
                        except ValueError as e:
                            print(f"Could not migrate the {short_name} table to the SQL database.\n{e}")
                elif report_url.endswith('.xml'):
                    print('.xml extension link detected. Unable to to process the table.\
                           \n.xml extension link support is expected to be developed in the future.')
                else:
                    print(f'Table for filing number {filing_number} could not be detected.')

        DBConnection.close_conn()

    # Normalize the data.
    def transpose(self):

        db2_path = db_path.replace('.db', '_transposed.db')
        with DBConnection.open_conn(db_path) as conn:
            try:
                df_table_list = pd.read_sql_query(
                    """
                SELECT name AS table_name
                FROM sqlite_master
                WHERE type='table'
                """, conn)
            except ValueError as e:
                print(f"Could not retrieve table list.\n{e}")
            for row in df_table_list.itertuples(index=False):
                try:
                    df_table = pd.read_sql_query(
                        """ SELECT * FROM "{}" """.format(row.table_name), con=conn)
                except ValueError as e:
                    print(f"Could not read table {table_name}.\n{e}")
                else:
                    try:
                        while row.table_name not in ['filing_list', 'individual_report_links']:
                            # Remove duplicate rows that have the same values.
                            df_table = df_table.drop_duplicates()
                            # Transpose the pandas DataFrame.
                            df_table = df_table.T
                            # Transform first rows into the header.
                            df_table.columns = df_table.iloc[0]
                            df_table = df_table[1:]
                            # Remove special characters, replace empty spaces with _
                            df_table = df_table.rename(columns=lambda x: re.sub('\W+', '_', str(x)))
                            df_table.columns = df_table.columns.str.strip('_')
                            df_table.columns = df_table.columns.str.lower()
                            # Convert index of the DataFrame into a column.
                            df_table.reset_index(level=0, inplace=True)
                            # Format the date column.
                            try:
                                date_list = []
                                for item in df_table.iloc[:, 0]:
                                    match = re.search('\D{3}. \d{2}, \d{4}', item)
                                    if match is not None:
                                        # .strftime removes the time stamp.
                                        date = parser.parse(match.group()).strftime("%Y-%m-%d")
                                        date_list.append(date)
                                    else:
                                        date_list.append(item)
                                df_table.rename(columns={df_table.columns[0]: "date"}, inplace=True)
                                df_table['date'] = date_list
                                print('Successfully formatted the date.')
                            except Exception as e:
                                df_table.rename(columns={df_table.columns[0]: "name"}, inplace=True)
                                print(e)

                            # Convert rows to numeric data types such as integers and floats.
                            df_table.replace(',', '', regex=True, inplace=True)
                            df_table = df_table.apply(pd.to_numeric, errors='ignore')
                            # Dynamically rename duplicate rows that have the same name.
                            if any(df_table.columns.duplicated()):
                                print('Duplicate column name detected.\nRenaming the duplicate column name.  ')
                                columns_series = pd.Series(df_table.columns)
                                for dup in columns_series[columns_series.duplicated()].unique():
                                    columns_series[columns_series[columns_series == dup].index.values.tolist()] = \
                                        [dup + '.' + str(i) if i != 0 else dup for i in
                                         range(sum(columns_series == dup))]
                                df_table.columns = columns_series
                            break
                    except Exception as e:
                        print(f"Could not transpose the table.\n{e}")
                    else:
                        with DBConnection.open_conn(db2_path) as conn2:
                            # Check to see if table already exists in the database.
                            with closing(conn2.cursor()) as cursor:
                                cursor.execute(f""" SELECT count(name)
                                              FROM sqlite_master
                                              WHERE type='table' AND name= '{row.table_name}' """)  # SQL injection vulnerability.
                                # If count is 1, then table exists
                                if cursor.fetchone()[0] == 1 and row.table_name not in ['filing_list',
                                                                                        'individual_report_links']:
                                    print(f'Table {row.table_name} already exists.')
                                else:
                                    try:
                                        print(f'Connected to the {db2_path} database.')
                                        print(f'Inserting data from the DataFrame into SQL table {row.table_name}')
                                        # Write records that are stored in the DataFrame into a SQL server database.
                                        df_table.to_sql(con=conn2,
                                                        name=row.table_name,
                                                        schema='SCHEMA',
                                                        if_exists='replace',
                                                        index=False
                                                        )

                                    except Exception as e:
                                        print(
                                            f"Could not migrate the {row.table_name} table to the normalized SQL database.\n{e}")
        DBConnection.close_conn()


connection1 = DBConnection(db_name, folder_path, db_path)
connection1.create_folder()
filings1 = Filing_Links(company_CIKs, filing_types, start_date, end_date)
filings1.Get_Filing_Links()
filings1.get_table_links()
data1 = Extract_Data()
data1.get_tables()
data1.transpose()