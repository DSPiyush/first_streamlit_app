import streamlit
import pandas as pd
import requests

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

streamlit.dataframe(my_fruit_list.loc[fruits_to_show])


streamlit.header('Fruityvice Fruit Advice!')

fruit_choice = streamlit.text_input(label  = "For which fruit do you need help", placeholder = 'Kiwi')
streamlit.write("The user Entered", fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
# streamlit.text(fruityvice_response) #check the response status code
# streamlit.text(fruityvice_response.json()) # if the above is 200 - the json format is visible for the url we have in get, THIS WILL JUST SHOW THE TEXT AS IT ISON SCREEN

# Take your json response and normalize it 
try:
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
catch requests.exceptions.JSONDecodeError:
  print("You have not entered any value yet")


# to make it look like a table on your streamlit app, we have already used dataframe before lets use it again!

streamlit.dataframe(fruityvice_normalized)

# AS OF NOW everything is shown here in the app - the response status code - the json raw text - the tabular json format(normalized) we will keep only table

# Now lets make the api call dynamic and let the user decide for which 1 fruit he needs advice and we can take his input from the text input!





























