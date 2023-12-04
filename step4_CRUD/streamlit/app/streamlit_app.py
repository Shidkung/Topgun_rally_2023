# Import necessary libraries
from collections import namedtuple
import altair as alt
import pandas as pd
import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId
import plotly.express as px
import requests
from PIL import Image


# MongoDB connection
# Fetch data from MongoDB

# Custom CSS for styling
custom_css = """
<style>
body {
    background-color: black !important;
    color: white !important;
    font-family: 'Arial', sans-serif; /* Change the font if needed */
}

.sidebar {
    background-color: #333;
    padding: 20px;
}

.sidebar p {
    color: #5ba865;
    font-size: 25px;
    font-weight: bold;
    text-align: center;
}

.sidebar button {
    background-color: #5ba865;
    color: white;
    font-size: 16px;
    padding: 10px 15px;
    border-radius: 5px;
    cursor: pointer;
}

.sidebar button:hover {
    background-color: #4a7d4a;
}

.main-content {
    padding: 20px;
}

.chart-container {
    margin-top: 20px;
}

.footer {
    color: #8B4513;
    font-size: 45px;
    font-weight: bold;
    text-align: center;
    background-color: lightyellow;
}
</style>
"""

# Apply custom CSS to the entire app
st.markdown(custom_css, unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='color: #FFFFFF; text-shadow: 2px 2px black;font-size: 45px;font-weight: bold; margin-bottom:50px'>H2O TEAM</p>", unsafe_allow_html=True)


    

# Create the selectbox

nav_option = st.sidebar.selectbox(
    "Select a page.",
    ("Water Level data", "TS16 แม่น้ำมูล เมืองอุบลราชธานี (M.7)", "About Us")
)
st.sidebar.markdown(f"<p style='color:#FFFFFF;  font-size: 25px;font-weight: bold; margin-bottom:20px;'></p>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='color:#FFFFFF; text-shadow:2px 2px black; font-size: 25px;font-weight: bold; '>Get water data.</p>", unsafe_allow_html=True)

if st.sidebar.button("Get value!"):
    response = requests.get("http://192.168.1.59:80/mqtt")
    st.sidebar.write(f"Get it!")

image = Image.open('h2o.png')
st.sidebar.image(image)
# Display content based on the selected option

MONGO_DETAILS = "mongodb://tesarally:contestor@mongoDB:27017"
client = MongoClient(MONGO_DETAILS)
db2 = client["heightdata"]
waterdata = db2["height"]
db3 = client["QH3data"]
HS3 = db3["QH3"]
Hs3data = HS3.find()
HS3list = list(Hs3data)
Hs3d = HS3list[len(HS3list)-1]
Hs3d_height = Hs3d["height"]
Hs3d_discharge = Hs3d["discharge"]
Hs3d_Day = Hs3d["Day"]

if nav_option == "Water Level data":
    water = waterdata.find()
    waterlist = list(water)
    data = waterlist[len(waterlist)-1]
    data = data["height"]
    height_data = [entry["height"] for entry in waterlist]
    df = pd.DataFrame({"Timestamp": range(1, len(height_data) + 1), "Height": height_data})
    st.markdown(f"<p style='color:white; font-size: 25px;font-weight: bold; text-align:center; text-shadow: 2px 2px #6699ff;'>Water level from past to Now</p>", unsafe_allow_html=True)
    
    col1,col2,col3,col4,col5 = st.columns([12,12,12,12,12])
    with col1:
        data = waterlist[len(waterlist)-5]
        data = data["height"]
        st.markdown(f"<p style='color: #4d88ff; font-size: 24px;text-align:center;'>{data:.2f}</p>", unsafe_allow_html=True)
    with col2:
        data = waterlist[len(waterlist)-4]
        data = data["height"]
        st.markdown(f"<p style='color: #4d88ff; font-size: 25px;text-align:center;'>{data:.2f}</p>", unsafe_allow_html=True)
    with col3:
        data = waterlist[len(waterlist)-3]
        data = data["height"]
        st.markdown(f"<p style='color: #4d88ff; font-size: 26px;text-align:center;'>{data:.2f}</p>", unsafe_allow_html=True)
    with col4:
        data = waterlist[len(waterlist)-2]
        data = data["height"]
        st.markdown(f"<p style='color:#4d88ff; font-size: 27px;text-align:center;'>{data:.2f}</p>", unsafe_allow_html=True)
    with col5:
            
            data = waterlist[len(waterlist)-1]
            data = data["height"]
            st.markdown(f"<p style='color:#4d88ff; font-size: 28px;background-color: #e6eeff;  border-radius:30px; position: static;text-align:center; width:120px;'>{data:.2f}</p>", unsafe_allow_html=True)
            #st.write(data)
    df = pd.DataFrame({"Timestamp": range(1, len(height_data) + 1), "Height": height_data})
    coll,colsc = st.columns([10,10])
# Plot the line chart
    fig = px.line(df, x="Timestamp", y="Height", title="Water Level Over Time(line)", width=350, height=300)
    fig.update_traces(line=dict(color='blue'))
    fig.update_layout(
        xaxis_title="Timestamp",
        yaxis_title="Water Level",
        template="plotly_dark",  # You can change the template to match your desired style
        title_x=0.2,  # Set x to 0.5 for center alignment
    title_y=0.95,  # Set y to 0.95 for top alignment (adjust as needed)
        )
    with coll:
        # Display the plot in Streamlit
        st.plotly_chart(fig)

    fig = px.scatter(df, x="Timestamp", y="Height", title="Water Level Over Time(scatter)",width=350, height=300)
    fig.update_traces(marker=dict(color='red'))
    fig.update_layout(
        xaxis_title="Timestamp",
        yaxis_title="Water Level",
        template="plotly_dark",  # You can change the template to match your desired style
        title_x=0.2,  # Set x to 0.5 for center alignment
    title_y=0.95,  # Set y to 0.95 for top alignment (adjust as needed)
        )
    with colsc:
        st.plotly_chart(fig)
    fig = px.line(df, x="Timestamp", y="Height", title="Line and Scatter Plot",width=600, height=400)
    fig.add_scatter(x=df["Timestamp"], y=df["Height"], mode="markers", name="Scatter Points")
    fig.update_traces(line=dict(color='blue'))
    fig.update_traces(marker=dict(color='red'))
# Update layout
    fig.update_layout(
    xaxis_title="Timestamp",
    yaxis_title="Height",
    )

# Display the plot in Streamlit
    st.plotly_chart(fig)


    
    df = pd.DataFrame({"Timestamp": range(1, len(height_data) + 1), "Height": height_data})
    
    average_height = sum(height_data) / len(height_data)
    max_value = df["Height"].max()
    min_value = df["Height"].min()
    colors = {"Max": "red", "Min": "blue"}
    max_min_df = pd.DataFrame({"Value": [max_value, min_value], "Type": ["Max value", "Min value"]})

# Set the width and height of the bar chart
    width, height = 600, 400

# Plot bar chart for max and min values
    fig = px.bar(
    max_min_df,
    x="Type",
    y="Value",
    text="Value",
    color="Type",
    
    title="Maximum and Minimum Values Bar Chart",
    width=width,
    height=height,
)

# Update layout
    fig.update_layout(
    yaxis_title="Height",
    )
# Display the plot in Streamlit
    st.plotly_chart(fig)
    st.markdown(f"<p style='color: white; text-shadow:  2px 2px #6699ff;; font-size: 27px;font-weight: bold; position: static;text-align:center;'>Average of height&nbsp&nbsp : &nbsp &nbsp {average_height:.2f}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #6699ff; font-size: 45px;font-weight: bold; text-align:center;background-color: #e6eeff; border-radius: 25px;'>Water level Data </p>", unsafe_allow_html=True)
    df = pd.DataFrame({"Timestamp": range(1, len(height_data) + 1), "Height": height_data})
    st.table(df)
elif nav_option == "TS16 แม่น้ำมูล เมืองอุบลราชธานี (M.7)":
    HS3_data = [entry["height"] for entry in HS3list]
    HS3Day_data = [entry["Day"] for entry in HS3list]
    HS3dis_data = [entry["discharge"] for entry in HS3list]
    
    df = pd.DataFrame({"Day": HS3Day_data, "Height": HS3_data})
    st.title("Ubon Ratchathani")
   
    fig = px.line(df, x="Day", y="Height", title="Height  Plot", width=300, height=400)
    fig.update_traces(line=dict(color='red'))

# Update layout
    fig.update_layout(
    xaxis_title="Day",
    yaxis_title="Height",
    )
    col1,col2 = st.columns([1,1])
# Display the plot in Streamlit
    with col1 :
        st.plotly_chart(fig)
    df = pd.DataFrame({"Day": HS3Day_data, "Height":  HS3dis_data })
    fig = px.line(df, x="Day", y="Height", title=" discharge Plot", width=300, height=400)
    fig.update_traces(line=dict(color='black'))
    with col2:
        st.plotly_chart(fig)
    HS3_data = [entry["height"] for entry in HS3list]
    HS3Day_data = [entry["Day"] for entry in HS3list]
    HS3dis_data = [entry["discharge"] for entry in HS3list]

# Create a DataFrame

    df = pd.DataFrame({
    'Day': HS3Day_data,
    'Discharge': HS3dis_data,
    'Height': HS3_data
})

# Plotting with Plotly Express
    fig = px.line(df, x='Day', y=['Discharge', 'Height'],
              labels={'Day': 'Day', 'value': 'Value'},
              line_shape='linear', line_dash_sequence=['solid', 'dash'],
              color_discrete_sequence=['black', 'red'])  # Set line colors here

# Streamlit app title
    st.title("Graph integral")

# Display the plot in Streamlit
    st.plotly_chart(fig)
    st.table(HS3_data)

elif nav_option == "About Us":
    
    
    st.title("About Us")
    st.markdown(f"<p>We are H2O flow like a water, from KMITL , from ESLxHCRL</p>", unsafe_allow_html=True)

    image1 = Image.open('pic/Nin.jpg')
    st.image(image1)
    st.markdown(f"<p style='color:#282157;'>1.Bantita Wongwan (Role: Aiot)</p>", unsafe_allow_html=True)

    image2 = Image.open('pic/Palm.jpg')
    st.image(image2)
    st.markdown(f"<p style='color:#282157;'>2.Krisakorn boonpan (Role: Aiot)</p>", unsafe_allow_html=True)

    image3 = Image.open('pic/Dan.jpeg')
    st.image(image3)
    st.markdown(f"<p style='color:#282157;'>3.Daniel Reeyawong (Role: Data Computing)</p>", unsafe_allow_html=True)

    image4 = Image.open('pic/Kid.jpg')
    st.image(image4)
    st.markdown(f"<p style='color:#282157;'>4.Pitpibul Pongpotchanatam (Role: Server)</p>", unsafe_allow_html=True)

    image5 = Image.open('pic/Tonfah.jpg')
    st.image(image5)
    st.markdown(f"<p style='color:#282157;'>5.Wiroon Samphaothong (Role: Data Computing)</p>", unsafe_allow_html=True)