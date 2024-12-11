
import pandas as pd
import streamlit as st
import plotly.express as px
import json
import datetime
import numpy as np


st.set_page_config(layout='wide')

########################Loading data ###########################
df1 = pd.read_csv('Data/df1.csv')
df2 = pd.read_csv('Data/df2.csv')
df3 = pd.read_csv('Data/df3.csv')
inactive_customers = pd.read_csv('Data/inactive_customers.csv')
customers = pd.read_csv(''Data/df2.customers.csv')
df3['days_to_deliver'] = pd.to_timedelta(df3['days_to_deliver']).dt.days
#########################  Tabs  ###################################################
st.markdown(
    """
    <style>
    /* Overall tab container styling */
    .stTabs [role="tablist"] {
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 8px;
    }

    /* Unselected tab styling */
    .stTabs [role="tab"] {
        color: #555;
        font-size: 16px;
        font-weight: 500;
        padding: 10px 20px;
        border-radius: 5px 5px 0 0;
        background-color: #f9f9f9;
    }

    /* Hover effect on tabs */
    .stTabs [role="tab"]:hover {
        background-color: #DBE2E9;
    }

    /* Active tab styling */
    .stTabs [aria-selected="true"] {
        color: #fff;
        background-color: #4B68B8;
        font-weight: bold;
        border-bottom: 3px solid #0827F5;
    }
    </style>
    """,unsafe_allow_html=True)

tab1,tab2,tab3,tab4=st.tabs(['Demographical Analysis','Geographical analysis',' Sales performance','SLA'])
################################################################

##### Demographical analysis 
with tab1:
    
    Demo_selection = st.radio('Choose a category:', ['age', 'gender'])
    
    col1,col2,col3= st.columns([9,0.5,6])
    with col1:
        fig = px.histogram(inactive_customers,x=Demo_selection,template='simple_white',
            title='The Demographical Analysis for Customer Base'.title(), text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
        
        fig11 = px.histogram(inactive_customers[inactive_customers['active']=='Yes'],x=Demo_selection,
                             template='simple_white', color_discrete_sequence=['#85BFFF'],
            title='Active customer only'.title(),text_auto=True)
        st.plotly_chart(fig11, use_container_width=True)
        
    with col3:
        fig1= px.pie(inactive_customers,names='active',
                     title=f'Base distribution out of {len(inactive_customers)} customers'.title(),
                     template='presentation')
        st.plotly_chart(fig1, use_container_width=True)
        
        if Demo_selection == 'age':
            fig2 = px.box(inactive_customers,y='age',template='simple_white',
                     color='active',title='active and inactive ages'.title())
        else:
            fig2 = px.histogram(inactive_customers,x='gender',template='simple_white',color='active',title='per gender')
    
        st.plotly_chart(fig2, use_container_width=True)

#################### Geographical Analysis###########

with tab2:
    
    Geo=df3.groupby('state').agg(Revenue=('total_price','sum'),
                             sold_pieces=('sold_quantity','sum'),
                              TotOrders=('order_id','nunique')).reset_index().sort_values(by='Revenue',ascending=False)

    # Load GeoJSON data (Australian States boundaries)
    with open(r'C:\sherif\DS course\python sessions\session 40\shopping Card Project - Assignment\australian-states.geojson') as f:
        geojson = json.load(f)

    # Create a choropleth map
    fig = px.choropleth(
        Geo,
        geojson=geojson,
        locations='state',
        featureidkey="properties.STATE_NAME",  
        color='Revenue',
        hover_name='state',
        color_continuous_scale="Blues",
        title="Revenue by State in Australia"
        
    )

    # Update the map layout to focus on Australia
    fig.update_geos(
        projection_type="mercator",
        fitbounds="locations",
        visible=False
    )

    #fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
    
    
    col1,col2,col3= st.columns([6,6,6])
    
   
    with col1:
        
        fig1=px.bar(Geo,x='Revenue',y='state',template='simple_white',text='Revenue',title='Revenue per States')
        fig1.update_traces(marker_color=px.colors.sequential.Blues[6])
        st.plotly_chart(fig1,use_container_width=True)
    
    with col2:
    
        fig2=px.bar(Geo,x='sold_pieces',y='state',template='simple_white',text='sold_pieces',title='Sold Pieces per States')
        fig2.update_traces(marker_color=px.colors.sequential.Blues[7])
        st.plotly_chart(fig2,use_container_width=True)
    with col3:

        fig3=px.bar(Geo,x='TotOrders',y='state',template='simple_white',text='TotOrders',title='Total Orders per States')
        fig3.update_traces(marker_color=px.colors.sequential.Blues[8])
        st.plotly_chart(fig3,use_container_width=True)

################################### Sales ##############################
with tab3:
    
    # Slicers 
    with st.container():
        col1,col2,col3 = st.columns([4,7,4])
        with col1:
            Sales_View= st.selectbox(" Please choose the view you want : " ,
                                     ['Monthly Trend','Weekly Trend','Daily Trend','Week Days'])
        with col3:
            prod=['Select All']
            prod_select=prod +list(df3['product_type'].unique())
            Product_select= st.selectbox("Product: ",prod_select )
    # loading dataframes         
    if Sales_View == 'Monthly Trend': 
        scope = 'month'
        product=Product_select
        if Product_select == 'Select All':
           
            dfx = df3.groupby('month').agg(Revenue=('total_price', 'sum'),
                                       sold_pieces=('sold_quantity', 'sum'),
                                       TotalOrders=('order_id', 'nunique')).reset_index().sort_values(by='month', ascending=True)
        
        else:
            
            dfx = df3[df3['product_type'] == Product_select].groupby('month').agg(Revenue=('total_price', 'sum'),
                                       sold_pieces=('sold_quantity', 'sum'),
                                       TotalOrders=('order_id', 'nunique')).reset_index().sort_values(by='month', ascending=True)
        
            
    elif Sales_View == 'Weekly Trend': 
        scope = 'week'
        product=Product_select
        if Product_select == 'Select All':
            dfx = df3.groupby('week').agg(Revenue=('total_price', 'sum'),
                                                sold_pieces=('sold_quantity', 'sum'),
                                                TotalOrders=('order_id', 'nunique')).reset_index().sort_values(by='week', ascending=True)
        else:
            dfx = df3[df3['product_type'] == Product_select].groupby('week').agg(Revenue=('total_price', 'sum'),
                                                sold_pieces=('sold_quantity', 'sum'),
                                                TotalOrders=('order_id', 'nunique')).reset_index().sort_values(by='week', ascending=True) 
            
            
            
            
    elif Sales_View == 'Daily Trend':
        scope = 'order_date'
        product=Product_select
        if Product_select == 'Select All':
            dfx = df3.groupby('order_date').agg(Revenue=('total_price', 'sum'),
                                                sold_pieces=('sold_quantity', 'sum'),
                                                TotalOrders=('order_id', 'nunique')).reset_index().sort_values(by='order_date', ascending=True)
        else:
            dfx = df3[df3['product_type'] == Product_select].groupby('order_date').agg(Revenue=('total_price', 'sum'),
                                                sold_pieces=('sold_quantity', 'sum'),
                                                TotalOrders=('order_id', 'nunique')).reset_index().sort_values(by='order_date', ascending=True)
        
            
    ## ##########################Trends
    average_revenue = int(dfx['Revenue'].mean())
    
    mean_revenue = dfx['Revenue'].mean()
    std_dev_revenue = dfx['Revenue'].std()
    ucl = mean_revenue + 3 * std_dev_revenue 
    lcl = mean_revenue - 3 * std_dev_revenue
    
    fig=px.line(dfx, x=scope , y='Revenue', template='simple_white' ,
                title = f'Sales Revenue {Sales_View} with average:  {average_revenue}', text='Revenue')
    
    fig.update_traces( marker=dict(size=10, symbol='circle', color='navy'), textposition='top center')
    fig.update_layout(title={ 'text': f'Sales Revenue {Sales_View} with average: {average_revenue}', 'x': 0.5, 
                         'xanchor': 'center', 'yanchor': 'top' },
                  title_font=dict(size=24, family='Arial, sans-serif', color='black'))
   
    fig.add_shape(type='line',x0=dfx[scope].min(), x1=dfx[scope].max(),y0=average_revenue, y1=average_revenue,
    line=dict(color='blue', width=4, dash='dash'),
    name='Average Revenue')
    #UCL & LCL
    fig.add_shape( type='line', x0=dfx[scope].min(),x1=dfx[scope].max(),
                  y0=ucl, y1=ucl,line=dict(color='Green', width=1, dash='dash'), name='UCL')
    fig.add_shape( type='line', x0=dfx[scope].min(), x1=dfx[scope].max(),
                  y0=lcl, y1=lcl, line=dict(color='Green', width=1, dash='dash'), name='LCL' )

    st.plotly_chart(fig, use_container_width=True)
    
    
    #Sales Trend Analysis 
    out_of_control= dfx[(dfx['Revenue']>ucl)| (dfx['Revenue']<lcl)]
    out_of_control_count=out_of_control.shape[0]
    #count Datapoint
    ponitsCount= dfx['Revenue'].shape[0]
    #below AVG
    belowAVG= dfx[dfx['Revenue']<average_revenue].shape[0]
    
    ####################### download#################
    
    csv = dfx.to_csv(index=False).encode()
    st.markdown(
        f"""
        <a href="data:text/csv;charset=utf-8,{csv.decode()}" download="Sales_data.csv">
            <button style="
                font-size: 16px;
                color: white;
                background: linear-gradient(to bottom, #003366 0%, #00509E  100%);
                border: 2px solid #003366 ;
                border-radius: 5px;
                padding: 10px 20px;
                cursor: pointer;
                text-shadow: 0px 1px 2px rgba(0,0,0,0.5);
                box-shadow: 0px 4px 6px rgba(0,0,0,0.2);
            ">
                Download data as CSV
            </button>
        </a>
        """,
        unsafe_allow_html=True)
        
        ############################ Descriptive ##############3
    with st.container():
        st.markdown(
            f"""
            <div style="border: 2px solid navy; padding: 10px; border-radius: 5px;">
                <p>1- <strong>{Sales_View}</strong> illustrates {ponitsCount} datapoints.</p>
                <p>2- We found in <strong>{Sales_View}</strong>: {out_of_control_count} datapoint{"s" if out_of_control_count > 1 else ""} out of control.</p>
                <p>3- We found in <strong>{Sales_View}</strong>: {belowAVG} datapoint{"s" if belowAVG > 1 else ""} below average.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    ###################################################3
    dfpro=df3.groupby(['product_type']).agg(Revenue=('total_price', 'sum'),
                                                sold_pieces=('sold_quantity', 'sum'),
                                                TotalOrders=('order_id', 'nunique')).reset_index().sort_values(by='product_type')
    
    dfpro2=df3.groupby(['product_type','product_name']).agg(Revenue=('total_price', 'sum'),
                                                sold_pieces=('sold_quantity', 'sum'),
                                                TotalOrders=('order_id', 'nunique')).reset_index().sort_values(by='product_type')
    
    

   
    st.write('')
    with st.container():
        col1,col2,col3,col4,col5= st.columns([4,4,4,4,4])
        with col1:        
            st.metric('Product Category', df3['product_type'].unique().shape[0])
        with col2:
            st.metric('Products', df3['product_name'].unique().shape[0])
        with col3:
            st.metric('AVG pieces per product', round(dfpro2['sold_pieces'].mean(),1))
        with col4:
            st.metric('Max pieces per product', round(dfpro2['sold_pieces'].max(),1))
        with col5:
            st.metric('Min pieces per product', round(dfpro2['sold_pieces'].min(),1))
    
    
    st.write('')
    with st.container():
        
        measure=st.selectbox("customize your measurements:", ['Revenue','sold_pieces','TotalOrders'])
        
        
       
    
        col1,col2,col3=st.columns([10,0.5,5])
        with col1:
            
            fig22 = px.bar(dfpro2, 
                                 x='product_type', 
                                 y=measure, 
                                 color='product_name',
                                 template='presentation',
                                 title=f" {measure} per Producs".title(),text=measure)
            st.plotly_chart(fig22, use_container_width=True)
        with col3:
            figx=px.pie(dfpro, names='product_type', values=measure,template='presentation',title='Products')
            st.plotly_chart(figx, use_container_width=True)
            
    
    fig = px.treemap(dfpro2, path= ['product_type','product_name'], color= measure ,
                     title=f' {measure} treamap for products'.title())
    st.plotly_chart(fig,use_container_width=True)

    
#######################################################################

with tab4:
    prod=['Select All']
    state_select=prod +list(df1['state'].unique())
    DeSel=st.selectbox('State',state_select)
    
    if DeSel == 'Select All':
        dfsd= df1
    else:
        dfsd= df1[df1['state']== DeSel]
            
    Deliver_AVG=round(dfsd['days_to_deliver'].mean(),2)
    Deliver_max=dfsd['days_to_deliver'].max()
    Deliver_min=dfsd['days_to_deliver'].min()
    Deliver_median=dfsd['days_to_deliver'].median()
    Deliver_stdev=round(dfsd['days_to_deliver'].std(),1)
    Deliver_Q1 = dfsd['days_to_deliver'].quantile(0.25)  # 25th percentile
    Deliver_Q3 = dfsd['days_to_deliver'].quantile(0.75)
    IQR = Deliver_Q3-Deliver_Q1
    UO=Deliver_median + (IQR*1.5)
    LO=Deliver_median - (IQR*1.5)
    
    dfsd['outlier']= np.where((dfsd['days_to_deliver'] > UO) | (dfsd['days_to_deliver'] < LO), 1, 0)
    outl= dfsd['outlier'].sum()
    
    if outl.sum() == 0:
        st.markdown( " We don't have any outliers")
    else:
        st.markdown(f" there are {outl} outlier datapoints ")

    with st.container():
        st.markdown( '<div style="border: 2px solid #000083; padding: 20px; color: gray; text-align: center; font-size: 24px; margin-bottom: 20px;"><h3>Delivery (days) Descriptive Statistics</h3></div>',
                    unsafe_allow_html=True )
        col1, col2, col3, col4, col5, col6, col7 = st.columns([4, 4, 4, 4, 4, 4, 4])
        with col1:
            st.markdown(
                f'<div style="border: 2px solid #000083; padding: 10px; color: gray; text-align: center;"><h5>Average</h5><h3>{Deliver_AVG}</h3></div>',
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f'<div style="border: 2px solid #000083; padding: 10px; color: gray; text-align: center;"><h5>Max</h5><h3>{Deliver_max}</h3></div>',
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                f'<div style="border: 2px solid #000083; padding: 10px; color: gray; text-align: center;"><h5>Min</h5><h3>{Deliver_min}</h3></div>',
                unsafe_allow_html=True
            )
        with col4:
            st.markdown(
                f'<div style="border: 2px solid #000083; padding: 10px; color: gray; text-align: center;"><h5>StDev</h5><h3>{Deliver_stdev}</h3></div>',
                unsafe_allow_html=True
            )
        with col5:
            st.markdown(
                f'<div style="border: 2px solid #000083; padding: 10px; color: gray; text-align: center;"><h5>Median</h5><h3>{Deliver_median}</h3></div>',
                unsafe_allow_html=True
            )
        with col6:
            st.markdown(
                f'<div style="border: 2px solid #000083; padding: 10px; color: gray; text-align: center;"><h5>Q1</h5><h3>{Deliver_Q1}</h3></div>',
                unsafe_allow_html=True
            )
        with col7:
            st.markdown(
                f'<div style="border: 2px solid #000083; padding: 10px; color: gray; text-align: center;"><h5>Q3</h5><h3>{Deliver_Q3}</h3></div>',
                unsafe_allow_html=True
            )

    
    
    
    fig= px.histogram(dfsd, x= 'days_to_deliver',template="simple_white", title='Time to deliver in hours'.title(),
                     marginal='box')
    st.plotly_chart(fig,use_container_width=True)
    
    dfdel=df1.groupby(['state']).agg(Delivey=('days_to_deliver', 'mean')).reset_index().sort_values(by='Delivey')
    dfdel['Delivey']=round(dfdel['Delivey'],1)
                                     
    figd= px.bar(dfdel,y= 'Delivey', x='state',template='presentation', text='Delivey')
    st.plotly_chart(figd,use_container_width=True)
