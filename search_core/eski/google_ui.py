import streamlit as st

def google_header():

    st.markdown(
    """
    <h1 style='text-align:center;font-size:60px'>
    SpaceSearch
    </h1>
    """,
    unsafe_allow_html=True
    )


def google_search_box():

    col1,col2,col3=st.columns([1,2,1])

    with col2:

        query=st.text_input(
            "",
            placeholder="SpaceSearch'te Ara",
            label_visibility="collapsed"
        )

    return query



def show_results(results):

    st.markdown("---")

    for r in results:

        st.markdown(
        f"""
### [{r['title']}]({r['url']})

{r['url']}

{r['content'][:250]}...
"""
        )


def show_ai(answer,suggestions):

    st.markdown("## 🤖 AI Cevap")

    st.write(answer)

    st.markdown("---")

    st.markdown("## 🔎 AI Önerileri")

    st.write(suggestions)