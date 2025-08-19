from flask import Flask, render_template, request, Response
import io
import pandas
import os
from dataManager import dataManager 

dm = dataManager()

app = Flask(__name__)
@app.route('/',methods=["GET","POST"])
def loading():
    button = False
    if request.method=="POST":
        if "action" in request.form:
            match request.form["action"]:
                case "Upload":
                    dm.setData(request.files["dataFile"])
                case "Delete":
                    dm.dataFrame = pandas.DataFrame()
                case "Restore":
                    dm.dataFrame = dm.copy
                case "Sort":
                    sortColumn = request.form.get("sortColumn")
                    if(request.form.get("ascendingOption")=="Ascending"):
                        ascendingOption = True
                    else:
                        ascendingOption = False
                    dm.dataFrame = dm.dataFrame.sort_values(by=sortColumn, ascending=ascendingOption)
                case "Filter":
                    filterValue = request.form.get("filterValue")
                    filterColumn = request.form.get("filterColumn")
                    if(button == True):
                        filterValue2 = request.form.get("filterValue2")
                        print(filterValue, filterValue2,filterColumn)
                        dm.dataFrame = dm.dataFrame[dm.dataFrame[filterColumn].isin([filterValue,filterValue2])]
                    else:
                        dm.dataFrame = dm.dataFrame[dm.dataFrame[filterColumn] == filterValue]
                    button = False
                case "Add+":
                    button = True
                case "toNumeric":
                    toNumericColumn = request.form.get("toNumericColumn")
                    dm.dataFrame[toNumericColumn] = pandas.to_numeric(dm.dataFrame[toNumericColumn],errors="coerce")
                case "fillColumn":
                    fillColumn = request.form.get("fillColumn")
                    dm.fixMissingValue(fillColumn)
                case "removeDuplicates":
                    dm.dataFrame = dm.dataFrame.drop_duplicates()
    return render_template("home.html",table=dm.getHTML(),button=button,columns = dm.getColumns())

@app.route("/export/<format>")
def exportFile(format):
    match format:
        case "csv":
            data = dm.dataFrame.to_csv(index=False)
            return Response(data, mimetype='text/csv', headers={"Content-disposition": "attachment; filename=data.csv"})
        case "xlsx":
            output = io.BytesIO()
            with pandas.ExcelWriter(output, engine='xlsxwriter') as writer:
                dm.dataFrame.to_excel(writer, index=False, sheet_name='Sheet1')
            output.seek(0)
            return Response(output.getvalue(), mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={"Content-disposition": "attachment; filename=data.xlsx"})
        case "json":
            data = dm.dataFrame.to_json(orient="records")
            return Response(data, mimetype='application/json', headers={"Content-disposition": "attachment; filename=data.json"})
        case "html":
            data = dm.dataFrame.to_html(classes='table table-striped',index=False)
            return Response(data, mimetype='text/html', headers={"Content-disposition": "attachment; filename=data.html"})


if __name__ == '__main__':
    app.run()




