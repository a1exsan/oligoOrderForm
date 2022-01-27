import streamlit as st
import order_back as back


st.set_page_config(layout="wide")

st.sidebar.write("Лаборатория олигонуклеотидов компании Биолабмикс")

st.text_input("Ваш e-mail:", '')

col1, col2, col3 = st.columns(3)

with col1:
    ord_names = st.text_area("Наименование олига", '')

with col2:
    ord_seqs = st.text_area("Последовательность олига", '')

with col3:
    ord_amountss = st.text_area("Количество олига", '')

    units = st.radio('единицы количества:', ('AU260', 'nmol', 'umol'))

st.write('Ваш заказ:')

order = back.oligoOrder(ord_names, ord_seqs, ord_amountss, units)
order_data = order.create_order()
if order != None:
    st.table(order_data)
else:
    st.write(order.msg_equal_seq)

st.button('Отправить заказ')
