import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
from dash_extensions.enrich import Dash, Input, State, Output, html, dcc

# start Dash
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])

# declare colors
colors = {
    'BLACK': '#000000',
    'TEXT': '#696969',
    'PLOT_COLOR': '#C0C0C0',
    'WHITE': '#FFFFFF',
    'GOLD': '#EEBC35',
    'BROWN': '#53354D',
    'GREEN': '#42CE90',
    'RED': '#F87861',
    'YELLOW': '#F1F145',
    'SKY_BLUE': '#A3DBE1',
    'SILVER': '#CCCCCC',
    'LIGHT_BLACK': '#374649'
}

# import data
kenya_data = pd.read_csv('kenya.csv', low_memory=False)

all_data = kenya_data
all_data = all_data[
    ['indicator', 'classif2', 'time',
     'sex', 'sex.label', 'classif1', 'classif1.label', 'classif2.label', 'obs_value', 'ref_area.label']]

#rename long values
mapping = {'Age (Youth bands): 15-19': '15-19', 'Age (Youth bands): 20-24': '20-24',
           'Age (Youth bands): 25-29': '25-29', 'Household type: One person': 'One Person',
           'Household type: Couple without children': 'Couple without children',
           'Household type: Couple with children': 'Couple with Children',
           'Household type: Lone parent': 'Lone Parent',
           'Household type: Extended family': 'Extended family',

           }

all_data['classif1.label'] = all_data['classif1.label'].map(mapping)
all_data.replace(
    'Transition forms: 2 - School leavers in satisfactory temporary or self-employment, not wanting to change '
    'job', 'SL, Satisfactory self employmnt')

youth_age_transition = all_data[(all_data['indicator'] == 'POP_3FOR_SEX_AGE_TRA_NB') &
                                (all_data['classif1'] != 'AGE_YTHBANDS_Y15-29') &
                                (all_data['classif2'] != 'TRA_FORMS_TOTAL')]
col_mappint2 = {'Transition forms: 1 - School leavers in stable employment': 'SL, Stable Emplymnt',
                'Transition stages: 2 - In transition': 'In Transition',
                'Transition forms: 3 - Students in the labour force': 'Student in Labor Force',
                'Transition forms: 4 - Unemployed school leavers': 'Unemployed',
                'Transition forms: 5 - School leavers in non-stable or non-satisfactory employment, wanting to '
                'change job':
                    'SL wishing to switch job',
                'Transition forms: 6 - Outside the labour force - school leavers in potential labour force or aiming '
                'to look for work later':
                    'SL aiming to look for work ',
                'Transition forms: 7 - Outside the labour force - students': 'Students out of labour force',
                'Transition forms: 8 - Outside the labour force - school leavers with no intention of looking for work':
                    'SL not searching for work'
                }
youth_age_transition['classif2.label'] = youth_age_transition['classif2.label'].map(col_mappint2)

# get data on education for the unemployed youth
youth_age_education = all_data[(all_data['indicator'] == 'UNE_TUNE_SEX_AGE_EDU_NB') &
                               (all_data['time'] == 2019) &
                               (all_data['classif2'] != 'EDU_AGGREGATE_TOTAL') &
                               (all_data['classif2'] != 'EDU_ISCED11_TOTAL') &
                               (all_data['classif2'] != 'EDU_ISCED11_X') &
                               (all_data['classif2'] != 'EDU_ISCED11_0') &
                               (all_data['classif2'] != 'EDU_ISCED11_1') &
                               (all_data['classif2'] != 'EDU_ISCED11_2') &
                               (all_data['classif2'] != 'EDU_ISCED11_3') &
                               (all_data['classif2'] != 'EDU_ISCED11_6') &
                               (all_data['classif1'] != 'AGE_AGGREGATE_YGE65') &
                               (all_data['classif1'] != 'AGE_10YRBANDS_TOTAL') &
                               (all_data['classif1'] != 'AGE_10YRBANDS_YLT15') &
                               (all_data['classif1'] != 'AGE_YTHADULT_Y15-24') &
                               (all_data['classif1'] != 'AGE_5YRBANDS_TOTAL') &
                               (all_data['classif1'] != 'AGE_5YRBANDS_Y00-04') &
                               (all_data['classif1'] != 'AGE_10YRBANDS_YGE65') &
                               (all_data['classif1'] != 'AGE_10YRBANDS_Y55-64') &
                               (all_data['classif1'] != 'AGE_5YRBANDS_Y05-09') &
                               (all_data['classif1'] != 'AGE_5YRBANDS_Y10-14') &
                               (all_data['classif1'] != 'AGE_5YRBANDS_Y15-19') &
                               (all_data['classif1'] != 'AGE_5YRBANDS_Y20-24') &
                               (all_data['classif1'] != 'AGE_5YRBANDS_Y25-29') &
                               (all_data['classif1'] != 'AGE_5YRBANDS_Y30-34') &
                               (all_data['classif1'] != 'AGE_YTHADULT_Y15-64') &
                               (all_data['classif1'] != 'AGE_5YRBANDS_Y35-39') &
                               (all_data['classif1'] != 'AGE_5YRBANDS_Y40-44') &
                               (all_data['classif1'] != 'AGE_5YRBANDS_Y45-49') &
                               (all_data['classif1'] != 'AGE_YTHADULT_YGE25') &
                               (all_data['classif1'] != 'AGE_5YRBANDS_Y50-54') &
                               (all_data['classif1'] != 'AGE_5YRBANDS_Y55-59') &
                               (all_data['classif1'] != 'AGE_5YRBANDS_Y60-64') &
                               (all_data['classif1'] != 'AGE_YTHADULT_YGE15') &
                               (all_data['classif1'] != 'AGE_5YRBANDS_YGE65') &
                               (all_data['classif1'] != 'AGE_AGGREGATE_TOTAL') &
                               (all_data['classif1'] != 'AGE_AGGREGATE_Y25-54') &
                               (all_data['classif1'] != 'AGE_AGGREGATE_Y15-24') &
                               (all_data['classif1'] != 'AGE_AGGREGATE_Y25-34') &
                               (all_data['classif1'] != 'AGE_5YRBANDS_YGE65') &
                               (all_data['classif1'] != 'AGE_AGGREGATE_Y55-64') &
                               (all_data['classif1'] != 'AGE_10YRBANDS_Y45-54') &
                               (all_data['classif1'] != 'AGE_10YRBANDS_Y35-44') &
                               (all_data['classif2'] != 'MTS_AGGREGATE_TOTAL') &
                               (all_data['classif2'] != 'MTS_DETAILS_TOTAL') &
                               (all_data['classif2'] != 'MTS_DETAILS_SGLE') &
                               (all_data['classif2'] != 'MTS_DETAILS_MRD') &
                               (all_data['classif2'] != 'MTS_DETAILS_UNION') &
                               (all_data['classif2'] != 'MTS_DETAILS_WID') &
                               (all_data['classif2'] != 'MTS_DETAILS_SEP') &
                               (all_data['classif2'] != 'MTS_DETAILS_X')
                               ]

