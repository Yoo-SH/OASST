# oasst-preprocessor

### duckdb

20240807 데이터전처리 생 파이썬코드로 짜면 병렬처리랑 메모리관리가 안되서 처리시간이 너무 오래걸릴 수 있어서, 데이터 병렬처리 라이브러리 duckdb 사용하기, 실행시간 오래 걸리는거도 디버그할때 계속 기다려야되서 문제가 되기 때문에, 개발생산성 향상을 위해서도 code실행시간도 중요함 \
그냥python코드나 pandas 쓰면 메모리가 터져서 왜 안되는지 모르는 문제가 생길수 있을 것 같고... spark는 개발환경셋팅도 무슨 문제가 생길지 모르고, 코드짜는게 10gb이하 작은 데이터셋 처리하기에는 spark전용코드문법을 알아야 되서 복잡함 - 작은데이터는 sql이나 pandas 문법으로 처리가능하면 편하고 좋기 떄문에, **duckdb 사용하기로 결정함**

⇒ duckdb 실무에서 중고나라 같이 상용급으로 쓰고있고, sql은 postgresql syntax준수한다고 하고, code문법은 일반적으로 pandas나 mongodb에서 보던거라 익숙함 \
**=> duckdb 코드가 대중적인 코드라, copilot gpt한테 만들어달라고 하면 크게 작동문제 없을듯**

- https://duckdb.org/docs/installation/index?version=stable&environment=python duckdb 설치방법 - python 개발시 그냥 pip로 설치하면 됨

- https://duckdb.org/docs/api/python/overview duckdb python 개발문서

- https://duckdb.org/docs/sql/introduction duckdb sql 개발문서


#### Python Function API - udf 사용시 유의사항

https://duckdb.org/2023/07/07/python-udf.html DuckDB now supports vectorized Scalar Python User Defined Functions (UDFs)

duckdb 내장함수-내장type을 쓰는것이 가장 빠름, duckdb 뿐만 아니고 모든 병렬분산처리 라이브러리가 똑같은 특징을 가짐

1. 파이썬에서는 객체 생성과 일반적인 사용이 다소 느립니다. 이는 자동 메모리 관리, 해석 및 동적 타이핑을 포함한 여러 가지 이유 때문입니다. 2) PyArrow UDF는 데이터 복사가 필요하지 않습니다. 3) PyArrow UDF는 벡터화된 방식으로 실행되어 개별 행 대신 데이터 청크를 처리합니다.

duckdb에 명확히 나와있지는 않지만, 추정상 pyarrow 처리된 function은 변수type크기 정의를 해줘야되서 개발이 귀찮아지고, 디버그 하기가 힘들것임 \
**=> udf를 pyarrow 처리 하기전에, 일반 python function으로 개발-테스트 완료하기**


#### DBeaver 연결

다양한 connector를 제공하는 DBeaver와도 연결이 가능하다.

MEMORY 버전과 .db 파일 연동 둘 다 가능하며, read_only 사용 시는 이미지처럼 driver properties에서 duckdb.read_only 값을 적용해주어야 한다.

https://duckdb.org/docs/guides/sql_editors/dbeaver.html


#### 타 데이터프레임과 호환

DuckDB의 가장 큰 장점은 Pandas, Delta Table, Polars, Vaex의 데이터 프레임과 호환이 된다. Apache Arrow 포맷을 따르기 때문이다.

pandas의 경우, 데이터프레임 변수 이름을 그대로 테이블명으로 사용할 수 있다.

다른 데이터 프레임은 arrow_table로 변환하면 테이블명으로 사용할 수 있다.

```python
df = pd.read_csv( ... )
conn.sql(
    f"""
    SELECT * FROM df LIMIT 10
    """
)
```

### Connection

DuckDB는 다른 데이터베이스들과 마찬가지로 connection을 만들어 재사용할 수 있다. 각 connection은 쿼리 실행에 필요한 데이터 및 메타데이터를 메모리에 캐시해두었다가 연결이 끊기면 날려버리므로, 작은 쿼리를 여러번 실행시켜야 하는 경우에는 connection을 유지하는 것이 성능에 좋다.

