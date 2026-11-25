"""Snowflake Badge 3: smoothie ordering app for Streamlit Community Cloud."""


import streamlit as st
import requests
from snowflake.snowpark.functions import col


st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# For Streamlit Community Cloud, configure [connections.snowflake] in
# the app's private Secrets settings during Lesson 10.
connection = st.connection("snowflake")
session = connection.session()

# Streamlit's multiselect works reliably with a simple list of strings.
fruit_rows = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"))
    .sort(col("FRUIT_NAME"))
    .collect()
)
fruit_options = [row["FRUIT_NAME"] for row in fruit_rows]

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5,
)

if ingredients_list:
    ingredients_string = " ".join(ingredients_list) + " "

    if st.button("Submit Order"):
        # Safely bind customer input rather than concatenating raw SQL.
        session.sql(
            "INSERT INTO SMOOTHIES.PUBLIC.ORDERS "
            "(INGREDIENTS, NAME_ON_ORDER) VALUES (?, ?)",
            params=[ingredients_string, name_on_order],
        ).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!")


if ingredients_list:
    ingredients_string = " ".join(ingredients_list) + " "

    for fruit_chosen in ingredients_list:
        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/watermelon"
        )

        sf_df = st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )

    if st.button("Submit Order"):
        session.sql(
            "INSERT INTO SMOOTHIES.PUBLIC.ORDERS "
            "(INGREDIENTS, NAME_ON_ORDER) VALUES (?, ?)",
            params=[ingredients_string, name_on_order],
        ).collect()

        st.success(f"Your Smoothie is ordered, {name_on_order}!")


