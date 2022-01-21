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
    __page: str

    def __init__(self, code):
        self.code = code
