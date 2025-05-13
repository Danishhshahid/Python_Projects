import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


# st.title("Large title on streamlit")
# st.header("this is a header")
# st.subheader("this is a subheader")
# st.text("this is a simple text")
# st.markdown("this is markdown bold text")

# name = "danish"
# age = 20
# st.write(f"hello {name}")
# st.write(f"age {age}")

# if st.button("click me"):
#     st.write("button clicked")

# checked = st.checkbox("check me")
# if checked:
#     st.write("checkbox is clicked")

# age = st.slider("select your age: ",0,70,25)
# st.write(f"your age is: {age}")

# name = st.text_input("enter your name",value="")
# st.write(f"hello {name}")

# st.title("wellcome here")

# name = st.text_input("enter your name: ")
# age = st.slider("select your age",0,100)

# if st.button("submit"):
#     st.write(f"hello {name}, your age is {age} years old")

# name = st.text_input("enter your name : ")
# age = st.slider("select your age : ",0,100,18)
# fvrt_color = st.text_input("enter your favourate color: ")
# if st.button("submit"):
#     st.write(f"your name is {name}, your age is {age} YO , your favourate color is {fvrt_color}")

# age = st.number_input("enter you age,", value=18)
# st.write("entered age: " , age)

# data = {
#     "name" : ["john","amna","peter","linda"],
#     "age" : [22,29,18,22],
#     "city" : ["new york","karachi","larkana","sukkur"]

# }
# df = pd.DataFrame(data)

# # st.dataframe(df)
# st.table(df)

# data = {
#     "name" : ["john","amna","peter","linda"],
#     "age" : [22,29,18,22,33],
#     "address" :
#       {
#           "address" : "miro khan chowk",
#         "city" : "new york"}

# }

# st.json(data)

# data = {
#     "name" : ["john","amna","peter","linda"],
#     "age" : [22,29,18,22],
#     "city" : ["new york","karachi","larkana","sukkur"],
#     "score": [80,22,92,99]

# }
# df = pd.DataFrame(data)

# city = st.selectbox("choose a city to filter",df["city"].unique())
# filtered_data = df[df["city"] == city]

# st.write(f"data for city: {city}")
# st.dataframe(filtered_data) 


# value_of_style = st.number_input("enter the minimum number to disply in yellow", value = 80)

# styled_df = df.style.applymap(lambda x : "background-color: yellow" if isinstance(x,int) and x >= value_of_style else "background-color: red" )

# st.dataframe(styled_df)

# data = pd.DataFrame(
#     np.random.randn(250,6),
#     columns = ["A","B","C","E","F","G"]
# )
# st.bar_chart(data)

# data = pd.DataFrame({
#     "fruit": ["apples","bananas","cherry"],
#     "amount" : [10,20,30]
# })

# fig = px.bar(data,x= "fruit", y = "amount", title="fruit sales")

# st.plotly_chart(fig)

# data = pd.DataFrame(
#     np.random.randn(100,3),
#     columns=["A","B","C",]
# )

# plt.figure(figsize=(10,6))
# sns.scatterplot(x = data["A"],y = data["B"])
# plt.title("Scatter a to b")

# st.pyplot(plt)

# col1,col2,col3 = st.columns(3)

# with col1:
#     st.header("column1")
#     st.write("this is first colomun")
#     st.button("Button 1")
# with col2:
#     st.header("column2")
#     st.write("this is second colomun")
#     st.button("Button 2")
# with col3:
#     st.header("column2")
#     st.write("this is second colomun")
#     st.button("Button 3")

# with st.expander("see more details"):
#     st.write("here are some additional details")
#     st.line_chart([0,80,44,70,99,2,32])

# st.sidebar.title("hello there its navigation")

# option = st.sidebar.selectbox("choose a page : ", ["Home","about","contact"])

# if option == "Home":
#     st.write("this is wellcome page for home")

# elif option == "about":
#     st.write("this is wellcome page for about")

# elif option == "contact":
#     st.write("this is wellcome page for home")


# st.set_page_config(page_title="themed app",layout="wide",initial_sidebar_state="expanded")

# st.title("themed streamlit app")
# st.write("hello its custom themed")