# OASST processor

## references

-- https://www.google.com/search?q=dask+vs+spark+performance

- https://arxiv.org/html/2406.01409v1 2024 Dask와 Apache Spark의 HPC 시스템 성능 비교

- https://www.bing.com/search?q=dask+vaex

- https://github.com/UpstageAI/dataverse 2024 현재 약 50개의 기능이 ETL 프로세스로 등록되어 있으며 \
  dask가 100tb이하 데이터에서는 성능이 더 좋다-메모리 사용량이 spark 대비 작다 뭐 이런얘기가 있는데, 자주쓰는 데이터 전처리모듈 개발해놓은 data처리 라이브러리를 우선적으로 쓰는게 맞음... 데이터처리모듈 모아놓은 오픈소스 라이브러리 생각보다 찾기가 힘드네?(전처리 code가 )

-- https://www.bing.com/search?q=data+preprocessing+code+python+module+opensource

- https://github.com/topics/data-preprocessing?l=python

- https://github.com/elisemercury/AutoClean

- https://github.com/skrub-data/skrub

- https://github.com/bab2min/kiwipiepy (Kiwipiepy, Python용 Kiwi 패키지)

#git
-pip install -r requirements.txt (패키지 버전 통합관리)
-git lfs install ==> git lfs track "\*." (깃 LFS 설치 및 트래킹)
-pip install python-dotenv ==> os.getenv(key), os.environ.get(key) (파일로드 및 환경변수 로드)
