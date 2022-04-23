
from dash import Input, Output, html,dcc,dash_table, Input, Output,State
from  dash import * 
import dash_bootstrap_components as dbc
from datetime import date
import pandas as pd
import plotly.graph_objects as go 
from urllib.parse import urlparse

import plotly.express as px
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from urllib.parse import urlparse
import sqlite3,time
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d




def prepareDataframe(start_date, end_date, client_id='3blue'):
    
    query ="""SELECT `javascript.enabled`, `document.referrer`, validity, `server.country`, `server.useragent.info`, `server.region`, count(id) as visits FROM sample_sql_db
    WHERE `pixel.timestamp` > {}
    AND `pixel.timestamp` < {}
    AND `var.ClientID` = '{}'
    GROUP BY `javascript.enabled`, `document.referrer`, validity, `server.country`, `server.useragent.info`, `server.region`
    ORDER BY visits DESC""".format(start_date, end_date, client_id)
    records = conn.execute(query).fetchall()

    columns = ['javascript.enabled','document.referrer','validity','server.country','server.useragent.info','server.region','visits']
    df = pd.DataFrame(data=[x.values() for x in records],columns=columns)
    return df


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Traffic Analysis"

df = pd.read_excel(open("data.xlsx",'rb'), sheet_name='Sheet1')

sql_data = 'database.db'
conn = sqlite3.connect(sql_data,check_same_thread=False)
conn.row_factory = dict_factory


def getBotSourceDataTable():
    alphabetical = ['Direct', 'Search', 'Social',  'Display' , 'Unknown']
    tbody = []
    local_df = df
    temp_df = local_df[(local_df['javascript.enabled'] == 1) |  (local_df['javascript.enabled'] == True)]

    for index,source in enumerate(alphabetical[:]):
    #     # Direct
        if index==0:
            temp_df2 = temp_df[  (temp_df['document.referrer'] == '[NULL]') ]
        elif index==1:
            temp_df2 = temp_df[  temp_df["document.referrer"].str.contains("baidu|google|bing|duckduckgo")    ]
        elif index==2:
            temp_df2 = temp_df[  temp_df["document.referrer"].str.contains("baidu|google|facebook|t.co")    ]
        elif index==3:
            temp_df2 = temp_df[  temp_df["document.referrer"].str.contains("site-tracking.com")    ]
        elif index==4:
            temp_df2 = local_df[  (local_df['javascript.enabled'] == '[NULL]') ]
            # print(temp_df2.shape)
            
            
            
            
        total_rows = temp_df2.shape[0]
        if total_rows>0:
            humans = round(temp_df2[(temp_df2['validity']=='valid')].shape[0] / total_rows * 100,2)
            bots = round(temp_df2[(temp_df2['validity']=='invalid') | (temp_df2['validity']=='suspicious')].shape[0] / total_rows * 100,2)
            unknown = round(temp_df2[(temp_df2['validity']=='unknown')].shape[0] / total_rows * 100,2)
        else:
            humans = 0
            bots = 0
            unknown = 0
            
        tbody.append([
            source, total_rows , humans, bots , unknown, {"show":True}
        ])
    tbody = sorted(tbody, key=lambda x: x[1])[::-1]
    
    return {
        "thead": ["Bot Source", "Site Visitors", "% Humans", "% Bots"],
        "tbody": tbody,
        "filters": alphabetical,
        "dropdown_id":"bot_sources_dropdown",
        "title":"Bot Sources",
        "table_id":"bot_sources",
        
        
    } 
            
            
    
    
    


def getDomainDataTabel(): 
    alphabetical =  list(set(df['document.referrer'].values.tolist()))
    alphabetical = [x for x in alphabetical if x] 
    alphabetical = list(set([urlparse(x).netloc.replace(".com","").replace("www.","").capitalize() for x in alphabetical]))
    alphabetical = [x for x in alphabetical if x] 
    
    tbody = []
    for index,source in enumerate(alphabetical[:]):
        temp_df = df[  df["document.referrer"].str.contains(source.lower(), na=False)    ]
        
        total_rows = temp_df.shape[0]
        if total_rows>0:
            humans = round(temp_df[(temp_df['validity']=='valid')].shape[0] / total_rows * 100,2)
            bots = round(temp_df[(temp_df['validity']=='invalid') | (temp_df['validity']=='suspicious')].shape[0] / total_rows * 100,2)
            unknown = round(temp_df[(temp_df['validity']=='unknown')].shape[0] / total_rows * 100,2)
        else:
            humans = 0
            bots = 0
            unknown = 0
            
        tbody.append([
            source.lower(), total_rows , humans, bots , unknown, {"show":True}
        ])
    alphabetical = [x.lower() for x in alphabetical if x] 
    tbody = sorted(tbody, key=lambda x: x[1])[::-1]
    return {
        "thead": ["Bot Source", "Site Visitors", "% Humans", "% Bots"],
        "tbody": tbody,
        "filters": alphabetical,
        "dropdown_id":"domain_performance_dropdown",
        "title":"Domain / Platform Reporting",
        "table_id":"domain_performance",
        
        
    } 
    
    


