from emojis_deleter import remove_emojis
import uuid
import logging



def get_rows_from_tree_jsonForm(tree, column_field):
    """
    댓글 트리에서 데이터를 추출하여 JSON 형식으로 반환합니다.

    Args:
        tree (defaultdict): 댓글의 계층 구조를 나타내는 중첩된 딕셔너리입니다.
        column_field (dict): 데이터 컬럼 필드 이름과 번호를 매핑하는 딕셔너리입니다.

    Returns:
        list: 각 행이 댓글 데이터를 나타내는 딕셔너리로 구성된 리스트입니다.
    """

    rows = []

    logging.info("트리 row를 json형식으로 가져오는 중입니다.")
    
    
    for root, levels in tree.items():
        root_uuid = levels['uuid']
        root_date = levels['date']
        seen_comments = set()  # 중복된 댓글을 추적하기 위한 집합
        
        # 댓글을 저장할 리스트
        root_replies = []

        for level_2_uuid, level_2_data in levels['Level_2'].items():
            level_2_comment = level_2_data['comment']
            level_2_date = level_2_data['date']
            
            if level_2_comment not in seen_comments and level_2_comment != 'None' and level_2_comment != '':  # 중복 검사, 추출안된 None값, 비밀댓글 삭제.
                seen_comments.add(level_2_comment)
                
                level_2_replies = []
                
                for level_3_uuid, level_3_data in levels['Level_3'].get(level_2_uuid, {}).items():
                    level_3_comment = level_3_data['comment']
                    level_3_date = level_3_data['date']
                    
                    if level_3_comment not in seen_comments:  # 중복 검사
                        seen_comments.add(level_3_comment)
                        
                    
                        level_2_replies.append({
                            column_field[1]: level_3_uuid,
                            column_field[2]: level_2_uuid,
                            column_field[3]: str(uuid.uuid4()),  # UUID를 문자열로 변환
                            column_field[4]: level_3_date,
                            column_field[5]: 'null',
                            column_field[6]: remove_emojis(level_3_comment),
                            column_field[7]: 'None',
                            column_field[8]: 'assistant',
                            column_field[9]: 'ko',
                            column_field[10]: 0,
                            column_field[11]: 'null',
                            column_field[12]: 'false',
                            column_field[13]: 'null',
                            column_field[14]: 'false',
                            column_field[15]: 'null',
                            column_field[16]: '{ "toxicity": 0.0, "severe_toxicity": 0.0, "obscene": 0.0, "identity_attack": 0.0, "insult": 0.0, "threat": 0.0, "sexual_explicit": 0.0 }',
                            column_field[17]: root_uuid,
                            column_field[18]: "ready_for_export",
                            column_field[19]: '{ "name": [ "_skip_labeling" ], "count": [ 2 ] }',
                            column_field[20]: '{ "name": [ "spam", "lang_mismatch", "pii", "not_appropriate", "hate_speech", "sexual_content", "quality", "toxicity", "humor", "creativity", "violence" ], "value": [ 0, 0, 0, 0, 0, 0, 0.5833333333333334, 0.08333333333333333, 0.08333333333333333, 0.4166666666666667, 0 ], "count": [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3 ] }'
                        })
                

                if level_2_replies:
                    root_replies.append({
                    column_field[1]: level_2_uuid,
                    column_field[2]: root_uuid,
                    column_field[3]: str(uuid.uuid4()),  # UUID를 문자열로 변환
                    column_field[4]: level_2_date,
                    column_field[5]: 'null',
                    column_field[6]: remove_emojis(level_2_comment),
                    column_field[7]: 'None',
                    column_field[8]: 'assistant',
                    'replies': level_2_replies
                })
                else: 
                    root_replies.append({
                    column_field[1]: level_2_uuid,
                    column_field[2]: root_uuid,
                    column_field[3]: str(uuid.uuid4()),  # UUID를 문자열로 변환
                    column_field[4]: level_2_date,
                    column_field[5]: 'null',
                    column_field[6]: remove_emojis(level_2_comment),
                    column_field[7]: 'None',
                    column_field[8]: 'assistant',
                    column_field[9]: 'ko',
                    column_field[10]: 0,
                    column_field[11]: 'null',
                    column_field[12]: 'false',
                    column_field[13]: 'null',
                    column_field[14]: 'false',
                    column_field[15]: 'null',
                    column_field[16]: '{ "toxicity": 0.0, "severe_toxicity": 0.0, "obscene": 0.0, "identity_attack": 0.0, "insult": 0.0, "threat": 0.0, "sexual_explicit": 0.0 }',
                    column_field[17]: root_uuid,
                    column_field[18]: "ready_for_export",
                    column_field[19]: '{ "name": [ "_skip_labeling" ], "count": [ 2 ] }',
                    column_field[20]: '{ "name": [ "spam", "lang_mismatch", "pii", "not_appropriate", "hate_speech", "sexual_content", "quality", "toxicity", "humor", "creativity", "violence" ], "value": [ 0, 0, 0, 0, 0, 0, 0.5833333333333334, 0.08333333333333333, 0.08333333333333333, 0.4166666666666667, 0 ], "count": [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3 ] }'
                })

                    
                    
        if root_replies:
            rows.append({
            column_field[1]: root_uuid,
            column_field[2]: 'null',
            column_field[3]: str(uuid.uuid4()),  # UUID를 문자열로 변환
            column_field[4]: root_date,
            column_field[5]: remove_emojis(root.split('_seperation_title_')[0]),  # 제목
            column_field[6]: remove_emojis(root.split('_seperation_title_')[0] + root.split('_seperation_title_')[1]),  # 내용
            column_field[8]: 'prompter',
            column_field[10]: 0,
            'replies': root_replies
        })
        else:
            rows.append({
            column_field[1]: root_uuid,
            column_field[2]: 'null',
            column_field[3]: str(uuid.uuid4()),  # UUID를 문자열로 변환
            column_field[4]: root_date,
            column_field[5]: remove_emojis(root.split('_seperation_title_')[0]),  # 제목
            column_field[6]: remove_emojis(root.split('_seperation_title_')[0] + root.split('_seperation_title_')[1]),  # 내용
            column_field[8]: 'prompter',
            column_field[10]: 0,
            column_field[9]: 'ko',
            column_field[10]: 0,
            column_field[11]: 'null',
            column_field[12]: 'false',
            column_field[13]: 'null',
            column_field[14]: 'false',
            column_field[15]: 'null',
            column_field[16]: '{ "toxicity": 0.0, "severe_toxicity": 0.0, "obscene": 0.0, "identity_attack": 0.0, "insult": 0.0, "threat": 0.0, "sexual_explicit": 0.0 }',
            column_field[17]: root_uuid,
            column_field[18]: "ready_for_export",
            column_field[19]: '{ "name": [ "_skip_labeling" ], "count": [ 2 ] }',
            column_field[20]: '{ "name": [ "spam", "lang_mismatch", "pii", "not_appropriate", "hate_speech", "sexual_content", "quality", "toxicity", "humor", "creativity", "violence" ], "value": [ 0, 0, 0, 0, 0, 0, 0.5833333333333334, 0.08333333333333333, 0.08333333333333333, 0.4166666666666667, 0 ], "count": [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3 ] }'
        })

    
    logging.info("종료. 트리 row를 json형식으로 반환.")
    return rows
