import pandas as pd

df = pd.read_excel('Project List.xlsx',sheet_name='Project List') # Load Sheet 1
logic_cols = ['Year Started', 'Last Active','Department', 'Completed?','Designed For?']

# print(df.columns.values)

counts = df.groupby(logic_cols).size().reset_index(name='count')
overlaps = counts[counts['count'] > 1]

if overlaps.empty:
    print("No overlaps found!")
else:
    print("Found overlaps! These combinations have multiple projects:")
    print(overlaps.to_string(index=False))
    
    print("\n--- Detailed list of projects involved in overlaps ---")
    collision_details = df[df.set_index(logic_cols).index.isin(overlaps.set_index(logic_cols).index)]
    print(collision_details[logic_cols + ['Project Name (Long)']].sort_values(by=logic_cols).to_string(index=False))