import json
with open('Use Case3 - sql_config_ex1.json') as f:
    data = json.load(f)

#print(data)


def generateExpression(operator, column, params):
    ex = ''
    if operator == "BETWEEN":
        ex += column + " BETWEEN '" + params[0] + "' AND '" + params[1] + "'"

    if operator == "IN":
        ex += column + " IN ("
        for i, p in enumerate(params):
            ex += "'" + p + "'"
            if i != len(params) - 1:
                ex += ", " 
        ex += ')'

    if operator == "=":
        ex += column + " = '" + params + "'"

    if operator == "!=":
        ex += column + " != '" + params + "'"

    return ex


d = {}

query = "select " + ", ".join(data['columns']) + " FROM ("
query += data['sql'] + " WHERE ("

with open("Use Case3 - params_s2.txt") as f:
    line = f.readline()
    l = line.split(" : ")
    if l[0] != 'start_date':
        l[1] = l[1][:-1]
    if "," in l[1]:
        l[1] = l[1].split(",")
    d[l[0]] = l[1]
    while line:
        
        line = line[:-1]
        l = line.split(" : ")
        if "," in l[1]:
            l[1] = l[1].split(",")
        d[l[0]] = l[1]
        line = f.readline()


if 'start_date' in d:
    d['date'] = [d['start_date'], d['end_date']]
    del d['start_date']
    del d['end_date']


expressions = []
for filterDict in data["filters"]:
    if filterDict["operator"] == "AND":
        for subDict in filterDict["filters"]:
            if subDict["operator"] != "OR":
                if subDict["params"][0] in d:
                    ex = generateExpression(subDict["operator"], subDict["column"], d[subDict["params"][0]])
                    expressions.append(ex)
                if subDict["params"][0] == "start_date":
                    ex = generateExpression(subDict["operator"], subDict["column"], d["date"])
                    expressions.append(ex)
                
            else:
                new = []
                for subsubDict in subDict["filters"]:
                    if subsubDict["params"][0] in d:
                        ex = generateExpression(subsubDict["operator"], subsubDict["column"], d[subsubDict["params"][0]])
                        new.append(ex)
                    if subsubDict["params"][0] == "start_date":
                        ex = generateExpression(subsubDict["operator"], subsubDict["column"], d["date"])
                        new.append(ex)
                expressions.append( "(" + " OR ".join(new) + ")")


        query += "("
        query += " AND ".join(expressions)
        query += ")"

    elif filterDict["operator"] == "OR":
        for subDict in filterDict["filters"]:
            if subDict["params"][0] in d:
                ex = generateExpression(subDict["operator"], subDict["column"], d[subDict["params"][0]])
                expressions.append(ex)
            if subDict["params"][0] == "start_date":
                ex = generateExpression(subDict["operator"], subDict["column"], d["date"])
                expressions.append(ex)
        query += "("
        query += " OR ".join(expressions)
        query += ")"

    else:
        if filterDict["params"][0] in d:
            ex = generateExpression(filterDict["operator"], filterDict["column"], d[filterDict["params"][0]])
            expressions.append(ex)
        if filterDict["params"][0] == "start_date":
            ex = generateExpression(filterDict["operator"], filterDict["column"], d["date"])
            expressions.append(ex)
    


query += "))"
print(query)
