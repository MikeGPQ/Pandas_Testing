import pandas
import os
import io

class dataManager:
    def __init__(self):
        self.dataFrame = pandas.DataFrame() 
        self.copy = pandas.DataFrame()
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
        self.copy = self.dataFrame.copy()
    def getHTML(self):
        if(self.dataFrame.empty):
            return None
        return self.dataFrame.to_html(classes='table table-striped')
    def getColumns(self):
        if(self.dataFrame.empty):
            return None
        return self.dataFrame.columns.to_list()
    def fixMissingValue(self,column):
        self.dataFrame[column] = self.dataFrame[column].fillna(self.dataFrame[column].mode().iloc[0])

        


    
