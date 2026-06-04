import sqlite3
import pandas as pd

# ── Carga y limpieza ──────────────────────────────────────────────────────────
df = pd.read_csv('vgsales.csv')
print(df.head())

df = df.drop_duplicates()

# Year: float con nulos → convertir a int (0 = desconocido)
df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)

# Publisher: rellenar nulos con "Unknown"
df['Publisher'] = df['Publisher'].fillna("Unknown")

# Columnas numéricas: nulos a 0
for col in ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

print(f"Filas cargadas: {len(df)}")

# ── Análisis globales ─────────────────────────────────────────────────────────
# Ventas globales por género
sales_by_genre = df.groupby("Genre")["Global_Sales"].sum().reset_index()
print("\nVENTAS GLOBALES POR GÉNERO:")
print(sales_by_genre)

# TOP 10 editores por ventas globales
top_publishers = (df[df["Publisher"] != "Unknown"]
                  .groupby("Publisher")["Global_Sales"]
                  .sum().nlargest(10).reset_index())
print("\nTOP 10 EDITORES POR VENTAS GLOBALES:")
print(top_publishers)

# ── Japón ─────────────────────────────────────────────────────────────────────
japan_sales = df.groupby("Name")["JP_Sales"].sum().nlargest(10).reset_index()
print("\nTOP 10 JUEGOS MÁS VENDIDOS EN JAPÓN:")
print(japan_sales)

japan_sales_genre = df.groupby("Genre")["JP_Sales"].sum().nlargest(10).reset_index()
print("\nTOP 10 GÉNEROS MÁS VENDIDOS EN JAPÓN:")
print(japan_sales_genre)

# ── América del Norte ────────────────────────────────────────────────────────
north_america_sales = df.groupby("Name")["NA_Sales"].sum().nlargest(10).reset_index()
print("\nTOP 10 JUEGOS MÁS VENDIDOS EN AMÉRICA DEL NORTE:")
print(north_america_sales)

north_america_sales_genre = df.groupby("Genre")["NA_Sales"].sum().nlargest(10).reset_index()
print("\nTOP 10 GÉNEROS MÁS VENDIDOS EN AMÉRICA DEL NORTE:")
print(north_america_sales_genre)

# ── Europa ───────────────────────────────────────────────────────────────────
european_union_sales = df.groupby("Name")["EU_Sales"].sum().nlargest(10).reset_index()
print("\nTOP 10 JUEGOS MÁS VENDIDOS EN EUROPA:")
print(european_union_sales)

european_union_sales_genre = df.groupby("Genre")["EU_Sales"].sum().nlargest(10).reset_index()
print("\nTOP 10 GÉNEROS MÁS VENDIDOS EN EUROPA:")
print(european_union_sales_genre)

# ── Nuevas tablas ─────────────────────────────────────────────────────────────
# Juegos menos vendidos (nombre + plataforma), excluye ventas = 0
worst_games_platform = (df[df["Global_Sales"] > 0]
                        .groupby(["Name", "Platform"])["Global_Sales"]
                        .sum().nsmallest(10).reset_index())
print("\nJUEGOS MENOS VENDIDOS (NOMBRE Y PLATAFORMA):")
print(worst_games_platform)

# Plataformas con menos ventas globales
worst_by_platform = (df.groupby("Platform")["Global_Sales"]
                     .sum().nsmallest(10).reset_index())
print("\nPEORES PLATAFORMAS POR VENTAS GLOBALES:")
print(worst_by_platform)

# Top 10 juegos más vendidos por nombre y género
top_games_genre = (df.groupby(["Name", "Genre"])["Global_Sales"]
                   .sum().nlargest(10).reset_index())
print("\nJUEGOS MÁS VENDIDOS POR NOMBRE Y GÉNERO:")
print(top_games_genre)

# Peores 10 publicadores en ventas de Japón (excluye Unknown)
worst_publishers = (df[df["Publisher"] != "Unknown"]
                    .groupby("Publisher")["JP_Sales"]
                    .sum().nsmallest(10).reset_index())
print("\nPEORES 10 PUBLICADORES EN VENTAS JAPÓN:")
print(worst_publishers)

# ── Guardar en SQLite ─────────────────────────────────────────────────────────
conn = sqlite3.connect("videogames.db")

df.to_sql("vgsales_clean",              conn, if_exists="replace", index=False)
sales_by_genre.to_sql("sales_by_genre", conn, if_exists="replace", index=False)
top_publishers.to_sql("top_publishers", conn, if_exists="replace", index=False)
japan_sales.to_sql("japan_sales",       conn, if_exists="replace", index=False)
japan_sales_genre.to_sql("jp_genre_sales",          conn, if_exists="replace", index=False)
north_america_sales.to_sql("na_sales_name",         conn, if_exists="replace", index=False)
north_america_sales_genre.to_sql("na_sales",        conn, if_exists="replace", index=False)
european_union_sales.to_sql("eu_sales_name",        conn, if_exists="replace", index=False)
european_union_sales_genre.to_sql("eu_sales",       conn, if_exists="replace", index=False)
worst_games_platform.to_sql("worst_games_platform", conn, if_exists="replace", index=False)
worst_by_platform.to_sql("worst_by_platform",       conn, if_exists="replace", index=False)
top_games_genre.to_sql("top_games_genre",           conn, if_exists="replace", index=False)
worst_publishers.to_sql("worst_publishers",         conn, if_exists="replace", index=False)

conn.close()
print("\nDatos cargados en la base de datos.")
