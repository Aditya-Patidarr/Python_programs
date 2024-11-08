import requests
import pandas as pd

dframe = pd.read_excel(r'C:\Users\aadit\Documents\Python_assignments\Health_checker\website_data.xlsx')

for index, website in dframe.iterrows():
    try:
        response = requests.get(website["WEBSITE NAME:"])
        dframe.at[index, "STATUS:"] = "site is up and running with status code : {}".format(response.status_code)

    except:
        dframe.at[index, "STATUS:"] = "site is down or not available"

print(dframe)