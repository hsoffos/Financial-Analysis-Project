import pandas as pd
import sqlalchemy

from SomeFuncs import get_balance_sheets, get_company_overview, get_income_statements
from sqlalchemy import create_engine, exc
from sqlalchemy.schema import CreateSchema, CreateTable

conn = 'postgresql://postgres:soso1015@localhost/FinancialData'

schema_name = ""

# Prepare table variables
overview_table = pd.DataFrame()
balance_table = pd.DataFrame()
income_table = pd.DataFrame()

company_symbols = ['IBM', 'MSFT', 'DAC', 'GOOG']

# Call functions for company symbols
for symbol in company_symbols:
    overview_table = pd.concat([overview_table, get_company_overview(symbol)])
    balance_table = pd.concat([balance_table, get_balance_sheets(symbol)])
    income_table = pd.concat([income_table, get_income_statements(symbol)])
    #print(overview_table)
    #print(balance_table)
    #print(income_table)
    schema_name = str(symbol)
    engine = create_engine('postgresql://postgres:soso1015@localhost/FinancialData')
    try:
        engine.execute(CreateSchema(schema_name))
    except sqlalchemy.exc.ProgrammingError:
        pass
    overview_table.to_sql('Company_Overview', engine, if_exists='replace', schema=schema_name)
    balance_table.to_sql('Balance_Sheets', engine, if_exists='replace', schema=schema_name)
    income_table.to_sql('Income_Statements', engine, if_exists='replace', schema=schema_name)
    #engine.execute(CreateTable)
    # Empty tables between symbols
    overview_table = overview_table.iloc[0:0]
    balance_table = balance_table.iloc[0:0]
    income_table = income_table.iloc[0:0]
    print(symbol, " Success")

print("Finished : ", company_symbols)

