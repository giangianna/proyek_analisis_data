import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns

st.title('Proyek Analisis Data')
st.header('Dashboard by Gian Gianna Pallan Pallas')
st.subheader('E-Commerce Public Dataset :sparkles:')

st.write("""
Kumpulan data ini berisi informasi tentang 100 ribu pesanan dari tahun 2016 hingga 2018 yang dibuat di beberapa pasar di Brasil.
""")

# dataset customers
df = pd.read_csv('./main_dataset.csv')
st.dataframe(data=df)

tab1, tab2, tab3, tab4 = st.tabs(["Pelanggan Aktif", "Pelanggan Baru", "Repeat Order", "Rata-rata transaksi "])

with tab1:
    st.text('Jumlah pelanggan aktif dari tahun 2016 s/d 2018')
    df_active = df.groupby(by='year')['customer_unique_id'].count().reset_index()
    st.dataframe(data=df_active)

    st.text('Fungsi untuk menghitung Growth Year over Year (%YoY)')
    code = """def hitung_yoy(df, column_name):
    start = 0
    list_yoy = []
    for year in df['year']:
        now = df[df['year']==year][column_name].values[0]
        if start == 0:
            yoy = ((now-0)/now)*100
            list_yoy.append(yoy)
        else:
            tahun_lalu = df[df['year']==(year-1)][column_name].values[0]
            yoy = ((now-tahun_lalu)/tahun_lalu)*100
            list_yoy.append(yoy)
        start += 1
    return list_yoy"""
    st.code(code, language='python')


    def hitung_yoy(df, column_name):
        start = 0
        list_yoy = []
        for year in df['year']:
            now = df[df['year'] == year][column_name].values[0]
            if start == 0:
                yoy = ((now - 0) / now) * 100
                list_yoy.append(yoy)
            else:
                tahun_lalu = df[df['year'] == (year - 1)][column_name].values[0]
                yoy = ((now - tahun_lalu) / tahun_lalu) * 100
                list_yoy.append(yoy)
            start += 1
        return list_yoy


    df_active['customer_active_yoy'] = hitung_yoy(df_active, 'customer_unique_id')
    df_active['customer_active_yoy'] = df_active['customer_active_yoy'].astype(int)
    st.text('Setelah di tambahkan Growth Year over Year (%YoY)')
    st.dataframe(data=df_active)

    st.subheader('Jumlah pelanggan aktif dari tahun 2016 s/d 2018')

    # colors
    colors = ['#FF0000', '#0000FF', '#FFFF00']
    # explosion
    explode = (0.05, 0.05, 0.05)
    plt.pie(df_active['customer_unique_id'], labels=df_active['year'],
            colors=colors, autopct='%1.1f%%',
            pctdistance=0.85, explode=explode)
    # draw circle
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()

    # Adding Circle in Pie chart
    fig.gca().add_artist(centre_circle)

    st.pyplot(plt)

    col1, col2, col3 = st.columns(3)

    with col1:
        value = df_active[df_active['year'] == 2016]['customer_unique_id'].values[0]
        value_yoy = df_active[df_active['year'] == 2016]['customer_active_yoy'].values[0]

        st.metric(label='2016', value=str(value), delta=str(value_yoy) + '%')

    with col2:
        value = df_active[df_active['year'] == 2017]['customer_unique_id'].values[0]
        value_yoy = df_active[df_active['year'] == 2017]['customer_active_yoy'].values[0]

        st.metric(label='2017', value=str(value), delta=str(value_yoy) + '%')

    with col3:
        value = df_active[df_active['year'] == 2018]['customer_unique_id'].values[0]
        value_yoy = df_active[df_active['year'] == 2018]['customer_active_yoy'].values[0]

        st.metric(label='2018', value=str(value), delta=str(value_yoy) + '%')

    st.write("""
    ### Berapa jumlah pelanggan aktif yang ada setiap tahun?
        - Jumlah pelanggan aktif tahun 2016 sebesar 329 pelanggan
        - pada tahun 2017 sebesar 45,101 terjadi peningkatan yang sangat signifikan 
          yaitu 13,608% dari tahun lalu
        - sedangkan pada tahun 2018 jumlah pelanggan aktif sebesar 54,011 
          dengan peningkatan sebesar 19.7% dari tahun lalu
    """)

