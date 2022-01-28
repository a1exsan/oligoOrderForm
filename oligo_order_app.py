
import streamlit as st
import order_back as back
import telegram_bot as tbot


st.set_page_config(layout="wide")

st.sidebar.write("Лаборатория олигонуклеотидов компании Биолабмикс")

email = st.text_input("Ваш e-mail:", '')

col1, col2, col3 = st.columns(3)

with col1:
    ord_names = st.text_area("Наименование олига", '')

with col2:
    ord_seqs = st.text_area("Последовательность олига", '')

with col3:
    ord_amountss = st.text_area("Количество олига", '')

    units = st.radio('единицы количества:', ('AU260', 'nmol', 'umol'))

st.write('Ваш заказ:')

order = back.oligoOrder(ord_names, ord_seqs, ord_amountss, units, email)
order_data = order.create_order()
if order != None:
    st.table(order_data)
else:
    st.write(order.msg_equal_seq)

chatID = st.secrets['chat_id']
token_ = st.secrets['chat_token']

if st.button('Отправить заказ'):
    df = order.create_send_df()
    if not df.empty:
        hash = order.create_data_hash()
        if not back.compare_files_hash(hash, path='data'):
            Fname = f'data/{hash}_{order.date.date()}_{order.user}.csv'
            order.data.to_csv(Fname)
            tbot.send_document(Fname, message=f'from: {order.user}', token=token_, chat_id=chatID)
            st.write("Заказ успешно создан!")
        else:
            st.write("Данный заказ уже был создан!")




