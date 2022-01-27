import streamlit as st
import pandas as pd
import oligomass as omass


def get_order_dataframe(names, seqs, amounts):
    names = names.split('\n')
    seqs = seqs.split('\n')
    amounts = amounts.split('\n')
    if len(amounts) != len(seqs):
        amounts = [amounts[0] for s in seqs]

    df = pd.DataFrame({'Name': names})
    df['Sequence'] = seqs
    df['Amounts'] = amounts

    df['Mass, Da'] = [round(omass.oligoSeq(s).getMolMass(), 2) for s in seqs]

    df['Extinction'] = [omass.get_simple_ssdna_extinction(s, omass.get_extinction_dict()) for s in seqs]

    return df

st.set_page_config(layout="wide")

st.sidebar.write("Put your order")

st.sidebar.write("Oligonucleotide preparation service")

col1, col2, col3 = st.columns(3)

with col1:
    ord_names = st.text_area("Enter order labels", '')

with col2:
    ord_seqs = st.text_area("Enter order sequences", '')

with col3:
    ord_amountss = st.text_area("Enter order amounts", '')

st.write('Your order:')

st.table(get_order_dataframe(ord_names, ord_seqs, ord_amountss))
