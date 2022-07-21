import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

def get_fruitvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice.strip())
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return(fruityvice_normalized)

streamlit.title("My Parents' New Healthy Diner")
streamlit.header("Breakfast Menu")
streamlit.text("Eggs and Avocados")
streamlit.text("Shakshuka")
streamlit.header('Breakfast Menu (Course)')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)
streamlit.header("Fruityvice Fruit Advice!")
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','')
  if not fruit_choice:
    streamlit.error("please select a fruit for info")
  else:
    fruityvice_normalized = get_fruitvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error(e)

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("INSERT INTO fruit_load_list values ('" + new_fruit + "')")
        return "Thanks for adding " + new_fruit
# if len(fruit_choice2) > 0:
#   my_cur.execute("INSERT INTO fruit_load_list values ('" + fruit_choice2 + "')")

try:
  fruit_choice2 = streamlit.text_input('What fruit would you like to add to list?','')
  if not fruit_choice2:
    streamlit.error("please select a fruit for info")
  else:
    streamlit.write('Adding fruit to list ', fruit_choice2)
    insert_row_snowflake(fruit_choice2.strip())
except URLError as e:
  streamlit.error(e)

if streamlit.button('Get Fruit Load List'):
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)
