import logging
import uuid
from collections import defaultdict
from datetime import datetime

def format_date(date_str):
    """
    날짜 문자열을 표준 ISO 8601 형식으로 포맷합니다. 날짜 문자열이 유효하지 않은 경우 현재 날짜와 시간을 반환합니다.

    Args:
        date_str (str): 포맷할 날짜 문자열입니다.

    Returns:
        str: ISO 8601 형식으로 포맷된 날짜 문자열입니다.
    """
    logging.debug(f"날짜 포맷팅: {date_str}")
    try:
        dt = datetime.strptime(date_str, "%Y.%m.%d. %H:%M")
        formatted_date = dt.strftime("%Y-%m-%dT%H:%M:%S.%f+09:00")  # 한국 표준시 UTC+09:00
        return formatted_date
    except ValueError:
        try:
            dt = datetime.strptime(date_str, "%y.%m.%d")  # 날짜만 포함된 경우(naver_cafe의 detal_content)
            formatted_date = dt.strftime("%Y-%m-%dT00:00:00.000000+09:00")  # 한국 표준시 UTC+09:00
            return formatted_date
        except ValueError:
            current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f+09:00")  # 현재 시간을 반환(로톡)
            logging.warning(f"유효하지 않은 날짜 형식. 현재 날짜를 반환합니다: {current_date}")
            return current_date

def format_uuid():
    """
    새로운 UUID를 생성합니다.

    Returns:
        str: 생성된 UUID 문자열입니다.
    """
    uuid_value = str(uuid.uuid4())
    logging.debug(f"생성된 UUID: {uuid_value}")
    return uuid_value

def build_comment_tree(extracted_texts):
    """
    추출된 텍스트 데이터를 기반으로 댓글의 계층 구조를 구축합니다.
    댓글이 pasing된 순서대로 1계층 2계층 댓글과 3계층 댓글을 구축합니다.
    1계층은 원글, 2계층은 댓글, 3계층은 대댓글을 의미. 
    2계층 댓글을 index를 추적하면서 3계층의 부모로 할당.


    Args:
        extracted_texts (list of dict): XML 항목에서 추출된 데이터의 리스트입니다.

    Returns:
        defaultdict: 댓글의 계층 구조를 나타내는 중첩된 딕셔너리입니다.
    """
    logging.info("댓글 트리 구축 중")
    # 트리 구조를 초기화합니다.
    tree = defaultdict(lambda: {
        'Level_2': defaultdict(dict),
        'Level_3': defaultdict(lambda: defaultdict(dict)),
        'registered_date': None,
        'uuid': None
    })


    for item in extracted_texts:
        # 제목이나 상세 내용이 누락된 경우 기본값을 빈 문자열로 설정합니다.
        title = item.get('title', '')
        detail_content = item.get('detail_content', '')
        registered_date = item.get('registered_date', 'No Date')
        root = str(title) + '\n' + str(detail_content)

        if not root.strip():
            logging.debug(f"빈 루트 노드 건너뜁니다")
            continue

        # 'ul[data-v-7db6cb9f].comment_list .comment_content'의 댓글을 추출합니다.
        all_comments = item['html_texts'].get("ul[data-v-7db6cb9f].comment_list .comment_content", [])

        # 레벨 2 댓글과 레벨 3 댓글을 추출합니다.
        level_2_comments = item['html_texts'].get("li[data-v-49558ed9][data-v-7db6cb9f]:not(.reply) .comment_content", [])
        level_3_comments = item['html_texts'].get("li[data-v-49558ed9][data-v-7db6cb9f].reply .comment_content", [])
        
        # 댓글들의 날짜를 추출합니다.
        comment_dates = item['html_texts'].get(".date", [])

        # 레벨 2 댓글과 레벨 3 댓글의 인덱스를 추적하기 위한 변수입니다.
        level_2_index = 0
        level_3_index = 0
        date_index = 0
        
        # 레벨 2 댓글을 추적할 변수입니다.
        current_level_2_comment = None

        # 루트 노드에 UUID를 추가합니다.
        tree[root]['uuid'] = format_uuid()
        tree[root]['datre'] = format_date(registered_date)
        
        # 'ul[data-v-7db6cb9f].comment_list .comment_content'의 댓글을 순회합니다.
        for comment in all_comments:
            comment_date = comment_dates[date_index] if date_index < len(comment_dates) else 'No Date'
            formatted_date = format_date(comment_date)
            date_index += 1
            
            if level_2_index < len(level_2_comments) and comment == level_2_comments[level_2_index]:
                # 현재 댓글이 레벨 2 댓글이면 UUID를 추가하고 현재 레벨 2 댓글을 설정합니다.
                comment_uuid = format_uuid()
                tree[root]['Level_2'][comment_uuid] = {
                    'comment': comment,
                    'date': formatted_date
                }
                current_level_2_comment = comment_uuid
                level_2_index += 1
            elif level_3_index < len(level_3_comments) and comment == level_3_comments[level_3_index]:
                # 현재 댓글이 레벨 3 댓글이면 현재 레벨 2 댓글에 UUID를 추가합니다.
                if current_level_2_comment:
                    comment_uuid = format_uuid()
                    tree[root]['Level_3'][current_level_2_comment][comment_uuid] = {
                        'comment': comment,
                        'date': formatted_date
                    }
                level_3_index += 1

    logging.info("댓글 트리 구축 완료")
    return tree




def print_comment_tree(tree):
    """
    댓글 트리 구조를 출력합니다.

    Args:
        tree (defaultdict): 댓글의 계층 구조를 나타내는 중첩된 딕셔너리입니다.
    """
    logging.info("댓글 트리 출력 중")
    for root, levels in tree.items():
        print(f"레벨 1 본글: {root} (UUID: {levels['uuid']}), 날짜 {levels['registered_date']}")
        for level_2_uuid, level_2_data in levels['Level_2'].items():
            print(f"  레벨 2 댓글: {level_2_data['comment']} (UUID: {level_2_uuid}, 날짜: {level_2_data['date']})")
            for level_3_uuid, level_3_data in levels['Level_3'][level_2_uuid].items():
                print(f"    레벨 3 댓글: {level_3_data['comment']} (UUID: {level_3_uuid}, 날짜: {level_3_data['date']})")
 
    
    
def get_rows_from_tree(tree):
    rows = []

    for root, levels in tree.items():
        root_uuid = levels['uuid']
        root_date = levels['registered_date']
        rows.append({
            'message_id': root_uuid,
            'text': root,
            'created_date': root_date
        })
        
        for level_2_uuid, level_2_data in levels['Level_2'].items():
            level_2_comment = level_2_data['comment']
            level_2_date = level_2_data['date']
            rows.append({
                'message_id': level_2_uuid,
                'text': level_2_comment,
                'created_date': level_2_date
            })
            
            for level_3_uuid, level_3_data in levels['Level_3'][level_2_uuid].items():
                level_3_comment = level_3_data['comment']
                level_3_date = level_3_data['date']
                rows.append({
                    'message_id': level_3_uuid,
                    'text': level_3_comment,
                    'created_date': level_3_date
                })

    return rows
    
