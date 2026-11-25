
"""Snowflake Badge 3: smoothie ordering app for Streamlit Community Cloud."""

import streamlit as st
import requests
from snowflake.snowpark.functions import col

st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Connect to Snowflake
connection = st.connection("snowflake")
session = connection.session()

# Load available fruits from Snowflake
fruit_rows = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"))
    .sort(col("FRUIT_NAME"))
    .collect()
)

fruit_options = [row["FRUIT_NAME"] for row in fruit_rows]

# Allow users to select up to five fruits
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5,
)

if ingredients_list:
    ingredients_string = " ".join(ingredients_list) + " "

    # Retrieve nutrition information for each selected fruit
    for fruit_chosen in ingredients_list:
        st.subheader(f"{fruit_chosen} Nutrition Information")

        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + fruit_chosen
        )

        sf_df = st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )

    # Submit the smoothie order to Snowflake
    if st.button("Submit Order"):
        session.sql(
            "INSERT INTO SMOOTHIES.PUBLIC.ORDERS "
            "(INGREDIENTS, NAME_ON_ORDER) VALUES (?, ?)",
            params=[ingredients_string, name_on_order],
        ).collect()

        st.success(f"Your Smoothie is ordered, {name_on_order}!")
