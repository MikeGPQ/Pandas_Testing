from dataManager import dataManager
from flask import Flask, render_template, request, Response
import io
import pandas

dm = dataManager()
restored = dataManager()

app = Flask(__name__)
@app.route('/',methods=["GET","POST"])
def loading():
    if request.method=="POST":
        if "action" in request.form:
            match request.form["action"]:
                case "Upload":
                    dm.setData(request.files["dataFile"])
                    restored.dataFrame = dm.dataFrame
                    return render_template("home.html",table=dm.dataFrame.to_html()) 
                case "Delete":
                    dm.dataFrame = None
                    return render_template("home.html",table=None)
                case "Restore":
                    dm.dataFrame = restored.dataFrame
                    return render_template("home.html",table=dm.dataFrame.to_html()) 
                case "Sort":
                    sortColumn = request.form.get("sortColumn")
                    if(request.form.get("ascendingOption")=="Ascending"):
                        ascendingOption = True
                    else:
                        ascendingOption = False
                    dm.dataFrame = dm.dataFrame.sort_values(by=sortColumn, ascending=ascendingOption)
                    return render_template("home.html",table=dm.dataFrame.to_html()) 
                case "Filter":
                    filterValue = request.form.get("filterValue")
                    filterColumn = request.form.get("filterColumn")
                    dm.dataFrame = dm.dataFrame[dm.dataFrame[filterColumn] == filterValue]
                    return render_template("home.html",table=dm.dataFrame.to_html()) 
    return render_template("home.html",table=None)

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



