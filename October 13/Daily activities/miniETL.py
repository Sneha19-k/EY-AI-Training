import pandas as pd

# Extract - Read CSV
df= pd.read_csv("students.csv")

# Transform - Clean and Calculate
df.dropna(inplace=True)   # remove missing rows
df["Marks"]= df["Marks"].astype(int)
df["Result"]=df["Marks"].apply(lambda x: "Pass" if x>=50 else "Fail")

# Load - Save transformed Data
df.to_csv("cleaned_students.csv", index=False)
print("Data Pipeline Completed. Cleaned Data saved to cleaned_students.csv")
