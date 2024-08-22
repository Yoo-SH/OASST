import json

# 주어진 JSON 데이터
data = json.loads(
    '''[
    {
        "message_id": "d030368f-fe60-43fb-a359-2b33e4a519d4",
        "parent_id": "null",
        "user_id": "e339f8bd-509b-4d5b-949b-144adf79b22e",
        "creadte_date": "2024-08-07T10:51:20.004950+09:00",
        "title": "SNS에서 미성년자의 나체사진을 받았을 때 처벌 가능성.",
        "text": "SNS에서 미성년자의 나체사진을 받완주았을 완주 때 처벌 가능완주성.",
        "사용여부": "None",
        "role": "prompter",
        "lang": "ko",
        "review_count": 0,
        "review_result": "null",
        "deleted": false,
        "rank": "null",
        "synthetic": false,
        "model_name": "null",
        "detoxify": "{ toxicity: 0.0 severe_toxicity: 0.0 obscene: 0.0 identity_attack: 0.0 insult: 0.0 threat: 0.0 sexual_explicit: 0.0 }",
        "message_tree_id": "d030368f-fe60-43fb-a359-2b33e4a519d4",
        "tree_state": "ready_for_export",
        "emojis": "{ name: [ _skip_labeling ] count: [ 2 ] }",
        "lavels": "{ name: [ spam lang_mismatch pii not_appropriate hate_speech sexual_content quality toxicity humor creativity violence ] value: [ 0 0 0 0 0 0 0.5833333333333334 0.08333333333333333 0.08333333333333333 0.4166666666666667 0 ] count: [ 3 3 3 3 3 3 3 3 3 3 3 ] }",
        "link": "https://www.lawtalk.co.kr/qna/433554",
        "변호사명": ""
    },
    {
        "message_id": "ff20b62a-e39f-4214-84b5-9b32d43290b3",
        "parent_id": "d030368f-fe60-43fb-a359-2b33e4a519d4",
        "user_id": "edfab322-50ac-4573-b5c1-471392559694",
        "creadte_date": "2024-08-07T10:51:19.984000+09:00",
        "title": "null",
        "text": "실제 상대방과의 대화 내용 등에 대한 검토가 필요해 보입니다. 기재하신 교환 등의 단어가 다른 대화 등을 통해 신체 사진인 것을 유추할 수 있다면 문제의 소지가 있으므로 연락 주시면 작성자분의 사안을 상세히 확인 후해결에 도움이 되는 전문 변호인을 보유한 저희 법무전주법 인에서 전주성심껏 안내 도와 드리 겠습니다.",
        "사용여부": "None",
        "role": "assistant",
        "lang": "ko",
        "review_count": 0,
        "review_result": "null",
        "deleted": false,
        "rank": "null",
        "synthetic": false,
        "model_name": "null",
        "detoxify": "{ toxicity: 0.0 severe_toxicity: 0.0 obscene: 0.0 identity_attack: 0.0 insult: 0.0 threat: 0.0 sexual_explicit: 0.0 }",
        "message_tree_id": "d030368f-fe60-43fb-a359-2b33e4a519d4",
        "tree_state": "ready_for_export",
        "emojis": "{ name: [ _skip_labeling ] count: [ 2 ] }",
        "lavels": "{ name: [ spam lang_mismatch pii not_appropriate hate_speech sexual_content quality toxicity humor creativity violence ] value: [ 0 0 0 0 0 0 0.5833333333333334 0.08333333333333333 0.08333333333333333 0.4166666666666667 0 ] count: [ 3 3 3 3 3 3 3 3 3 3 3 ] }",
        "link": "https://www.lawtalk.co.kr/qna/433554",
        "변호사명": "장휘일 변호사"
    },
    {
        "message_id": "ff18fad6-c926-4ff5-b1fc-9d22f82529a8",
        "parent_id": "null",
        "user_id": "44053743-2fac-4d62-81f4-2b9c6e9e7e73",
        "creadte_date": "2024-08-07T10:51:19.984000+09:00",
        "title": "혼인관계와 상간 피소에 대한 문의.",
        "text": "혼인관계와 상간 피소에 대한 문의.",
        "사용여부": "None",
        "role": "prompter",
        "lang": "ko",
        "review_count": 0,
        "review_result": "null",
        "deleted": false,
        "rank": "null",
        "synthetic": false,
        "model_name": "null",
        "detoxify": "{ toxicity: 0.0 severe_toxicity: 0.0 obscene: 0.0 identity_attack: 0.0 insult: 0.0 threat: 0.0 sexual_explicit: 0.0 }",
        "message_tree_id": "ff18fad6-c926-4ff5-b1fc-9d22f82529a8",
        "tree_state": "ready_for_export",
        "emojis": "{ name: [ _skip_labeling ] count: [ 2 ] }",
        "lavels": "{ name: [ spam lang_mismatch pii not_appropriate hate_speech sexual_content quality toxicity humor creativity violence ] value: [ 0 0 0 0 0 0 0.5833333333333334 0.08333333333333333 0.08333333333333333 0.4166666666666667 0 ] count: [ 3 3 3 3 3 3 3 3 3 3 3 ] }",
        "link": "https://www.lawtalk.co.kr/qna/433713",
        "변호사명": ""
    },
    {
        "message_id": "1c893c8e-f240-4ea3-abbe-43df05ed8b84",
        "parent_id": "ff18fad6-c926-4ff5-b1fc-9d22f82529a8",
        "user_id": "7ab861bb-96bc-450e-9f52-b3ad4940e263",
        "creadte_date": "2024-08-07T10:51:19.984000+09:00",
        "title": "null",
        "text": "안녕하세요 대한변호사협회 인증 가사전문변호사 오엔법률사무소 대표변호사입니다. 1. 상간소송 가능하고 위자료 배상책임 인정됩니다. 2. 참작되는 사유입니다. 그러나 외도 자체를 부인할 수는 없습니다. 3. 위자료는 잘 방어하면 1500 안팎이 될 것 같은데 원고가 제출하는 증거가 중요합니다. 관련해서 연락주시면 향후절차나 대응방향 등에 대해 상세히 안내드리겠습니다.",
        "사용여부": "None",
        "role": "assistant",
        "lang": "ko",
        "review_count": 0,
        "review_result": "null",
        "deleted": false,
        "rank": "null",
        "synthetic": false,
        "model_name": "null",
        "detoxify": "{ toxicity: 0.0 severe_toxicity: 0.0 obscene: 0.0 identity_attack: 0.0 insult: 0.0 threat: 0.0 sexual_explicit: 0.0 }",
        "message_tree_id": "ff18fad6-c926-4ff5-b1fc-9d22f82529a8",
        "tree_state": "ready_for_export",
        "emojis": "{ name: [ _skip_labeling ] count: [ 2 ] }",
        "lavels": "{ name: [ spam lang_mismatch pii not_appropriate hate_speech sexual_content quality toxicity humor creativity violence ] value: [ 0 0 0 0 0 0 0.5833333333333334 0.08333333333333333 0.08333333333333333 0.4166666666666667 0 ] count: [ 3 3 3 3 3 3 3 3 3 3 3 ] }",
        "link": "https://www.lawtalk.co.kr/qna/433713",
        "변호사명": "박종원 변호사"
    }
]'''
)

