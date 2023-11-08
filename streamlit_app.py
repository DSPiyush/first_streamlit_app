import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

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

#NEW SECTION
streamlit.header('Fruityvice Fruit Advice!')

# fruit_choice = streamlit.text_input("For which fruit do you need help", 'Kiwi')
#streamlit.write("The user Entered", fruit_choice) # This is removed 
def get_fruityvice_data(this_fruit_choice):
    # Take your json response and normalize it , this is the same code we were using before
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
try:
  fruit_choice = streamlit.text_input("For which fruit do you need help") # changes from above to this
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    # to make it look like a table on your streamlit app, we have already used dataframe before lets use it again!
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.errot()


streamlit.stop()
# below code is for the connection from snowflake to streamlit, after we have made the changes in Streamlit app -> settings -> secrets 

# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
first_row = my_cur.execute('select * from fruit_load_list')
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains: ")
streamlit.dataframe(my_data_rows)



# adding a second text input box
add_my_fruit = streamlit.text_input(label = 'What Fruit would you like to add ?')
streamlit.write('Thanks for adding '+add_my_fruit)

my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")




















