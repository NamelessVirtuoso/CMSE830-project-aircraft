import streamlit as st
import seaborn as sns
import pandas as pd
import plotly as pl
import plotly.express as px
iris_data = sns.load_dataset("iris")
species = iris_data.species
print(species)
df_form = iris_data
st.write("""
# Iris Dataset
How are sepal length, sepal width and pedal width correlated to species in Iris dataset?
""")
df = px.data.iris()
fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width', color='species')
fig.show()