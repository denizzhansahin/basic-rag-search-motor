from langdetect import detect
from bs4 import BeautifulSoup


def dili_bul(html, text):

    soup = BeautifulSoup(html, "html.parser")

    # 1️⃣ HTML lang attribute
    html_tag = soup.find("html")
    if html_tag and html_tag.get("lang"):
        return html_tag.get("lang")

    # 2️⃣ meta language
    meta_lang = soup.find("meta", attrs={"http-equiv": "content-language"})
    if meta_lang and meta_lang.get("content"):
        return meta_lang.get("content")

    # 3️⃣ metinden tespit
    try:
        return detect(text)
    except:
        return None