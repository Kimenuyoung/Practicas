import os
import sqlite3
import pandas as pd
import streamlit as st


def render_bar_section(title: str, data: pd.DataFrame, label_column: str, value_column: str) -> None:
	st.subheader(title)
	st.bar_chart(data.set_index(label_column)[value_column])
	st.dataframe(data, use_container_width=True, hide_index=True)


# Conectar a la base
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videogames.db")

with sqlite3.connect(db_path) as conn: 
	df = pd.read_sql("SELECT * FROM vgsales_clean", conn)
	top_publishers = pd.read_sql("SELECT * FROM top_publishers", conn)
	top_japan_games = pd.read_sql("SELECT * FROM japan_sales", conn)
	jp_genre_sales = pd.read_sql("SELECT * FROM jp_genre_sales", conn)
	eu_sales_name = pd.read_sql("SELECT * FROM eu_sales_name", conn)
	na_sales_name = pd.read_sql("SELECT * FROM na_sales_name", conn)
	eu_genre_sales = pd.read_sql("SELECT * FROM eu_sales", conn)
	na_genre_sales = pd.read_sql("SELECT * FROM na_sales", conn)

# Dashboard
st.title("Ventas de Videojuegos")

st.subheader("Ventas Globales por Género")
st.bar_chart(df.groupby("Genre")["Global_Sales"].sum())

st.subheader("Ventas Globales por Año")
st.bar_chart(df.groupby("Year")["Global_Sales"].sum())

render_bar_section("Top Publishers en Ventas Globales", top_publishers, "Publisher", "Global_Sales")
render_bar_section("Top Juegos Más Vendidos en Japón", top_japan_games, "Name", "JP_Sales")
render_bar_section("Ventas por Género en Japón", jp_genre_sales, "Genre", "JP_Sales")
render_bar_section("Top Juegos Más Vendidos en Europa", eu_sales_name, "Name", "EU_Sales")
render_bar_section("Top Juegos Más Vendidos en Norteamérica", na_sales_name, "Name", "NA_Sales")
render_bar_section("Ventas por Género en Europa", eu_genre_sales, "Genre", "EU_Sales")
render_bar_section("Ventas por Género en Norteamérica", na_genre_sales, "Genre", "NA_Sales")