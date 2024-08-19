# gui_app

홈팁스 데이터 tool with huggingface, autogluon, other - classify priority

20231227 gradio는 ml framework들-과 연동

20230821 사용을 안하는건 아닌데, 분류 성능이 autogluon 버전이 더 좋다

pickdata_hugging_face_text_classification : 100 MB 이상이라 삭제 - G:\공유드라이브\에픽모바일-공유드라이브\공용\_public_workspace공유드라이브\ml-models\pickdata_hugging_face_text_classification

비개발자가 local에서 직접 설치해서 실행하라고 하려고 했는데; 셋팅과정을 해보니 개발자인 사람도 어렵다; \
=> 그냥 웹 접속이 가능하게 docker 인스턴스 띄워주자

## setup, how to use?

아래 내용 순서대로 셋팅하면 큰 문제 없을듯

windows 환경 기준으로, linux macos 환경에서는 조금 다를 수 있음

### conda 셋팅

기본 내용은 root project root dir/README.md 확인

```shell
## conda env가 base 사용시 기준
conda env update -n base --file environment.yml
## OR using conda-lock.yml
conda env update -n base --file conda-lock.yml

## Or update a specific environment without activating it:
conda env update --name envname --file environment.yml

## conda-lock 실행시 한글주석이 encoding error가 발생함 -> 한글주석 삭제한 conda-env.yml 파일 생성
python .\utils\yaml_delete_comment.py --inputfile .\environment.yml --outputfile .\environment-delcomment.yml
## https://conda.github.io/conda-lock/output/
## Conda lock's default output format is a unified multi-platform lockfile.
conda-lock --file .\environment-delcomment.yml
```

### poetry 셋팅

기본 내용은 root project root dir/README.md 확인

```shell
poetry install   # 기본적으로 install은 전체 설치이기 때문에, with을 추가해도 전체설치와 동일한 결과
poetry install —without dev    # 명시한 group dependencies를 제외하여 설치합니다.
poetry install --only main,group    # 명시한 group dependencies를 포함하여 설치하나 —only는 main도 제외하기 때문에 주의해야 합니다.
```

### gradio, streamlit 셋팅

기본 내용은 root project root dir/README.md 확인

gradio streamlit 중 딱 하나만 사용하는게 아니고, 둘다 사용할수도 있을듯

=> 단순 다중 페이지가 필요하면 streamlit, ml framework 연동이 필요하면 gradio

#### gradio

multi page가 안됨. page 전환 대안으로 [tab](https://www.gradio.app/docs/tab)이 있긴함

gradio는 1page 1interface 임. 20231227 multipage app지원안함. \
tabbed interface는 tab위젯 형식으로 여러가지 페이지 이용이 가능하긴한데, 1page기준이라 많은 페이지를 만들수는 없다;

[Blocks] Need for multiple separate interfaces - https://github.com/gradio-app/gradio/issues/450 \
2022년11월 Support multiple pages in a gradio app - https://github.com/gradio-app/gradio/issues/2654 \
=> gradio 개발팀에서 multipage 지원에 대해서 긍정적이지는 않은듯;

[gradio custom component](https://www.gradio.app/guides/custom-components-in-five-minutes) 가 있다고 하지만, \
백앤드 프론트 code 전부 개발해야되서, page같은 기능을 직접 개발하기에는 streamlit 대비 손이 너무 많이감;

ml framework나 huggingface와 integration이 streamlit 대비 많이 되어 있음 https://www.gradio.app/guides/using-hugging-face-integrations

#### streamlit

페이지 정렬 순서-방식: https://docs.streamlit.io/develop/concepts/multipage-apps/pages-directory#how-pages-are-sorted-in-the-sidebar \

```dockerfile
## dockerfile 기준이지만, shell에서도 똑같음
# 이렇게 실행하면 ModuleNotFoundError: No module named 'gui_app' 발생;
# CMD ["streamlit" "run", "./src/streamlit/streamlit_app_mainpage.py"]

## 이렇게 실행하면 import path문제 없이 정상실행됨
## 명령어 실행path: hometips-ai-flow-models\gui_app
CMD ["python" "-m", "streamlit" "run", "./gui_app/streamlit/streamlit_app_mainpage.py"] \
```

```shell
## https://docs.streamlit.io/library/advanced-features/configuration
## windows 환경에서 개발테스트시 불편사항: PYTHON_ENV=staging  같은 패턴의 실행 전 환경변수 삽입방법은 linux 에서만 작동함, windows 에서는 실행전 환경변수 삽입이 조금 다름
PYTHON_ENV=staging python -m streamlit run ./gui_app/streamlit/streamlit_app_mainpage.py --server.runOnSave true
PYTHON_ENV=production python -m streamlit run ./gui_app/streamlit/streamlit_app_mainpage.py --server.port 8080

## => poe(poethepoet) 이용해서 편리하게 crossenv 같은 환경변수 삽입 + env파일 함께 적용해서 코드 실행가능함
poetry run poe streamlit_start_staging
```

multipage 개발가능. 1file 1page로 개발구조가 직관적임. 10page 이상 대량 페이지도 개발관리 쉬울듯 - https://discuss.streamlit.io/t/trick-simple-multpage/26121/4

ml framework 연동은 gradio 보다는 안되어 있음 - ml framework연동을 못하는건 아니지만, hf hub 같은 연동시 각종기능을 직접 개발해야됨

page

### docker셋팅

./Dockerfile 참고

## references

https://huggingface.co/spaces/katanaml/table-query/blob/main/app/tapas.py

https://www.gradio.app/playground

https://github.com/crxi/multipage_streamlit
