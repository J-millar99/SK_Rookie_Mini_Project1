# reqeusts, bs4 import
import requests, bs4
# BeautifulSoup 클래스 import
from bs4 import BeautifulSoup

def classify_jobs(soup, occ2_id_dict):
    url = "https://job.incruit.com/jobdb_list/searchjob.asp?occ2="
    total = "https://job.incruit.com/s_common/searchjob/v3/searchjob_getcount_ajax.asp?occ2="
    
    for occ2_id in occ2_id_dict.keys():
        detail_job = dict()
        res1 = requests.get(url + occ2_id)
        res2 = requests.get(total + occ2_id)
        if res2.ok:
            data = res2.text
            print(data)