def getCountryDataTable():
    alphabetical =  list(set(df['server.country'].values.tolist()))
    alphabetical = [x for x in alphabetical if not str(x)=='[NULL]'  and type(x) is str and len(str(x))>0] 
    
    
    tbody = []
    for index,source in enumerate(alphabetical[:]):
        temp_df = df[  (df['server.country'] ==  str(source) ) ]
        total_rows = temp_df.shape[0] 
        
        if total_rows>0:
            humans = round(temp_df[(temp_df['validity']=='valid')].shape[0] / total_rows * 100,2)
            bots = round(temp_df[(temp_df['validity']=='invalid') | (temp_df['validity']=='suspicious')].shape[0] / total_rows * 100,2)
            unknown = round(temp_df[(temp_df['validity']=='unknown')].shape[0] / total_rows * 100,2)
        else:
            humans = 0
            bots = 0
            unknown = 0
        
        if type(source) is str: 
            tbody.append([
                source, total_rows , humans, bots , unknown, {"show":True}
            ])
         
        
    tbody = sorted(tbody, key=lambda x: x[1])[::-1]
    return {
        "thead": ["Bot Source", "Site Visitors", "% Humans", "% Bots"],
        "tbody": tbody,
        "filters": alphabetical,
        "dropdown_id":"country_data_table_dropdown",
        "title":"Country Bots",
        "table_id":"country_data_table",
    } 





def getAllStates(country_name='United States'): 
    global df
    states = list(set(df['server.region'].values.tolist())) 
    return [x for x in states if 'nan' not in  str(x).lower() and 'null' not in  str(x).lower()]
 
def getChannelsList():
    return ['Direct', 'Search', 'Social', 'Programmatic', 'Display' , 'Unknown']

def horizonalLine():
    return html.Div(
        [],
        style= {" border": "0px","border-top": "3px solid #ff7069",},
        className='p-0 my-1' 
    )

### Left Panel ###
# -> Stat Grid Panel
 

stat_label_description={
    "Total Site Users": "'Total site Users' = The total number of vistors to the site in the given time period.",
    '% Bots': '"% Bots" = The total number of bot visitors',
    '% Humans': '"% Humans" = The total number of human visitors',
    '% Friendly Bots': '"% Friendly Bots" = Good bots that you want on your website',
    '% Malicious Bots': '"% Malicious Bots" = "Bad bots that you don"t want on your website',
}

def generateStatPanelChilds(label='',data=''):
    label_element = html.Span(label, id=label, style={'font-size': '14px', "font-weight":"bold"})
    label_element = html.Div(
        [
            label_element,
            dbc.Tooltip(
                stat_label_description[label] if len(label)>2 else '',
                target=label,
                placement="bottom"
            ),
        ]
    )
    
    data_card_element = html.Div(data, className="p-3 m-1 d-flex  justify-content-center", style={"border":"1.5px solid #6c757d", "background-color":"#f5fcff","border-radius":"5px", 'font-size': '16px', "font-weight":"bold","max-width":"100%"})
    component = html.Div(
        [
            label_element if data=='' else data_card_element,
        ],
        className = '', 
    )
    return component


