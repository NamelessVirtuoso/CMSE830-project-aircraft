import streamlit as st
import seaborn as sns
import pandas as pd
import plotly as pl
import plotly.express as px
data = pd.read_csv("data.csv")
result = data.diagnosis
st.write("""
# WI cancer dataset
What is the most important factor when deciding if I patient has breast cancer?
""")

option = st.selectbox(
    'What would you like to include in the plot?',
    ('radius_worst', 'perimeter_worst', 'area_worst'))

st.write('You selected:', option)

option2 = st.selectbox(
    'What would you like to compare to the previous one?',
    ('area_worst', 'perimeter_worst', 'radius_worst'))

st.write('You selected:', option2)

you_chart = sns.lineplot(x = data[option], y  = data[option2])

st.pyplot(you_chart.figure)

#sns_chart = sns.pairplot(data,
#                         x_vars=["radius_mean", "texture_mean", "perimeter_mean","area_mean"],
 #                       y_vars=["radius_mean", "texture_mean", "perimeter_mean","area_mean"],
 #                       hue = "diagnosis",diag_kind="hist")

#sns_chart.fig.suptitle("Pairplot of some important factor", y = 1.08)
#st.pyplot(sns_chart)
