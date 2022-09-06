import pandas as pd
import os
import matplotlib.pyplot as plt

### Paramters ###
sensors = {
            "footfall-1-1.csv": "Briggate",
            "footfall-2-1.csv": "Briggate at McDonalds",
        #    "footfall-3-1.csv": "Headrow",
        #    "footfall-4-1.csv": "Dortmund Square",
        #    "footfall-5-1.csv": "Albion Street North",
        #    "footfall-6-1.csv": "Albion Street South",
       #     "footfall-7-1.csv": "Commercial Street at Sharps",
         #   "footfall-8-1.csv": "Commercial Street at Barratts",
        #    "footfall-9-1.csv": "Albion Street at McDonalds",
        #    "footfall-A-1.csv": "Park Row",
        }


sDate = "2022-01-01"
eDate = "2030-12-31"

TIMES = [   
        '00:00', 
        '01:00', 
        '02:00', 
        '03:00', 
        '04:00', 
        '05:00', 
        '06:00', 
        '07:00', 
        '08:00', 
        '09:00', 
        '10:00', 
       '11:00', 
        '12:00', 
        '13:00', 
        '14:00', 
       '15:00', 
        '16:00', 
        '17:00', 
        '18:00', 
       '19:00', 
        '20:00', 
        '21:00', 
        '22:00', 
       '23:00'
        ]

MONTHS_EXCLUDE = [
        #    1,
        #    2,
        #   3,
        #    4,
        #     5,
        #    6,
        #    7,
        #    8,
        #    9,
        #    10,
        #    11,
        #    12
        ]
#GROUP_BY : "none" "Weekday"  "Year" "Month" "Week"
GROUP_BY = "Month"
                
ISO_DATE_FORMAT = '%Y-%m-%d'
def getDates(sensorData):
    return pd.to_datetime(sensorData["Date"],format=ISO_DATE_FORMAT)


def getDailyTotals(sensorData):
    dailyTotals = []
    for rName, row in sensorData.iterrows():
        sum = 0
        for column in TIMES:
            sum += row[column]
        dailyTotals.append(int(sum))
    
    return dailyTotals

def filterByDate(data,startDate="1970-01-01",endDate="2100-01-01"):
    data = data[data["Date"] >= startDate]  
    data = data[data["Date"] <= endDate]

    for month in MONTHS_EXCLUDE:
        data = data[data["Date"].dt.month != month]

    return data

#Deals with null values - by default pandas will change an entire intger column to float values if it contains on null
def fixNulls(data):
    for col in list(data)[1:]:
        data[col] = data[col].astype(pd.Int64Dtype())
    

DIR = "Data"
OUTPUT_FILE_NAME = "collated-footfall-test.csv"


output = pd.DataFrame({"Date" : []})
for fName in sensors:
    file = os.path.join(DIR,fName)
    sensorData = pd.read_csv(file)
    pSensorData =  pd.DataFrame({"Date" : getDates(sensorData),sensors[fName] : getDailyTotals(sensorData)})
    pSensorData = filterByDate(pSensorData,startDate=sDate,endDate=eDate)
    output = pd.merge(output,pSensorData,how="outer",left_on="Date",right_on="Date") 


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
output.plot(y=list(sensors.values()), kind='bar',use_index=True)
plt.show()
#print(output)
showIndex = GROUP_BY != "none"

output.to_csv(OUTPUT_FILE_NAME,index=showIndex,date_format=ISO_DATE_FORMAT)