def getStatBarData():
    global df
    temp_df = df 
    total_site_users = temp_df.shape[0] 
    humans = round(temp_df[(temp_df['validity']=='valid')].shape[0]/total_site_users*100,2  ) 
    invalid_bots = temp_df[temp_df["validity"].str.contains("invalid")].shape[0]
    total_bots = temp_df[temp_df["validity"].str.contains("invalid")].shape[0] 
    friendly_bots = temp_df[temp_df["server.useragent.info"].str.contains("bot") & temp_df["server.useragent.info"].str.contains("Googlebot|BingBot|yandex|archive.org") ].shape[0]
    friendly_bots = round(friendly_bots/total_bots*100 ,2)
    malicious_bots = invalid_bots - friendly_bots
    malicious_bots = round(malicious_bots/total_bots*100,2)
    bots = round(total_bots/total_site_users*100,2)


    
    return {
        "total_site_users":total_site_users,
        "humans":humans,
        "friendly_bots":friendly_bots,
        "malicious_bots":malicious_bots,
        "bots":bots,
    }



def generateStatBar():
    stat_panel_child_classes = "p-0 m-0"
    stat_panel_data = getStatBarData()
    stat_panel = dbc.Row(
        [
            # Main Stat Grid
            dbc.Col(
                [
                    # Labels
                    dbc.Row(
                        [
                            dbc.Col(generateStatPanelChilds("Total Site Users",), className=stat_panel_child_classes),
                            dbc.Col(generateStatPanelChilds("% Bots",), className=stat_panel_child_classes),
                            dbc.Col(generateStatPanelChilds("% Humans",), className=stat_panel_child_classes),
                            dbc.Col(generateStatPanelChilds("% Friendly Bots",), className=stat_panel_child_classes),
                            dbc.Col(generateStatPanelChilds("% Malicious Bots",), className=stat_panel_child_classes), 
                        ], 
                        className='p-0 m-0' 
                    ),
                    dbc.Row(
                        [horizonalLine(), ], className='p-0 mx-1' 
                    ),
                    # Data Cards
                    dbc.Row(
                        [
                            dbc.Col(generateStatPanelChilds(data= str(stat_panel_data['total_site_users']) ), className=stat_panel_child_classes),
                            dbc.Col(generateStatPanelChilds(data= str(stat_panel_data['bots'])+"%" ), className=stat_panel_child_classes),
                            dbc.Col(generateStatPanelChilds(data= str(stat_panel_data['humans'])+"%" ), className=stat_panel_child_classes),
                            dbc.Col(generateStatPanelChilds(data= str(stat_panel_data['friendly_bots'])+"%" ), className=stat_panel_child_classes),
                            dbc.Col(generateStatPanelChilds(data= str(stat_panel_data['malicious_bots'])+"%" ), className=stat_panel_child_classes),
                            
                        ], 
                        className='p-0 m-0' 
                    )


                ]
                
            ),
    
    
        ], 
        
        className='p-0 m-0' ,
        id='stat_panel_main_div'
    )

    return stat_panel



stat_bar_init_form = generateStatBar()


# ------------------------------------------------------------------------------------------------------
map_select_state_dropdown = html.Div(
    [
        dbc.Label("Select a State", html_for="dropdown",className='px-4'),
        dcc.Dropdown(
            id="map_select_state_dropdown",
            options=[
                {"label": x, "value": x} for x in getAllStates()
            ],
        ),
    ],
    className="",
)

map_header_div = html.Div(
    [
        # Map Header Div
        html.Br(),
        html.Div(
            [
                html.Div(
                    [
                        html.Span("Traffic Map" , style={'font-size': '20px', }),
                        html.Br(),
                        html.Span("United States" , style={'font-size': '20px', "font-weight":"bold" }),
                    ]
                ),
                
                map_select_state_dropdown
                
            ],
            style={"display":"flex","flex-direction":"row","justify-content":"space-between","align-items":"center"}
        ),
    ],
)

