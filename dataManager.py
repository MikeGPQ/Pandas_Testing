import pandas
import os
import io

class dataManager:
    def __init__(self):
        self.dataFrame = pandas.DataFrame() 
    def setData(self,file):
        match (os.path.splitext(file.filename)[1]):
            case ".csv":
                self.dataFrame = pandas.read_csv(file)
            case ".xlsx":
                self.dataFrame = pandas.read_excel(file)
            case ".json":
                self.dataFrame = pandas.read_json(file)
            case ".html":
                htmlFile = file.read().decode("utf-8")
                self.dataFrame = pandas.read_html(io.StringIO(htmlFile))[0]
        


    
