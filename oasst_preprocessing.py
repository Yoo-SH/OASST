# -*- coding: utf-8 -*-
import pandas as pd
from kiwipiepy import Kiwi, Match
from kiwipiepy.utils import Stopwords


#kiwi 생성자 정보 Kiwi(num_workers=0, model_path=None, load_default_dict=True, integrate_allomorph=True, model_type='knlm', typos=None, typo_cost_threshold=2.5)

kiwi = Kiwi()
sentences = "안녕하세요. 최선을 다하는 이희범 변호사입니다. 1. 우선 상속인, 상속재산이 있었는지 등에 대한 판단이 필요해 보입니다. 2. 동사무소에 방문하여 상속재산 원스톱 서비스 등을 신청하시길 바랍니다.  더 궁금한 점이 있으시면 언제든지 연락 주시면 친절히 상담 드리도록 하겠습니다. [라미 법률사무소 대표 변호사 / 이희범 배상] - 대한 변호사 협회 등록 형사전문 변호사/ 공인 도로교통사고 감정사 - 대한 변호사 협회 등록 학교폭력 전문변호사 / 공인 가맹거래사 - 한 권에 담은 음주운전 사건 사고처리 저자 - 한 권에 담은 개인회생 사건 사고처리 저자 - 한 권에 담은 학교폭력의 바이블 저자"


# 토큰화
tokens = kiwi.tokenize(sentences)

# NNG만 추출
nng_tokens = [token[0] for token in tokens if token[1] == 'NNG']

# 결과 출력
print(f"NNG Tokens: {nng_tokens}")
#print(f"Tokens: {tokens}")