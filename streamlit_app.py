import streamlit
import pandas as pd

streamlit.title("My Mom's New Healthy Diner")

streamlit.header("Breakfast Favourites")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")

streamlit.header("🍌🥭Build your own fruit smoothie🥝🍇")

# reading the csv file and creating a dataframe to use it in our app
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#We are going to create a multi select (picker Object) for the users to chose their choice of fruit for the smoothie - it'll be like a widget
#We need to change the index of the my_fruit_list dataframe to fruit column as they are unique and not null and thats what we are going to be seing in our widget

my_fruit_list.set_index('Fruit', inplace = True)

# After setting the index as fruit we are going to create the widget from multiselect and let the user pick the fruit, lets see how
#streamlit.multiselect(label = "Pick some fruits:", options = list(my_fruit_list.index), default=['Avocado','Strawberries'])

#Now we need to make the table shown there a bit dynamic, limiting the rows to show only the selected fields by the user

fruits_to_show = streamlit.multiselect(label = "Pick some fruits:", options = list(my_fruit_list.index), default=['Avocado','Strawberries'])

streamlit.dataframe(fruits_to_show)

