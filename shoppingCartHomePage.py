


st.set_page_config(
    layout='wide', page_title='Shopping Cart', page_icon='🛒'
)

st.sidebar.success('Please select page above: ')

########################Loading data ###########################
df1 = pd.read_csv('Data/df1.csv')
df2 = pd.read_csv('Data/df2.csv')
df3 = pd.read_csv('Data/df3.csv')
inactive_customers = pd.read_csv('Data/inactive_customers.csv')
customers = pd.read_csv('Data/customers.csv')

################################################################


import datetime

# Add custom CSS to remove the unused space above the header


st.markdown("""
    <style>
        /* Page background - applying to the entire page */
        body {
            background-color: #f6f6f6 !important;
        }
        .stApp {
            background-color: #f6f6f6 !important; /* Targets the Streamlit app container */
        }

         /* Title styling */
        .title {
            background-color: #ffffff;  /* White background */
            color: #616f89;              /* Light gray text color */
            padding: 20px;
            text-align: center;
            font-size: 46px;
            font-weight: bold;
            border: 4px solid #000083; /* Navy blue border */
            border-radius: 10px;       /* Optional rounded corners */
            box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.2); /* Subtle shadow for the box */
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);  /* Shadow for the text */
        
        }

        /* Metric styling */
        .metric {
            background-color: white;
            border: 2px solid #000083;  /* Border color for metric boxes */
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 10px 15px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        /* Metric value font color and shadow */
        .metric p {
            color: #000083;
            font-size: 28px;
            font-style: italic;
            text-shadow: 1px 1px 2px #000083;
           
        }

        /* Metric title styling */
        .metric h3 {
            margin-bottom: 10px;
            font-size: 20px;
            font-weight: bold;
            color: #999999;
        
        }
    </style>
""", unsafe_allow_html=True)

# Title for the homepage
st.markdown('<div class="title">🛒 Shopping Cart Overview</div>', unsafe_allow_html=True)

st.write('')

# Create columns for layout
col1, col2, col3 = st.columns(3)

# Add metrics to each column
with col1:
    st.markdown(f'''
        <div class="metric">
            <h3>Total customer base</h3>
            <p>{len(customers)}</p>
        </div>
    ''', unsafe_allow_html=True)
    st.write(" ")
    st.markdown(f'''
        <div class="metric">
            <h3>Total inactive customers</h3>
            <p>{inactive_customers[inactive_customers['active']=='No'].shape[0]}</p>
        </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown(f'''
        <div class="metric">
            <h3>🛒Total Orders</h3>
            <p>{len(df1)}</p>
        </div>
    ''', unsafe_allow_html=True)
    
    st.write(" ")
    
    st.markdown(f'''
        <div class="metric">
            <h3>Sold Pieces</h3>
            <p>{df3['sold_quantity'].sum()}</p>
        </div>
    ''', unsafe_allow_html=True)

with col3:
    st.markdown(f'''
        <div class="metric">
            <h3>Total Revenue</h3>
            <p>{df3['total_price'].sum()}</p>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown(" ")
    state = df3.groupby('state')['total_price'].sum().reset_index().sort_values(by='total_price', ascending=False)

    state_MaxRev = state[['state']].head(1)
    highest_revenue_state = state_MaxRev.iloc[0]['state']

    st.markdown(f'''
        <div class="metric">
            <h3>Highest Revenue state</h3>
            <p>{highest_revenue_state}</p>
        </div>
    ''', unsafe_allow_html=True)
