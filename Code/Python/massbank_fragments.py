import os

gnps_massbank_respect_path = "G:\\Dev\\Data\\concatenated-Pos-GNPS-MassBank-Respect.msp.txt"
msp_fragments_path = "G:\\Dev\\Data\\GNPS-MassBank-Respect"

with open(gnps_massbank_respect_path, 'r') as f:
    content = f.readlines()

for index, line in enumerate(content):
    if line.startswith("NAME: "):
        compound_name = line[6:].split(";")[0]
        parent_mass_index = index + 1
        ionization_index = parent_mass_index + 1
        smiles_index = ionization_index + 5
        inchi_key_index = smiles_index + 2
        formula_index = inchi_key_index + 2
        mass_bank_accession_index = formula_index + 3
        links_index = mass_bank_accession_index + 1
        loop_index = links_index + 3

        if content[loop_index] != "\n":
            parent_mass = content[parent_mass_index][13:]
            ionization = content[ionization_index][15:]
            smiles = content[smiles_index][8:]
            inchi_key = content[inchi_key_index][10:]

            formula = content[formula_index][9:]
            mass_bank_accession = content[mass_bank_accession_index][19:]
            links = content[links_index][7:]
            filename = ""

            if mass_bank_accession != "\n":
                filename = mass_bank_accession
            elif links != "\n":
                filename = links
            else:
                filename = inchi_key

            print(filename[:-1])
            filepath = os.path.join(msp_fragments_path, filename[:-1] + ".ms")

            # >compound Kanamycin A M+H
            # >formula C18H36N4O11
            # >parentmass 485.0
            # >ionization [M + H]+
            # >InChI InChI=1S/C18H36N4O11/c19-2-6-10(25)12(27)13(28)18(30-6)33-16-5(21)1-4(20)15(14(16)29)32-17-11(26)8(22)9(24)7(3-23)31-17/h4-18,23-29H,1-3,19-22H2/t4-,5+,6-,7-,8+,9-,10-,11-,12+,13-,14-,15+,16-,17-,18-/m1/s1
            # >InChIKey N/A
            # >smiles O
            #
            # >ms2peaks
            with open(filepath, 'w') as f:
                if not compound_name.endswith("\n"):
                    compound_name += "\n"
                f.write(">compound " + compound_name)
                f.write(">formula " + formula)
                f.write(">parentmass " + parent_mass)
                f.write(">ionization " + ionization)
                f.write(">InChI N/A\n")
                f.write(">InChIKey " + inchi_key)
                f.write(">smiles " + smiles)
                f.write("\n")
                f.write(">ms2peaks\n")
                while content[loop_index] != "\n":
                    mass, intensity = content[loop_index].split()
                    f.write(mass + " " + intensity + "\n")
                    loop_index += 1
