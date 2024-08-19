import os
import streamlit as st
from elasticsearch import Elasticsearch
import pandas as pd
from io import BytesIO
import base64
from utils.logger import set_logger
import utils.config
import json

logger = set_logger('gui_app/streamlit/pages/3_htdata_query_page')

# os.getenv("ELASTICSEARCH_API_URL")
# os.getenv("ELASTICSEARCH_API_AUTH")

## https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config
## This must be the first Streamlit command used on an app page, and must only be set once per page.
st.set_page_config(
    # page_title="Ex-stream-ly Cool App",
    # page_icon="🧊",
    layout="wide",
    # initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)

## https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/connecting.html#auth-bearer
# Set up Elasticsearch connection
# es = Elasticsearch(['http://localhost:9200'])

## streamlit 에서는 global 변수가 값이 유지가 안됨; 그냥 st.session변수 사용하기
# --- I don't understand the necessity of this line. But it is needed
#    to preserve session_state in the cloud. Not locally.
# st.session_state.update(st.session_state)
# if 'es_instance' not in st.session_state:
#     st.session_state.es_instance = None
# global es_instance
# es_instance = None
# es = {}
#     # 'http://localhost:9200',
#     os.getenv("ELASTICSEARCH_API_URL"),
#     # bearer_auth=os.getenv("ELASTICSEARCH_API_AUTH"),
#     basic_auth=(os.getenv("ELASTICSEARCH_USERNAME"), os.getenv("ELASTICSEARCH_USER_PASSWORD"))
#     # ca_certs="/path/to/http_ca.crt",
# )


# def query_es(index, queryBody, size, from_, knn):
# """_summary_
# Args:
#     index (_type_): _description_
#     query (_type_): _description_
#     size (_type_): _description_
#     from_ (_type_): _description_
#     knn (object): https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html
#     fields (object):
# """

# def recreate_es_instance(old_es_instance, new_api_url, new_username, new_password):
#     # Get the current connection information
#     old_connection_info = old_es_instance.info()

#     # Check if the new connection information is different
#     if old_connection_info['url'] != new_api_url or old_connection_info['username'] != new_username:
#         # If it is, recreate the Elasticsearch instance
#         new_es_instance = Elasticsearch(
#             [new_api_url],
#             # http_auth=(new_username, new_password),
#             basic_auth=(new_username, new_password)
#         )
#         return new_es_instance


# def query_es(current_es_instance, es_url, es_username, es_userpass, index, queryBody):
def query_es(es_url, es_username, es_userpass, index, queryBody):
    """
    global 변수로 es_instance를 사용하면, streamlit에서는 값이 유지가 안됨;
    st.session변수로 es_instance를 사용해도, streamlit 에서는 값이 유지가 안됨;
    => 그냥 request 할때마다 es_instance 새로 생성해서 사용하는게 좋을듯
    https://elasticsearch-py.readthedocs.io/en/master/
    https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html

    Args:

    Returns:
        df: pd.DataFrame
    """

    ## 빈문자열"" None 할당은, in globals() 구문에서 true 로 인식됨
    # global es_instance
    # es_instance = st.session_state.es_instance

    # if os.getenv("ELASTICSEARCH_API_URL") is None:
    #     logger.error("ELASTICSEARCH_API_URL is not set")
    #     return

    # Recreate the Elasticsearch instance if the connection information has changed
    # if es_instance is None or es_instance.info()['url'] != es_url or es_instance.info()['username'] != es_username:
    # if 'my_var' in locals() and my_var is not None:
    # if current_es_instance is None or current_es_instance.info()['url'] != es_url or current_es_instance.info()['username'] != es_username:
    #     current_es_instance = Elasticsearch(
    #         [es_url],
    #         # http_auth=(es_username, es_userpass or os.getenv("ELASTICSEARCH_USER_PASSWORD")),
    #         basic_auth=(es_username, es_userpass or os.getenv("ELASTICSEARCH_USER_PASSWORD")),
    #     )
    ## https://github.com/elastic/elasticsearch-py/issues/223
    ## https://elasticsearch-py.readthedocs.io/en/master/connection.html#connection-pool
    ## 일반 connection은 미사용시 가비지 컬렉션으로 삭제됨. connection_pool은 명시적으로 close 가능
    es_instance = Elasticsearch(
        [es_url],
        # http_auth=(es_username, es_userpass or os.getenv("ELASTICSEARCH_USER_PASSWORD")),
        basic_auth=(es_username, es_userpass or os.getenv("ELASTICSEARCH_USER_PASSWORD")),
    )
    # es = Elasticsearch(
    #     # 'http://localhost:9200',
    #     os.getenv("ELASTICSEARCH_API_URL"),
    #     # bearer_auth=os.getenv("ELASTICSEARCH_API_AUTH"),
    #     basic_auth=(os.getenv("ELASTICSEARCH_USERNAME"), os.getenv("ELASTICSEARCH_USER_PASSWORD"))
    #     # ca_certs="/path/to/http_ca.crt",
    # )

    # Query Elasticsearch
    res = es_instance.search(index=index, body=queryBody)
    ## https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_creating_an_index
    ## https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html#paginate-search-results
    ## https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/01-keyword-querying-filtering.ipynb
    # res = es.search(index=index, query=query, size=size, from_=from_, knn=knn)

    # Convert results to DataFrame
    df = pd.DataFrame([doc['_source'] for doc in res['hits']['hits']])
    return df


def delete_streamlit_elements(elements):
    for element in elements:
        # st.session_state[element].empty()
        element.empty()


# def es_querytext_parse_to_json(text):
def check_querybody_text_isjson():
    """
    https://docs.streamlit.io/library/advanced-features/session-state#example-3-use-args-and-kwargs-in-callbacks
    """
    # Attempt to parse input as JSON
    # text = clean_json_string(st.session_state.query_body)
    # text = txt or st.session_state.query_body
    text = st.session_state.query_body

    try:
        query_json = json.loads(text)
        status = True
        ## success, error는 버튼누르면 사라지는게 없음; -> 그냥 button으로 알림띄우기 - 누르면 알림element 전부 삭제되게
        # st.success("QueryBody text is valid JSON")
        jsonviewer = st.json(query_json)
    except json.JSONDecodeError:
        status = False
        # st.error("The input is not valid JSON")

    ## label color: https://docs.streamlit.io/1.20.0/library/api-reference/text/st.markdown#stmarkdown
    label = ""
    if status:
        label = ":green[QueryBody text is valid JSON - 클릭시 삭제됨]"
    else:
        label = ":red[QueryBody text is not valid JSON - 클릭시 삭제됨]"

    button = st.button(label)
    if button:
        delete_streamlit_elements([button, jsonviewer])


def clean_json_string(json_string):
    # Load the JSON string into a Python object
    data = json.loads(json_string)

    # Convert the Python object back into a JSON string, without whitespace
    clean_json_string = json.dumps(data, separators=(',', ':'))

    return clean_json_string


with st.container():

    col1, col2 = st.columns(2)

    with col1:
        # Get user input for index, query, size, and page number
        elasticsearch_url = st.text_input('elasticsearch_url', value=os.getenv("ELASTICSEARCH_API_URL"))
        elasticsearch_username = st.text_input('elasticsearch_username', value='elastic')
        elasticsearch_password = st.text_input('elasticsearch_password', value="", type='password')

    with col2:
        es_index = st.text_input('ES_Index', value='your_elasticsearch_index_name - ex> cities_table')
        ## https://docs.streamlit.io/library/api-reference/widgets/st.number_input
        dataframe_height = st.number_input('dataframe_height', min_value=1, max_value=10000, value=500, key="dataframe_height")

# if 'query_body' not in st.session_state:
#     st.session_state.query_body = ''
query_body = st.text_area('ES_QueryBody', value='{"query": {"match_all": {}}}', on_change=check_querybody_text_isjson, key="query_body")
#   args=(st.session_state["query_body"], ))
# size = st.number_input('Size', min_value=1, max_value=10000, value=10)
# page = st.number_input('Page', min_value=1, value=1)
# Calculate from_ parameter for Elasticsearch
# from_ = (page - 1) * size

# Query Elasticsearch
# df = query_es(index, {"query": {"match_all": {}}}, size, from_)
# df = query_es(index, query_body)

# Initialize session state for dataframe if it doesn't exist
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

# Add "Play Query" button
if st.button('Play Query'):
    data = json.loads(clean_json_string(query_body))
    st.session_state.df = query_es(elasticsearch_url, elasticsearch_username, elasticsearch_password, es_index, data)

## https://docs.streamlit.io/library/api-reference/session-state
## 2023 st Session State basics https://www.youtube.com/watch?v=92jUAXBmZyU&list=TLGGYqrRVqMdT0wyOTAxMjAyNA&t=372s
# Display DataFrame in Streamlit
# st.dataframe(df)
st.dataframe(st.session_state.df, height=st.session_state.dataframe_height)


# def convert_dataframe_to_excel(df):
#     # Convert DataFrame to Excel
#     excel_file = BytesIO()
#     df.to_excel(excel_file, index=False)
#     excel_file.seek(0)
#     excel_data = excel_file.read()

# # Create download link for Excel file
# st.download_button(
#     label="Download data as Excel",
#     on_click=
#     data=excel_data,
#     file_name='data.xlsx',
#     mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
# )
