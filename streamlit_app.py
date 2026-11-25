
"""Snowflake Badge 3: Smoothie Order Form."""

import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Connect to Snowflake
connection = st.connection("snowflake")
session = connection.session()

# Retrieve both the display name and API search name
my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"), col("SEARCH_ON"))
    .sort(col("FRUIT_NAME"))
)

# Convert Snowpark DataFrame to Pandas
pd_df = my_dataframe.to_pandas()

# Use friendly fruit names in the dropdown
fruit_options = pd_df["FRUIT_NAME"].tolist()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5,
)

if ingredients_list:
    ingredients_string = " ".join(ingredients_list) + " "

    for fruit_chosen in ingredients_list:

        # Find the API search value for the chosen fruit
        search_on = pd_df.loc[
            pd_df["FRUIT_NAME"] == fruit_chosen,
            "SEARCH_ON"
        ].iloc[0]

        # Temporary output to verify the lookup
        st.write(
            "The search value for",
            fruit_chosen,
            "is",
            search_on
        )

        st.subheader(f"{fruit_chosen} Nutrition Information")

        # API call will be updated in Finishing Touches
        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + fruit_chosen
        )

        st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )

    if st.button("Submit Order"):
        session.sql(
            "INSERT INTO SMOOTHIES.PUBLIC.ORDERS "
            "(INGREDIENTS, NAME_ON_ORDER) VALUES (?, ?)",
            params=[ingredients_string, name_on_order],
        ).collect()

        st.success(
            f"Your Smoothie is ordered, {name_on_order}!"
        )
