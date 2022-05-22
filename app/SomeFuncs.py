import requests
import pandas as pd


def get_balance_sheets(ticker):
    fields = ['fiscalDateEnding', 'reportedCurrency', 'totalAssets', 'totalCurrentAssets',
              'cashAndCashEquivalentsAtCarryingValue', 'cashAndShortTermInvestments', 'inventory',
              'currentNetReceivables', 'totalNonCurrentAssets', 'propertyPlantEquipment',
              'accumulatedDepreciationAmortizationPPE', 'intangibleAssets', 'intangibleAssetsExcludingGoodwill',
              'goodwill', 'investments', 'longTermInvestments', 'shortTermInvestments', 'otherCurrentAssets',
              'otherNonCurrrentAssets', 'totalLiabilities', 'totalCurrentLiabilities', 'currentAccountsPayable',
              'deferredRevenue', 'currentDebt', 'shortTermDebt', 'totalNonCurrentLiabilities',
              'capitalLeaseObligations', 'longTermDebt', 'currentLongTermDebt', 'longTermDebtNoncurrent',
              'shortLongTermDebtTotal',
              'otherCurrentLiabilities', 'otherNonCurrentLiabilities', 'totalShareholderEquity', 'treasuryStock',
              'retainedEarnings', 'commonStock', 'commonStockSharesOutstanding']
    df = pd.DataFrame()
    func = 'BALANCE_SHEET'
    apikey = 'KM2RBMGCOTIXETTD'
    url = "https://www.alphavantage.co/query?function={}&symbol={}&apikey={}".format(func, ticker, apikey)
    r = requests.get(url)
    f = r.json()
    for metadata in f:
        if metadata == 'symbol':
            continue
        if metadata == 'annualReports':
            continue
        for i, detail in enumerate(f[metadata]):
            frame_values = list(f[metadata][i].values())
            df2 = pd.DataFrame(frame_values).T
            df2.set_index([pd.Series(i)])
            df = pd.concat([df, df2])

    df.columns = fields
    df['symbol'] = ticker
    # print(df)
    return df


def get_income_statements(ticker):
    fields = ["fiscalDateEnding", "reportedCurrency", "grossProfit", "totalRevenue",
              "costOfRevenue", "costofGoodsAndServicesSold", "operatingIncome",
              "sellingGeneralAndAdministrative", "researchAndDevelopment", "operatingExpenses",
              "investmentIncomeNet", "netInterestIncome", "interestIncome",
              "interestExpense", "nonInterestIncome", "otherNonOperatingIncome",
              "depreciation", "depreciationAndAmortization", "incomeBeforeTax",
              "incomeTaxExpense", "interestAndDebtExpense", "netIncomeFromContinuingOperations",
              "comprehensiveIncomeNetOfTax", "ebit", "ebitda", "netIncome"]

    df = pd.DataFrame()
    func = 'INCOME_STATEMENT'
    apikey = 'KM2RBMGCOTIXETTD'
    url = "https://www.alphavantage.co/query?function={}&symbol={}&apikey={}".format(func, ticker, apikey)
    r = requests.get(url)
    f = r.json()
    for metadata in f:
        if metadata == 'symbol':
            continue
        if metadata == 'quarterlyReports':
            continue
        for i, detail in enumerate(f[metadata]):
            df2 = pd.DataFrame(list(f[metadata][i].values())).T
            df2.set_index([pd.Series(i)])
            df = pd.concat([df, df2])

    df.columns = fields
    df['symbol'] = ticker
    return df.reset_index()


def get_company_overview(ticker):
    fields = ["Symbol", "AssetType", "Name", "Description",
              "CIK", "Exchange", "Currency", "Country", "Sector",
              "Industry", "Address", "FiscalYearEnd", "LatestQuarter",
              "MarketCapitalization", "EBITDA", "PERatio", "PEGRatio", "BookValue",
              "DividendPerShare", "DividendYield", "EPS", "RevenuePerShareTTM", "ProfitMargin",
              "OperatingMarginTTM", "ReturnOnAssetsTTM", "ReturnOnEquityTTM", "RevenueTTM",
              "GrossProfitTTM", "DilutedEPSTTM", "QuarterlyEarningsGrowthYOY",
              "QuarterlyRevenueGrowthYOY", "AnalystTargetPrice", "TrailingPE",
              "ForwardPE", "PriceToSalesRatioTTM", "PriceToBookRatio", "EVToRevenue",
              "EVToEBITDA", "Beta", "52WeekHigh", "52WeekLow", "50DayMovingAverage",
              "200DayMovingAverage", "SharesOutstanding", "DividendDate", "ExDividendDate"]

    df = pd.DataFrame()
    func = 'OVERVIEW'
    apikey = 'KM2RBMGCOTIXETTD'
    url = "https://www.alphavantage.co/query?function={}&symbol={}&apikey={}".format(func, ticker, apikey)
    r = requests.get(url)
    f = r.json()

    df2 = pd.DataFrame(list(f.values())).T
    # df2.set_index([pd.Series(0)])
    df = pd.concat([df, df2])

    df.columns = fields
    df['symbol'] = ticker
    return df.reset_index()

