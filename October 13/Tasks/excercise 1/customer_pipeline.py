import pandas as pd
from datetime import datetime

def run_pipeline():
# Extract data
    df = pd.read_csv("customers.csv")

# Transform
    # Filter out customers younger than 20
    df = df[df["Age"] >= 20]

    # Add AgeGroup column
    def get_age_group(age):
        if age < 30:
            return "Young"
        elif age < 50:
            return "Adult"
        else:
            return "Senior"

    df["AgeGroup"] = df["Age"].apply(get_age_group)

# Load transformed data
    df.to_csv("filtered_customers.csv", index=False)

    # Step 4: Print execution time
    print(f"Pipeline executed at {datetime.now()}")

if __name__ == "__main__":
    run_pipeline()
