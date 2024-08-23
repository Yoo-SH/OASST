import json

# JSON 파일 경로 설정
input_file = '../../data/sample_preprocessor/naver_result.json'
output_file = '../../data/sample_preprocessor/result3.json'

# 파일을 열고 데이터 로드
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 새로운 메시지 트리를 저장할 리스트
message_tree = []

# 메시지들로 구성된 딕셔너리 생성 (message_id를 키로 사용)
messages = {msg['message_id']: msg for msg in data}

# 중복 필드를 제외할 키 목록
keys_to_remove = ["message_id", "parent_id", "user_id", "creadte_date", "title", "text", "role"]

# 각 메시지에 대해 parent_id를 참조해 계층 구조 설정
for message_id, message in messages.items():
    parent_id = message.get('parent_id')
    if parent_id and parent_id in messages:
        parent_message = messages[parent_id]
        if 'replies' not in parent_message:
            parent_message['replies'] = []

        # 마지막 계층에서는 중복 필드를 유지
        if 'replies' in message and len(message['replies']) > 0:
            # 중복되는 필드 삭제
            for key in keys_to_remove:
                if key in message:
                    message[key] = None
        parent_message['replies'].append(message)
    else:
        message_tree.append(message)

# 트리 구조를 가진 데이터를 JSON으로 저장
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(message_tree, f, ensure_ascii=False, indent=4)
