import requests
import sqlite3
import urllib.parse
import concurrent.futures
import time


HEADERS = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://www.lagou.com",
    "pragma": "no-cache",
    "referer": "https://www.lagou.com/jobs/list_Python/p-city_3?px=default",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "x-anit-forge-code": "0",
    "x-anit-forge-token": "None",
    "x-requested-with": "XMLHttpRequest",
}


def save_position(location, position_id, name, salary_low, salary_high):
    print(f"save: {location}, {position_id}, {name}, {salary_low}, {salary_high}")
    with sqlite3.connect("lagou.db") as conn:
        c = conn.cursor()
        c.execute("select * from positions where position_id=?", (position_id,))
        if not c.fetchone():
            c.execute(
                "insert into positions (location, position_id, name, salary_low, salary_high) values (?, ?, ?, ?, ?)",
                (location, position_id, name, salary_low, salary_high),
            )


def parse_salary(salary: str):
    [low, high] = salary.split("-")
    return (int(low.replace("k", "000")), int(high.replace("k", "000")))


def scrawl_url(url, session, cookies):
    time.sleep(30)
    response = session.post(
        url["url"],
        data={"first": url["first"], "pn": url["pn"], "kd": url["kd"]},
        headers=HEADERS,
        cookies=cookies,
    )
    result = response.json()
    print(result)
    positions = result["content"]["positionResult"]["result"]
    for position in positions:
        location = position["city"].strip()
        position_id = position["positionId"]
        name = position["positionName"].strip()
        (salary_low, salary_high) = parse_salary(position["salary"].strip())
        save_position(location, position_id, name, salary_low, salary_high)


if __name__ == "__main__":
    parameters = [
        {"px": "default", "city": city, "needAdditionalResult": False}
        # for city in ["北京", "上海", "广州", "深圳"]
        # for city in ["北京", "上海", "广州", "深圳"]
        # for city in ["北京", "上海", "广州", "深圳"]
        # for city in ["北京", "上海", "广州", "深圳"]
        for city in ["深圳"]
    ]
    urls = [
        {
            "first": i == 1,
            "pn": i,
            "kd": "python",
            "url": "https://www.lagou.com/jobs/positionAjax.json?"
            + urllib.parse.urlencode(p),
        }
        for p in parameters
        for i in range(1, 8)
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        with requests.Session() as session:
            response = session.get(
                "https://www.lagou.com/jobs/list_python/p-city_2?px=default#filterBox",
                headers=HEADERS,
            )
            for url in urls:
                executor.submit(scrawl_url, url, session, response.cookies)
