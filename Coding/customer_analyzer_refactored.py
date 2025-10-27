"""
Customer Analyzer
-----------------
A simple Python project for simulating, analyzing, and visualizing customer data.

Features:
- Generates fake customer records (age, purchases, total spend)
- Calculates key metrics (average spend, top customers)
- Visualizes total spend and age-group spending
- Exports results and plots to organized folders

Dependencies:
- pandas
- matplotlib
- random (standard library)
- os (standard library)
"""

import pandas as pd
import random
import matplotlib.pyplot as plt
import os


# -------------------------
# DATA GENERATION FUNCTIONS
# -------------------------

def generate_customers(num_customers=20):
    """Generate a list of fake customers with random attributes."""
    customers = []
    for i in range(1, num_customers + 1):
        customer = {
            "CustomerID": i,
            "Name": f"Customer_{i}",
            "Age": random.randint(18, 65),
            "Total_Spend": round(random.uniform(100, 2000), 2),
            "Purchases": random.randint(1, 20)
        }
        customers.append(customer)
    return pd.DataFrame(customers)


# -------------------------
# ANALYSIS FUNCTIONS
# -------------------------

def analyze_customers(data):
    """Add derived metrics and perform simple aggregations."""
    data["Avg_Spend_Per_Purchase"] = data["Total_Spend"] / data["Purchases"]
    bins = [18, 25, 35, 50, 65]
    labels = ["18-25", "26-35", "36-50", "51-65"]
    data["Age_Group"] = pd.cut(data["Age"], bins=bins, labels=labels, right=True)
    top_customers = data.sort_values(by="Total_Spend", ascending=False).head(5)
    avg_spend_by_age = data.groupby("Age_Group")["Total_Spend"].mean().round(2)
    return data, top_customers, avg_spend_by_age


# -------------------------
# VISUALIZATION FUNCTIONS
# -------------------------

def create_plots(data, avg_spend_by_age, output_dir="outputs"):
    """Generate and save visualizations to the output directory."""
    os.makedirs(output_dir, exist_ok=True)

    # Total spend distribution
    plt.figure(figsize=(8, 4))
    plt.hist(data["Total_Spend"], bins=10, color='skyblue', edgecolor='black')
    plt.title("Distribution of Total Spend")
    plt.xlabel("Total Spend ($)")
    plt.ylabel("Number of Customers")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "spend_distribution.png"))
    plt.close()

    # Average spend by age group
    plt.figure(figsize=(6, 4))
    avg_spend_by_age.plot(kind="bar", color='lightgreen', edgecolor='black')
    plt.title("Average Total Spend by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Average Spend ($)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "avg_spend_by_age.png"))
    plt.close()


# -------------------------
# MAIN EXECUTION LOGIC
# -------------------------

def main():
    """Run the full customer analyzer pipeline."""
    print("🚀 Generating customer data...")
    data = generate_customers()
    data.to_csv("customers.csv", index=False)
    print("✅ Customer data saved to 'customers.csv'.")

    print("\n🔍 Analyzing customer data...")
    data, top_customers, avg_spend_by_age = analyze_customers(data)

    print("\n--- TOP 5 CUSTOMERS ---")
    print(top_customers[["CustomerID", "Name", "Total_Spend"]])

    print("\n--- AVERAGE SPEND BY AGE GROUP ---")
    print(avg_spend_by_age)

    print("\n📊 Creating visualizations...")
    create_plots(data, avg_spend_by_age)

    top_customers.to_csv(os.path.join("outputs", "top_customers.csv"), index=False)
    print("\n✅ All results exported to the 'outputs' folder!")


# -------------------------
# ENTRY POINT
# -------------------------
if __name__ == "__main__":
    main()