def getMapData():
    global df
    temp_df = df[  (df['server.country'] == 'United States') ]
    total_rows = temp_df.shape[0]
    states = temp_df['server.region'].values.tolist()
    stateDictionary =  {"Alaska" : "AK", "Alabama" : "AL", "Arkansas" : "AR", "American Samoa" : "AS", "Arizona" : "AZ", "California" : "CA", "Colorado" : "CO", "Connecticut" : "CT", "District of Columbia" : "DC", "Delaware" : "DE", "Florida" : "FL", "Georgia" : "GA", "Guam" : "GU", "Hawaii" : "HI", "Iowa" : "IA", "Idaho" : "ID", "Illinois" : "IL", "Indiana" : "IN", "Kansas" : "KS", "Kentucky" : "KY", "Louisiana" : "LA", "Massachusetts" : "MA", "Maryland" : "MD", "Maine" : "ME", "Michigan" : "MI", "Minnesota" : "MN", "Missouri" : "MO", "Mississippi" : "MS", "Montana" : "MT", "North Carolina" : "NC", "North Dakota" : "ND", "Nebraska" : "NE", "New Hampshire" : "NH", "New Jersey" : "NJ", "New Mexico" : "NM", "Nevada" : "NV", "New York" : "NY", "Ohio" : "OH", "Oklahoma" : "OK", "Oregon" : "OR", "Pennsylvania" : "PA", "Puerto Rico" : "PR", "Rhode Island" : "RI", "South Carolina" : "SC", "South Dakota" : "SD", "Tennessee" : "TN", "Texas" : "TX", "Utah" : "UT", "Virginia" : "VA", "Virgin Islands" : "VI", "Vermont" : "VT", "Washington" : "WA", "Wisconsin" : "WI", "West Virginia" : "WV", "Wyoming" : "WY"}
    
    states = list(set([x for x in states if str(x) not in  ['[NULL]', 'nan','NULL','NONE'] ]))

    states = [x for x in states if len(str(x))>0 and str(x)!='None' ]

    
    density = []
    total_site_users_list = []
    percentage_bots = []
    percentage_humans = []
    percentage_friendly_bots = []
    percentage_malicious_bots = []

    
    for state in states:
        local = df[(df['server.region'] ==state)]
        bots = local[local["validity"].str.contains("invalid")].shape[0]
        if bots>0:
            bots = round(bots/local.shape[0] *100,2)
        density.append(bots)    
        temp_df2 = df[  (df['server.region'] == state) ] 
        total_site_users = temp_df2.shape[0] 
        if total_site_users>0:
            humans = round(temp_df2[(temp_df2['validity']=='valid')].shape[0]/total_site_users*100,2  ) 
        else:
            humans=0
        invalid_bots = temp_df2[temp_df2["validity"].str.contains("invalid")].shape[0]
        total_bots = temp_df2[temp_df2["validity"].str.contains("invalid")].shape[0] 
        friendly_bots = temp_df2[temp_df2["server.useragent.info"].str.contains("bot") & temp_df2["server.useragent.info"].str.contains("Googlebot|BingBot|yandex|archive.org") ].shape[0]
        if total_bots>0:
            friendly_bots = round(friendly_bots/total_bots*100 ,2)
            malicious_bots = invalid_bots - friendly_bots
            malicious_bots = round(malicious_bots/total_bots*100,2)
            bots = round(total_bots/total_site_users*100,2)
        else:
            friendly_bots = 0
            malicious_bots = 0
            malicious_bots = 0
            bots = 0
        
        total_site_users_list.append(total_site_users)
        percentage_bots.append(bots)
        percentage_humans.append(humans)
        percentage_friendly_bots.append(friendly_bots)
        percentage_malicious_bots.append(malicious_bots)
        
        
    states = [stateDictionary[x] for x in states]
    density = [100 if x>10 else 0 for x in density]
    percentage_malicious_bots = [x if x>0 else 0 for x in percentage_malicious_bots]
    percentage_bots = [str(x)+"%" for x in percentage_bots]
    percentage_humans = [str(x)+"%" for x in percentage_humans]
    percentage_friendly_bots = [str(x)+"%" for x in percentage_friendly_bots]
    percentage_malicious_bots = [str(x)+"%" for x in percentage_malicious_bots]
    
    
    
    columns = ['states','density','total_site_users','percentage_bots','percentage_humans','percentage_friendly_bots','percentage_malicious_bots']
    return pd.DataFrame(data=zip(states,density,total_site_users_list,percentage_bots,percentage_humans,percentage_friendly_bots,percentage_malicious_bots), columns=columns) 


def getGraph():
    global df
    
    color_discrete_sequence=[ "#00db1d",  "#57ff52",   "#ff7154","#ff5d47", ]
 
    map_data = getMapData() 
    
    labels={'states':'State','density':"Density",'total_site_users':"Total Site Users",'percentage_bots':"% Bots", "percentage_humans": "% Humans", "percentage_friendly_bots": "% Friendly Bots","percentage_malicious_bots":"% Malicious Bots"}
    hover_data = ['states','density','total_site_users','percentage_bots','percentage_humans','percentage_friendly_bots','percentage_malicious_bots']
    figure=px.choropleth(map_data,labels=labels,locations='states', locationmode="USA-states",color='density', hover_data= hover_data,  scope="usa",color_continuous_scale=color_discrete_sequence)
    figure.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    figure.layout.coloraxis.colorbar.title = 'Density'
    
    
    graph = dcc.Graph(
            id='map',
            figure=figure,
            className="p-0 m-0"
        )
    return graph




