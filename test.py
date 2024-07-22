import pandas as pd
import uuid



column_filed = {
    1: 'message_id',  # string
    2: 'parent_id',  # string 
    3: 'user_id',  # string
    4: 'create_date',  # string
    5: 'text',  # string
    6: 'role',  # string
    7: 'lang',  # string
    8: 'review_count',  # int 
    9: 'review_result',  # bool
    10: 'deleted',  # bool
    11: 'rank',  # int
    12: 'synthetic',  # bool
    13: 'model_name',  # string
    14: 'detoxify',  # dict
    15: 'message_tree_id',  # string
    16: 'tree_state',  # string
    17: 'emojis',  # sequence
    18: 'labels'  # sequence
}


columns_to_extract = [column_filed[1], column_filed[2], column_filed[3], column_filed[4], column_filed[5], column_filed[6], column_filed[7], column_filed[8], column_filed[9], column_filed[10], column_filed[11], column_filed[12], column_filed[13], column_filed[14], column_filed[15], column_filed[16], column_filed[17], column_filed[18]]


# 예제 데이터 (실제 데이터로 교체해야 합니다)
data = [
    {
        'message_id': str(uuid.uuid4()),
        'parent_id': str(uuid.uuid4()),
        'user_id': 'user123',
        'create_date': '2024-07-22',
        'text': 'Sample text',
        'role': 'admin',
        'lang': 'en',
        'review_count': 10,
        'review_result': True,
        'deleted': False,
        'rank': 1,
        'synthetic': True,
        'model_name': 'modelA',
        'detoxify': {'score': 0.5},
        'message_tree_id': str(uuid.uuid4()),
        'tree_state': 'active',
        'emojis': ['😊', '👍'],
        'labels': ['label1', 'label2']
    }
    # 추가 데이터 항목들을 여기에 포함시킬 수 있습니다.
]

# 데이터 프레임 생성
df = pd.DataFrame(data, columns=columns_to_extract)

# 엑셀 파일로 저장
df.to_excel('extracted_texts.xlsx', index=False)

print("Data has been written to extracted_texts.xlsx")
