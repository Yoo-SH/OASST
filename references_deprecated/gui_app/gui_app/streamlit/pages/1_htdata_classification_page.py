"""
https://docs.streamlit.io/library/api-reference/layout/st.tabs
"""

import streamlit as st

# import gui_app.src.htdata_category_autogluon_tabularpredictor as htdata_category_at_tp
# import gui_app.htdata_category_autogluon_tabularpredictor as htdata_category_at_tp
# # import htdata_category_autogluon_tabularpredictor as htdata_category_at_tp
# import gui_app.htdata_pickdata_autogluon_tabularpredictor as htdata_pick_at_tp
# import gui_app.htdata_pickdata_huggingface_text_classification as htdata_pick_hf_text_cla


tab1, tab2 = st.tabs(["htdata_category", "htdata_pickdata"])

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
    uploaded_file = st.file_uploader("Choose an Excel file", type=["csv", "xlsx"], accept_multiple_files=False)

    if uploaded_file is not None:
        execute_query_result = htdata_category_at_tp.execute_query(uploaded_file)
        result_dict = {
            'number': execute_query_result[0],
            'category_result': execute_query_result[1],
            'result': execute_query_result[2],
            'file_txt': execute_query_result[3],
            'file_xlsx': execute_query_result[4],
        }
        #    {
        #         'number': number,
        #         'category_result': category_result,
        #         'result': result,
        #         'file_txt': file_txt,
        #         'file_xlsx': file_xlsx,
        #     }

        with open(result_dict['file_txt'], "rb") as f:
            file_txt = f.read()

        with open(result_dict['file_xlsx'], "rb") as f:
            file_xlsx = f.read()

        st.text(result_dict['number'])
        st.dataframe(result_dict['category_result'])
        st.dataframe(result_dict['result'])
        # st.download_button(label="Download txt file", data=result_dict['file_txt'])
        # st.download_button(label="Download xlsx file", data=result_dict['file_xlsx'])
        st.download_button(label="Download txt file", data=file_txt, file_name=result_dict['file_txt'])
        st.download_button(
            label="Download xlsx file",
            data=file_xlsx,
            file_name=result_dict['file_xlsx'],
        )


with tab2:
    st.header("htdata_pickdata_classification")
    #    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
    st.title("Choose an algorithm")

    ## https://docs.streamlit.io/library/api-reference/widgets/st.radio
    option = st.radio(
        'Select a tab',
        (
            'htdata_pickdata_autogluon_tabularpredictor',
            'htdata_pickdata_huggingface_text_classification',
        ),
    )

    #    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    uploaded_file = st.file_uploader("Choose an Excel file", type=["csv", "xlsx"], accept_multiple_files=False)

    if uploaded_file is not None:
        if option == 'htdata_pickdata_autogluon_tabularpredictor':
            execute_query_result = htdata_pick_at_tp.execute_query(uploaded_file)
        elif option == 'htdata_pickdata_huggingface_text_classification':
            execute_query_result = htdata_pick_hf_text_cla.execute_query(uploaded_file)

        result_dict = {
            'number': execute_query_result[0],
            'category_result': execute_query_result[1],
            'result': execute_query_result[2],
            'file_txt': execute_query_result[3],
            'file_xlsx': execute_query_result[4],
        }

        with open(result_dict['file_txt'], "rb") as f:
            file_txt = f.read()

        with open(result_dict['file_xlsx'], "rb") as f:
            file_xlsx = f.read()

        st.text(result_dict['number'])
        st.dataframe(result_dict['category result'])
        st.dataframe(result_dict['result'])
        st.download_button(label="Download txt file", data=file_txt, file_name=result_dict['file_txt'])
        st.download_button(
            label="Download xlsx file",
            data=file_xlsx,
            file_name=result_dict['file_xlsx'],
        )

# if __name__ == "__main__":
#     main()
