import json

# 중복 제거할 필드 목록 (이 필드들은 최하위 노드에만 존재해야 함)
fields_to_deduplicate = [
    "lang",
    "review_count",
    "review_result",
    "deleted",
    "rank",
    "synthetic",
    "model_name",
    "detoxify",
    "message_tree_id",
    "tree_state",
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
            # 최상위 노드로 추가
            tree[message_id] = message
            tree[message_id]['replies'] = []
        else:
            # 부모 메시지를 찾아서 자식으로 추가
            parent = message_map.get(parent_id)
            if parent:
                if 'replies' not in parent:
                    parent['replies'] = []
                parent['replies'].append(message)

    # 트리 구조를 리스트로 변환
    return [tree[message_id] for message_id in tree]


# 필드를 최하위 노드로만 남기고, 상위 노드에서는 제거하는 함수
def deduplicate_fields(node):
    if 'replies' in node and node['replies']:
        for reply in node['replies']:
            deduplicate_fields(reply)

        # 자식 노드들이 모두 처리된 후, 부모 노드에서 중복 필드 제거
        for field in fields_to_deduplicate:
            if field in node:
                del node[field]


# 파일에서 JSON 데이터를 읽어옴
with open('../../data/sample_preprocessor/result.json', 'r', encoding='utf-8') as infile:
    data = json.load(infile)

# 트리 구조를 생성
tree = build_tree(data)

# 필드 중복 제거
for root in tree:
    deduplicate_fields(root)

# 결과를 출력 파일로 저장
with open('../../data/sample_preprocessor/result2.json', 'w', encoding='utf-8') as outfile:
    json.dump(tree, outfile, ensure_ascii=False, indent=2)

print("처리가 완료되었습니다.")
