import pandas as pd

unique_smiles_path = "G:\\Dev\\Data\\unique_smiles.tsv"
npa_atlas_smiles_path = "G:\\Dev\\Data\\NPAtlas_DB_last_version.tsv"
filtered_npatlas_smiles_path = "G:\\Dev\\Data\\NPAtlas_DB_last_version_filtered.tsv"
duplicate_mibig_npatlas_path = "G:\\Dev\\Data\\duplicate_npatlas_mibig.csv"

# df = pd.read_csv("smiles.tsv", sep="\t")
# df = df.drop_duplicates(subset=['SMILES'])
# df.to_csv(unique_smiles_path, sep='\t', index=False)

mibig_smiles_df = pd.read_csv(unique_smiles_path, sep="\t")
npatlas_smiles_df = pd.read_csv(npa_atlas_smiles_path, sep="\t")

duplicate_npatlas_df = npatlas_smiles_df[npatlas_smiles_df['SMILES'].isin(mibig_smiles_df['SMILES'])]

#print(duplicate_smiles['NPAID'])

data = []

for index, smiles in enumerate(duplicate_npatlas_df["SMILES"]):
    mibig_row = mibig_smiles_df.loc[mibig_smiles_df['SMILES'] == smiles]
    if mibig_row is not None:
        data.append((duplicate_npatlas_df.iloc[index]["NPAID"], mibig_row["MOLID"].item(), mibig_row["SMILES"].item()))

duplicate_smiles_df = pd.DataFrame(data, columns=['NPAID', 'MOLID', 'SMILES'])
duplicate_smiles_df.to_csv(duplicate_mibig_npatlas_path, sep=",", index=False)

# for index, row in duplicate_smiles.iterrows():
#     if row["SMILES"].isin(mibig_smiles_df['SMILES']):
#         count += 1
    #mibig_row = mibig_smiles_df.loc[mibig_smiles_df['SMILES'] == row["SMILES"]]
    #print(mibig_row["MOLID"])
    #data.append((row[]))
    #print(row)
npatlas_smiles_df = npatlas_smiles_df[~npatlas_smiles_df['SMILES'].isin(mibig_smiles_df['SMILES'])]
npatlas_smiles_df.drop_duplicates(subset=['SMILES'])

#npatlas_smiles_df.to_csv(filtered_npatlas_smiles_path, sep='\t', index=False)
