from bs4 import BeautifulSoup
import re
import io

with open("compact_data.html", "r") as fp:
    soup = BeautifulSoup(fp, "lxml")

def isQuestion(tag):
    return tag.name == "b" and re.compile("q_\d* ").search(tag.string)

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


print(resultObjs["v_17"])
# htmlString=u"<table><thead><tr><th>Variablenname</th><th>Frage</th><th>Ausprägungen</th></tr></thead>"

# for result in resultObjs:
#     htmlString+=u"<tr>"
#     htmlString+=u"<td>" + unicode(result["Variablenname"]) + u"</td>"
#     htmlString+=u"<td>" + unicode(result["Frage"]) + u"</td>"
#     htmlString+=u"<td></td>"
#     htmlString+="</tr>"
#     for valuePair in result["Werte"]:
#         htmlString+=u"<tr><td></td><td></td><td>" + unicode(valuePair["val1"]) + " - " + unicode(valuePair["val2"]) + u"</td></tr>"

# resultsFile = io.open("results.html", "w", encoding="utf-8")

# resultsFile.write(htmlString)

# resultsFile.close()
    
    


