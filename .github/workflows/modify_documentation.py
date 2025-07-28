import yaml
import sys, os
import re
import pathlib

def load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            patch_data = yaml.safe_load(file)
        print("YAML Version Data loaded successfully.\n\n")
        return patch_data
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found.\n\n")
        sys.exit(1)
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML file: {exc}\n\n")
        sys.exit(1)

def load_md(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
        print("Markdown file loaded successfully.\n\n")
        return content
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found.\n\n")
        sys.exit(1)

def save_md(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
    print("Markdown file saved successfully.\n\n")

# def gi_software_compile_docs(gi_software, overrides, documentation):
#     for each_patch in gi_software:
#         version = each_patch['version']
#         file_names = []
#         for file in each_patch['files']:
#             file_names.append(file['name'])
#             file_names.append(file['alt_name'])
        
#         if overrides['category'] != "":
#             category = overrides['category']
#         else:
#             category = "Base - eDelivery or OTN"
        
#         if overrides['software_piece'] != "":
#             software_piece = overrides['software_piece']
#         else:
#             software_piece = "Oracle Database {0} for Linux x86-64".format(version)
        
#         if overrides['file_name'] != "":
#             files = overrides['file_name']
#         else:
#             files = "{0} or {1}".format(file_names[0], file_names[1])

#         table_row = """<tr>\n<td>{oracle_release}</td>\n<td>{category}</td>\n<td>{software_piece}</td>\n<td>{files}</td>\n</tr>\n""". format(
#             oracle_release=version,
#             category=category,
#             software_piece=software_piece,
#             files=files
#         )
#         table_found = False
#         section_found = False
#         for line in documentation:
#             if table_found and section_found:
#                 if line.strip() == "<tbody>":
#                     documentation.insert(documentation.index(line) + 1, table_row)
#                     print("Added patch information to the documentation.\n\n")
#                     break
#             if line.strip() == "#### Required Oracle Software - Download Summary":
#                 section_found = True
#             if section_found and line.strip() == "<table>":
#                 table_found = True

#     return documentation        

def opatch_insert_patch(opatch_patches, overrides, documentation):
    for each_patch in opatch_patches:
        version = each_patch['release']
        patchfile = each_patch['patchfile']
        
        if overrides['category'] != "":
            category = overrides['category']
        else:
            category = ""
        
        if overrides['software_piece'] != "":
            software_piece = overrides['software_piece']
        else:
            software_piece = "OPatch Utility"
        
        if overrides['file_name'] != "":
            files = overrides['file_name']
        else:
            files = patchfile

        table_row = """<tr>\n<td></td>\n<td>{category}</td>\n<td>{software_piece}</td>\n<td>{files}</td>\n</tr>\n\n""". format(
            category=category,
            software_piece=software_piece,
            files=files
        )
        table_found = False
        section_found = False
        base_found = False
        for idx, line in enumerate(documentation):

            if section_found and table_found:
                try:
                    if len(line.split(">")) == 3:
                        version_text = line.split(">")[1].split("<")[0]
                        if re.match(r'^[0-9.]+$', version_text):
                            if version_text != version and version_text < version:
                                documentation.insert(idx - 1 , table_row)
                                break
                except IndexError:
                    continue
            
            if line.strip() == "#### Required Oracle Software - Download Summary":
                section_found = True
                
            if section_found and line.strip() == "<tbody>":
                table_found = True
            
            if table_found and line.strip() == "</tbody>":
                break 
        
        
    return documentation

def main():
    dir_path = pathlib.Path(__file__).parent.parent.parent
    input_yml = os.path.join(dir_path, 'modify_patchlist.yaml')
    documentation = load_md(os.path.join(dir_path, 'docs/user-guide.md'))
    patch_data = load_yaml(input_yml)

    # documentation = gi_software_compile_docs(patch_data['gi_software'], patch_data["documentation_overrides"]['gi_software'], documentation)

    documentation = opatch_insert_patch(patch_data['opatch_patches'], patch_data["documentation_overrides"]['opatch_patches'], documentation)

    documentation = 
    # Save the modified documentation
    save_md(os.path.join(dir_path, 'docs/user-guide.md'), ''.join(documentation))
if __name__ == "__main__":
    main()