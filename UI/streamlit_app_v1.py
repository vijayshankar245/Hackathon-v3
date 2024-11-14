#from openai import OpenAI
import streamlit as st
import shelve
import pandas as pd
import numpy as np
#from openai import AzureOpenAI
import datetime

import os

#df = pd.read_csv(r"C:\Users\USithiah\Documents\Incidents_Test_Database.csv")
df = pd.read_csv(r"C:\Hackathon\Azure Hackathon V2\UI\Incidents_stats.csv")

df = df[~df.isna()].copy()

#df = df.str.replace('$', ''), 

#st.markdown(df.columns)
# # st.write ("data",data)


with st.sidebar:
     #st.title('Summary Of IT Incidents')
    st.markdown(f'<h1 style="color:#1589FF;font-size:24px;">{"Summary Of IT Incidents"}</h1>', unsafe_allow_html=True)

#st.write (df)

#cat_type = 

#df["Category"].unique()
cat_choice = st.sidebar.selectbox('Select Your Category Type:', ['', 'Application Failure',
                                                                    'Cybersecurity/Data Breach',
                                                                    'Infrastructure Management',
                                                                    'Misconfigurations in cloud services',
                                                                    'Network Performance',
                                                                    'Phishing attacks',
                                                                    'Policy violations',
                                                                    'Security Breach',
                                                                    'Server down',
                                                                    'SLA Violations',
                                                                    'Technical Issue']
                                                                    )

sev_type = df["Severity"].loc[df["Category"] == cat_choice].unique()
#sev_type = sev_type.append('All')
sev_choice = st.sidebar.selectbox('Select the Severity:', sev_type)

selected_level = st.sidebar.selectbox ('Common Filters', ['All','Top 5 High Severity Incidents','Top 10 High Severity Incidents','Top 10 High Cost Incidents','Top 5 High Cost Incidents'])

if selected_level == 'Top 5 High Cost Incidents':
    df2 = df.nlargest(5, columns = ["Cost"])

if selected_level == 'Top 10 High Cost Incidents':
    df2 = df.nlargest(10, columns = ["Cost"])    


if selected_level == 'Top 5 High Severity Incidents':
    df2 = df.where(df["Severity"] == "High") 
    df2 = df2.nlargest(5, columns = ["Cost"]) 

if selected_level == 'Top 10 High Severity Incidents':
    df2 = df.where(df["Severity"] == "High") 
    df2 = df2.nlargest(10, columns = ["Cost"])
if cat_choice:
    df2 = df.where(df["Category"] == cat_choice) 
    df2 = df2.sort_values(by="Category") 
else:
    df2 =df    

df2.reset_index(drop = True, inplace = True)
st.write (df2)
#if selected_level == "Top 5"

df = df.loc[df["Severity"] == sev_choice]

chart_data = pd.DataFrame(np.random.randn(20, 2), columns=["Category", "Severity"])
st.area_chart(chart_data)

#      streaming_on = st.toggle('Streaming')

# st.title("Streamlit Chatbot Interface")

#col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 1, 2, 1, 2])

#with col1 : 
# st.subheader ("Top 10 High Priority Incidents")
# st.table (df.sort_values(by = 'Priority', ascending= True).reset_index(drop= True).head(10))




# #with col2 :
# st.subheader ("Top 10 High Cost Incidents")
# st.table (df[df['Cost'] == 'High'].head(10))

# #with col3 :

# st.subheader ("Top 10 High Cost Incidents")
# st.table (df.sort_values(by = 'Cost', ascending= False).reset_index(drop= True).head(10))

# data = ''
# st.audio(data, format="audio/mpeg", loop=True)


# inci_type = df["incident type"].unique()
# incident_choice = st.sidebar.selectbox('Select Your Incident Type:', inci_type)

# label = df["label"].loc[df["incident type"] == incident_choice].unique()
# label_choice = st.sidebar.sidebar.selectbox('Select Your label:', label)
 
#column = st.sidebar.selectbox('Select a category', list(['Category', 'Severity', 'Severity'])) #df.columns

#filtered_df = df.groupby ([field, 'Date']).size().reset_index(name='Count')

# sort_column = st.selectbox('Select column to sort by:', df.columns[1:])
# df_sorted = df.sort_values(by=sort_column, ascending=False)

# cost = st.sidebar.slider(
#     "Select a range of cost",min_value=0, max_value = int(df['Cost'].max()), value =int(df['Cost'].min()))

# severity = st.sidebar.slider(
#     "Select a range of severity ",min_value= int(df['Severity'].min()), max_value = int(df['Severity'].max()), value =int(df['Severity'].min()))

# # priority = st.sidebar.slider(
# #     "Select a range of severity ",min_value= int(df['Priority'].min()), max_value = int(df['Priority'].max()), value = int(df['Priority'].min()))


# #filtered_df = df [(df['Category'] == category) & (df['Priority'].isin(priority)) & (df['severity'].between(severity, severity))]
# filtered_df = df [(df['Severity'].between(severity, severity))] #(df['Category'] == category) & 
# filtered_df = filtered_df.groupby ([category_val, 'Date']).size().reset_index(name='Count')
 

#st.write("You selected wavelengths between", start_color, "and", end_color)

# st.dataframe(df_sorted)

# N = 20
# name_list = df_sorted['name'].head(N).tolist()

# st.write(name_list)

#Line Chart
# st.subheader ('Line Chart')
# st.line_chart (filtered_df.pivot(index='Date', columns=category_val, values ='Count'))



#with col4: 
#Bar Chart

df['month'] = pd.to_datetime(df['Created Date']).dt.strftime('%B')

st.subheader ('By ' + 'Category' + ": ")
df1 = df.groupby (['Category']).size().reset_index(name='Count')
#df1 = df1.head(5)
st.bar_chart (df1.pivot(index='Category', columns='Count', values ='Count'))

#with col5: 
    #Bar Chart
st.subheader ('By ' + 'Priority' + ": ")
df2 = df.groupby (['Priority', 'month']).size().reset_index(name='Count')
st.bar_chart (df2.pivot(index='month', columns='Priority', values ='Count'))

#with col6: 
    #Bar Chart
st.subheader ('By ' + 'Severity' + ": ")
df3 = df.groupby (['Severity', 'month']).size().reset_index(name='Count')
st.bar_chart (df3.pivot(index='month', columns='Severity', values ='Count'))

