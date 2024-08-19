FROM epicmobile181/hometips-ai-flow-models:base-cpu as builder
## continuumio/miniconda3 - Debian GNU/Linux 11 (bullseye)
##  우분투는 데비안에서 나온 운영체제이며, 우분투에서 볼 수 있는 대부분의 핵심 유틸리티는 데비안에서 나왔습니다
## https://www.google.com/search?q=debian+linux+ubuntu

ENV HOME=${HOME:-/root}

## https://www.google.com/search?q=nginx+install+debian
## https://www.google.com/search?q=docker+nginx+reverse+proxy+subdir+path
## nginx


COPY ./your-script.sh /your-script.sh
RUN chmod +x /your-script.sh
CMD ["/your-script.sh"]

## 이렇게 실행하면 ModuleNotFoundError: No module named 'gui_app' 발생;
# CMD ["streamlit" "run", "./src/streamlit/streamlit_app_mainpage.py"]

## 명령어 실행path: hometips-ai-flow-models\gui_app
# CMD ["python" "-m", "streamlit" "run", "./src/streamlit/streamlit_app_mainpage.py"]


## https://docs.docker.com/config/containers/multi-service_container/ - compose 안쓰고 Dockerfile에서 multi service 돌리는 방법
## 당연히 1docker instnce당 1service 돌리는게 best임, compose로 돌리는게 나을수도 있는데
## compose파일 만드는게 귀찮거나, 실행하는 service들이 무겁게 사용되지 않는경우, 1container에 2service 정도는 돌려도 될듯
## Run multiple processes in a container - Use a wrapper script, Use Bash job controls, Use Bash job controls, Use a process manager
## https://www.bing.com/search?q=docker+run+--init
## https://docs.docker.com/engine/reference/run/#specify-an-init-process
## https://stackoverflow.com/questions/43122080/how-to-use-init-parameter-in-docker-run