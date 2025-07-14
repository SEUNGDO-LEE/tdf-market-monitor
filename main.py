# main.py
import streamlit as st
from datetime import date, timedelta, datetime as dt
from get_tdf_yield import fetch_asset_returns
from get_tdf_market import load_tdf_csv
from draw_charts import plot_asset_returns, draw_tdf_market_trend
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd


st.set_page_config(page_title="TDF 시장 모니터링", layout="wide")
st.title("📈 TDF(Target Date Fund) 시장 모니터링")

tab1, tab2 = st.tabs(["자산군별 수익률", "국내 TDF 시장 추이"])

# ─────────────────── TAB 1 ────────────────────
with tab1:
    
    st.subheader("📊 자산군별 수익률 현황")
    col1, col2 = st.columns(2)
    default_start = date.today() - timedelta(days=7)

    with col1:
        start_date = st.date_input("시작일", default_start,
                                key="tab1_start")
    with col2:
        end_date = st.date_input("종료일", date.today(),
                                key="tab1_end")

    if start_date >= end_date:
        st.error("⛔ 시작일은 종료일보다 앞서야 합니다.")
    else:
        with st.spinner("자산군별 수익률 조회 중"):
            asset_df = fetch_asset_returns(start_date, end_date)
            st.dataframe(asset_df)
            plot_asset_returns(asset_df)

# ─────────────────── TAB 2 ────────────────────
with tab2:
    st.subheader("📈 TDF 시장 현황 (CSV 기반)")
    st.markdown(
        """
        <a href="https://docs.google.com/spreadsheets/d/e/2PACX-1vRmIynF-2CN1SuW9Umo05scJS-VeamxlhKv__juw0rgtb_Jbp_bYCw4rkxfrb7HBQ/pub?gid=1953031699&single=true&output=csv" target="_blank">
            <button style='font-size:16px;padding:10px 20px;'>📥 샘플 TDF 데이터 다운로드 (CSV)</button><br></br>
        </a>
    """,    unsafe_allow_html=True
    )
    uploaded_file = st.file_uploader("TDF 시장 데이터를 포함한 CSV 파일을 업로드하세요", type=["csv"])

    if uploaded_file:
        df = load_tdf_csv(uploaded_file)
        st.success("✅ 데이터 업로드 및 처리 완료")

        st.dataframe(df)

        st.markdown("---")
        draw_tdf_market_trend(df)
    else:
        st.warning("⚠️ CSV 파일을 업로드해 주세요.")
    