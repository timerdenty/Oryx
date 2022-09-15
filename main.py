import pandas as pd
import streamlit as st
# from st_aggrid import AgGrid
import plotly.express as px


st.header('Потери техники в Украино-российской войне')
st.subheader('Данные собраны исследовательской группой Oryx на основании анализа фотографий с полей боя')
st.caption("Сбор данных осуществлялся с 24.02.2022 по 04.09.2022")

losses_russia_row = pd.read_csv('losses_russia.csv')
losses_ukraine_row = pd.read_csv('losses_ukraine.csv')

# Подготовка данных
losses_russia = losses_russia_row.fillna(0)
losses_ukraine = losses_ukraine_row.fillna(0)
losses_russia['manufacturer'] = losses_russia['manufacturer'].str.replace('the ', '')
losses_ukraine['manufacturer'] = losses_ukraine['manufacturer'].str.replace('the ', '')
losses_ukraine['manufacturer'] = losses_ukraine['manufacturer'].str.replace('%281794%E2%80%931815%2C 1830%E2%80%931974%2C 2020%E2%80%93present%29', '')
losses_ukraine['manufacturer'] = losses_ukraine['manufacturer'].str.replace('%28converted%29', '')

tab1, tab2, tab3, tab4 = st.tabs(["📈 Общие данные", "Cтрана-производитель", "Категории техники", "Исходные данные"])

with tab1:

    st.subheader('Потери Украины')
    col1, col2, col3 = st.columns(3)
    col1.metric('Всего потеряно техники', sum(losses_ukraine['losses_total']), delta=None, delta_color="normal", help=None)
    st.text('в том числе:')
    col1, col2, col3 = st.columns(3)
    col1.metric('Уничтожено', sum(losses_ukraine['destroyed'].astype(int)),
                delta='(' + str(round(sum(losses_ukraine['destroyed'].astype(int)) / sum(losses_ukraine['losses_total']) * 100, 2)) + '%)',
                delta_color="off",
                help=None)
    col2.metric('Захвачено противником', sum(losses_ukraine['captured'].astype(int)),
                delta='(' + str(round(sum(losses_ukraine['captured'].astype(int)) / sum(losses_ukraine['losses_total']) * 100, 2)) + '%)',
                delta_color="off", help=None)
    col3.metric('Брошено', sum(losses_ukraine['abandoned'].astype(int)),
                delta='(' + str(round(sum(losses_ukraine['abandoned'].astype(int)) / sum(losses_ukraine['losses_total']) * 100, 2)) + '%)',
                delta_color="off", help=None)
    col1.metric('Захвачено и уничтожено', sum(losses_ukraine['captured and destroyed'].astype(int)),
                delta='(' + str(round(sum(losses_ukraine['captured and destroyed'].astype(int)) / sum(losses_ukraine['losses_total']) * 100, 2)) + '%)',
                delta_color="off", help=None)
    col2.metric('Повреждено', sum(losses_ukraine['damaged'].astype(int)),
                delta='(' + str(round(sum(losses_ukraine['damaged'].astype(int)) / sum(losses_ukraine['losses_total']) * 100, 2)) + '%)',
                delta_color="off", help=None)
    drone = (sum(losses_ukraine['sunk'].astype(int))) + (sum(losses_ukraine['sunk but raised by Russia'].astype(int)))

    losses_ukraine_from_drons = sum(losses_ukraine['damaged by Forpost-R']
                                    + losses_ukraine['damaged by Orion and captured']
                                    + losses_ukraine['destroyed by Forpost-R']
                                    + losses_ukraine['destroyed by Orion']
                                    + losses_ukraine['destroyed by loitering munition'])

    col3.metric('Потери после атаки дронов', int(losses_ukraine_from_drons),
                delta='(' + str(round(losses_ukraine_from_drons / sum(losses_ukraine['losses_total']) * 100, 2)) + '%)',
                delta_color="off", help=None)
    st.info('в скобках указан % от общего числа потерь')

    st.subheader('Потери россии')
    col1, col2, col3 = st.columns(3)
    col1.metric('Всего потеряно техники', sum(losses_russia['losses_total']), delta=None, delta_color="normal", help=None)
    st.text('в том числе:')
    col1, col2, col3 = st.columns(3)
    col1.metric('Уничтожено', sum(losses_russia['destroyed'].astype(int)),
                delta='(' + str(round(sum(losses_russia['destroyed'].astype(int)) / sum(losses_russia['losses_total']) * 100, 2)) + '%)',
                delta_color="off", help=None)
    col2.metric('Захвачено противником', sum(losses_russia['captured'].astype(int)),
                delta='(' + str(round(sum(losses_russia['captured'].astype(int)) / sum(losses_russia['losses_total']) * 100, 2)) + '%)',
                delta_color="off", help=None)
    col3.metric('Брошено', sum(losses_russia['abandoned'].astype(int)),
                delta='(' + str(round(sum(losses_russia['abandoned'].astype(int)) / sum(losses_russia['losses_total']) * 100, 2)) + '%)',
                delta_color="off", help=None)
    col1.metric('Захвачено и уничтожено', sum(losses_russia['captured and destroyed'].astype(int)),
                delta='(' + str(round(sum(losses_russia['captured and destroyed'].astype(int)) / sum(losses_russia['losses_total']) * 100, 2)) + '%)',
                delta_color="off", help=None)
    col2.metric('Повреждено', sum(losses_russia['damaged'].astype(int)),
                delta='(' + str(round(sum(losses_russia['damaged'].astype(int)) / sum(losses_russia['losses_total']) * 100, 2)) + '%)',
                delta_color="off", help=None)

    losses_russia_from_drons = sum(losses_russia['damaged by Bayraktar TB2']
                                   + losses_russia['destroyed by Bayraktar TB2']
                                   + losses_russia['destroyed by Bayraktar TB2 and Harpoon AShM'])

    col3.metric('Потери после атаки дронов', int(losses_russia_from_drons),
                delta='(' + str(round(int(losses_russia_from_drons) / sum(losses_russia['losses_total']) * 100, 2)) + '%)',
                delta_color="off", help=None)

    st.info('в скобках указан % от общего числа потерь')