def generateMapPanel():
    return html.Div(
        [
            map_header_div,
            html.Br(),
            getGraph()
        ],
        # className='px-1',
        style={},
        id="map_panel_main_div"
    )


map_panel_init_form = generateMapPanel()





# ------------------------------------------------------------------------------------------------------
def generateLeftPanel():
    return html.Div(
    [
        # Stat Panel
        stat_bar_init_form, 
        # Map Panel
        map_panel_init_form  ,
       
        
    ],  
    className='vh-100 m-2',
  
    
)







# ------------------------------------------------------------------------------------------------------
def generateTableHeader(title,dropdown_id,filters):
    dropdown = html.Div(
        [
            # Map Header Div 
            html.Div(
                [
                    # Table Title
                    html.Div(
                        [
                            html.Span(title , style={'font-size': '25px', }), 
                        ]
                    ), 
                    # Table Filter
                    html.Div(
                            [ 
                                dcc.Dropdown(
                                    id=dropdown_id,
                                    options=[
                                        {"label": x, "value": x} for x in filters
                                    ],
                                    style={"width":"200px"} , 
                                ),
                            ],
                            className="",
                        ) 
                ],
                
                style={"display":"flex","flex-direction":"row","justify-content":"space-between","align-items":"center"}
            ),
        ],
    )
    return dropdown
        



def generateTable(data,top_bar_required=True):
    global df
    table_top_bar = generateTableHeader(title=data['title'], dropdown_id=data['dropdown_id'], filters=data['filters'] )
    table_header = [
        html.Thead(
            html.Tr(
                [
                    html.Th(heading) for heading in data['thead']
                ], 
            ), 
            style= {"border": "0px","border-bottom": "3px solid #ff7069","margin-bottom":""},
        )
    ] 
    
    rows = []
    for row in data['tbody']:
        if row[-1]['show']:
            rows.append(
                html.Tr(
                    [
                        html.Td(row[0]), 
                        html.Td(row[1]), 
                        html.Td(str(row[2])+"%"), 
                        html.Td(str(row[3])+"%"), 
                    ]
                )
            )
        
        
    table_body = [html.Tbody(rows)]
    table = dbc.Table(table_header + table_body, bordered=False,borderless =True, id=data['table_id'], style={"margin":"0px"})
    if top_bar_required:
        return html.Div([
            table_top_bar,
            table,
        ])
    else:
        return table
        





# bot_sources_dropdown



 
bot_source_data_table_init_form = getBotSourceDataTable()
domain_data_table_init_form = getDomainDataTabel()
country_data_table_init_form = getCountryDataTable()


start_date_object =date(2022, 4, 1)
end_date_object =date(2022, 4, 25)

def generateDateFilterDiv():
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            dcc.DatePickerSingle(
                                id='start_date_picker', 
                                initial_visible_month=start_date_object,
                                date=start_date_object,
                            ),
                            dcc.DatePickerSingle(
                                id='end_date_picker', 
                                initial_visible_month=end_date_object,
                                date=end_date_object,
                                
                            ),
                        ]
                    ),
                    dbc.Button("Fetch Data", color="primary", className="me-1",id="date_filter_submit_btn"),
                    # html.Span("",id='temp_span')
                    # dbc.Button("Fetch Data",size='lg', color="primary", className="me-1")
                ],
                className='date_range_filter_div'
                
            )
        ],
        className="shadow  bg-white rounded p-2  sticky-top ",
        style={"position": "absolute",'top': '10px',"width":"49%"}
        
    )


def generateAllTablesDiv():
    return html.Div(
                [
                    generateTable(data=bot_source_data_table_init_form),
                    html.Br(),
                    generateTable(data=domain_data_table_init_form),
                    html.Br(),
                    generateTable(data=country_data_table_init_form),
                ], 
                id="all_tables_div"  
            )


all_tables_div_init_form = generateAllTablesDiv()


def generateRightPanel():
    return    html.Div(
        [
            generateDateFilterDiv(),
            html.Div(
                [
                    all_tables_div_init_form
                ],
                className="shadow  bg-white rounded p-2",
                style={"margin-top":"75px"}
            )
        ],
        
        className="m-2",
        style={"display":"flex","flex-direction":"column","align-items":"", },
        id="right_panel_main_div"
    )