# get household data
monthly_earning_household_kids = all_data[(all_data['indicator'] == 'GED_PEAR_SEX_HHT_CHL_NB') &
                                          (all_data['classif1'] != 'HHT_AGGREGATE_TOTAL') &
                                          (all_data['classif2'] != 'CHL_NUMLT6_TOTAL') &
                                          (all_data['classif2'] != 'CHL_AGET6_TOTAL') &
                                          (all_data['classif2'] != 'CHL_AGET6_YES') &
                                          (all_data['classif2'] != 'CHL_AGET6_NO')
                                          ]

# remove nulls
monthly_earning_household_kids['obs_value'] = monthly_earning_household_kids['obs_value'].replace('0.00', np.nan)
monthly_earning_household_kids = monthly_earning_household_kids.dropna(axis=0, subset=['obs_value'])

# get education data
youth_age_education = youth_age_education[['sex', 'sex.label', 'classif1', 'classif1.label', 'classif2', 'obs_value']]
youth_age_education = youth_age_education.dropna(axis=0, subset=['obs_value'])

# calculate the subtotal for each education category
less_than_basec_total = youth_age_education.loc[
    youth_age_education['classif2'] == 'EDU_AGGREGATE_LTB', 'obs_value'].sum()
basic_total = youth_age_education.loc[youth_age_education['classif2'] == 'EDU_AGGREGATE_BAS', 'obs_value'].sum()
intermediate_total = youth_age_education.loc[youth_age_education['classif2'] == 'EDU_AGGREGATE_INT', 'obs_value'].sum()
advanced_total = youth_age_education.loc[youth_age_education['classif2'] == 'EDU_AGGREGATE_ADV', 'obs_value'].sum()

# create dataframe that will be used to generate pie chart
totals_df = pd.DataFrame({'EducationLevels': ['Less than Basic',
                                              'Basic',
                                              'Intermediate',
                                              'Advanced'],
                          'Values': [less_than_basec_total, basic_total, intermediate_total, advanced_total]})

#draw pie chart
totals_pie = px.pie(totals_df, values='Values', names='EducationLevels')

totals_pie.update_traces(title_font=dict(size=25,
                                         family='Verdana',
                                         color='darkred'
                                         ),
                         hoverinfo='label+percent',
                         textfont_size=20),

totals_pie.update_layout(legend=dict(
    entrywidth=100,
    yanchor="top",
    y=-0.1,
    xanchor="right",
    x=1
))

# draw barc chart of monthly earning
fig3 = px.bar(monthly_earning_household_kids, x="classif1.label", y="obs_value",
              color="classif2.label",
              barmode='group')
fig3.update_layout(legend=dict(
    entrywidth=100,
    yanchor="top",
    y=-0.1,
    xanchor="right",
    x=1
))

# draw bar graph of transition forms
fig = px.bar(youth_age_transition, x="classif1.label", y="obs_value",
             color="classif2.label",
             barmode='group')

fig.update_layout(legend=dict(
    entrywidth=100,
    yanchor="top",
    y=-0.1,
    xanchor="right",
    x=1
))

