import datetime
import platform

import pandas as pd
import requests

import os
from django.conf import settings

# Datasets scraped can be found in the following URL's:
# ¹ Johns Hopkins: https://github.com/CSSEGISandData/COVID-19 
# ² Our World In Data: https://github.com/owid/covid-19-data/tree/master/public/data
# ³ New York Times: https://github.com/nytimes/covid-19-data

# Different styles in zero-padding in date depend on operating systems
if platform.system() == 'Linux':
    STRFTIME_DATA_FRAME_FORMAT = '%-m/%-d/%y'
elif platform.system() == 'Windows':
    STRFTIME_DATA_FRAME_FORMAT = '%#m/%#d/%y'
else:
    STRFTIME_DATA_FRAME_FORMAT = '%-m/%-d/%y'


def daily_report(date_string=None):
    # Reports aggegrade data, dating as far back to 01-22-2020
    # If passing arg, must use above date formatting '01-22-2020'
    report_directory = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
    
    if date_string is None: 
        yesterday = datetime.date.today() - datetime.timedelta(days=2)
        file_date = yesterday.strftime('%m-%d-%Y')
    else: 
        file_date = date_string 
    
    df = pd.read_csv(report_directory + file_date + '.csv', dtype={"FIPS": str})
    return df

# ### change ****************
# def daily_confirmed():
#     # returns the daily reported cases for respective date, 
#     # segmented globally and by country
#     df = pd.read_csv('https://covid.ourworldindata.org/data/ecdc/new_cases.csv')
#     return df
 
# ### change ********************
# def daily_deaths():
#     # returns the daily reported deaths for respective date
#     df = pd.read_csv('https://covid.ourworldindata.org/data/ecdc/new_deaths.csv')
#     return df


def confirmed_report():
    # Returns time series version of total cases confirmed globally
    df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    return df, df[df['Country/Region']=="Nepal"]


def deaths_report():
    # Returns time series version of total deaths globally
    df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    return df, df[df['Country/Region']=="Nepal"]


def recovered_report():
    # Return time series version of total recoveries globally
    df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    return df, df[df['Country/Region']=="Nepal"]


def realtime_growth(date_string=None, weekly=False, monthly=False):
    """[summary]: consolidates all reports, to create time series of statistics.
    Columns excluded with list comp. are: ['Province/State','Country/Region','Lat','Long'].

    Args:
        date_string: must use following date formatting '4/12/20'.
        weekly: bool, returns df for last 8 weks
        monthly: bool, returns df for last 3 months
    Returns:
        [growth_df] -- [growth in series]
    """ 
    df1 = confirmed_report()[0][confirmed_report()[0].columns[4:]].sum()
    df2 = deaths_report()[0][deaths_report()[0].columns[4:]].sum()
    df3 = recovered_report()[0][recovered_report()[0].columns[4:]].sum()

    n_df1 = confirmed_report()[1][confirmed_report()[1].columns[4:]].sum()
    n_df2 = deaths_report()[1][deaths_report()[1].columns[4:]].sum()
    n_df3 = recovered_report()[1][recovered_report()[1].columns[4:]].sum()

    growth_df = pd.DataFrame([])
    growth_df['Confirmed'], growth_df['Deaths'], growth_df['Recovered'],growth_df['n_Confirmed'], growth_df['n_Deaths'], growth_df['n_Recovered'] = df1, df2, df3, n_df1, n_df2, n_df3 
    growth_df.index = growth_df.index.rename('Date')
    
    yesterday = pd.Timestamp('now').date() - pd.Timedelta(days=1)
    
    if date_string is not None: 
        return growth_df.loc[growth_df.index == date_string]
    
    if weekly is True: 
        weekly_df = pd.DataFrame([])
        intervals = pd.date_range(end=yesterday, periods=8, freq='7D').strftime(STRFTIME_DATA_FRAME_FORMAT).tolist()
        for day in intervals:
            weekly_df = weekly_df.append(growth_df.loc[growth_df.index==day])
        return weekly_df
    
    elif monthly is True:
        monthly_df = pd.DataFrame([])
        intervals = pd.date_range(end=yesterday, periods=3, freq='1M').strftime(STRFTIME_DATA_FRAME_FORMAT).tolist()
        for day in intervals:
            monthly_df = monthly_df.append(growth_df.loc[growth_df.index==day])
        return monthly_df
    
    return growth_df


