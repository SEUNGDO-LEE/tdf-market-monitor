import pandas as pd

def load_tdf_csv(file) -> pd.DataFrame:
    """
    사용자가 업로드한 CSV 파일에서 TDF 데이터를 불러옵니다.
    :param file: Streamlit의 file_uploader로 업로드된 파일 객체
    :return: 시계열 순자산총액 데이터 (DataFrame)
    """
    df = pd.read_csv(file)

    # 날짜 컬럼 처리
    df = df.rename(columns=lambda x: x.strip())
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    df = df.dropna(subset=["날짜"])
    df = df.sort_values("날짜").reset_index(drop=True)

    # 숫자형 변환
    num_cols = ["펀드수", "순자산총액", "설정원본", "순유입액"]
    for col in num_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(",", "").astype(float)

    return df
