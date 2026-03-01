import sys
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))


import math
from urllib.parse import urlparse

from search_core.keyword_search import keyword_search
from search_core.vector_search import vector_search


def domain_score(url):

    domain=urlparse(url).netloc

    authority={

        "wikipedia":1.0,
        "github":0.9,
        "medium":0.8

    }

    for d in authority:

        if d in domain:
            return authority[d]

    return 0.5



def freshness_score(date):

    try:

        year=int(str(date)[:4])

        age=2026-year

        return math.exp(-age/3)

    except:

        return 0.5




def hybrid_search(query):

    v_results=vector_search(query)

    k_results=keyword_search(query)


    merged={}


    # VECTOR

    for r in v_results:

        url=r.payload["metadata"].get(
            "source_url"
        )

        if not url:
            continue

        merged[url]={

            "title":
            r.payload["metadata"].get(
                "title","Başlık Yok"
            ),

            "url":url,

            "content":
            r.payload.get(
                "page_content",""
            ).replace("\n"," "),

            "vector":
            float(r.score)
        }


    # KEYWORD

    for row in k_results:

        url,title,desc,content,date=row

        text=(content if content else desc)

        text=text.replace("\n"," ")

        if url not in merged:

            merged[url]={

                "title":title,

                "url":url,

                "content":text,

                "vector":0
            }

        merged[url]["keyword"]=1
        merged[url]["date"]=date



    results=[]


    for url,data in merged.items():

        vector=data.get("vector",0)

        keyword=data.get("keyword",0)

        freshness=freshness_score(
            data.get("date","")
        )

        authority=domain_score(url)


        score=(

            vector*0.6
            +keyword*0.2
            +freshness*0.1
            +authority*0.1

        )


        data["score"]=score

        results.append(data)


    return sorted(
        results,
        key=lambda x:x["score"],
        reverse=True
    )[:30]