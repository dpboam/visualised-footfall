import pandas as pd
import os
import matplotlib.pyplot as plt
import yaml
import sys

PATH = sys.argv[1] if len(sys.argv) >= 2 else 'config_template.yml'
with open(PATH) as f:
    PARAMS = yaml.safe_load(f) 

ISO_DATE_FORMAT = '%Y-%m-%d'
def getDates(sensorData):
    return pd.to_datetime(sensorData["Date"],format=ISO_DATE_FORMAT)


def getDailyTotals(sensorData):
    dailyTotals = []
    for rName, row in sensorData.iterrows():
        sum = 0
        for column in PARAMS["times"]:
            sum += row[column]
        dailyTotals.append(int(sum))
    
    return dailyTotals

def filterByDate(data,startDate="1970-01-01",endDate="2100-01-01"):
    data = data[data["Date"] >= startDate]  
    data = data[data["Date"] <= endDate]

    for month in PARAMS["months_exclude"]:
        data = data[data["Date"].dt.month != month]

    return data

#Deals with null values - by default pandas will change an entire intger column to float values if it contains on null
def fixNulls(data):
    for col in list(data)[1:]:
        data[col] = data[col].astype(pd.Int64Dtype())
    

URL_BASE = "https://open-innovations.github.io/traffic-growth/data/leeds/"



output = pd.DataFrame({"Date" : []})
sensors = PARAMS["sensors"]
for fName in sensors:
    url = URL_BASE + fName
    sensorData = pd.read_csv(url)
    pSensorData =  pd.DataFrame({"Date" : getDates(sensorData),sensors[fName] : getDailyTotals(sensorData)})
    pSensorData = filterByDate(pSensorData,startDate=PARAMS["sDate"],endDate=PARAMS["eDate"])
    output = pd.merge(output,pSensorData,how="outer",left_on="Date",right_on="Date") 

GROUP_BY = PARAMS["group_by"]
if GROUP_BY == "none":
    fixNulls(output)
elif GROUP_BY == "Weekday":
    output = output.groupby(output["Date"].dt.weekday)[list(sensors.values())].mean().fillna(-1).astype(int)
elif GROUP_BY == "Year":
    output = output.groupby(output["Date"].dt.year)[list(sensors.values())].mean().fillna(-1).astype(int)
elif GROUP_BY == "Month":
    output = output.groupby(output["Date"].dt.month)[list(sensors.values())].mean().fillna(-1).astype(int)
elif GROUP_BY == "Week":
    output = output.groupby(output["Date"].dt.isocalendar().week)[list(sensors.values())].mean().fillna(-1).astype(int)


#output = output.set_index("Date")
output.plot(y=list(sensors.values()), kind=PARAMS["chart_type"],use_index=True)
plt.show()
#print(output)
showIndex = GROUP_BY != "none"

OUTPUT_FILE_DIR = "output_csv"
OUTPUT_FILE_NAME = os.path.join(OUTPUT_FILE_DIR,PARAMS["file_name"]+ ".csv")
output.to_csv(OUTPUT_FILE_NAME,index=showIndex,date_format=ISO_DATE_FORMAT)
