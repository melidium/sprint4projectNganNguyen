# import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# import dataframe
file_path = 'vehicle_us.csv'
df_vehicle_us = pd.read_csv(file_path)

#filling in NaN Values:
df_vehicle_us['is_4wd'] = df_vehicle_us['is_4wd'].fillna(0)

cylinder_median = df_vehicle_us['cylinders'].median()
df_vehicle_us['cylinders'] = df_vehicle_us['cylinders'].fillna(cylinder_median)

model_year_median = df_vehicle_us['model_year'].median()
df_vehicle_us['model_year'] = df_vehicle_us['model_year'].fillna(model_year_median)
df_vehicle_us['model_year'] = df_vehicle_us['model_year'].astype(int)

odometer_nan = df_vehicle_us.groupby(['model_year', 'model'])['odometer'].transform('median')
df_vehicle_us['odometer'] = df_vehicle_us.groupby(['model_year', 'model'])['odometer'].fillna(odometer_nan)

# Scatter Plot for model type and transmission comparison with price:
fig_model_transmission = px.scatter( df_vehicle_us, x='odometer', y='price', color='transmission' )

# Histogram for Car's Paint Color Price:
fig_color_type = px.histogram( df_vehicle_us, title='Price Based on Vehicle\'s Paint Color', x='price', color='paint_color', nbins=100, labels={'paint_color':'Paint Color', 'price':'Price'} )


# Streamlit Localhost:
header = st.container()
dataset = st.container()
model_transmission = st.container()
color_type = st.container()
comparison_model = st.container()

with header:
    st.header("Vehicle Price Data")

with dataset:
    st.header("Info About Vehicle Data in the US")
    st.dataframe(df_vehicle_us)

with model_transmission:
    st.header("Model of Car and Transmission Price")
    st.plotly_chart(fig_model_transmission)


with color_type:
    st.header("Vehicle Popular Color and Type of Car")
    st.plotly_chart(fig_color_type)

    
# Interactive Plot: Car Model and Model Year Price
df_vehicle_us = df_vehicle_us.dropna(subset=['model_year', 'model'])
df_vehicle_us['model_year'] = df_vehicle_us['model_year'].astype(int)
df_vehicle_us = df_vehicle_us.sort_values(by=['model_year'], ascending=False)

selected_models = st.multiselect('Select Models', df_vehicle_us['model'].unique())
selected_models = sorted(selected_models, reverse=True)

# Filter the DataFrame based on selected models
if selected_models:
    df_vehicle_us = df_vehicle_us[df_vehicle_us['model'].isin(selected_models)]

# Allow users to select multiple model years
selected_years = st.multiselect('Select Model Years', df_vehicle_us['model_year'].unique())
selected_years = sorted(selected_years, reverse=True)

# Filter the DataFrame based on selected model years
if selected_years:
    df_vehicle_us = df_vehicle_us[df_vehicle_us['model_year'].isin(selected_years)]

fig_year_model = px.histogram(df_vehicle_us, x='price', color='model', )
fig_year_model.layout.showlegend = False


with comparison_model:
    st.header("Comparing Price between Car Model")

    st.plotly_chart(fig_year_model)
