# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:04:02 2020

@author: scriba
"""

import urllib
import json
import pandas as pd
url = "https://trouver.datasud.fr/api/3/action/datastore_search?resource_id=787a02c2-0ae6-43d9-ab08-aecc6a56435e"
response = urllib.request.urlopen(url)
response_dict = json.loads(response.read())
df = pd.DataFrame.from_records(response_dict["result"]["records"], index='_id')
df