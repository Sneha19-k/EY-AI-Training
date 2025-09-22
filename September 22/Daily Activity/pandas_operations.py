import numpy as np
import pandas as pd

data = {
    "Name": ["Rahul", "Priya", "Arjun", "Neha", "Vikram"],
    "Age": [21, 22, 20, 23, 21],
    "Course": ["AI", "ML", "Data Science", "AI", "ML"],
    "Marks": [85, 90, 78, 88, 95]
}
df = pd.DataFrame(data)
# print(df)

#selecting data
# print(df["Name"])          #single columns
# print(df[["Name","Age"]])  #multiple columns
# print(df.iloc[0])          #first row navigation
# print(df.loc[2,"Marks"])  #column navigation, value at row 2

#filter data

high_scorers= df[df["Marks"] > 80]    #students with marks greater than 80
# print(high_scorers)


#add pass/fail column
df["Result"]= np.where(df["Marks"] > 80, "Pass", "Fail")
#update Neha's marks
df.loc[df["Name"]== "Neha", "Marks"] =92
print(df)