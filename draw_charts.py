# draw_charts.py
import matplotlib.pyplot as plt
import streamlit as st

def plot_asset_returns(df):
    fig, ax = plt.subplots(figsize=(14, 6))  # 넓고 여유 있는 그래프 크기

    # 색상 10개
    colors = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
    ]

    df = df.copy()

    # ✅ 자산군 라벨을 두 줄로 분리 ("중국 (FXI)" → "중국\n(FXI)")
    df.index = [label.replace("(", "\n(") for label in df.index]
    df.index = df.index.astype(str)

    # 막대그래프
    bars = ax.bar(df.index, df["누적 수익률 (%)"], color=colors[:len(df)])
    
    

    ax.set_title("Asset Class Returns", fontsize=16)
    ax.set_ylabel("Return (%)")

    # ✅ x축 라벨과 레이블 사이 간격 확대
    ax.set_xlabel("Asset", labelpad=20)
    ax.grid(True, linestyle="--", alpha=0.5)

    # ✅ 작은 글씨로 두 줄 레이블 표현
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(df.index, rotation=45, ha='center', fontsize=9)

    # 수익률 값 표시
    for bar, value in zip(bars, df["누적 수익률 (%)"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.5,                  # ✅ 항상 위쪽에 위치
            f"{value:.2f}%",
            ha='center',
            va='bottom',
            fontsize=8
        )

    # ✅ 충분한 하단 여백 확보
    plt.subplots_adjust(bottom=0.35)

    st.pyplot(fig)
    
def draw_tdf_market_trend(df):
    st.markdown("### 📊 순자산총액 시계열")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["날짜"], df["순자산총액"], marker="o")
    ax.set_title("TDF Net Asset Value Trend")
    ax.set_ylabel("억원")
    ax.grid(True)
    st.pyplot(fig)

    st.markdown("### 🔄 전월 대비 증감률")
    df["MoM"] = df["순자산총액"].pct_change() * 100
    st.bar_chart(df.set_index("날짜")["MoM"])
