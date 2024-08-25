import requests
import streamlit as st

from gridiot.schemas import translate_to_quickwit
from query import generate_query


st.header("Player search")
query = st.text_input("Enter your query here")

if st.button("Query"):
    response = generate_query(query)
    qw_query = translate_to_quickwit(response)

    response = requests.get(
        "http://127.0.0.1:7280/api/v1/players/search", params={"query": qw_query}
    )
    response.raise_for_status()

    st.dataframe(response.json()["hits"])
