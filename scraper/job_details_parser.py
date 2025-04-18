# reqeusts, bs4 import
import requests, bs4
# BeautifulSoup 클래스 import
from bs4 import BeautifulSoup

req_header = { "user-agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'}

def calculate_page_count(count_str):
    count = int(count_str.replace(",", ""))
    page = ((count - 1) // 30) + 1
    return page

def get_page_url_list(occ2_id_dict):
    count_url = "https://job.incruit.com/s_common/searchjob/v3/searchjob_getcount_ajax.asp?occ2="
    url = "https://job.incruit.com/jobdb_list/searchjob.asp?articlecount=30&occ2="

    page_list = []
    for occ2_id in occ2_id_dict.keys():
        res = requests.get(count_url + occ2_id)
        if res.ok:
            page_url = url + occ2_id + "&page="
            page_num = calculate_page_count(res.text)
            for page_index in range(1, page_num + 1):
                page_list.append(page_url + str(page_index))
        else:
            print(f"에러 코드 = {res.status_code}")
    return page_list

def first_cell_parser(li_tag_list):
    for li_tag in li_tag_list:
        first_cell = li_tag.find('div.cell_first') # 기업 이름과 태그
        company = first_cell.find('a')
        print(company.text)

def mid_cell_parser(li_tag_list):
    for li_tag in li_tag_list:
        mid_cell = li_tag.find('div.cell_mid') # 채용 공고
        title = mid_cell.find('a')
        print(title.text)

def classify_jobs(occ2_id_dict):
    page_url_list = get_page_url_list(occ2_id_dict)
    for page_url in page_url_list[:2]:
        res = requests.get(page_url, headers=req_header)
        if res.ok:
            html = res.text
            soup = BeautifulSoup(html, "html.parser")
            li_tag_list = soup.select("li.c_row")
            first_cell_parser(li_tag_list)
            mid_cell_parser(li_tag_list)
        else:
            print(f"에러 코드 = {res.status_code}")