#specify available dropdown options
gender_options = [{'label': i, 'value': i} for i in youth_age_transition['sex.label'].unique()]
country_options = [{'label': i, 'value': i} for i in youth_age_transition['ref_area.label'].unique()]

# dashboard layout
app.layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    [html.H1(children='Youth Employment Trends'),
                     html.P(['Transition trends across different age groups', html.Br(),
                             html.A('ILO Data Youth Unemployment Challenge',
                                    href='https://urlhere.report',
                                    target='_blank'),
                             html.Br(),
                             ]
                            ),
                     html.Br()
                     ]), md=12
            )
        ]
    ),
    dbc.Row([
        dbc.Col(

            html.Div(
                html.P("")
            ), md=1
        ),
        dbc.Col(
            html.Div(
                [
                    dcc.Dropdown(id='country-dropdown',
                                 options=country_options,
                                 value='Kenya'), html.Br()
                ]), md=5
        ),
        dbc.Col(
            html.Div(
                [
                    dcc.Dropdown(id='gender-dropdown',
                                 options=gender_options,
                                 value='Sex: Total'), html.Br()
                ]), md=5
        ),
        dbc.Col(

            html.Div(
                html.P("")
            ), md=1
        )
    ]

    ),
    dbc.Row(
        [
            dbc.Col(

                html.Div(
                    html.P("")
                ), md=1
            ),
            dbc.Col(
                html.Div(
                    [dcc.Graph(id='happiness-graph',
                               figure=fig), html.Br()]
                ), md=5
            ),
            dbc.Col(
                html.Div(
                    [dcc.Graph(id='graph2-graph',
                               figure=totals_pie), html.Br()]
                ), md=5
            ),
            dbc.Col(
                html.Div(
                    html.P("")
                ), md=1
            )
        ]
    ),
    dbc.Row([
        dbc.Col(

            html.Div(
                html.P("")
            ), md=3
        ),
        dbc.Col(
            html.Div(
                [
                    dcc.Graph(id='graph3-graph',
                              figure=fig3)
                ]), md=6
        ),
        dbc.Col(

            html.Div(
                html.P("")
            ), md=3
        )
    ]

    )

])

# event handlers section, for the different data selections

@app.callback(
    Output('happiness-graph', 'figure'),
    Input('gender-dropdown', 'value'))
def update_graph(selected_country):
    filtered_happiness = youth_age_transition[youth_age_transition['sex.label'] == selected_country]
    fig = px.bar(filtered_happiness, x="classif1.label", y="obs_value",
                 color="classif2.label",
                 barmode='group')

    fig.update_layout(title='Forms of Transition among Different Age Bands',
                      paper_bgcolor=colors['LIGHT_BLACK'],
                      plot_bgcolor=colors['LIGHT_BLACK'],
                      font={'color': colors['WHITE']},
                      xaxis_tickfont_size=14,
                      xaxis=dict(showgrid=True,
                                 title='Age bands',
                                 titlefont_size=16,
                                 tickfont_size=14,
                                 ),
                      yaxis=dict(showgrid=True,
                                 title='Youth working-age population (thousands)',
                                 titlefont_size=16,
                                 tickfont_size=14,
                                 ), showlegend=True)
    return fig


@app.callback(
    Output('graph2-graph', 'figure'),
    Input('gender-dropdown', 'value'))
def update_graph2(selected_country):
    # filtered_data = totals_df[totals_df['sex.label'] == selected_country]

    totals_pie = px.pie(totals_df, values='Values', names='EducationLevels')
    totals_pie.update_traces(title_font=dict(size=25,
                                             family='Verdana',
                                             color='darkred'
                                             ),
                             hoverinfo='label+percent',
                             textfont_size=20),

    totals_pie.update_layout(title='Education Level of the Unemployed Youth',
                             paper_bgcolor=colors['LIGHT_BLACK'],
                             plot_bgcolor=colors['LIGHT_BLACK'],
                             font={'color': colors['WHITE']},
                             xaxis_tickfont_size=14,
                             yaxis=dict(showgrid=True,
                                        title='',
                                        titlefont_size=16,
                                        tickfont_size=14,
                                        ), showlegend=True)
    return totals_pie


@app.callback(
    Output('graph3-graph', 'figure'),
    Input('gender-dropdown', 'value'))
def update_graph2(selected_country):
    filtered_data = monthly_earning_household_kids[monthly_earning_household_kids['sex.label'] == selected_country]
    new_figure = px.bar(filtered_data, x="classif1.label", y="obs_value",
                        color="classif2.label",
                        barmode='group')

    new_figure.update_layout(title='Mean Monthly Earning Per Household with Children',
                             paper_bgcolor=colors['LIGHT_BLACK'],
                             plot_bgcolor=colors['LIGHT_BLACK'],
                             font={'color': colors['WHITE']},
                             xaxis_tickfont_size=14,
                             xaxis=dict(showgrid=True,
                                        title='Household Categories',
                                        titlefont_size=16,
                                        tickfont_size=14,
                                        ),
                             yaxis=dict(showgrid=True,
                                        title='Mean Monthly Income (Lcy)',
                                        titlefont_size=16,
                                        tickfont_size=14,
                                        ), showlegend=True)
    return new_figure


