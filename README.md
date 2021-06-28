### Description
The **main(UID)** is a function that 
1) takes UniProtID as the input
2) extracts the corresponding data from the UniProt database
3) selects protein names, gene names and protein functions
4) writes the slected data to the results.xls (the same path as the main script), protein names - Sheet1, gene names - Sheet2, protein functions - Sheet3

### Files
- **vitali_uniProt.py** - the main script. When executing "python3 vitali_uniProt.py" in the terminal, the function **main(UID)** will be called in for loop for all UniProtIDs specified in the task
- **vitali_uniProt.ipynb** - the corresponding jupiter notebook
- **requirements.txt** - the dependencies that might be not installed (openpyxl, XlsxWriter, xmlschema). Please run: "pip3 install -r requirements.txt"