with tab2:
    st.text("Pelanggan baru yang bergabung dari tahun 2016 s/d 2018")

    df_customer_by_year = df.groupby(by='year')['customer_unique_id'].nunique().reset_index()
    st.dataframe(data=df_customer_by_year)

    st.text('Fungsi untuk menghitung pelanggan baru setiap tahun')
    code = """def new_customer_by_year(df, column_name):
    start = 0
    list_new_customers = []
    for year in df['year']:
        if start == 0:
            new = df[df['year'] == year][column_name].values[0]
            list_new_customers.append(new)
        else:
            new = df[df['year'] == year][column_name].values[0] - df[df['year'] == (year - 1)][column_name].values[
                0]
            list_new_customers.append(new)
        start += 1

    return list_new_customers"""
    st.code(code, language='python')


    # fungsi untuk menghitung pelanggan baru setiap tahun
    def new_customer_by_year(df, column_name):
        start = 0
        list_new_customers = []
        for year in df['year']:
            if start == 0:
                new = df[df['year'] == year][column_name].values[0]
                list_new_customers.append(new)
            else:
                new = df[df['year'] == year][column_name].values[0] - df[df['year'] == (year - 1)][column_name].values[
                    0]
                list_new_customers.append(new)
            start += 1

        return list_new_customers

    st.text("Setelah di tambahkan jumlah new customer dan perhitungan %YoY")
    df_customer_by_year['new_customer_by_year'] = new_customer_by_year(df_customer_by_year, 'customer_unique_id')
    df_customer_by_year['new_customer_%yoy'] = hitung_yoy(df_customer_by_year, 'customer_unique_id')
    st.dataframe(data=df_customer_by_year)

    st.subheader('Jumlah pelanggan baru dari tahun 2016 s/d 2018')

    # colors
    colors = ['#FF0000', '#0000FF', '#FFFF00']
    # explosion
    explode = (0.05, 0.05, 0.05)
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.pie(df_customer_by_year['new_customer_by_year'], labels=df_customer_by_year['year'],
            colors=colors, autopct='%1.1f%%',
            pctdistance=0.85, explode=explode)
    # draw circle
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()

    # Adding Circle in Pie chart
    fig.gca().add_artist(centre_circle)

    st.pyplot(fig)

    col1, col2, col3 = st.columns(3)

    with col1:
        value = df_customer_by_year[df_customer_by_year['year'] == 2016]['new_customer_by_year'].values[0]
        value_yoy = df_customer_by_year[df_customer_by_year['year'] == 2016]['new_customer_%yoy'].values[0]

        st.metric(label='2016', value=str(value), delta=str(value_yoy) + '%')

    with col2:
        value = df_customer_by_year[df_customer_by_year['year'] == 2017]['new_customer_by_year'].values[0]
        value_yoy = df_customer_by_year[df_customer_by_year['year'] == 2017]['new_customer_%yoy'].values[0]

        st.metric(label='2017', value=str(value), delta=str(value_yoy) + '%')

    with col3:
        value = df_customer_by_year[df_customer_by_year['year'] == 2018]['new_customer_by_year'].values[0]
        value_yoy = df_customer_by_year[df_customer_by_year['year'] == 2018]['new_customer_%yoy'].values[0]

        st.metric(label='2018', value=str(value), delta=str(value_yoy) + '%')

    st.write("""
        ### Berapa banyak pelanggan baru yang bergabung setiap tahun?
            - Jumlah pelanggan baru tahun 2016 sebesar 326 pelanggan
            - pada tahun 2017 sebesar 43,387 terjadi peningkatan yang sangat signifikan 
              yaitu 13,308% dari tahun lalu
            - sedangkan pada tahun 2018 jumlah pelanggan baru sebesar 9,036 terjadi 
              peningkatan sebesar 20% dari tahun lalu
        """)

with tab3:
    st.text('Pelanggan yang melakukan repeat order (pemesanan ulang) dari tahun 2016 s/d 2018')

    df_order_customer = df.groupby(by=['year', 'customer_unique_id']).size().reset_index(name='counts')
    # pelanggan yang telah membeli lebih dari 1 kali
    df_repeat_order = df_order_customer.loc[df_order_customer['counts'] > 1]
    sum_repaeat_year = df_repeat_order.groupby(by='year')['customer_unique_id'].nunique().reset_index(
        name='customer_repeat_order')

    sum_repaeat_year['%yoy'] = hitung_yoy(sum_repaeat_year, 'customer_repeat_order')
    st.dataframe(data=sum_repaeat_year)

    st.bar_chart(sum_repaeat_year, x="year", y="customer_repeat_order")

    col1, col2, col3 = st.columns(3)

    with col1:
        value = sum_repaeat_year[sum_repaeat_year['year'] == 2016]['customer_repeat_order'].values[0]
        value_yoy = sum_repaeat_year[sum_repaeat_year['year'] == 2016]['%yoy'].values[0]

        st.metric(label='2016', value=str(value), delta=str(value_yoy) + '%')

    with col2:
        value = sum_repaeat_year[sum_repaeat_year['year'] == 2017]['customer_repeat_order'].values[0]
        value_yoy = sum_repaeat_year[sum_repaeat_year['year'] == 2017]['%yoy'].values[0]

        st.metric(label='2017', value=str(value), delta=str(value_yoy) + '%')

    with col3:
        value = sum_repaeat_year[sum_repaeat_year['year'] == 2018]['customer_repeat_order'].values[0]
        value_yoy = sum_repaeat_year[sum_repaeat_year['year'] == 2018]['%yoy'].values[0]

        st.metric(label='2018', value=str(value), delta=str(value_yoy) + '%')

    st.write("""
        ### Berapa banyak pelanggan yang melakukan repeat order (pemesanan ulang) setiap tahun?
            - Jumlah pelanggan yang melakukan repeat order pada tahun 2017 adalah 3 pelanggan
            - Jumlah pelanggan yang melakukan repeat order pada tahun 2017 sebesar 1,256 pelanggan
              terjadi kenaikan yang signifikan 41,766% dari tahun lalu
            - Sedangkan pada tahun 2018 sebesar 1,167 pelanggan terjadi 
              penurunan -7% dari tahun lalu
    """)

with tab4:
    st.text("Rata-rata transaksi")

    df_order_by_year = df.groupby(by='year')['order_id'].count().reset_index(name='jml_order')
    df_customer_by_year = df.groupby(by='year')['customer_unique_id'].nunique().reset_index(name='jml_customer')
    df_avg_order_by_customer = df_order_by_year.merge(df_customer_by_year, on='year', how='left')
    df_avg_order_by_customer['avg_order'] = df_avg_order_by_customer['jml_order'] / df_avg_order_by_customer[
        'jml_customer']
    st.dataframe(data=df_avg_order_by_customer)

    st.bar_chart(df_avg_order_by_customer, x="year", y="avg_order")

    st.write("""### Berapa rata-rata transaksi yang dilakukan oleh pelanggan setiap tahun?
        - rata rata transaksi pelanggan dari tahun ke tahun 2016 s/d 2018 1 transaksi
    """)


st.caption('Gian Gianna - Copyright (c) 2024')