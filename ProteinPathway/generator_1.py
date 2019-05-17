import json
import pandas as pd
import numpy as np
import seaborn as sns
import os
import re
import urllib
from urllib.error import HTTPError
from urllib.request import urlopen


upper = 1.5
lower = 0.8
# 

# with open("./json/Patient-6.json","r") as file1:#change this part
#     data_patient = json.load(file1)
# # useful = {}
# # for keys in data_patient["data"].keys():
# #    if keys in related_dict.keys():
# #       useful[keys] = data_patient["data"][keys]
# # df=pd.DataFrame.from_dict(list(useful.items()))
# df = pd.DataFrame.from_dict(list(data_patient["data"].items()))
# df_outer = pd.DataFrame.from_dict(list(data_patient["data"].items()))

# patient_number=sorted(os.listdir("./json"))[2:]
# regex = "Patient-[0-9]+"
# ls = ["Patient-1"]
# for patients in patient_number:
#     if re.match(regex,patients)!=None:
#         names = patients[:-5]
        
#         with open("./json/" + patients) as file:
#             data_patient = json.load(file)
# #             useful = {}
# #             for keys in data_patient["data"].keys():
# #                 if keys in related_dict.keys():
# #                     useful[keys] = data_patient["data"][keys]
#         dfi =pd.DataFrame.from_dict(list(data_patient["data"].items()))
#         df = df.merge(dfi,left_on = 0, right_on = 0)
#         ls.append(names)
            
# ls.insert(0,"Protein")
# df.columns=ls
# abnormal_count = df[(df>upper)|(df<lower)].count()


# df_t = df.transpose()
# df_t.columns = df.iloc[:,0]
# df_t = df_t.drop("Protein", axis =0)
# df_t = df_t.astype('float64') 
# corr = df_t.corr()

ROOT = "/home/uestclzy/6895project/ProteinPathway/static/txt/"

exs = pd.read_csv(ROOT + "exs.csv")
abnormal_count = exs[(exs>upper)|(exs<lower)].count()
pro = exs.transpose()[abnormal_count>60]
pro[(pro<upper) & (pro > lower)] = None
corr = pro.transpose().corr()
for i in range(corr.shape[0]):
    corr.iloc[i,i] = 0
print("System Running... \n")


def score_to_graph(pro_list):
        nodes = []
        f = open(ROOT +'anootation.txt','a')
        k = 0
        for i in range(len(pro_list)): 
            string_api_url = "https://string-db.org/api"
            output_format = "tsv-no-header"
            method = "get_string_ids"
            my_genes = [pro_list[i]]
            species = "9606"
            request_url = string_api_url + "/" + output_format + "/" + method + "?"
            request_url += "identifiers=%s"%"%0d".join(my_genes)
            request_url += "&" + "species=" + species
            try:
                    res = urlopen(request_url)
                    for line in res:
                        k = k+1
                        inf = str(line, encoding = "utf-8").split("\t")
                        dict = {}
                        dict['id'] = inf[4]
                        if k == 1:
                            f.write('{} :{}'.format(inf[4],inf[5]))
                        else:
                            f.write('\n{} :{}'.format(inf[4],inf[5]))
                        dict["group"] = 1
                        nodes.append(dict)
            except HTTPError as e:
                    print("Error: ", e,"\n",request_url)

        f.close()
   
       
        string_api_url = "https://string-db.org/api"
        output_format = "tsv-no-header"
        method = "network"

        my_genes = pro_list
        species = "9606"


        ## Construct the request

        request_url = string_api_url + "/" + output_format + "/" + method + "?"
        request_url += "identifiers=%s" % "%0d".join(my_genes)
    #     request_url += "&" + "species=" + species
        # request_url += "&" + "caller_identity=" + my_app
        # print(request_url)
        # try:
    #     print(request_url)
        try:
            res = urlopen(request_url)
            links = []
            for line in res:
                inf = str(line, encoding = "utf-8").split("\t")
                dict = {}
                dict['source'] = inf[2]
                dict["target"] = inf[3]
                dict["value"] = float(inf[5])
                links.append(dict)
            json_dict = {}
            json_dict['nodes'] = nodes
            json_dict['links'] = links
            with open('/home/uestclzy/6895project/ProteinPathway/static/json/1.json', 'w') as f:
                    json.dump(json_dict, f)
            f.close
            if (len(links)==0):
                    print("There is no interaction found among those proteins.")
            print("The protein interactions detected based on STRING DataBase:")
            print(pd.DataFrame(links))
        except HTTPError as e:
            print("Error: ", e,"\n",request_url)

        # except urllib.error as err:
        #     error_message = err.read()
        #     print (error_message)
        # sys.exit()
        
        ## Read and parse the results


def corr_to_json(pro_list,threholds = 0.95):
    nodes = []
    links = []
    up = exs[exs>upper].count()
    low = exs[exs<lower].count()
    for i in range(len(pro_list)):
        dict = {}
        dict['id'] = pro_list[i]
        if up[pro_list[i]]//low[pro_list[i]] >6:
            dict['group'] = 1

        elif low[pro_list[i]]//up[pro_list[i]] >6:
            dict['group'] = 2

        else:
            dict['group'] = 3
        nodes.append(dict)
        for j in range(len(pro_list) - 1, i, -1):
#             print(i, j)
            if (pro_list[i] in corr.index) and (pro_list[j] in corr.index) :
                if (corr.loc[pro_list[i], pro_list[j]] > threholds):
#                 print(pro_list[i], pro_list[j])
#                 print(corr.loc[pro_list[i], pro_list[j]])
#                 dict = {}
#                 dict['id'] = pro_list[i]
#                 dict['group'] = 1
#                 nodes.append(dict)
                    dict = {}
                    dict['source'] = pro_list[i]
                    dict['target'] = pro_list[j]
                    dict['value'] = abs(corr.loc[pro_list[i], pro_list[j]])
                    links.append(dict)
    json_dict = {}
    json_dict['nodes'] = nodes
    json_dict['links'] = links
    #  print(nodes, links)
    with open('/home/uestclzy/6895project/ProteinPathway/static/json/2.json', 'w') as f:
                json.dump(json_dict, f)
    f.close