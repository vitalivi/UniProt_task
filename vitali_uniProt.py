#!/usr/bin/env python
# coding: utf-8

# ## Task for Vitali. BostoneGene interview

# In[4]:


import xmlschema #is used for converting the data from UniProt .xml file to python dictionary
import pathlib
import pandas as pd


# In[5]:


# UniProtIDs from the task 
UniProtID = {'sCD40L':'P29965', 'EGF': 'Q9UHF1', 'Eotaxin':'P51671', 'FGF-2':'P09038', 'FLT-3L':'P49771', 'Fractalkine':'P78423', 'G-CSF':'Q99062','GM-CSF':'A9CB23','GRO-a':'B5X8A6','IFN-a2':'B5ANN6', 'IFN-g':'Q2PE57', 'IL-1a':'P01583'}


# In[6]:


# function that returns the list of protein names
def extract(protein_data, UID):
    protein_names_list = []
    for type_of_name in  list(protein_data.keys()):
            if type_of_name == 'component':
                continue
            if type(protein_data[type_of_name]) is dict:  
                for subtype_of_name in protein_data[type_of_name]:
                    if type(protein_data[type_of_name][subtype_of_name]) is dict:
                        current_list = [UID, type_of_name, subtype_of_name, protein_data[type_of_name][subtype_of_name]['$']]
                        protein_names_list.append(current_list)
                    if type(protein_data[type_of_name][subtype_of_name]) is list:
                        if type(protein_data[type_of_name][subtype_of_name][0]) is dict:
                            current_list = [UID, type_of_name, subtype_of_name, protein_data[type_of_name][subtype_of_name][0]['$']]
                        else:
                            current_list = [UID, type_of_name, subtype_of_name, protein_data[type_of_name][subtype_of_name][0]]
                        protein_names_list.append(current_list)                        
                    if type(protein_data[type_of_name][subtype_of_name]) is str:
                        current_list = [UID, type_of_name, subtype_of_name, protein_data[type_of_name][subtype_of_name]]
                        protein_names_list.append(current_list) 
            if type(protein_data[type_of_name]) is list:
                if type(protein_data[type_of_name][0]) is str:
                    current_list = [UID, type_of_name, 'None', protein_data[type_of_name][0]]
                else:
                    for name_variant in protein_data[type_of_name]:
                        for subtype_of_name in name_variant:
                            if type(name_variant[subtype_of_name]) is dict:
                                current_list = [UID, type_of_name, subtype_of_name, name_variant[subtype_of_name]['$']]
                                protein_names_list.append(current_list)
                            if type(name_variant[subtype_of_name]) is list:
                                if type(name_variant[subtype_of_name][0]) is dict:
                                    current_list = [UID, type_of_name, subtype_of_name, name_variant[subtype_of_name][0]['$']]
                                else:
                                    current_list = [UID, type_of_name, subtype_of_name, name_variant[subtype_of_name][0]]
                                protein_names_list.append(current_list)                        
                            if type(name_variant[subtype_of_name]) is str:
                                current_list = [UID, type_of_name, subtype_of_name, name_variant[subtype_of_name]]
                                protein_names_list.append(current_list)     
    if len(protein_names_list) == 0:
        protein_names_list = [[UID,'No information','No information','No information']]
    return protein_names_list


# In[7]:


# function that returns the list of gene names 
def extract_gene(gene_data, UID):
    gene_names_list =[]
    for gene_data_dict in gene_data:
        if type(gene_data_dict['name']) is list:
            for gene_name_dict in gene_data_dict['name']:
                current_list = [UID, gene_name_dict['@type'], gene_name_dict['$']]
                gene_names_list.append(current_list)
        if type(gene_data_dict['name']) is dict:
            current_list = [UID, gene_name_dict['name']['@type'], gene_name_dict['name']['$']]
            gene_names_list.append(current_list)
    if len(gene_names_list) == 0:
        gene_names_list = [[UID,'No information','No information']]
    return gene_names_list


# In[9]:


# function that returns the list of protein functions
def extract_function(function_data, UID):
    function_list = []
    for entry in function_data:
        if entry['@type'] == 'function':
            for text in entry['text']:
                if type(text) is str:
                    current_line = [UID, text]
                    function_list.append(current_line)
                if type(text) is dict:
                    current_line = [UID, text['$']]
                    function_list.append(current_line)
    if len(function_list) == 0:
        function_list = [[UID,'No information']]
    return function_list


# In[10]:


