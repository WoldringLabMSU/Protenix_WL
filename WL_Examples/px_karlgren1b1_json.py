import pandas as pd
import json
import os
import re

# CONFIGURATION
excel_file = "karlgren_ligands.csv"   # Name of your excel file
output_folder = "karlgren_JSON_batch" # Where to save the JSONs
protein_sequence = "MDQNQHLNKTAEAQPSENKKTRYCNGLKMFLAALSLSFIAKTLGAIIMKSSIIHIERRFEISSSLVGFIDGSFEIGNLLVIVFVSYFGSKLHRPKLIGIGCFIMGIGGVLTALPHFFMGYYRYSKETNINSSENSTSTLSTCLINQILSLNRASPEIVGKGCLKESGSYMWIYVFMGNMLRGIGETPIVPLGLSYIDDFAKEGHSSLYLGILNAIAMIGPIIGFTLGSLFSKMYVDIGYVDLSTIRITPTDSRWVGAWWLNFLVSGLFSIISSIPFFFLPQTPNKPQKERKASLSLHVLETNDEKDQTANLTNQGKNITKNVTGFFQSFKSILTNPLYVMFVLLTLLQVSSYIGAFTYVFKYVEQQYGQPSSKANILLGVITIPIFASGMFLGGYIIKKFKLNTVGIAKFSCFTAVMSLSFYLLYFFILCENKSVAGLTMTYDGNNPVTSHRDVPLSYCNSDCNCDESQWEPVCGNNGITYISPCLAGCKSSSGNKKPIVFYNCSCLEVTGLQNRNYSAHLGECPRDDACTRKFYFFVAIQVLNLFFSALGGTSHVMLIVKIVQPELKSLALGFHSMVIRALGGILAPIYFGALIDTTCIKWSTNNCGTRGSCRTYNSTSFSRVYLGLSSMLRVSSLVLYIILIYAMKKKYQEKDINASENGSVMDEANLESLNKNKHFVPSAGADSETHC"

# CREATE OUTPUT FOLDER
os.makedirs(output_folder, exist_ok=True)

# READ EXCEL
df = pd.read_csv(excel_file, encoding='cp1252')

# GENERATE FILES
for index, row in df.iterrows():
    drug_name = re.sub(r'[^A-Za-z0-9_]', '', str(row['pdb_id']).replace(" ", "_"))#clear special characters
    smiles = row['smiles']

    data = [
      {
        "name": f"px_oatp1b1_{drug_name}",
        "dialect": "alphafold3",
        "sequences": [
          {
            "proteinChain": {
              "id": ["A"],
              "sequence": protein_sequence,
              "count": 1
            }
          },
          {
            "ligand": {
              "id": ["B"],
              "ligand": smiles,
              "name": drug_name,
              "count": 1
            }
          }
        ]
      }
    ]

    # Save as separate files: drug_0.json, drug_1.json, etc.
    filename = f"{output_folder}/drug_{index}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

print(f"Done! Generated {len(df)} JSON files in '{output_folder}'")