def percentage_trends():
    """[summary]: Returns percentage of change, in comparison to week prior.
    
    Returns:
        [pd.series] -- [percentage objects]
    """    
    current = realtime_growth(weekly=True).iloc[-1]
    last_week = realtime_growth(weekly=True).iloc[-2]
    trends = round(number=((current - last_week)/last_week)*100, ndigits=1)
    
    rate_change = round(((current.Deaths/current.Confirmed)*100)-((last_week.Deaths / last_week.Confirmed)*100), ndigits=2)
    n_rate_change = round(((current.n_Deaths/current.n_Confirmed)*100)-((last_week.n_Deaths / last_week.n_Confirmed)*100), ndigits=2)
    trends = trends.append(pd.Series(data=rate_change, index=['Death_rate']))
    trends = trends.append(pd.Series(data=rate_change, index=['n_Death_rate']))
    return trends


def global_cases():
    """[summary]: Creates a table on total statistics of all countries,
    sorted by confirmations.

    Returns:
        [pd.DataFrame]
    """
    df = daily_report()[['Country_Region', 'Confirmed', 'Recovered', 'Deaths', 'Active']]
    df.rename(columns={'Country_Region':'Country'}, inplace=True) 
    df = df.groupby('Country', as_index=False).sum()  # Dataframe mapper, combines rows where country value is the same
    df.sort_values(by=['Confirmed'], ascending=False, inplace=True)
    
    for index, row in df.iterrows():
        countryCases = int(row['Confirmed'])
        countryDeaths = int(row['Deaths'])
        if(countryCases == 0):
            deathRateFormatted = format(0, '.2f')
            df.loc[index, 'Death Rate'] = deathRateFormatted
        else:
            deathRate = float(countryDeaths / countryCases)*100
            deathRateFormatted = format(deathRate, '.2f')
            df.loc[index, 'Death Rate'] = deathRateFormatted
    return df


def nep_state_counties():
    """[summary]: Returns live cases of Nepal at state level
    
    source:
        ³ nytimes
    Returns:
        [pd.DataFrame]
    """
    populations = pd.read_csv(os.path.join(settings.STATICFILES_DIRS[0],'assets/geo-data/states-details.csv'))
    df = pd.read_csv(os.path.join(settings.STATICFILES_DIRS[0],'assets/geo-data/states-corona-details.csv'))
    df = pd.merge(df, populations, on='STATE')
    df['cases/state'] = (df.cases / df.Population)*1000
    return df


# def nep_districts_counties():
#     """[summary]: Returns live cases of Nepal at district level
    
#     source:
#         ³ nytimes
#     Returns:
#         [pd.DataFrame]
#     """
#     populations = pd.read_csv(os.path.join(settings.STATICFILES_DIRS[0],'assets/geo-data/states-details.csv'))
#     df = pd.read_csv(os.path.join(settings.STATICFILES_DIRS[0],'assets/geo-data/states-corona-details.csv'))
#     df = pd.merge(df, populations, on='STATE')
#     df['cases/state'] = (df.cases / df.Population)*1000

#     url = "https://data.nepalcorona.info/api/v1/districts"
#     response = requests.request(url)
#     data = json.loads(response)

#     df = pd.DataFrame([])
#     df['DIST_EN'] = [data[i]['title_en'] for i in range(77)]

#     return df


def filter_by_gender():
    r = requests.get('http://127.0.0.1:5000/gender')
    data = r.json()
    return [data[1][0], data[2][0]]


def filter_by_age():
    r = requests.get('http://127.0.0.1:5000/age')
    data = r.json()
    return data[1:-1]

def filter_by_districts():
    # in the form of list like label and cases 
    # [['rupandehi',100],[...],[....],['kathmandu',5424]]
    r = requests.get('http://127.0.0.1:5000/districts').json()
    return r