@app.callback(
    # Output('temp_span', 'children') ,
    Output('stat_panel_main_div', 'children') ,
    Output('map_panel_main_div', 'children') ,
    Output('all_tables_div', 'children') ,
    Input('date_filter_submit_btn', 'n_clicks'), 
    State('start_date_picker', 'date'),
    State('end_date_picker', 'date'),
)
def update_output(n_clicks,start_date_picker,end_date_object):
    
    start_date = time.mktime(datetime.strptime(start_date_picker, "%Y-%m-%d").timetuple())
    end_date = time.mktime(datetime.strptime(end_date_object, "%Y-%m-%d").timetuple())
    client_id = '3blue'
    global df
    global bot_source_data_table_init_form
    global domain_data_table_init_form
    global country_data_table_init_form
    global stat_bar_init_form
    global map_panel_init_form
    global all_tables_div_init_form
    
    
    if n_clicks is not None:
        
        temp = prepareDataframe(start_date=start_date,end_date=end_date)
        print(temp.shape)
        
        df = temp
        # global df
        # 1. update main df (data ranges beetween new time ranges )
        # 2. update stat panel
        # 3. update states Dropdown
        # 4. Update Map
        # 5. update tables
        bot_source_data_table_init_form = getBotSourceDataTable() 
        domain_data_table_init_form = getDomainDataTabel()
        country_data_table_init_form = getCountryDataTable()
        stat_bar_init_form = generateStatBar()
        map_panel_init_form = generateMapPanel()
        all_tables_div_init_form = generateAllTablesDiv()
        
        
        
        return  stat_bar_init_form, map_panel_init_form, all_tables_div_init_form
    else:
        return  stat_bar_init_form, map_panel_init_form, all_tables_div_init_form
    
    
    

@app.callback(
    Output('bot_sources', 'children'),
    Input('bot_sources_dropdown', 'value')
)
def update_output(value):
    
    temp_data = bot_source_data_table_init_form
    if value=='None' or value is None: 
        for index,row in enumerate(temp_data['tbody']):
            temp_data['tbody'][index][-1]['show']=True
        return generateTable(temp_data,top_bar_required=False)
    else:
        for index,row in enumerate(temp_data['tbody']):
            if row[0]==value:
                temp_data['tbody'][index][-1]['show']=True
            else:
                temp_data['tbody'][index][-1]['show']= False
            
         
        return generateTable(temp_data,top_bar_required=False)
     
     
     
@app.callback(
    Output('country_data_table', 'children'),
    Input('country_data_table_dropdown', 'value')
)
def update_output(value):
    
    temp_data = country_data_table_init_form
    if value=='None' or value is None: 
        for index,row in enumerate(temp_data['tbody']):
            temp_data['tbody'][index][-1]['show']=True
        return generateTable(temp_data,top_bar_required=False)
    else:
        for index,row in enumerate(temp_data['tbody']):
            if row[0]==value:
                temp_data['tbody'][index][-1]['show']=True
            else:
                temp_data['tbody'][index][-1]['show']= False
            
         
        return generateTable(temp_data,top_bar_required=False)
     
     
         

@app.callback(
    Output('domain_performance', 'children'),
    Input('domain_performance_dropdown', 'value')
)
def update_output(value): 
    temp_data = domain_data_table_init_form
    if value=='None' or value is None: 
        for index,row in enumerate(temp_data['tbody']):
            temp_data['tbody'][index][-1]['show']=True
        return generateTable(temp_data,top_bar_required=False)
    else:
        for index,row in enumerate(temp_data['tbody']):
            if row[0]==value:
                temp_data['tbody'][index][-1]['show']=True
            else:
                temp_data['tbody'][index][-1]['show']= False
            
         
        return generateTable(temp_data,top_bar_required=False)



def generateMainRow():
    return dbc.Row(
    [
        dbc.Col(generateLeftPanel(), className='p-0 m-0 vh-100 hidden_scroll_bar'),
        dbc.Col(generateRightPanel(),  className='p-0 m-0 vh-100 hidden_scroll_bar'), 
    ],
    className='p-0 m-0 bg-light vh-100', 
)





 

#  Main Container
app.layout = html.Div(
    generateMainRow(    )
)

if __name__ == "__main__":
    app.run_server(debug=True)