# the main function that 
# 0) takes UniProtID as the input
# 1) extracts the corresponding data from the UniProt database
# 2) selects protein names, gene names and protein functions
# 3) writes the slected data to the results.xls at the same path as the main script 
def main(UID):
# UID must be a string
#checking if the specified UniProtID is already in results.xls
    path_to_excel_file = pathlib.Path('results.xls')
    if path_to_excel_file.exists() == True:
        sheet1 = pd.read_excel(path_to_excel_file, sheet_name='Sheet1')
        if UID in list(sheet1['UniProtID']):
            print('UniProtID '+ str(UID) + ' is already in results.xls')
            return None    

# extracting the UID data from UniProt database
    link_uniprotid = 'https://www.uniprot.org/uniprot/' + str(UID) + '.xml'
    schema = xmlschema.XMLSchema('https://www.uniprot.org/docs/uniprot.xsd')
    entry_dict = schema.to_dict(link_uniprotid)
    entry_dict.keys()
    UnipProtID_data = entry_dict['entry'][0]
##################################################################protein names####################################################### 
#preparing the first sheet in excel
    protein_info = UnipProtID_data['protein']
    columns_protein = ['UniProtID','type of name', 'subtype of name','protein name']
# extracting the main information about protein names with function extract
    protein_names = extract(protein_info, UID)
# extracting additional information about components
    if 'component' in list(protein_info.keys()):
        if type(protein_info['component']) is list:
            for component_dict in protein_info['component']:
                component_list = extract(component_dict,UID)
                if type(component_list[0]) is list: 
                    for each_list in component_list:
                        each_list[1] = each_list[1] +  '_component'
                    protein_names = protein_names + component_list
                else:
                    component_list[1] = component_list[1] +  '_component'
                    protein_names = protein_names + [component_list]
        if type(protein_info['component']) is dict:
            component_list = extract(protein_info['component'],UID)
            if type(component_list[0]) is list:
                for each_list in component_list:
                    each_list[1] = each_list[1] +  '_component'
                protein_names = protein_names + component_list
            else:
                component_list[1] = component_list[1] +  '_component'
                protein_names = protein_names + [component_list]
# converting the list of protein names to pandas DataFrame
    protein_DataFrame = pd.DataFrame(protein_names, columns = columns_protein)

################################################################# gene names################################################### 
#preparing the second sheet in excel
    gene_info = UnipProtID_data['gene']
    columns_gene = ['UniProtID','type of name', 'gene name']
# extracting the main information about gene names with function expract_gene
    gene_names = extract_gene(gene_info, UID)
# converting the list of gene names to pandas DataFrame
    gene_DataFrame = pd.DataFrame(gene_names, columns = columns_gene)
    
###############################################################protein functions#####################################################   
#preparing the third sheet in excel
    function_info = UnipProtID_data['comment']
    columns_function = ['UniProtID','function']
# extracting the main information about protein functions with function extract_function
    functions = extract_function(function_info, UID)
# converting the list of gene names to pandas DataFrame
    function_DataFrame = pd.DataFrame(functions, columns = columns_function)      

    
#writing to results.xls
    if path_to_excel_file.exists() == True:
        sheet1 = pd.read_excel(path_to_excel_file, sheet_name='Sheet1', index_col= [0])
        sheet2 = pd.read_excel(path_to_excel_file, sheet_name='Sheet2', index_col= [0])
        sheet3 = pd.read_excel(path_to_excel_file, sheet_name='Sheet3', index_col= [0])
        new_sheet_protein = pd.concat([sheet1, protein_DataFrame], axis=0, ignore_index=True)
        new_sheet_gene = pd.concat([sheet2, gene_DataFrame], axis=0, ignore_index=True)
        new_sheet_function = pd.concat([sheet3, function_DataFrame], axis=0, ignore_index=True)
        with pd.ExcelWriter(path_to_excel_file) as writer:
            new_sheet_protein.to_excel(writer, sheet_name='Sheet1')
            new_sheet_gene.to_excel(writer, sheet_name='Sheet2')
            new_sheet_function.to_excel(writer, sheet_name='Sheet3')
    else:
        with pd.ExcelWriter(path_to_excel_file) as writer:
            protein_DataFrame.to_excel(writer, sheet_name='Sheet1')
            gene_DataFrame.to_excel(writer, sheet_name='Sheet2')
            function_DataFrame.to_excel(writer, sheet_name='Sheet3')
    return None


# In[11]:


if __name__ == '__main__':
    for key in UniProtID:
        main(UniProtID[key])

