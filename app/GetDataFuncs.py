import pandas as pd
from sqlalchemy import create_engine, text

global conn

class FinancialData:
    engine = create_engine('postgresql://postgres:soso1015@localhost/FinancialData')
    conn = engine.connect()

    def get_balance_sheets(self, ticker):
        engine = create_engine('postgresql://postgres:soso1015@localhost/FinancialData')
        conn = engine.connect()
        df = pd.DataFrame(conn.execution_options(stream_results=True).execute(text('select * from "{}"."Balance_Sheets"'.format(ticker))))
        return df

    def get_overview_table(self, ticker):
        df = pd.DataFrame(conn.execution_options(stream_results=True).execute(text('select * from "{}"."Company_Overview"'.format(ticker))))
        return df

    def get_income_statements(self, ticker):
        df = pd.DataFrame(conn.execution_options(stream_results=True).execute(text('select * from "{}"."Income_Statements"'.format(ticker))))
        return df