with tab2:
    st.subheader('Страны-производители потерянной техники')

    losses_russia_final = losses_russia.groupby(['manufacturer'])['losses_total'].sum()
    losses_ukraine_final = losses_ukraine.groupby(['manufacturer'])['losses_total'].sum()

    losses_russia.loc[losses_russia['losses_total'] <= 1, 'manufacturer'] = 'Other countries' # Represent only large countries
    fig = px.pie(losses_russia, values='losses_total', names='manufacturer', title='Производитель техники, потерянной  россией',
                 color_discrete_map={'Soviet Union': 'red',
                                     'Russia': 'blue'}
                 )
    st.write(fig)
    losses_ukraine.loc[losses_ukraine['losses_total'] <= 1, 'manufacturer'] = 'Other countries' # Represent only large countries
    fig2 = px.pie(losses_ukraine, values='losses_total', names='manufacturer', title='Производитель техники, потерянной Украиной',
                  color='losses_total',
                  color_discrete_map={'Soviet Union': 'red',
                                      'Ukraine': 'blue',}
                  )
    st.write(fig2)

    col1, col2 = st.columns(2)

    col1.subheader('Полные данные по стране-производителю потерянной техники (россия)')
    col1.table(losses_russia_final.sort_values(ascending=False))

    col2.subheader('Полные данные по стране-производителю потерянной техники (Украина)')
    col2.table(losses_ukraine_final.sort_values(ascending=False))


with tab3:
    losses_russia_by_category = losses_russia[['equipment', 'losses_total']]
    losses_russia_by_category = losses_russia_by_category.groupby('equipment')['losses_total'].sum()
    losses_russia_by_category = pd.DataFrame(losses_russia_by_category)
    losses_russia_by_category = losses_russia_by_category.reset_index(['equipment'])

    losses_ukraine_by_category = losses_ukraine[['equipment', 'losses_total']]
    losses_ukraine_by_category = losses_ukraine_by_category.groupby(['equipment'])['losses_total'].sum()
    losses_ukraine_by_category = pd.DataFrame(losses_ukraine_by_category)
    losses_ukraine_by_category = losses_ukraine_by_category.reset_index(['equipment'])

    col1, col2 = st.columns(2)
    col1.subheader('Потери россии по видам вооружений')
    col1.table(losses_russia_by_category)
    col2.subheader('Потери Украины по видам вооружений')
    col2.table(losses_ukraine_by_category)


with tab4:
    st.subheader('Потери россии ')
    st.table(losses_russia_row)
    st.subheader('Потери Украины')
    st.table(losses_ukraine_row)