from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage,SystemMessage

class AISystem:

    def __init__(self):

        self.llm=ChatOllama(
            model="gemma3:4b",
            temperature=0.3
        )

    # -------- AI ANSWER --------

    def answer(self,query,results):

        context="\n\n".join([

            f"{r['title']}\n"
            f"{r['content'][:800]}\n"
            f"LINK:{r['url']}"

            for r in results[:5]

        ])


        sys="""

Sen Google benzeri bir arama motoru AI'sısın.

Cevap yapısı:

Özet

Detaylı açıklama

Kaynaklar (Linkleri listele)

"""


        user=f"""

Soru:

{query}

Veriler:

{context}

"""


        res=self.llm.invoke([

            SystemMessage(content=sys),

            HumanMessage(content=user)

        ])


        return res.content


    # -------- AI SUGGEST --------

    def suggestions(self,query,results):

        context="\n".join([

            f"{r['title']} -> {r['url']}"

            for r in results[:10]

        ])


        prompt=f"""

Kullanıcı:

{query}

Aşağıdaki sitelerden yararlanarak 5 öneri yap.

Format:

Başlık - Link

Veriler:

{context}

"""


        res=self.llm.invoke([

            HumanMessage(content=prompt)

        ])

        return res.content