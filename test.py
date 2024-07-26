import unicodedata

def remove_specific_characters(text):
    # 제거할 문자 목록
    chars_to_remove = "★▶◆○🌸📞✅⭐🤗"
    
    # 텍스트에서 각 문자를 검사하고 제거할 문자가 아니면 결과에 포함시킴
    filtered_text = ''.join(c for c in text if c not in chars_to_remove)
    
    return filtered_text

# 테스트
original_text = "여기에 ★,▶,◆,○,🌸,😃,😃,📞,✅,⭐,🤗 같은 문자가 포함되어 있습니다."
filtered_text = remove_specific_characters(original_text)
print(filtered_text)