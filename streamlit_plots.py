from click import option
import pandas as pd
import streamlit as st
import plotly_express as px
import plotly.graph_objects as go

import filter_correct_3 as fk
import bin_averaging_4 as ba

st.set_page_config(page_title='Kennlinientool', page_icon='🖖')   #st.image('logo_favicon.ico')


padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)


header_container = st.container()
pitch_container = st.container()
rpm_container = st.container()
data_available_container = st.container()
lk_container = st.container()




with header_container:
    # for example a logo or a image that looks like a website header
	st.image('omexom_logo.png')

	# different levels of text you can include in your app
	st.title("Kennlinien Tool")
	st.header("IEC Standardisierte Berechnung der Leistungskennlinie!")
	st.subheader("Hier werden die Ergebnisse gezeigt")
	st.write("Unten sind die Diagramme der Ergebnisse")

with pitch_container:
	df_filt = fk.df[(fk.df['Lower Limit Filter'] == True) & (fk.df['Active Power Filter'] == True)]

	pitch_plot = px.scatter(df_filt, x='Active Power', y='Pitch Angle', color='Identifier', title='Pitch Plot', width=1000, height=800)
	pitch_plot.add_scatter(
						x=fk.xpitch_plt, 
						y=fk.ypitch_plt,
						mode='lines',
						name='Pitch Winkel Filter'
						)

	st.write(pitch_plot)

with rpm_container:

	rpm_df = fk.df[(fk.df['Lower Limit Filter'] == True)]

	# Multiselect um die Anlagen anzuzeigen, die ausgewhählt wurden
	rpm_turbine = df_filt['Identifier'].drop_duplicates()
	rpm_turbine_selected = st.multiselect('Wählen Sie die Anlangen aus, die angezeigt werden sollen:', options=rpm_turbine)
	mask_rpm_turbine = rpm_df['Identifier'].isin(rpm_turbine_selected)
	rpm_df = rpm_df[mask_rpm_turbine]


	rpm_plot = px.scatter(rpm_df, x='Active Power', y='Rotor Speed', title='RPM Diagram', color='Identifier', width=1000, height=800)

	rpm_plot.add_scatter(x=fk.xrpm_plt, 
						y=fk.yrpm_plt,
						mode='lines',
						name='RPM Filter')


	st.write(rpm_plot)

with data_available_container:
	filtered_values = fk.df[(fk.df['Lower Limit Filter'] == True) & (fk.df['Active Power Filter'] == True)]
	unfiltered_values = fk.df

	data_available_plot = go.Figure()
	

	data_available_plot.add_scatter(x=unfiltered_values['Corrected Wind Speed'],
									y=unfiltered_values['Active Power'],
									mode='markers',
									name='Ungefilterte Daten')

	data_available_plot.add_scatter(x=filtered_values['Corrected Wind Speed'],
									y=filtered_values['Active Power'],
									mode='markers',
									name='Gefilterte Daten')

	#data_available_plot = px.scatter(filtered_values, x='Corrected Wind Speed', y='Active Power', title='Dataavailablity Diagram', color='Corrected Wind Speed')

	#data_available_plot.add_scatter(x=unfiltered_values['Corrected Wind Speed'],
	#								y=unfiltered_values['Active Power'],
	#								mode='markers',
	#								name='Ungefilterte Daten')
	
	data_available_plot.update_layout(
									width=1000,
									height=800
	)

	st.write(data_available_plot)

with lk_container:
	hk_df = ba.df_f[ba.df_f['Identifier'] == 'HK']
	lk_df = ba.df_f[ba.df_f['Identifier'] != 'HK']

	lk_turbine = lk_df['Identifier'].unique()

	print(lk_turbine)
	#lk_turbine_selected = st.multiselect('Wählen Sie die Anlangen aus, die angezeigt werden sollen:', options=lk_turbine)
	#mask_lk_turbine = rpm_df['Identifier'].isin(lk_turbine_selected)
	#lk_df = lk_df[mask_rpm_turbine]

	lk_df = lk_df.sort_values(by=['Identifier', 'V'])

	lk_plot = px.line(lk_df, x='V', y='P', title='Leistungskennlinie', color='Identifier', height=800, width=1000)
	
	lk_plot.add_scatter(x=hk_df['V'],
						y=hk_df['P'],
						mode='lines',
						name='Herstellerkennlinie')

	st.write(lk_plot)