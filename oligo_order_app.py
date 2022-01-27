import streamlit as st
import pandas as pd
import oligomass as omass


def get_order_dataframe(names, seqs):
    names = names.split('\n')
    seqs = seqs.split('\n')

    df = pd.DataFrame({'Name': names})
    df['Sequence'] = seqs

    df['Mass, Da'] = [round(omass.oligoSeq(s).getMolMass(), 2) for s in seqs]

    df['Extinction'] = [omass.get_simple_ssdna_extinction(s, omass.get_extinction_dict()) for s in seqs]

    return df

st.set_page_config(layout="wide")

st.sidebar.write("Put your order")

st.sidebar.write("Oligonucleotide preparation service")

col1, col2 = st.columns(2)

with col1:
    ord_names = st.text_area("Enter order labels", '')

with col2:
    ord_seqs = st.text_area("Enter order sequences", '')

st.write('Your order:')

st.dataframe(get_order_dataframe(ord_names, ord_seqs))
