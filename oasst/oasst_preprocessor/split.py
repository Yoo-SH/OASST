import json


def split_replies(input_file, output_file):
    """
    JSON 파일을 읽고, 각 메시지의 'replies' 필드의 값을 상위 메시지에서 분리하여
    새로운 파일에 저장합니다.

    Args:
        input_file (str): 입력 JSON 파일의 경로
        output_file (str): 결과를 저장할 JSON 파일의 경로
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    def process_message(message):
        """
        메시지에서 'replies' 필드를 분리하여 새로운 리스트에 저장합니다.

        Args:
            message (dict): 현재 메시지

        Returns:
            dict: 업데이트된 메시지와 분리된 replies 리스트
        """
        replies = message.pop('replies', [])
        separated_replies = []
        for reply in replies:
            # 'replies' 필드를 가지는 각 하위 메시지를 'replies' 키 없이 업데이트
            separated_replies.append(reply)
            process_message(reply)  # 재귀적으로 하위 메시지를 처리

        return separated_replies

    result = []
    for message in data:
        replies = process_message(message)
        if replies:
            # 메시지에서 'replies'를 분리하고, 별도의 리스트에 저장
            for reply in replies:
                result.append(reply)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


# 실행 예제
split_replies('../../data/sample_preprocessor/result.json', '../../data/sample_preprocessor/split_replies.json')
