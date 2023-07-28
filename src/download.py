import pandas as pd
import streamlit as st
from neoscr.utils import let_only_digits

def download_button(df: pd.DataFrame, doc: str, name_suffix: str):
    st.download_button(
        label="Download", 
        data=df.to_csv(sep=';', index=False).encode("utf-8"),
        file_name=f'{let_only_digits(doc)}_{name_suffix}.csv',
        mime='text/csv'
    )