보통은 하나의 connection만 사용하는 것이 좋지만 connection pool을 만들어 여러 connection들을 사용하는 것도 가능하다. DuckDB는 이미 각 쿼리를 실행시키기 위해 병렬성을 충분히 활용하도록 설계되어 있지만, 모든 케이스에 대해 병렬 처리를 적용하는 것은 불가능하다. 따라서 만약 CPU 사용률이 널널하고, 네트워크 전송 속도 등이 병목의 원인이라면 여러 connection을 만들어 동시성을 확보하는 것도 도움이 될 것이다.

팁) Python에서 사용되는 DuckDBPyConnection은 thread-safe하지 않다. 또한 single connection을 사용하더라도 쿼리가 실행되는 동안 lock이 걸린다. 따라서 multi-thread 환경에서서 데이터베이스에 접근하기 위해서는 위해서는 .cursur() 메서드를 호출해 각 thread마다 cursor를 만들어 주어야 한다.



## references

-- https://www.notion.so/epicmoble/duckdb-654337d04ae149bd9b63ceca783d56e1?pvs=4#4d56bf6609a54734bed183641045e014 duckdb 데이터프로세싱 기술 관련자료

-- https://github.com/epicmobile18/hometips-ai-flow-models

-- https://github.com/epicmobile18/RB-ScrapyServer

-- https://www.google.com/search?q=dask+vs+spark+performance

- https://arxiv.org/html/2406.01409v1 2024 Dask와 Apache Spark의 HPC 시스템 성능 비교
- https://www.bing.com/search?q=dask+vaex
- https://github.com/UpstageAI/dataverse 2024 현재 약 50개의 기능이 ETL 프로세스로 등록되어 있으며 \
  dask가 100tb이하 데이터에서는 성능이 더 좋다-메모리 사용량이 spark 대비 작다 뭐 이런얘기가 있는데, 자주쓰는 데이터 전처리모듈 개발해놓은 data처리 라이브러리를 우선적으로 쓰는게 맞음... 데이터처리모듈 모아놓은 오픈소스 라이브러리 생각보다 찾기가 힘드네?(전처리 code가 )
- https://docs.coiled.io/blog/tpch.html
- https://spark.apache.org/docs/latest/api/python/user_guide/sql/arrow_pandas.html ~~그렇게 좋은방법 같아보이지는 않는데..;~~ \
  => [spark, dask, duckdb] 끼리 대용량-GB단위 이상 연동시키고 싶으면, 그냥 parquet로 파일로 저장하고 다시 읽는 방식으로 사용하기
- https://www.google.com/search?q=arrow+vs+parquet
- https://medium.com/@diehardankush/comparing-data-storage-parquet-vs-arrow-aa2231e51c8a 2023
- https://medium.com/@diehardankush/feather-vs-pickle-a-comparative-analysis-of-data-storage-a5aa113a00a3 2023
- https://www.google.com/search?q=apache+arrow+parquet

- https://docs.pola.rs/user-guide/misc/comparison/

-- https://motherduck.com/blog/duckdb-versus-pandas-versus-polars/

- https://duckdb.org/2021/05/14/sql-on-pandas.html
- https://yahwang.github.io/posts/100 2023 duckdb 기본사용법
- https://ivoryrabbit.github.io/posts/DuckDB/ 2024 duckdb 팁 설명 한글
- https://duckdblabs.github.io/db-benchmark/
- https://github.com/davidgasquez/awesome-duckdb
- https://www.google.com/search?q=duckdb+udf+benchmark+performance

-- https://www.bing.com/search?q=data+preprocessing+code+python+module+opensource

- https://github.com/topics/data-preprocessing?l=python
- https://github.com/elisemercury/AutoClean
- https://github.com/skrub-data/skrub

- https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/


-- https://github.com/bab2min/kiwipiepy (Kiwipiepy, Python용 Kiwi 패키지)
```shell
#git

-pip install -r requirements.txt (패키지 버전 통합관리)

-git lfs install ==> git lfs track "\*." (깃 LFS 설치 및 트래킹)

-pip install python-dotenv ==> os.getenv(key), os.environ.get(key) (파일로드 및 환경변수 로드)
```