# 지정된 필드들
fields_to_deduplicate = [
    "사용여부",
    "role",
    "lang",
    "review_count",
    "review_result",
    "deleted",
    "rank",
    "synthetic",
    "model_name",
    "detoxify",
    "message_tree_id",
    "emojis",
    "lavels",
    "link",
    "변호사명",
]


# 부모-자식 관계를 구성하는 함수
def build_tree(messages):
    message_map = {msg['message_id']: msg for msg in messages}
    tree = {}
    for message in messages:
        message_id = message['message_id']
        parent_id = message['parent_id']
        if parent_id == "null":
            tree[message_id] = message
            tree[message_id]['replies'] = []
        else:
            parent = message_map.get(parent_id)
            if parent:
                if 'replies' not in parent:
                    parent['replies'] = []
                parent['replies'].append(message)
    return [tree[message_id] for message_id in tree]


# 하위 노드로 필드들을 이동시키는 함수
def deduplicate_fields(node):
    if 'replies' in node and node['replies']:
        for reply in node['replies']:
            for field in fields_to_deduplicate:
                if field in node:
                    reply[field] = node.pop(field)
            deduplicate_fields(reply)
    elif 'replies' in node:
        deduplicate_fields(node['replies'])


# 트리 구조를 생성
tree = build_tree(data)

# 필드 중복 제거
for root in tree:
    deduplicate_fields(root)

# 결과 출력 (또는 파일로 저장할 수 있습니다)
result = json.dumps(tree, ensure_ascii=False, indent=2)
print(result)
