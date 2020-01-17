from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import io
import sys
import getopt

inputFile = ""
outputFile = ""

try:
    opts, args = getopt.getopt(sys.argv[1:], "i:o:h", ["input=", "output=", "help"])
except:
    print("main.py -i <inputfile> -o <outputfile>")
    sys.exit(2)
for opt, arg in opts:
    if(opt in ("-h", "--help")):
        print("main.py -i <inputfile> -o <outputfile>")
        sys.exit()
    elif(opt in ("-i", "--input")):
        inputFile = arg
    elif(opt in ("-o", "--output")):
        outputFile = arg

with open(inputFile, "r") as fp:
    soup = BeautifulSoup(fp, "lxml")

def isQuestion(tag):
    return tag.name == "b" and re.compile(r"q_\d* ").search(tag.string)

def isVariableName(tag):
    return tag.name == "nobr" and tag.string == "Variablenname"

def getQuestionFromParentTable(parentTable):
    return parentTable.findNext(isQuestion)

def getParentTable(tag):
    for parent in tag.parents:
        if(parent.name == "table"):
            return parent
    return None

def getValuesFromVarName(varName):
    parentTableRow = varName.find_parent("tr")
    currentRow = parentTableRow
    result = []
    while(True):
        currentRow = currentRow.find_next_sibling("tr")
        if(not currentRow or currentRow.find("nobr")):
            break
        if(currentRow.has_attr("class") and "bgcolor_ffffff" in currentRow["class"]):
            continue
        desc = currentRow.select("td")[3].string
        value = currentRow.select("td")[2].string
        result.append({"description":desc, "value":value})
    return result

def getVarDescriptionFromVarName(varName):
    parentTableRow = varName.find_parent("tr")
    return parentTableRow.select("td")[3]


def sortObjByKeys(obj):
    sortedObj = {}
    for key in sorted(obj.keys()):
        sortedObj[key] = obj[key]
    return sortedObj

variables = soup.find_all(isVariableName)
variables = [var.find_next("nobr") for var in variables]

resultObjs = {}

for varName in variables:
    parentTable = getParentTable(varName)
    question = getQuestionFromParentTable(parentTable)
    values = getValuesFromVarName(varName)
    varDesc = getVarDescriptionFromVarName(varName)
    varObj = {
        "Variablenname": varName.string,
        "Beschreibung": varDesc.string,
        "Frage": question.string,
        "Werte": values
    }
    resultObjs[varName.string] = varObj

resultObjs = OrderedDict(sorted(resultObjs.items(), key=lambda obj: int(obj[0][2:])))

htmlString=u"<html><head><meta charset=\"UTF-8\"></head>"
htmlString+=u"<body>"
htmlString+=u"<table><thead><tr><th>Variablenname</th><th>Variablenbeschreibung</th><th>Frage</th><th>Auspr&auml;gungen</th></tr></thead>"

for key in resultObjs:
    htmlString+=u"<tr>"
    htmlString+=u"<td style=\"border: 1px solid black;\">" + unicode(resultObjs[key]["Variablenname"]) + u"</td>"
    htmlString+=u"<td style=\"border: 1px solid black;\">" + unicode(resultObjs[key]["Beschreibung"]) + u"</td>"
    htmlString+=u"<td style=\"border: 1px solid black;\">" + unicode(resultObjs[key]["Frage"]) + u"</td>"
    htmlString+=u"<td style=\"border: 1px solid black;\"></td>"
    htmlString+="</tr>"
    for valuePair in resultObjs[key]["Werte"]:
        htmlString+=u"<tr><td style=\"border: 1px solid black;\"></td><td style=\"border: 1px solid black;\"></td><td style=\"border: 1px solid black;\"></td><td style=\"border: 1px solid black;\">" + unicode(valuePair["description"]) + " - " + unicode(valuePair["value"]) + u"</td></tr>"

htmlString+="</body></html>"

resultsFile = io.open(outputFile, "w", encoding="utf-8")

resultsFile.write(htmlString)

resultsFile.close()
    
    


