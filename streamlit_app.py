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


#NEW SECTION
streamlit.header("🍌🥭Build your own fruit smoothie🥝🍇")
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list.set_index('Fruit', inplace = True)
fruits_to_show = streamlit.multiselect(label = "Pick some fruits:", options = list(my_fruit_list.index), default=['Avocado','Strawberries'])
streamlit.dataframe(my_fruit_list.loc[fruits_to_show])

#NEW SECTION
streamlit.header('Fruityvice Fruit Advice!')

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
  streamlit.error()


#NEW SECTION
streamlit.header("The fruit load list contains: ")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute('select * from fruit_load_list')
        return my_cur.fetchall()


if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)


add_my_fruit = streamlit.text_input(label = 'What Fruit would you like to add ?')
streamlit.write('Thanks for adding '+add_my_fruit)

my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")


def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")
        return "Thanks for adding" + new_fruit 
        
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)

















