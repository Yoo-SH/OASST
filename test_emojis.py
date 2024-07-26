import re

def remove_unwanted_characters(text):
    """
    주어진 텍스트에서 이모지와 다양한 특수 기호를 제거합니다.
    
    Args:
        text (str): 이모지와 기호를 제거할 텍스트입니다.
    
    Returns:
        str: 이모지와 기호가 제거된 텍스트
    """
    # 이모지 및 기호 범위
    unwanted_pattern = re.compile(
        # 기상 기호 및 기호
        "[\u2600-\u26FF"            # Miscellaneous Symbols
        "\u2700-\u27BF"            # Dingbats
        "\u2B50"                   # Star Symbol
        "\u2B55"                   # White Heavy Check Mark
        "\u2300-\u23FF"            # Miscellaneous Technical
        "\u2B00-\u2BFF"            # Miscellaneous Symbols and Arrows
        "\u1F000-\u1F9FF"          # Mahjong Tiles, Domino Tiles, Playing Cards, and various symbols
        "\u1F300-\u1F5FF"          # Miscellaneous Symbols and Pictographs
        "\u1F600-\u1F64F"          # Emoticons
        "\u1F680-\u1F6FF"          # Transport and Map Symbols
        "\u1F700-\u1F77F"          # Alchemical Symbols
        "\u1F780-\u1F7FF"          # Geometric Shapes Extended
        "\u1F800-\u1F8FF"          # Supplemental Geometric Shapes
        "\u1F900-\u1F9FF"          # Supplemental Symbols and Pictographs
        "\u1FA00-\u1FA6F"          # Chess Symbols and other symbols
        "\u1FA70-\u1FAFF"          # Symbols and Pictographs Extended-A
        "\uFE0F"                   # Variation Selector-16 (Emoji modifier)
        "\u1F004"                  # Mahjong Tile Red Dragon
        "\u1F0CF"                  # Playing Card Black Joker
        "\u2B06"                   # Upwards Arrow
        "\u2194-\u21AA"            # Arrows
        "\u2300-\u23FF"            # Technical Symbols
        "]+", re.UNICODE)

    # 정규 표현식을 사용하여 이모지 및 기호를 제거합니다
    return unwanted_pattern.sub('', text)

# 테스트
original_text = "여기에 ▶,◆,○,🌸📞✅⭐🤗 같은 문자가 포함되어 있습니다."
filtered_text = remove_unwanted_characters(original_text)
print(filtered_text)
