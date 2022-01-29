import struct
from datetime import datetime, timezone
import pytz
import requests
from bs4 import BeautifulSoup


class Fund:
    name: str
    code: str
    last_price: float
    daily_change: float
    number_of_shares: int
    total_value: float
    category: str
    last_year_rank: int
    number_of_investors: int
    market_share: float
    returns = {'last_month': float, 'last_3_months': float, 'last_6_months': float, 'last_year': float}
    historical_prices = []
    page: str
    base_url = 'https://www.tefas.gov.tr'  # http://www.fundturkey.com.tr also possible
    info_endpoint = "/api/DB/BindHistoryInfo"
    detail_endpoint = "/api/DB/BindHistoryAllocation"
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://www.tefas.gov.tr',
        'Referer': 'http://www.tefas.gov.tr/TarihselVeriler.aspx',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    def __init__(self, code):
        self.session = requests.Session()
        _ = self.session.get(self.base_url)
        self.cookies = self.session.cookies.get_dict()
        self.code = code.upper()
        self.page = ''

    def get_fund_page(self):
        if self.page == '':
            url = 'https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod=NNF' + self.code
            self.page = requests.get(url).text
        return self.page

    def get_fund_name(self):
        soup = BeautifulSoup(self.get_fund_page(), 'html.parser')
        self.name = soup.find('span', {'id': 'MainContent_FormViewMainIndicators_LabelFund'}).text

    def get_fund_details(self):
        soup = BeautifulSoup(self.get_fund_page(), 'html.parser')
        self.name = soup.find('span', {'id': 'MainContent_FormViewMainIndicators_LabelFund'}).text

    def get_historical_prices(self, starting_date: str, ending_date: str):
        url = self.base_url + self.info_endpoint
        payload = 'fontip=YAT&fonkod=' + self.code + '&bastarih=' + starting_date + '&bittarih=' + ending_date
        response = requests.request("POST", url, headers=self.headers, data=payload)
        # print(response.text)
        price_data = response.json().get('data', {})
        formatted_prices = {}
        for price in price_data:
            # convert unix timestamp to date
            # get first 10 digits of string
            date = datetime.fromtimestamp(int(price['TARIH'][:10]), pytz.timezone("Europe/Istanbul")).strftime(
                '%d-%m-%Y')
            formatted_prices[date] = price['FIYAT']
        return formatted_prices
