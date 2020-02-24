import requests
import json
import csv

def makeSpeciesByCountry(STEM, TOKEN, filename, country):
    """MAKES API CALL AND WRITE THE TEXT FILE - DO THIS ONLY ONCE"""
    request = requests.get(STEM + 'country/getspecies/' + country + TOKEN)
    response = request.json()

    writeTXTFile(filename, response)

    #LOADS JSON FOR PARSING BY 'result', ADDS COUNTRY COLUMN
    with open(filename + '.txt', 'r') as f:
        contents = json.load(f)
        result = contents['result']
        for key in result:
            key.update({'country': country})
        f.close()
    print('Parsing', filename, 'object')

    writeCSVFile(filename, result)

def makeGlobalSpeciesAssesment(STEM, TOKEN):
    """MAKES API CALL AND WRITE THE TEXT FILES - DO THIS ONLY ONCE"""    
    page = 0
    page_list =[]
    while True:
        request = requests.get(STEM + 'species/page/' + str(page) + TOKEN)
        response = request.json()
        filename = 'globalSpeciesPage' + str(page)
        # print('page', page, response['count'])
        if response['count'] == 0:
            break
        page_list.append(filename + '.txt')
        writeTXTFile(filename, response)
        page += 1

    #LOADs FROM EXISTING JSON TEXT FILES AND EXTENDs LIST 'result'
    result = []
    for p in page_list:
        with open(p, 'r') as f:
            contents = json.load(f)
            result.extend(contents['result'])
            f.close()

    #WRITES THE CONCATENATED 'result' LIST OF DICTS TO CSV
    writeCSVFile('globalSpeciesAssessment', result)

def writeTXTFile(filename, response):
    """GENERIC CODE TO WRITE TXT FILE FROM 'response' """
    with open(filename + '.txt', 'w', newline='') as f:
        json.dump(response, f)
        f.close()
    print('Made', filename + '.txt')

def writeCSVFile(filename, result):
    """GENERIC CODE TO WRITE CSV FILE FROM PARSED 'result' """
    with open(filename + '.csv', 'w', newline='') as f:
        fieldnames = result[0].keys()
        write = csv.DictWriter(f, fieldnames=fieldnames)
        write.writeheader()
        for entry in result:
            write.writerow(entry)
        f.close()
    print('Made', filename + '.csv')

def main():
    STEM = 'https://apiv3.iucnredlist.org/api/v3/'
    #TOKEN = '?token=08053c6eb08b60c5e0b4c5dbbe60144d85a768b23c0f5d7e0e7a7839fc5420b7'

    with open('token.txt', 'r') as t:
        TOKEN = t.read()
        #print(t)
        t.close()
    #MAKES SPECIES BY COUNTRY TXT AND CSV FILES
    countries = ['CD', 'CG', 'GA', 'CM']
    files_made = []

    for c in countries:
        filename = 'all' + c + 'species'
        # makeSpeciesByCountry(STEM, TOKEN, filename, c)
        files_made.append(filename)

    #MAKES GLOBAL SPECIES ASSESSMENT
    makeGlobalSpeciesAssesment(STEM, TOKEN)

main()

