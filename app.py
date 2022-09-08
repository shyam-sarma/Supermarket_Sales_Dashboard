from re import sub
from turtle import title
import pandas as pd
import streamlit as st
import plotly.express as px

#emojis : https://www.webfx.com/tools/emoji-cheat-sheet/
#stream docs reference : https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config
st.set_page_config(page_title = "Supermarket Sales Dashboard",
                    page_icon= ':chart_with_upwards_trend:',
                    layout = 'wide')

#pandas ref : https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io = '/Users/shyam/Desktop/Streamlit Apps/Sales_Dashboard/data/supermarkt_sales.xlsx',
        skiprows = 3,
        usecols = 'B:R')
    #Add hour column to dataframe
    df["hour"] = pd.to_datetime(df["Time"],format = "%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

#st.dataframe(df)


#---SIDEBAR-----
st.sidebar.header("Please Filter Here: ")
city = st.sidebar.multiselect(
    label = "Select The City",
    options= df['City'].unique(),
    default= df['City'].unique()
)


customer_type = st.sidebar.multiselect(
    label = "Select The Customer Type",
    options= df['Customer_type'].unique(),
    default= df['Customer_type'].unique()
)

gender = st.sidebar.multiselect(
    label = "Select The Gender",
    options= df['Gender'].unique(),
    default= df['Gender'].unique()
)

# df.query ref :   https://sparkbyexamples.com/pandas/pandas-dataframe-query-examples/
df1 = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

#st.write(df1)


#----MainPage------
title_left,title_mid,title_right = st.columns(3)
with title_mid: 
    st.title(":bar_chart: Sales Dashboard")
    st.markdown('##')

#TOP KPI's
total_sales= int(df1["Total"].sum())
average_rating = round(df1["Rating"].mean(),1)
star_rating = ":star:" * int(round(average_rating,0))
average_sale = round(df1['Total'].mean(),2)

left_col,mid_col,right_col = st.columns(3)

with left_col:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")

with mid_col:
    st.subheader("Average Rating:")
    st.subheader(f"{star_rating} : {average_rating}")

with right_col:
    st.subheader("Average Sale Per Transaction: ")
    st.subheader(f"US $ {average_sale}")


st.markdown("---")

Sales_by_product_line = df1.groupby(by = ['Product line']).sum()[["Total"]].sort_values(by="Total")


fig_product_sales = px.bar(
    Sales_by_product_line,
    x= "Total",
    y=Sales_by_product_line.index,
    orientation='h',
    title="<b>Sales By Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(Sales_by_product_line),
    template= 'plotly_white'
    )

fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis =(dict(showgrid = False))
)





#Sales by Hour Bar Chart

sales_by_hour = df1.groupby(by = ["hour"]).sum()[["Total"]]

fig_sales_by_hour = px.bar(
    sales_by_hour,
    x = sales_by_hour.index,
    y= "Total",
    orientation='v',
    title="<b>Sales By Hour </b>",
    color_discrete_sequence=["#0083B8"] * len(Sales_by_product_line),
    template= 'plotly_white'
)

fig_sales_by_hour.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis =(dict(showgrid = False))
)

st.plotly_chart(fig_product_sales,use_container_width=True)
st.plotly_chart(fig_sales_by_hour,use_container_width=True)


#chart_leftcol, chart_rightcol = st.columns(2)
#chart_leftcol.plotly_chart(fig_product_sales,use_container_width=True)
#chart_rightcol.plotly_chart(fig_sales_by_hour,use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)