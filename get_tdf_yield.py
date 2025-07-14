# get_tdf_yield.py
import yfinance as yf
import pandas as pd

ASSET_TICKERS = {
    "Global\n(ACWI)": "ACWI",
    "US\n(SPY)": "SPY",
    "Korea\n(KODEX200)": "KODEX200.KS",
    "Nasdaq\n(QQQ)": "QQQ",
    "Japan\n(EWJ)": "EWJ",
    "Europe\n(VGK)": "VGK",
    "China\n(FXI)": "FXI",
    "Emerging\n(EEM)": "EEM",
    "Bond\n(TLT)": "TLT",
    "Gold\n(GLD)": "GLD"
}


def fetch_asset_returns(start_date, end_date):
    returns_dict = {}

    for name, ticker in ASSET_TICKERS.items():
        try:
            data = yf.download(ticker, start=start_date, end=end_date)

            if data.empty:
                print(f"[경고] {name}({ticker})에 대한 데이터가 비어 있습니다.")
                continue

            if isinstance(data.columns, pd.MultiIndex):
                close_price = data[("Close", ticker)] if ("Close", ticker) in data.columns else None
            else:
                close_price = data.get("Adj Close") or data.get("Close")

            if close_price is None:
                print(f"[경고] {name}({ticker})에 유효한 종가 컬럼이 없습니다.")
                continue

            returns = (close_price[-1] / close_price[0] - 1) * 100
            returns_dict[name] = round(returns, 2)

        except Exception as e:
            print(f"[에러] {name}({ticker}) 수익률 계산 중 오류 발생: {e}")
            continue

    # 상위 10개 수익률 기준으로 정렬 후 DataFrame 반환
    sorted_returns = dict(sorted(returns_dict.items(), key=lambda x: x[1], reverse=True)[:10])
    df = pd.DataFrame.from_dict(sorted_returns, orient='index', columns=["누적 수익률 (%)"])

    return df
