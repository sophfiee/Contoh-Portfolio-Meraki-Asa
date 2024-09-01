# -------------------------------------- Import Library ------------------------------
#Run using: streamlit run streamlit.py
import json
## Read Data and Preprocessing Data
import pandas as pd

## Visualization
import plotly.express as px 

## Dashboard 
import streamlit as st 

# ------------------------------ CONFIG ------------------------------
st.set_page_config(
    page_title="Dashboard Analisis Penjualan Supermarket",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------------------------- Read dataset ------------------------------
df = pd.read_pickle("data_sales_dash.pkl")

# -------------------------------------- Membuat Sidebar ---------------------------

with st.sidebar:
    #Menambahkan logo pribadi
    st.write("Hello 👋")
    st.image("asset/data-science.png")
    st.write("""
            Saya Sophia mempersembahkan Dashboard Analisis Penjualan Supermarket,
             sebuah alat yang memudahkan menganalisis data perusahaan dengan visualisasi
             yang mendalam dan interaktif. 
            """)
    st.caption('Copyright © Toni Andreas Susanto 2024')

# -------------------------------------- ROW 1 ---------------------------
st.write("# Dahboard Analisis Penjualan Supermarket")
st.write("""
         Analisis ini menggunakan bahasa pemrograman Python dan visualisasi 
         interaktif (Plotly Express). Data yang digunakan adalah data penjualan 
         supermarket yang diperoleh dari https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales.
         """)
with st.expander("Klik untuk melihat detail dataset!"):
    st.write("Data Penjualan Supermarket",df)

# -------------------------------------- ROW 2 ---------------------------
st.write("### 1. Bagaimana Performa (Total, Quantity, Gross Income) Perusahaan dalam rentang waktu tertentu?")

# ---------- A. Filter Indicator
choices = st.radio("Pick One Indicator!",
         ("Total", "Quantity", "Gross Income"))

# ---------- B. Filter Date - Input Rentang Tanggal
min_date = df['Date'].min()
max_date = df['Date'].max()

# Input Data
start_date, end_date = st.date_input("Pick a Date Range!",
              value=[min_date,max_date],
              min_value=min_date,
              max_value=max_date)

# Ubah tipe data input date
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data
cond_min_max = (df['Date'] >= start_date) & (df['Date'] <= end_date)
filtered_df = df[cond_min_max]

# ---------- C. Persiapan Data
trend=filtered_df.groupby("Date")[choices].sum().reset_index()

# ---------- D. Visualisasi Data
fig_line=px.line(trend,
        x="Date",
        y=choices,
        title=f"The {choices} Value Over Time",
        markers=True,
        color_discrete_sequence=["skyblue"])

st.plotly_chart(fig_line)

# -------------------------------------- ROW 3 ---------------------------
st.write("### 2. Bagaimana Performa (Total, Quantity, Gross Income) pada Setiap Product Line?")

# A. Input Data
choices1 = st.radio("Pick One Indicator (Bar Chart)!",
         ("Total", "Quantity", "Gross Income"))

# B. Persiapan Data
big_pl = df.groupby("Product line")[choices1].sum().reset_index()

# C. Visualisasi
fig_bar = px.bar(big_pl.sort_values(by=choices1, ascending=True),
       x=choices1,
       y="Product line",
       title="Total Sales in Each Product Line",
       color_discrete_sequence=['skyblue'])

st.plotly_chart(fig_bar)

# -------------------------------------- ROW 4 ---------------------------
st.write("### 3. Bagaimana Persebaran Total Penjualan dalam Hari maupun Jam Tertentu?")

# A. Input Data
persebaran_day_hour = df.groupby(["Day of Week","Hour"])['Total'].sum().reset_index()

# B. Visualisasi

fig_heatmap = px.density_heatmap(persebaran_day_hour,
                   x="Day of Week",
                   y = "Hour",
                   z="Total",
                   title="Distribution of Total Transaction Value in Every Hour and Day",
                   color_continuous_scale="rdbu",
                   nbinsy=len(persebaran_day_hour['Hour'].unique()))

st.plotly_chart(fig_heatmap)

# -------------------------------------- ROW 5 ---------------------------

st.write("### 4. Bagaimana Perbandingan Gender Pembeli di Setiap Product Line?")

# A. Persiapan Data
gen_cus = pd.crosstab(
    index=df["Product line"],
    columns=df['Gender']
).reset_index()

pro_cus_melt=pd.melt(gen_cus,
        id_vars="Product line",
        var_name="Gender",
        value_name="Value")


# B. Visualisasi
fig_stack=px.bar(pro_cus_melt,
       x="Product line",
       y="Value",
       color="Gender",
       title="Comparison of Male and Female Buyers in Each Product Line")

st.plotly_chart(fig_stack)

