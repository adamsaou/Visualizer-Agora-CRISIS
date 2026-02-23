import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter


# Load data from the excel ile
FILE_PATH = "global_geopolitical_migration.xlsx"
df = pd.read_excel(FILE_PATH)

# data cleaning or helpers
def parse_percent(val):
    if isinstance(val, str):
        val = val.replace("%", "").strip()
        if "–" in val:
            return float(val.split("–")[0])
        if "<" in val:
            return float(val.replace("<", ""))
        if val.lower() in ["low", "very low", "net inflow"]:
            return 0.0
    try:
        return float(val)
    except:
        return 0.0

df["Risk"] = df["% Population at Risk"].apply(parse_percent)
df["Emigrate"] = df["% Emigrating"].apply(parse_percent)

#graphs
def graph_population_risk():
    plt.figure(figsize=(12,6))
    plt.bar(df["Country"], df["Risk"])
    plt.xticks(rotation=90)
    plt.ylabel("% Population at Risk")
    plt.title("Population at Risk by Country")
    plt.tight_layout()
    plt.show()

def graph_emigration():
    plt.figure(figsize=(12,6))
    plt.bar(df["Country"], df["Emigrate"])
    plt.xticks(rotation=90)
    plt.ylabel("% Emigrating")
    plt.title("Emigration Pressure by Country")
    plt.tight_layout()
    plt.show()

def graph_migration_destinations():
    destinations = []
    for val in df["Main Immigration Destinations"]:
        if isinstance(val, str) and "Receiver" not in val:
            destinations.extend([x.strip() for x in val.split(",")])

    counts = Counter(destinations)

    plt.figure(figsize=(10,5))
    plt.bar(counts.keys(), counts.values())
    plt.xticks(rotation=45)
    plt.ylabel("Number of Incoming Flows")
    plt.title("Most Common Migration Destinations")
    plt.tight_layout()
    plt.show()

def graph_blocs():
    bloc_counts = df["Bloc Alignment"].value_counts()
    plt.figure(figsize=(6,6))
    plt.pie(bloc_counts, labels=bloc_counts.index, autopct="%1.1f%%")
    plt.title("Bloc Alignment Distribution")
    plt.show()

def graph_priorities():
    priority_counts = df["Strategic Priority"].value_counts()
    plt.figure(figsize=(10,5))
    plt.bar(priority_counts.index, priority_counts.values)
    plt.xticks(rotation=45)
    plt.ylabel("Number of Countries")
    plt.title("Strategic Priorities")
    plt.tight_layout()
    plt.show()

def graph_risk_vs_emigration():
    plt.figure(figsize=(8,6))
    plt.scatter(df["Risk"], df["Emigrate"])

    for i, country in enumerate(df["Country"]):
        plt.text(df["Risk"][i]+0.5, df["Emigrate"][i]+0.5, country, fontsize=8)

    plt.xlabel("% Population at Risk")
    plt.ylabel("% Emigrating")
    plt.title("Risk vs Emigration Pressure")
    plt.grid(True)
    plt.show()

def graph_allies_network():
    G = nx.Graph()

    for _, row in df.iterrows():
        country = row["Country"]
        allies = row["Potential Allies (PPS-Focused)"]

        if isinstance(allies, str):
            for ally in allies.split(","):
                G.add_edge(country, ally.strip())

    plt.figure(figsize=(12,10))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=900, font_size=8)
    plt.title("Potential Allies Network")
    plt.show()

#Menu
while True:
    print("""
Choose a visualization:
1 - Population at Risk
2 - Emigration Pressure
3 - Migration Destinations
4 - Bloc Alignment
5 - Strategic Priorities
6 - Risk vs Emigration
7 - Allies Network
0 - Exit
""")

    choice = input("Your choice: ").strip()

    if choice == "1":
        graph_population_risk()
    elif choice == "2":
        graph_emigration()
    elif choice == "3":
        graph_migration_destinations()
    elif choice == "4":
        graph_blocs()
    elif choice == "5":
        graph_priorities()
    elif choice == "6":
        graph_risk_vs_emigration()
    elif choice == "7":
        graph_allies_network()
    elif choice == "0":
        print("Exiting.")
        break
    else:
        print("Invalid choice, try again.")
