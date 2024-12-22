import json
import pandas as pd

# Input and output files
input_file = "arxiv-metadata-oai-snapshot.json"
output_file = "arxiv_data.psv"

# Prepare an empty list to store processed rows
rows = []

# Open the JSON file and process each line
with open(input_file, "r", encoding="utf-8") as file:
    for line in file:
        # Parse the JSON line
        data = json.loads(line)
        
        # Extract relevant fields and format them
        row = {
            "ID": data.get("id", ""),
            "Submitter": data.get("submitter", ""),
            "Authors": data.get("authors", ""),
            "Title": data.get("title", "").replace("\n", " "),  # Remove newlines
            "Comments": data.get("comments", ""),
            "Journal Reference": data.get("journal-ref", ""),
            "DOI": data.get("doi", ""),
            "Report No": data.get("report-no", ""),
            "Categories": data.get("categories", ""),
            "Abstract": data.get("abstract", "").replace("\n", " "),  # Remove newlines
            "Update Date": data.get("update_date", ""),
            "Authors Parsed": "; ".join([f"{x[1]} {x[0]}" for x in data.get("authors_parsed", [])]),
            "Versions": "; ".join([f"{v['version']} ({v['created']})" for v in data.get("versions", [])])
        }
        
        # Append the row to the list
        rows.append(row)

# Convert the list of rows into a DataFrame
df = pd.DataFrame(rows)

# Save the DataFrame to a PSV file
df.to_csv(output_file, sep="|", index=False)

print(f"PSV file has been created: {output_file}")
