import pandas as pd
# Create two sample DataFrames
# df1 = pd.DataFrame({'Name': ['Alice', 'Bob'], 'Age': [25, 30]})
# df2 = pd.DataFrame({'City': ['New York', 'Los Angeles'], 'Salary': [70000, 80000], 'Name': ["Akash"], "Age": [25]})

# # Combine using concat() along columns
# combined_df = pd.concat([df1, df2], axis=1, ignore_index=False)
# print(combined_df)


# Merging on a common column
df1 = pd.DataFrame({'Name': ['Alice', 'Bob', "nameee"], 'Age': [25, 30, 1212]})
df2 = pd.DataFrame({'Name': ["Akash"], 'Age': [26]})

merged_df = df1.merge(df2, on='Name', how="outer", suffixes=("_d1Xcopy", "_d2Ycopy"))
for column in merged_df.columns:
    if(column.endswith("_d1Xcopy")):
        x_column_name = f"{column.split('_')[0]}_d1Xcopy"
        y_column_name = f"{column.split('_')[0]}_d2Ycopy"
        merged_df[column.split("_")[0]] = merged_df[y_column_name].fillna(merged_df[x_column_name])
        merged_df.drop([x_column_name, y_column_name], axis=1, inplace=True)

print(merged_df)