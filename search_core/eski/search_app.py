import sys
from pathlib import Path

# Şu anki dosyanın bulunduğu klasörü bul ve bir üst klasöre git
base_path = Path(__file__).resolve().parent.parent 
sys.path.append(str(base_path))

import streamlit as st

from search_core.search_engine import SearchEngine
from search_core.ai_module import AISystem
from search_core.google_ui import *

st.set_page_config(
    page_title="SpaceSearch",
    layout="wide"
)

engine=SearchEngine()
ai=AISystem()

google_header()

query=google_search_box()


if query:

    with st.spinner("Aranıyor..."):

        results=engine.hybrid_search(query)


    tab1,tab2=st.tabs([

        "AI",

        "Sonuçlar"

    ])


    with tab1:

        answer=ai.answer(query,results)

        sug=ai.suggestions(query,results)

        show_ai(answer,sug)


    with tab2:

        show_results(results)