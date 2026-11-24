# Badge 3 - Smoothie Order Form

Streamlit Community Cloud version of the **Custom Smoothie Order Form** from
Snowflake's **Data Application Builders Workshop (DABW)**.

## Lesson 9 deliverables

- `streamlit_app.py` — customer order app, based on the existing Streamlit in Snowflake app
- `requirements.txt` — Python dependencies for Streamlit Community Cloud
- `.gitignore` — prevents committing local connection secrets

Instead of `get_active_session()`, this version uses
`st.connection("snowflake").session()` to connect from Streamlit Community Cloud.
It reads the `SMOOTHIES.PUBLIC.FRUIT_OPTIONS` table, limits selection to five
fruits, and inserts orders into `SMOOTHIES.PUBLIC.ORDERS`. It uses SQL bind
parameters rather than concatenating names directly into SQL.

## Next: Lesson 10

Configure the **Snowflake connection secrets privately** in Streamlit Community
Cloud and deploy the GitHub repository. The application will not run until
those credentials and the correct Snowflake privileges are configured.

**Do not commit** Snowflake passwords, tokens, private keys, or a
`.streamlit/secrets.toml` file to this public GitHub repository.
