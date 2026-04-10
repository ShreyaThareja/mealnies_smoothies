import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title("🍹 Customize Your Smoothie!")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name input
name_on_order = st.text_input('Name on smoothie:')

# Snowflake session
session = get_active_session()

# Fetch fruits
df = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'))
fruit_list = [row['FRUIT_NAME'] for row in df.collect()]

# Select ingredients
ingredients_list = st.multiselect(
    'Choose ingredients:',
    fruit_list
)

# Submit button
if st.button('Submit Order'):

    if name_on_order and ingredients_list:

        # Convert list to string
        ingredients_string = " ".join(ingredients_list)

        # SQL insert
        my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
        """

        session.sql(my_insert_stmt).collect()

        st.success(f"Your Smoothie is ordered, {name_on_order}! 🍹", icon="✅")

    else:
        st.warning("Please enter name and select ingredients")
