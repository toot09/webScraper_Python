import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&limit={LIMIT}"


def extract_indeed_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all('a')
    pages = []

    #마지막은 Next이므로 제외
    for link in links[:-1]:
        #soup.title.string : string값만 추출
        #pages.append(link.find('span').string)
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find("div", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    company_anchor = company.find("a")
    #회사이름에 anchor가 있는게 있고 없는게 있어서 분기처리
    if company_anchor is not None:
        #"string".strip() : param 공백이면 공백으로 시작하는 공백문자 삭제. 알파벳 넣으면 없앰
        company = company_anchor.string.strip()
    else:
        company = company.string.strip()
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    #dictionary type return
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://kr.indeed.com/viewjob?jk={job_id}"
    }


def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping page {page}")
    result = requests.get(f"{URL}&START={LIMIT*page}")
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
        jobs.append(extract_job(result))
  return jobs
