import streamlit as st
import pandas as pd
import preprocessor
import helper

# Load data
#@st.cache
def load_data():
    df = pd.read_excel('athlete_events.xlsx')
    region_df = pd.read_csv('noc_regions.csv')
    return df, region_df

df, region_df = load_data()

# Streamlit UI
st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select years", years)
    selected_country = st.sidebar.selectbox("Select country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'overall' and selected_country == 'overall':
        st.title("Overall Tally")
    if selected_year != 'overall' and selected_country == 'overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'overall' and selected_country != 'overall':
        st.title(selected_country + " Overall Performance")
    if selected_year != 'overall' and selected_country != 'overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)

elif user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Stats")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Year", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Year", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Year", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    x_pivot = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
    ax = sns.heatmap(x_pivot, annot=True)
    st.pyplot(fig)

      
