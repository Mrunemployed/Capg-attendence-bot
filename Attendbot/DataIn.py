from typing import Any
import pandas as pd
from datetime import datetime
import datetime

class Bribe():

    def __init__(self) -> None:
        pass
    
    def manipulate(self,df:pd.DataFrame):
        try:
            
            for i,j in df.iterrows():
                if pd.notna(j["Attendance shift"]) and pd.notna(j["Rostered shift"]):
                    if (j["Rostered shift"] in ["PH","WO"] ) | (j["Attendance shift"] == "Leave"):
                        df.loc[i,"Mode"] = "ignore"
                    elif j["Attendance status"] == "PendingApproval":
                        df.loc[i,"Mode"] = "ignore"
                    elif not pd.isnull(j["Date"]) and datetime.datetime.strptime(j["Date"],"%d-%b-%y").month > datetime.datetime.now().month:
                    #type(df.loc[i,"Date"])!= float:
                        # if datetime.datetime.strptime(j["Date"],"%d-%b-%Y") >= datetime.datetime.now():
                        df.loc[i,"Mode"] = "ignore"
                    else:
                        in_time = j["In Time"]
                        out_time = j["Out Time"]

                        if in_time == "NoValue" and out_time== "NoValue":
                            pass
                        else:
                            diff = datetime.datetime.strptime(out_time,"%H:%M") - datetime.datetime.strptime(in_time,"%H:%M")
                            if int(in_time[:2]) == 0 and int(out_time[:2]) == 0:
                                df.loc[i,"Mode"] = "Manual Swipe Attendence"
                            elif int(in_time[:2]) != 0 and int(out_time[:2]) != 0 and diff < datetime.timedelta(hours=8):
                                df.loc[i,"Mode"] = "Swipe Adjustment"
                            else:
                                df.loc[i,"Mode"] = "ignore"
                else:
                    df.fillna("NoValue",inplace=True)
            return df
        except Exception as e:
            return str(e)

# df = pd.read_csv("sample.csv")
# br = Bribe()
# c = br.manipulate(df)
# print(c)


