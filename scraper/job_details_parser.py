# reqeusts, bs4 import
import requests, bs4
# BeautifulSoup 클래스 import
from bs4 import BeautifulSoup

def get_total_page(count_str):
    count = int(count_str.replace(",", ""))
    page = ((count - 1) // 30) + 1
    return page

def calculate_page_count(occ2_id_dict):
    count_url = "https://job.incruit.com/s_common/searchjob/v3/searchjob_getcount_ajax.asp?occ2="
    url = "https://job.incruit.com/jobdb_list/searchjob.asp?articlecount=30&occ2="

    page_list = []
    for occ2_id in occ2_id_dict.keys():
        res = requests.get(count_url + occ2_id)
        if res.ok:
            page_url = url + occ2_id + "&page="
            page_num = get_total_page(res.text)
            for page_index in range(1, page_num + 1):
                page_list.append(page_url + str(page_num))
    return page_list

def classify_jobs(soup, occ2_id_dict):
    page_list = calculate_page_count(occ2_id_dict)
    print(page_list)
