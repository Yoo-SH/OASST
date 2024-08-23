import json


def iterative_dfs(message_tree: list, keys_to_remove: list):
    """
    비재귀 DFS를 사용하여 트리를 순회하면서 중복 필드를 하위 메시지로 이동합니다.

    Args:
        message_tree (list): 메시지 트리 리스트
        keys_to_remove (list): 이동할 중복 필드의 키 목록
    """
    stack = list(message_tree)  # 스택에 트리의 모든 최상위 메시지를 추가
    while stack:
        message = stack.pop()

        # 현재 노드에서 상속받은 필드를 저장
        fields = {key: message[key] for key in keys_to_remove if key in message}

        # 현재 노드에서 상속받은 필드를 제거
        for key in fields:
            del message[key]

        # 현재 노드에 필드와 값을 추가
        if 'replies' not in message:
            for key, value in fields.items():
                if key not in message:
                    message[key] = value

        # 하위 메시지에 필드와 값을 추가
        if 'replies' in message:
            for reply in message['replies']:
                # 하위 메시지에 필드를 추가
                reply.update(fields)
                stack.append(reply)


def load_and_process_json(input_file: str, output_file: str) -> None:
    """
    주어진 JSON 파일을 읽고, 중복된 필드를 하위 메시지로 이동시키는 트리 구조로 변환한 후,
    결과를 새로운 JSON 파일로 저장합니다.

    Args:
        input_file (str): 입력 JSON 파일의 경로
        output_file (str): 결과를 저장할 JSON 파일의 경로
    """
    # 파일을 열고 데이터 로드
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 메시지들로 구성된 딕셔너리 생성 (message_id를 키로 사용)
    messages = {msg['message_id']: msg for msg in data}

    keys_to_remove = [
        'review_count',
        'review_result',
        'deleted',
        'rank',
        'synthetic',
        'model_name',
        'detoxify',
        'message_tree_id',
        'tree_state',
        'emojis',  # sequence
        'lavels',
        'link',
        '변호사명',
        '작업자명',
        '작업일자',
        '사용여부',
        'lang',
    ]

    # 새로운 메시지 트리를 저장할 리스트
    message_tree = []

    # 각 메시지에 대해 parent_id를 참조해 계층 구조 설정
    for message_id, message in messages.items():
        parent_id = message.get('parent_id')
        if parent_id and parent_id in messages:
            parent_message = messages[parent_id]
            if 'replies' not in parent_message:
                parent_message['replies'] = []

            # 부모 메시지의 'replies'에 현재 메시지를 추가

            parent_message['replies'].append(message)
        else:
            # 부모가 없는 메시지(즉, 최상위 메시지)는 트리에 추가
            message_tree.append(message)

    # 중복 필드를 하위 메시지로 이동시키기
    iterative_dfs(message_tree, keys_to_remove)

    # 트리 구조를 가진 데이터를 JSON으로 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(message_tree, f, ensure_ascii=False, indent=4)


# 실행
load_and_process_json('../../data/sample_preprocessor/naver_result.json', '../../data/sample_preprocessor/naver_result_tree.json')
