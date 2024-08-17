"""
https://docs.streamlit.io/library/api-reference/layout/st.tabs
"""

import streamlit as st

# import gui_app.src.htdata_category_autogluon_tabularpredictor as htdata_category_at_tp
# import gui_app.htdata_category_autogluon_tabularpredictor as htdata_category_at_tp
# # import htdata_category_autogluon_tabularpredictor as htdata_category_at_tp
# import gui_app.htdata_pickdata_autogluon_tabularpredictor as htdata_pick_at_tp
# import gui_app.htdata_pickdata_huggingface_text_classification as htdata_pick_hf_text_cla


tab1, tab2 = st.tabs(["oasst_maker", "oasst_preprocessing"])

# @st.cache_data
with tab1:
    ## with 쓰면 중복변수 초기화 되는거 맞나?
    st.header("htdata_category_classification")
    st.title("htdata_category_classification")

    #    option = st.radio(
    #         'Select a tab',
    #         ('htdata_category_at_tp', 'htdata_pick_at_tp', 'htdata_pick_hf_text_cla')
    #     )

    #    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
    #    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    ## https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader


with tab2:
    st.header("htdata_pickdata_classification")
    #    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
    st.title("Choose an algorithm")

    ## https://docs.streamlit.io/library/api-reference/widgets/st.radio


# if __name__ == "__main__":
#     main()
