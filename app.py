import streamlit as st
import pandas as pd
import numpy as np

#title
st.title("My First Streamlit App")

#header
st.header("Welcome to my app")

#subheader
st.subheader("This is a subheader")

#text
st.text("This is a text")

#markdown
st.markdown("## This is a markdown header")

#succes message
st.success("This is a success message")

st.warning("This is a warning message")

st.error("YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGGGGGGGGGGGGGGGGGGHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH - L")

st.code("print('Hello, World!')", language="python")
st.json({"name": "John", "age": 30, "city": "New York"})
st.latex("$$x^2 + y^2 = z^2$$")
st.image("https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png")
st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
st.file_uploader("Upload a file", type=["jpg", "png", "pdf"])
st.text_input("Enter your name")
st.text_area("Enter your bio")
st.number_input("Enter your age")
st.date_input("Enter your birth date")
st.button("Click me")
st.download_button("Download file", "file.txt")
st.link_button("Click me", "https://www.google.com")

st.error("This is an error message")
st.success("This is a success message")
st.warning("This is a warning message", icon="🔔")
st.info("This is an info message", icon="ℹ️")



st.balloons()

#line chart
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(chart_data)

#bar chart]
bar_data = pd.DataFrame(chart_data)
st.bar_chart(bar_data)

#area chart
area_data = pd.DataFrame(chart_data)
st.area_chart(area_data)

#map (latitude, longitude
st.map(pd.DataFrame({
    "latitude": [13.7563, 13.7564, 13.7565],
    "longitude": [100.5018, 100.5019, 100.5020]
}))

#scatter plot
st.scatter_chart(pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [1, 2, 3, 4, 5]
}))

#box plot
st.box_chart(pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [1, 2, 3, 4, 5]
}))