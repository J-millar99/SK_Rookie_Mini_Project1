# reqeusts, bs4 import
import requests, bs4
# BeautifulSoup 클래스 import
from bs4 import BeautifulSoup
from job_category_parser import select_occ1_id, select_occ2_id
from job_details_parser import classify_jobs

def scraper():
    url = "https://job.incruit.com/jobdb_list/searchjob.asp?occ1=100&occ1=101&occ1=102&occ1=150&occ1=104&occ1=160&occ1=110&occ1=106&occ1=140&occ1=120&occ1=170&occ1=103&occ1=107&occ1=190&occ1=200&occ1=210&occ1=130"
    res = requests.get(url)

    if res.ok:
        html = res.text

        soup = BeautifulSoup(html, "html.parser")
        occ1_id_dict = select_occ1_id(soup)
        # print(occ1_id_dict)
        occ2_id_dict = select_occ2_id(soup, occ1_id_dict.keys())
        # print(occ2_id_dict)

        classify_jobs(soup, occ2_id_dict)


    else:
        print(f"에러 코드 = {res.status_code}")

scraper()