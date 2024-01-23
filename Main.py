import pandas as pd
from CF_scraping import *
import streamlit as st



def remover(Options):
    df = pd.read_csv(f'{Country}.csv')
    df.drop(columns=Options, inplace=True)
    df.to_csv(f'{Country}.csv',index=False)
    return st.success("Columns Removed")

def Show_Database():
    df =pd.read_csv(f'{Country}.csv')
    st.dataframe(df)


columns = ['Coach_Name', 'Website', 'Email', 'Phone', 'Location', 'Rate',
       'Coaching Themes', 'Coaching Methods', 'Willing to Relocate',
       'Special Rates', 'Fee Range', 'Type of Client',
       'Organizational Client Types', 'Coached Organizations',
       'Industry Sectors Coached', 'Positions Held',
       'Has Prior Experience Delivering Coach Skills Training to Managers/Leaders',
       'Degrees', 'Gender', 'Age', 'Fluent Languages', 'Can Provide', 'Coach',
       'Credentials', 'First_Name', 'Last_Name']

#---------------------------------------------------
st.header("ICF Data Extractor")
st.subheader("Enter the Country Name.🌎")
Country = st.text_input('')
st.subheader("Enter the Country Code.📞")
Country_Code = st.text_input(' ')

if st.button("🔎Find Coaches"):
    try:
        Runner(Country, Country_Code)
    except:
        st.error("Enter a valid details")



if st.button("Show Database"):
    try:
        Show_Database()
    except:
        st.error("Enter a valid Database")


expander = st.expander("Data Scrapping Tools")

Options = expander.multiselect("Columns To be removed❌",columns)
if expander.button("Remove columns"):
    try:
        df =pd.read_csv(f'{Country}.csv')
        remover(Options)
        st.write(f"{Options} Have been removed Successfully")
    except:
        st.error("Error in Removing Columns")


old_word =expander.text_input('Word to be replaced')
new_word =expander.text_input('Replacing Word')
column_s = expander.selectbox("Pick one", columns)
if expander.button('Replace Words'):
    try:
        df = pd.read_csv(f'{Country}.csv')
        df[column_s] = df[column_s].str.replace(rf'({old_word})\s*', f'{new_word}', regex=True)
        df.to_csv(f'{Country}.csv', index=False)
    except:
        st.error("UNDER CONSTRUCTION")

