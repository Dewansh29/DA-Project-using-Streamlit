import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('startup_cleaned.csv')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    return df

df = load_data()

# Function to load overall analysis
def load_overall_analysis():
    st.title('Overall Analysis')
    
    # Total investment amount
    total = round(df['amount'].sum())
    
    # Max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).iloc[0]
    
    # Average ticket size
    avg_funding = round(df.groupby('startup')['amount'].sum().mean())
    
    # Total funded startups
    total_startup = df['startup'].nunique()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric('Total Investment', f"{total} Cr")
    
    with col2:
        st.metric('Max Funding', f"{max_funding} Cr")
    
    with col3:
        st.metric('Average Funding', f"{avg_funding} Cr")
    
    with col4:
        st.metric('Total Startups', str(total_startup))

    # Monthly over Month Graph
    st.header('MoM Graph')

    # Dropdown for selecting the type of graph
    selected_option = st.selectbox('Select Type', ['Total', 'Count'], key='selected_option')

    if selected_option == 'Total':
        # Show total investment per month
        df_monthly = df.groupby('month')['amount'].sum().reset_index()
        fig3, ax3 = plt.subplots()
        ax3.plot(df_monthly['month'], df_monthly['amount'], marker='o')
        ax3.set_xlabel('Month')
        ax3.set_ylabel('Total Investment')
        ax3.set_title('Total Investment Per Month')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig3)
    else:
        # Show month-over-month counts
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)
        
        fig3, ax3 = plt.subplots()
        ax3.plot(temp_df['x_axis'], temp_df['amount'], marker='o')
        ax3.set_xlabel('Month-Year')
        ax3.set_ylabel('Total Investment')
        ax3.set_title('Investment by Month-Year')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig3)

# Function to load investor details
def load_investor_details(investor):
    st.title(investor)
    
    # Filter data for the selected investor
    investor_df = df[df['investors'].str.contains(investor)]
    
    last_df = investor_df[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last_df)
    
    # Biggest investments
    big_df = investor_df.groupby('startup')['amount'].sum().sort_values(ascending=False)
    st.subheader('Biggest Investments')
    
    # Display the data
    st.dataframe(big_df)
    
    # Display the bar graph and pie chart below the table
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots()
        ax.bar(big_df.index, big_df.values)
        ax.set_ylabel('Investment Amount')
        ax.set_xlabel('Startup')
        ax.set_title('Biggest Investments by Amount')
        plt.xticks(rotation=0, ha='right')
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots()
        ax.pie(big_df, labels=big_df.index, autopct='%1.1f%%')
        ax.set_title('Investment Distribution')
        st.pyplot(fig)

    # Add year column
    investor_df['year'] = investor_df['date'].dt.year

    # Group by year to get YOY investment
    year_series = investor_df.groupby('year')['amount'].sum()
    
    st.subheader('YOY Investment')
    fig2, ax1 = plt.subplots()
    ax1.plot(year_series.index, year_series.values, marker='o')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Investment Amount')
    ax1.set_title('Year-Over-Year Investment')
    st.pyplot(fig2)

# Sidebar setup
st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investors'])

if option == 'Overall Analysis':
    if 'show_overall_analysis' not in st.session_state:
        st.session_state.show_overall_analysis = False

    btn0 = st.sidebar.button('Show Overall Analysis')
    if btn0:
        st.session_state.show_overall_analysis = True

    if st.session_state.show_overall_analysis:
        load_overall_analysis()

elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    if 'show_startup_details' not in st.session_state:
        st.session_state.show_startup_details = False

    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
    if btn1:
        st.session_state.show_startup_details = True
    
    if st.session_state.show_startup_details:
        st.write(f"Details for startup: {selected_startup}")
        # Add your startup analysis code here

elif option == 'Investors':
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    if 'show_investor_details' not in st.session_state:
        st.session_state.show_investor_details = False

    btn2 = st.sidebar.button('Find Investor Details')
    st.title('Investor Analysis')
    if btn2:
        st.session_state.show_investor_details = True
    
    if st.session_state.show_investor_details:
        load_investor_details(selected_investor)
