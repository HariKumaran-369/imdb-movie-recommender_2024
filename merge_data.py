import pandas as pd

print("Files Loading...")

df_own = pd.read_csv("movies.csv")
df_june = pd.read_csv("imdb_june_2024.csv")
df_sep = pd.read_csv("imdb_sep_2024.csv")
df_nov = pd.read_csv("imdb_nov_dec_2024.csv")
df_guvi = pd.read_csv("imdb_movies_2024.csv")

print("🔍 Actual Columns:", df_guvi.columns.tolist())

print(f"Original Data: {len(df_own)} movies")
print(f"June 2024 Data: {len(df_june)} movies")
print(f"September 2024 Data: {len(df_sep)} movies")
print(f"nov dec 2024 Data: {len(df_nov)} movies")
print(f"guvi Data: {len(df_guvi)} movies")

df_own = df_own[["movie_name", "storyline"]]
df_june = df_june[["movie_name", "storyline"]]
df_sep = df_sep[["movie_name", "storyline"]]
df_nov = df_nov[["movie_name", "storyline"]]

df_guvi = df_guvi.rename(columns={"movie name": "movie_name"})
df_guvi = df_guvi[["movie_name", "storyline"]]

df_combined = pd.concat([df_guvi, df_own, df_june, df_sep, df_nov], ignore_index=True)
print(f"\n Combine: {len(df_combined)} movies")

df_combined = df_combined.dropna(subset=["movie_name", "storyline"])
df_combined = df_combined[df_combined["storyline"].str.len() > 50]
df_combined.drop_duplicates(subset=["movie_name"], inplace=True)
df_combined.reset_index(drop=True, inplace=True)

print(f" Cleaned data: {len(df_combined)} movies")


df_combined.to_csv("movies_final.csv", index=False, encoding="utf-8")
print("\n 'movies_final.csv' new file ")
print(df_combined.head())
