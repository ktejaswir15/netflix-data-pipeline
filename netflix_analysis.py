import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# =====================
# EXTRACT
# =====================
def extract():
    print("Loading Netflix dataset...")
    df = pd.read_csv("netflix_titles.csv")
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

# =====================
# TRANSFORM
# =====================
def transform(df):
    print("Cleaning and transforming data...")

    # Drop rows where important columns are missing
    df = df.dropna(subset=["title", "type", "country", "release_year", "rating"])

    # Clean whitespace
    df["title"] = df["title"].str.strip()
    df["country"] = df["country"].str.strip()
    df["listed_in"] = df["listed_in"].str.strip()

    # Convert date_added to datetime
    df["date_added"] = pd.to_datetime(df["date_added"].str.strip(), errors="coerce")
    df["year_added"] = df["date_added"].dt.year

    print(f"After cleaning: {df.shape[0]} rows remaining")
    return df

# =====================
# ANALYZE
# =====================
def analyze(df):
    print("\n===== NETFLIX DATA ANALYSIS =====")

    # 1. Movies vs TV Shows
    type_counts = df["type"].value_counts()
    print(f"\nContent Type:\n{type_counts}")

    # 2. Top 10 countries producing content
    top_countries = df["country"].value_counts().head(10)
    print(f"\nTop 10 Countries:\n{top_countries}")

    # 3. Most common ratings
    ratings = df["rating"].value_counts().head(8)
    print(f"\nTop Ratings:\n{ratings}")

    # 4. Content added per year
    yearly = df["year_added"].value_counts().sort_index()
    print(f"\nContent Added Per Year:\n{yearly}")

    return type_counts, top_countries, ratings, yearly

# =====================
# VISUALIZE
# =====================
def visualize(df, type_counts, top_countries, ratings, yearly):
    print("\nCreating visualizations...")
    sns.set_style("darkgrid")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Netflix Data Analysis Dashboard", fontsize=18, fontweight="bold")

    # Chart 1 - Movies vs TV Shows
    axes[0, 0].pie(type_counts, labels=type_counts.index, autopct="%1.1f%%",
                   colors=["#E50914", "#221F1F"], startangle=90)
    axes[0, 0].set_title("Movies vs TV Shows", fontsize=13)

    # Chart 2 - Top 10 Countries
    sns.barplot(x=top_countries.values, y=top_countries.index, ax=axes[0, 1], palette="Reds_r")
    axes[0, 1].set_title("Top 10 Countries by Content", fontsize=13)
    axes[0, 1].set_xlabel("Number of Titles")

    # Chart 3 - Content Ratings
    sns.barplot(x=ratings.index, y=ratings.values, ax=axes[1, 0], palette="Reds_r")
    axes[1, 0].set_title("Most Common Content Ratings", fontsize=13)
    axes[1, 0].set_ylabel("Count")

    # Chart 4 - Content Added Per Year
    axes[1, 1].plot(yearly.index, yearly.values, color="#E50914", linewidth=2.5, marker="o")
    axes[1, 1].set_title("Content Added to Netflix Per Year", fontsize=13)
    axes[1, 1].set_xlabel("Year")
    axes[1, 1].set_ylabel("Number of Titles")

    plt.tight_layout()
    plt.savefig("netflix_dashboard.png", dpi=150)
    print("Dashboard saved as netflix_dashboard.png")
    plt.show()

# =====================
# LOAD
# =====================
def load(df):
    df.to_csv("netflix_cleaned.csv", index=False)
    print("Cleaned data saved to netflix_cleaned.csv")

# =====================
# RUN PIPELINE
# =====================
if __name__ == "__main__":
    raw = extract()
    cleaned = transform(raw)
    type_counts, top_countries, ratings, yearly = analyze(cleaned)
    visualize(cleaned, type_counts, top_countries, ratings, yearly)
    load(cleaned)
    print("\n🎉 Netflix Pipeline Complete!")