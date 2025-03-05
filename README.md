# OASST

## 목차

- [개요](#개요)
- [테이블 구조](#테이블-구조)
- [구현 방법 개요](#구현-방법-개요)
- [수집 데이터](#수집-데이터)
- [실행 방법](#실행-방법)
- [논의 내용](#논의-내용)
- [실행 방법](#실행-방법)
- [참고문서](#참고문서)

## 개요

OASST Table은 Open Assistant 프로젝트와 관련된 데이터 테이블을 관리하고 조작하는 구조를 설명합니다. 이 테이블은 주로 AI 모델 학습을 위한 데이터를 저장하며, 다양한 유형의 정보를 포함할 수 있습니다.

![Image](https://github.com/user-attachments/assets/42e9cfd3-9d2d-40c8-8742-3f39f5a1ccc8)
![Image](https://github.com/user-attachments/assets/4facf4c6-9e1d-4937-a03c-927a5c6dc545)
![Image](https://github.com/user-attachments/assets/e7ed2884-9631-43c6-b513-21a7d740dea3)

## 테이블 구조

### 1. `id`

    - **의미**: 각 메시지의 고유 식별자.
    - **작성방법**: 일반적으로 UUID 형식으로 자동 생성되며, 수동으로 작성할 필요는 없습니다.

### 2. `conversation_id`

    - **의미**: 메시지가 속한 대화의 고유 식별자.
    - **작성방법**: 각 대화에 대해 고유한 값을 부여합니다. UUID 형식이 일반적입니다.

### 3. `parent_id`

- **의미**: 메시지의 상위 메시지(이전 메시지)의 ID. 루트 메시지의 경우 `null`로 설정됩니다.
- **작성방법**: 이전 메시지의 `id` 값을 참조합니다. 루트 메시지의 경우 `null`로 설정합니다.

### 4. `text`

- **의미**: 메시지의 내용.
- **작성방법**: 실제 대화 내용을 포함합니다. 텍스트 형식으로 작성합니다.

### 5. `role`

- **의미**: 메시지를 생성한 주체를 나타냅니다.
- **작성방법**: 주로 두 가지 값이 사용됩니다.
- `user`: 대화의 사용자.
- `assistant`: 대화의 인공지능 모델.

### 6. `created_at`

- **의미**: 메시지가 생성된 시각.
- **작성방법**: ISO 8601 형식(예: `2024-07-17T12:34:56Z`)으로 작성합니다.

### 7. `updated_at`

- **의미**: 메시지가 마지막으로 업데이트된 시각.
- **작성방법**: ISO 8601 형식(예: `2024-07-17T12:34:56Z`)으로 작성합니다.

### 8. `deleted`

- **의미**: 메시지가 삭제되었는지 여부.
- **작성방법**: 삭제된 메시지의 경우 `true`, 그렇지 않은 경우 `false`로 작성합니다.

### 9. `meta`

- **의미**: 메시지에 대한 추가적인 메타데이터.
- **작성방법**: JSON 형식으로 작성하며, 예를 들어 메시지의 언어, 대화 주제 등의 정보를 포함할 수 있습니다.

### 10. `score`

- **의미**: 메시지의 품질을 나타내는 점수.
- **작성방법**: 숫자 형식으로 작성합니다. 주로 평가자가 부여하는 점수입니다.

### 11. `labels`

- **의미**: 메시지에 부여된 라벨.
- **작성방법**: JSON 배열 형식으로 작성하며, 예를 들어 `"helpful"`, `"not helpful"` 등의 값을 포함할 수 있습니다.

### 12. `model_name`

- **의미**: 메시지를 생성한 모델의 이름.
- **작성방법**: 문자열 형식으로 작성합니다. 예를 들어 `"gpt-3.5"` 등.

### 예시

```json
{
  "message_id": "218440fd-5317-4355-91dc-d001416df62b",
  "parent_id": "13592dfb-a6f9-4748-a92c-32b34e239bb4",
  "user_id": "8e95461f-5e94-4d8b-a2fb-d4717ce973e4",
  "text": "It was the winter of 2035, and artificial intelligence (..)",
  "role": "assistant",
  "lang": "en",
  "review_count": 3,
  "review_result": true,
  "deleted": false,
  "rank": 0,
  "synthetic": true,
  "model_name": "oasst-sft-0_3000,max_new_tokens=400 (..)",
  "labels": {
    "spam": { "value": 0.0, "count": 3 },
    "lang_mismatch": { "value": 0.0, "count": 3 },
    "pii": { "value": 0.0, "count": 3 },
    "not_appropriate": { "value": 0.0, "count": 3 },
    "hate_speech": { "value": 0.0, "count": 3 },
    "sexual_content": { "value": 0.0, "count": 3 },
    "quality": { "value": 0.416, "count": 3 },
    "toxicity": { "value": 0.16, "count": 3 },
    "humor": { "value": 0.0, "count": 3 },
    "creativity": { "value": 0.33, "count": 3 },
    "violence": { "value": 0.16, "count": 3 }
  }
}
```

이 예시는 루트 메시지를 나타내며, 이후 메시지들은 `parent_id` 필드를 사용하여 이 메시지와 연결될 수 있습니다. 각 필드는 대화 데이터의 특정 측면을 나타내며, 올바른 작성 방법을 통해 일관된 데이터를 유지할 수 있습니다.

### 대화 트리 테이블 구조 예시

가독성을 위해 여기에는 메시지 속성의 하위 집합만 표시됩니다.

```json
{
  "message_tree_id": "14fbb664-a620-45ce-bee4-7c519b16a793",
  "tree_state": "ready_for_export",
  "prompt": {
    "message_id": "14fbb664-a620-45ce-bee4-7c519b16a793",
    "text": "Why can't we divide by 0? (..)",
    "role": "prompter",
    "lang": "en",
    "replies": [
      {
        "message_id": "894d30b6-56b4-4605-a504-89dd15d4d1c8",
        "text": "The reason we cannot divide by zero is because (..)",
        "role": "assistant",
        "lang": "en",
        "replies": [
          // ...
        ]
      },
      {
        "message_id": "84d0913b-0fd9-4508-8ef5-205626a7039d",
        "text": "The reason that the result of a division by zero is (..)",
        "role": "assistant",
        "lang": "en",
        "replies": [
          {
            "message_id": "3352725e-f424-4e3b-a627-b6db831bdbaa",
            "text": "Math is confusing. Like those weird Irrational (..)",
            "role": "prompter",
            "lang": "en",
            "replies": [
              {
                "message_id": "f46207ca-3149-46e9-a466-9163d4ce499c",
                "text": "Irrational numbers are simply numbers (..)",
                "role": "assistant",
                "lang": "en",
                "replies": []
              },
              // ...
            ]
          }
        ]
      }
    ]
  }
```

데이터셋 구조는 메시지 트리로 이루어져 있습니다. 각 메시지 트리는 초기 프롬프트 메시지가 루트 노드로 있으며, 여러 개의 자식 메시지가 답변으로 있을 수 있습니다. 이 자식 메시지들도 또 다시 여러 개의 답변을 가질 수 있습니다. 모든 메시지는 역할 속성을 가지고 있으며, 이는 “assistant” 또는 "prompter"일 수 있습니다. 대화 스레드의 역할은 프롬프트에서 리프 노드까지 엄격하게 "prompter"와 "assistant"로 번갈아가며 나타납니다.

## 구현 방법 개요

### oasst 테이블 및 트리 형식 구현 방법

oasst maker를 이용하여, xlsx 테이블 형식으로 데이터를 출력하고, oasst preprocessor를 이용하여, xlsx 테이블 형식을 json tree형식 및 csv, feather, parquet, jsonl 파일로 형식 변환

### oasst maker

1. webharvy를 이용하여 크롤링 및 데이터 정제
2. 정제된 html 데이터에서 댓글 파싱 키 클래스 설정
3. 파싱된 데이터를 파이썬을 이용하여 oasst 테이블 형식으로 출력

### oasst preprocessor

1. duckdb를 이용하여 데이터 병렬처리(항상 utilization을 최대로 활용하기 위해, 처리하려는 데이터의 갯수와 가지고 있는 core갯수에 따라 스레드를 생성하여, 스레드마다 처리해야할 범위를 명시적으로 지정하여 cpu의 활용율을 max로 처리 = > cpu utilization 100%고정)
2. 유니코드 공식홈페이지에서 가져온 이모지. 최다빈도로 사용되는 1543개 이모지 제거 + 키보드에서 입력가능한 특수문자등을 제거
3. xlsx 파일 -> json, csv, feather, parquet, jsonl 파일로 형식 변환(인코딩 처리, json의 경우 트리 형식으로 변환)
4. 엔터, 콤마, 등 불필요한 문자 제거
5. 언더샘플링 처리( 텍스트 분류 AI 모델을 파인튜닝할 때 데이터 라벨이 편향되어 있을 경우, 모델의 성능과 일반화 능력에 부정적인 영향을 미침. 이런 상황을 피하기 위해 데이터 리샘플링 과정을 전처리에 넣음)

## 수집 데이터

### 대화형 법률 관련 데이터

- 네이버 블로그 대화형 법률 관련 데이터
- 네이버 카페 대화형 법률 관련 데이터
- 네이버 지식인 대화형 법률 관련 데이터
- 로톡 상담사례 대화형 법률 관련 데이터
- 로톡 법률사례 대화형 법률 관련 데이터
- 로톡 성공사례 대화형 법률 관련 데이터

### 테이블 출력 형식

- \*.xlsx
- \*.csv
- \*.json
- \*.parquet
- \*.feather
- \*.jsonl

### 데이터 수집 방법

- [webharvy](https://www.webharvy.com/)
- python

## Workflow

### 1. HTML 파싱 및 필터링을 위한 데이터 정제 (Data Cleaning)

**webharvy 크롤링 사용 예시**
![Image](https://github.com/user-attachments/assets/b10ff79d-5030-481a-903f-725a73b7441f)

**20240717 네이버 카페 모바일뷰 데이터 정제를 위한 코드**

```jsx
let targetElement = document.querySelector(
  "#app > div > div > div.ArticleContentWrap > #ct > div.CommonComment > div:nth-child(3) > div > div > ul.comment_list"
);
const arr = Array.from(targetElement.children);
let v;
arr.forEach((child) => {
  let item = child.querySelector("div > div.comment_item");
  let itemArr = Array.from(item.children);
  itemArr.forEach((dv) => {
    if (dv.className != "comment_content") {
      item.removeChild(dv);
    }
  });
});
```

**댓글관련 dom 제외하고 child dom 전부 삭제하는 코드**

```jsx
document.addEventListener("DOMContentLoaded", function () {
  // Select the target DOM element
  const targetElement = document.querySelector(
    "#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div:nth-child(2) > ul"
  );

  // Get all child elements of the target element
  const childElements = targetElement.children;

  // Convert HTMLCollection to an array for easy manipulation
  const childElementsArray = Array.from(childElements);

  // Iterate over the child elements
  childElementsArray.forEach((child) => {
    if (child.tagName.toLowerCase() !== "li") {
      // Remove the child element if it is not an <li> tag
      targetElement.removeChild(child);
    }
  });
});

document.querySelector(
  "#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div:nth-child(2) > ul"
);
```

**data cleaning된 데이터를 xml 형식으로 추출**
![Image](https://github.com/user-attachments/assets/6fb8c926-589f-44e7-8ee5-cc3ffd9facd1)

### 2. 정제된 html 데이터에서 댓글 파싱 키 클래스 설정

![Image](https://github.com/user-attachments/assets/ffc11b53-4406-4885-a1e3-86541f56a0b9)

```python

selectors_class = {
    # 각 파일에 대응하는 comment 파싱 키 클래스, 전체 comment를 파싱하는 class key , level2, level3의 comment를 parsing함 (with css selector)
    'comment_child_level_all': {
        'naver_cafe': 'ul[data-v-7db6cb9f].comment_list .comment_content',
        'naver_blog': '.u_cbox_contents',
        'naver_kin': '.se-main-container',
        'lawtalk_상담사례': '.case-card__answer',
        'lawtalk_성공사례': '.solution-card__content',
        'lawtalk_법률가이드': '.guide-card__content',
    },
    # 각 파일에 대응하는 child comment 파싱 키 클래스 , 전체 comment 중, level2 계층의 comment를 parsing함 (with css selector)
    'comment_child_level_2': {
        'naver_cafe': 'li[data-v-49558ed9][data-v-7db6cb9f]:not(.reply) .comment_content',
        'naver_blog': '.u_cbox_contents:not(.u_cbox_reply_area .u_cbox_contents)',
        'naver_kin': '.se-main-container',
        'lawtalk_상담사례': '.case-card__answer',
        'lawtalk_성공사례': '.solution-card__content',
        'lawtalk_법률가이드': '.guide-card__content',
    },
    # 각 파일에 대응하는 child comment 파싱 키 클래스 , 전체 comment 중, level3 계층의 comment를 parsing함 (with css selector)
    'comment_child_level_3': {
        'naver_cafe': 'li[data-v-49558ed9][data-v-7db6cb9f].reply .comment_content',
        'naver_blog': '.u_cbox_reply_area .u_cbox_contents',
        'naver_kin': 'No data',
        'lawtalk_상담사례': 'No data',
        'lawtalk_성공사례': 'No data',
        'lawtalk_법률가이드': 'No data',
    },
    # 각 파일에 대응하는 child comment 등록일 파싱키 클래스
    'comment_child_date': {
        'naver_cafe': '.date',
        'naver_blog': '.u_cbox_date',
        'naver_kin': '.se-main-container',
        'lawtalk_상담사례': '.answerDate',
        'lawtalk_성공사례': 'No data',
        'lawtalk_법률가이드': 'No data',
    },
}

```

### 3. 파싱된 데이터를 파이썬을 이용하여 oasst 테이블 형식으로 출력 및 oaast 형식으로 가공

![Image](https://github.com/user-attachments/assets/8d692c17-ac73-4027-a05e-60d9232bdaf5)

### 4. duckdb를 이용하여 데이터 전처리 병렬처리

```python
# preprocessor.py

filtering.preprocess_data(temp_file, input_extention, args.output, output_extention, args.filter_region, filter_extention, os.cpu_count())

```

```python
# parallel_processing.py
def parallel_processing(chunks, filter_pattern, num_threads):
    """
    데이터를 병렬로 처리하여 각 청크에 필터링을 적용한 후 결합합니다.

    Args:
        chunks (list of pd.DataFrame): 병렬로 처리할 데이터프레임 청크들의 리스트.
        filter_pattern (str): 적용할 정규식 필터 패턴.
        num_threads (int): 사용할 스레드 수.

    Returns:
        pd.DataFrame: 모든 청크가 병렬로 처리된 후 결합된 데이터프레임.
    """
    results = []

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_chunk, chunk, filter_pattern) for chunk in chunks]

        for future in futures:
            result_df = future.result()
            results.append(result_df)

    final_df = pd.concat(results, ignore_index=True)
    return final_df


```

### 5. 유니코드 공식홈페이지에서 가져온 이모지. 최다빈도로 사용되는 1543개 이모지 제거 + 키보드에서 입력가능한 특수문자등을 제거

```python
def remove_emojis(text):
    """_summary_

    Args:
        string: 이모지를 제거할 텍스트입니다.


    Returns:
        string :  이모지가 제거된 텍스트. 새로운 이모지가 추가되면 유니코드 블록을 업데이트 해야함.
    """

    # if text == None:
    if text is None:
        return ' '  # 네이버 블로그와 같은 경우, content 파싱이 안되는 경우가 존재하여 (js로 막아놓음) 공백일 시 변환처리/.
    # 유니코드 공식홈페이지에서 가져온 이모지. 최다빈도로 사용되는 1543개 이모지 제거 + 키보드에서 입력가능한 특수문자
    # chars_to_remove = chars_to_remove = (
    chars_to_remove = textwrap.dedent(
        """🌸📞✅⭐🤗☺️✔■�😂😍🤣😊🙏💕😭😘😊🥰🎉🥳🍕🌮👍😀😃
        😄😁😆😅🤣😂🙃😉😊😇💋💌💘💝💖💗💓💞💕💟❣💔❤🧡💛💚
        💙💜🤎🖤🤍💯💢💥💫💦💨🕳💣💬👁️‍🗨️🗨 🗯 💭 💤🀄🃏🅰️🅱️🅾️🅿️
        🆎🆑🆒🆓🆔🆕🆖🆗🆘🆙🆚🈁🈂️🈚🈯🈲🈳🈴🈵🈶🈷️🈸🈹🈺🉐
        🉑🌀🌁🌂🌃🌄🌅🌆🌇🌈🌉🌊🌋🌌🌍🌎🌏🌐🌑🌒🌓🌔🌕🌖🌗
        🌘🌙🌚🌛🌜🌝🌞🌟🌠🌡️🌤️🌥️🌦️🌧️🌨️🌩️🌪️🌫️🌬️🌭🌮🌯🌰🌱🌲
        🌳🌴🌵🌶️🌷🌸🌹🌺🌻🌼🌽🌾🌿🍀🍁🍂🍃🍄🍅🍆🍇🍈🍉🍊🍋
        🍌🍍🍎🍏🍐🍑🍒🍓🍔🍕🍖🍗🍘🍙🍚🍛🍜🍝🍞🍟🍠🍡🍢🍣🍤
        🍥🍦🍧🍨🍩🍪🍫🍬🍭🍮🍯🍰🍱🍲🍳🍴🍵🍶🍷🍸🍹🍺🍻🍼🍽️
        🍾🍿🎀🎁🎂🎃🎄🎅🎆🎇🎈🎉🎊🎋🎌🎍🎎🎏🎐🎑🎒🎓🎖️🎗️🎙️
        🎚️🎛️🎞️🎟️🎠🎡🎢🎣🎤🎥🎦🎧🎨🎩🎪🎫🎬🎭🎮🎯🎰🎱🎲🎳🎴
        🎵🎶🎷🎸🎹🎺🎻🎼🎽🎾🎿🏀🏁🏂🏃🏄🏅🏆🏇🏈🏉🏊🏋️🏌️🏍️
        🏎️🏏🏐🏑🏒🏓🏔️🏕️🏖️🏗️🏘️🏙️🏚️🏛️🏜️🏝️🏞️🏟️🏠🏡🏢🏣🏤🏥🏦
        🏧🏨🏩🏪🏫🏬🏭🏮🏯🏰🏳️🏳️‍🌈🏴🏴‍☠️🏴󠁧󠁢󠁥󠁮󠁧󠁿🏴󠁧󠁢󠁳󠁣󠁴󠁿🏴󠁧󠁢󠁷󠁬󠁳󠁿🏵️🏷️🏸🏹🏺🐀🐁🐂
        🐃🐄🐅🐆🐇🐈🐉🐊🐋🐌🐍🐎🐏🐐🐑🐒🐓🐔🐕🐖🐗🐘🐙🐚🐛
        🐜🐝🐞🐟🐠🐡🐢🐣🐤🐥🐦🐧🐨🐩🐪🐫🐬🐭🐮🐯🐰🐱🐲🐳🐴
        🐵🐶🐷🐸🐹🐺🐻🐼🐽🐾🐿️👀👁️👁️‍🗨️👂👃👄👅👆👇👈👉👊👋👌
        👍👎👏👐👑👒👓👔👕👖👗👘👙👚👛👜👝👞👟👠👡👢👣👤👥
        👦👧👨👨‍✈️👨‍❤️‍👨👨‍❤️‍💋‍👨👨‍⚕️👨‍⚖️👨‍🌾👨‍🍳👨‍🎓👨‍🎤👨‍🎨👨‍🏫👨‍🏭👨‍👦👨‍👦‍👦👨‍👧👨‍👧‍👦👨‍👧‍👧👨‍👨‍👦👨‍👨‍👦‍👦👨‍👨‍👧👨‍👨‍👧‍👦👨‍👨‍👧‍👧👨‍👩‍👦
        👨‍👩‍👦‍👦👨‍👩‍👧👨‍👩‍👧‍👦👨‍👩‍👧‍👧👨‍💻👨‍💼👨‍🔧👨‍🔬👨‍🚀👨‍🚒👨‍🦰👨‍🦱👨‍🦲👨‍🦳👩👩‍✈️👩‍❤️‍👨👩‍❤️‍👩👩‍❤️‍💋‍👨👩‍❤️‍💋‍👩👩‍⚕️👩‍⚖️👩‍🌾👩‍🍳👩‍🎓
        👩‍🎤👩‍🎨👩‍🏫👩‍🏭👩‍👦👩‍👦‍👦👩‍👧👩‍👧‍👦👩‍👧‍👧👩‍👩‍👦👩‍👩‍👦‍👦👩‍👩‍👧👩‍👩‍👧‍👦👩‍👩‍👧‍👧👩‍💻👩‍💼👩‍🔧👩‍🔬👩‍🚀👩‍🚒👩‍🦰👩‍🦱👩‍🦲👩‍🦳👪👫
        👬👭👮👯👰👱👲👳👴👵👶👷👸👹👺👻👼👽👾👿💀💁💂💃💄
        💅💆💇💈💉💊💋💌💍💎💏💐💑💒💓💔💕💖💗💘💙💚💛💜💝
        💞💟💠💡💢💣💤💥💦💧💨💩💪💫💬💭💮💯💰💱💲💳💴💵💶
        💷💸💹💺💻💼💽💾💿📀📁📂📃📄📅📆📇📈📉📊📋📌📍📎📏
        📐📑📒📓📔📕📖📗📘📙📚📛📜📝📞📟📠📡📢📣📤📥📦📧📨
        📩📪📫📬📭📮📯📰📱📲📳📴📵📶📷📸📹📺📻📼📽️📿🔀🔁🔂
        🔃🔄🔅🔆🔇🔈🔉🔊🔋🔌🔍🔎🔏🔐🔑🔒🔓🔔🔕🔖🔗🔘🔙🔚🔛
        🔜🔝🔞🔟🔠🔡🔢🔣🔤🔥🔦🔧🔨🔩🔪🔫🔬🔭🔮🔯🔰🔱🔲🔳🔴
        🔵🔶🔷🔸🔹🔺🔻🔼🔽🕉️🕊️🕋🕌🕍🕎🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙
        🕚🕛🕜🕝🕞🕟🕠🕡🕢🕣🕤🕥🕦🕧🕯️🕰️🕳️🕴️🕵️🕶️🕷️🕸️🕹️🕺🖇️
        🖊️🖋️🖌️🖍️🖐️🖕🖖🖤🖥️🖨️🖱️🖲️🖼️🗂️🗃️🗄️🗑️🗒️🗓️🗜️🗝️🗞️🗡️🗣️🗨️
        🗯️🗳️🗺️🗻🗼🗽🗾🗿😀😁😂😃😄😅😆😇😈😉😊😋😌😍😎😏😐
        😑😒😓😔😕😖😗😘😙😚😛😜😝😞😟😠😡😢😣😤😥😦😧😨😩
        😪😫😬😭😮😯😰😱😲😳😴😵😶😷😸😹😺😻😼😽😾😿🙀🙁🙂
        🙃🙄🙅🙆🙇🙈🙉🙊🙋🙌🙍🙎🙏🚀🚁🚂🚃🚄🚅🚆🚇🚈🚉🚊🚋
        🚌🚍🚎🚏🚐🚑🚒🚓🚔🚕🚖🚗🚘🚙🚚🚛🚜🚝🚞🚟🚠🚡🚢🚣🚤
        🚥🚦🚧🚨🚩🚪🚫🚬🚭🚮🚯🚰🚱🚲🚳🚴🚵🚶🚷🚸🚹🚺🚻🚼🚽
        🚾🚿🛀🛁🛂🛃🛄🛅🛋️🛌🛍️🛎️🛏️🛐🛑🛒🛠️🛡️🛢️🛣️🛤️🛥️🛩️🛫🛬
        🛰️🛳️🛴🛵🛶🛷🛸🛹🤐🤑🤒🤓🤔🤕🤖🤗🤘🤙🤚🤛🤜🤝🤞🤟🤠
        🤡🤢🤣🤤🤥🤦🤧🤨🤩🤪🤫🤬🤭🤮🤯🤰🤱🤲🤳🤴🤵🤶🤷🤸🤹
        🤺🤼🤽🤾🥀🥁🥂🥃🥄🥅🥇🥈🥉🥊🥋🥌🥍🥎🥏🥐🥑🥒🥓🥔🥕
        🥖🥗🥘🥙🥚🥛🥜🥝🥞🥟🥠🥡🥢🥣🥤🥥🥦🥧🥨🥩🥪🥫🥬🥭🥮
        🥯🥰🥳🥴🥵🥶🥺🥼🥽🥾🥿🦀🦁🦂🦃🦄🦅🦆🦇🦈🦉🦊🦋🦌🦍
        🦎🦏🦐🦑🦒🦓🦔🦕🦖🦗🦘🦙🦚🦛🦜🦝🦞🦟🦠🦡🦢🦴🦵🦶🦷
        🦸🦹🧀🧁🧂🧐🧑🧒🧓🧔🧕🧖🧗🧘🧙🧚🧛🧜🧝🧞🧟🧠🧡🧢🧣🧤
        🧥🧦🧧🧨🧩🧪🧫🧬🧭🧮🧯🧰🧱🧲🧳🧴🧵🧶🧷🧸🧹🧺🧻🧼🧽
        🧾🧿㊙️㊗️❤
        ♫☎•°♨✈✣☏■☀➑✂☑✉☼☆✄✔✆—☁★♕✘№‰♠✪✝╳©…♥✰†✎®¶♦✧‡✍❆♣✦◑
        ♀℮❅♤♡♪♂·★▶◆○＃＆＊＠§※☆★ㅁ9●◎◇◆□■△▲▽▼▷▶♤♠♡♥♧♣⊙◈▣◐◑☏☎☜☞㈜®ㅁㄻ"""
    )

    # Trim each line
    chars_to_remove = ''.join(line.strip() for line in chars_to_remove.splitlines())
    # Print or use the trimmed_emojis as needed
    # print(chars_to_remove)

    # 이모지 범위에 포함되지 않으며, 특정 문자 목록에도 포함되지 않는 문자를 추가로 제거.
    return ''.join(char for char in text if (char == ' ' or not (char.isascii() and 0x1F600 <= ord(char) <= 0x1F64F) and char not in chars_to_remove))


```

### 6. 지역명 삭제

**고유 지역명을 가진 DB 파일을 기반으로 필터 패턴을 생성**

```python
def create_filter_pattern(input_file, filter_extention):
    """
    필터링 조건이 포함된 feather 파일을 기반으로 필터 패턴을 생성합니다.

    Args:
        filter_feather_path (str): 필터 데이터가 포함된 feather 파일의 경로.

    Returns:
        str: 텍스트 필터링에 사용될 정규식 패턴.
    """
    logging.info(f"필터 패턴 생성 중: {input_file}")

    filter_file = read_file(input_file, filter_extention)
    filter_to_remove = [x for x in filter_file['지역명'] if pd.notnull(x)]
    filter_pattern = f"\\s*({'|'.join(map(re.escape, filter_to_remove))})\\s*"
    logging.info("필터 패턴 생성 완료")
    return filter_pattern
```

### 7. xlsx 파일 -> json, csv, feather, parquet, jsonl 파일로 형식 변환(인코딩 처리, json의 경우 트리 형식으로 변환)

**oasst table -> oasst tree 형식으로 변환 샘플**

```python
[
    {
        "message_id": "83d39c49-37f9-4726-b479-782e369c18e8",
        "parent_id": "null",
        "user_id": "f013f6c4-6d60-49e4-b594-9ce060f69cdb",
        "creadte_date": "2024-08-05T16:31:50.297489+09:00",
        "title": "금지명령 전 보정권고...",
        "text": "금지명령 전 보정권고...타사입니다..\n\n접수 후 재배당요구서와 보정권고가 먼저 나왔는데 이럴경우 금지명령은 보정을 다 할때까지 안나오나요? \n\n아니면 중간에 나올수도 있는건가요..?ㅠ\n\n사업자도 아니고 재회생도 아니고 부채는 7000정도인데..재배당은 왜 된건지..밥도 안넘어가고 피말리네요ㅠㅠ 금지라도 먼저 나왔으면 좋겠는데\n\n​",
        "role": "prompter",
        "replies": [
            {
                "message_id": "f50f92d0-d53b-444c-a7c1-0cee229ba60b",
                "parent_id": "83d39c49-37f9-4726-b479-782e369c18e8",
                "user_id": "4591dbe8-2c4e-4e69-b2de-b01084328d9c",
                "creadte_date": "2024-08-03T23:22:00.000000+09:00",
                "title": "null",
                "text": "재배당은 외부회생 위원이 선임 되는 것으로 보시면 됩니다",
                "사용여부": "None",
                "role": "assistant",
                "replies": [
                    {
                        "message_id": "94f644ef-fc62-4c0a-9821-237a75d45296",
                        "parent_id": "f50f92d0-d53b-444c-a7c1-0cee229ba60b",
                        "user_id": "9ead8a75-143d-4b1a-8603-6e827cfa7aa8",
                        "creadte_date": "2024-08-04T01:42:00.000000+09:00",
                        "title": "null",
                        "text": "감사합니다ㅠㅠ",
                        "사용여부": "None",
                        "role": "assistant",
                        "lang": "ko",
                        "review_count": 0,
                        "review_result": "null",
                        "deleted": "false",
                        "rank": "null",
                        "synthetic": "false",
                        "model_name": "null",
                        "detoxify": "{ \"toxicity\": 0.0, \"severe_toxicity\": 0.0, \"obscene\": 0.0, \"identity_attack\": 0.0, \"insult\": 0.0, \"threat\": 0.0, \"sexual_explicit\": 0.0 }",
                        "message_tree_id": "83d39c49-37f9-4726-b479-782e369c18e8",
                        "tree_state": "ready_for_export",
                        "emojis": "{ \"name\": [ \"_skip_labeling\" ], \"count\": [ 2 ] }",
                        "lavels": "{ \"name\": [ \"spam\", \"lang_mismatch\", \"pii\", \"not_appropriate\", \"hate_speech\", \"sexual_content\", \"quality\", \"toxicity\", \"humor\", \"creativity\", \"violence\" ], \"value\": [ 0, 0, 0, 0, 0, 0, 0.5833333333333334, 0.08333333333333333, 0.08333333333333333, 0.4166666666666667, 0 ], \"count\": [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3 ] }"
                    }
                ]
            },
            {
                "message_id": "1d1411b0-75d7-4ec6-8ddd-71c7f3cbdff6",
                "parent_id": "83d39c49-37f9-4726-b479-782e369c18e8",
                "user_id": "3232f4b4-a67c-4de4-887f-f66b12ac3cdf",
                "creadte_date": "2024-08-04T01:15:00.000000+09:00",
                "title": "null",
                "text": "영업소득자로 잡히신거 같은데요",
                "사용여부": "None",
                "role": "assistant",
                "replies": [
                    {
                        "message_id": "f7b92616-3671-4d98-a1f0-ee8a8947e909",
                        "parent_id": "1d1411b0-75d7-4ec6-8ddd-71c7f3cbdff6",
                        "user_id": "943ab279-9e44-4579-bfe7-24ea64a1c9f6",
                        "creadte_date": "2024-08-04T01:41:00.000000+09:00",
                        "title": "null",
                        "text": "영업을 한적이 없는데..ㅠㅠ 급여소득자에요..ㅠㅠ 일단 기다려 보려구요..",
                        "사용여부": "None",
                        "role": "assistant",
                        "lang": "ko",
                        "review_count": 0,
                        "review_result": "null",
                        "deleted": "false",
                        "rank": "null",
                        "synthetic": "false",
                        "model_name": "null",
                        "detoxify": "{ \"toxicity\": 0.0, \"severe_toxicity\": 0.0, \"obscene\": 0.0, \"identity_attack\": 0.0, \"insult\": 0.0, \"threat\": 0.0, \"sexual_explicit\": 0.0 }",
                        "message_tree_id": "83d39c49-37f9-4726-b479-782e369c18e8",
                        "tree_state": "ready_for_export",
                        "emojis": "{ \"name\": [ \"_skip_labeling\" ], \"count\": [ 2 ] }",
                        "lavels": "{ \"name\": [ \"spam\", \"lang_mismatch\", \"pii\", \"not_appropriate\", \"hate_speech\", \"sexual_content\", \"quality\", \"toxicity\", \"humor\", \"creativity\", \"violence\" ], \"value\": [ 0, 0, 0, 0, 0, 0, 0.5833333333333334, 0.08333333333333333, 0.08333333333333333, 0.4166666666666667, 0 ], \"count\": [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3 ] }"
                    }
                ]
            }
        ]
    },
]
```

### 8.언더샘플링 처리( 텍스트 분류 AI 모델을 파인튜닝할 때 데이터 라벨이 편향되어 있을 경우, 모델의 성능과 일반화 능력에 부정적인 영향을 미침. 이런 상황을 피하기 위해 데이터 리샘플링 과정을 전처리에 넣음)

```python
def under_sampling(input_file: str, ratio: float) -> None:
    """
    지정된 비율에 따라 분류열에 있는 데이터셋(형사, 민사, 이혼 등)을 토대로 샘플링하는 함수

    Parameters:
    - input_file (str): 샘플링할 파일의 경로 (xlsx, csv, json, parquet)
    - ratio (float): 샘플링 비율 (최소 클래스 샘플 수의 비율)
    """

    # 파일 확장자 확인
    file_extension = os.path.splitext(input_file)[1].lower()

    # 파일 확장자에 따라 파일 읽기
    if file_extension == '.xlsx':
        df = pd.read_excel(input_file)
    elif file_extension == '.csv':
        try:
            df = pd.read_csv(input_file, encoding=file_encoding_data.GLOBAL_ENCODING_UNIFICATION)
        except UnicodeDecodeError:
            raise ValueError(f"감지된 인코딩으로 파일을 디코딩할 수 없습니다: {file_encoding_data.GLOBAL_ENCODING_UNIFICATION}.")
    elif file_extension == '.json':
        df = pd.read_json(input_file)
    elif file_extension == '.parquet':
        df = pd.read_parquet(input_file)
    else:
        raise ValueError("지원되지 않는 파일 형식입니다. xlsx, csv, json, 또는 parquet 형식의 파일을 업로드하세요.")

    # 열 이름의 공백 제거
    df.columns = df.columns.str.strip()

    if file_extension != '.json':
        # 데이터셋에 필요한 열이 존재하는지 확인
        if '분류' not in df.columns or 'message_tree_id' not in df.columns:
            raise KeyError("필요한 열 '분류' 또는 'message_tree_id'가 데이터셋에 없습니다.")

        # 분류별로 데이터프레임 분리
        class_groups = {}
        for category in df['분류'].unique():
            class_groups[category] = df[df['분류'] == category]

        # 각 분류에서 고유한 message_tree_id의 수를 계산
        class_group_counts = {category: len(group['message_tree_id'].unique()) for category, group in class_groups.items()}

        # 가장 적은 그룹 수를 기준으로 최대 그룹 수 계산
        min_group_count = min(class_group_counts.values())
        max_groups = ceil(min_group_count * ratio)

        # 각 분류에서 그룹의 수를 제한하여 샘플링
        sampled_groups = []
        for category, group in class_groups.items():
            unique_tree_ids = group['message_tree_id'].unique()
            sampled_tree_ids = np.random.choice(unique_tree_ids, size=min(len(unique_tree_ids), max_groups), replace=False)
            sampled_group = group[group['message_tree_id'].isin(sampled_tree_ids)]
            sampled_groups.append(sampled_group)

        # 샘플링된 데이터프레임 생성
        df_resampled = pd.concat(sampled_groups)

    else:
        # JSON 파일의 경우, 그룹화 및 샘플링을 수행하지 않음
        original_class_counts = df['분류'].value_counts()
        min_class_count = original_class_counts.min()
        max_samples = ceil(min_class_count * ratio)
        df_resampled = df.groupby('분류').apply(lambda x: x.sample(min(len(x), max_samples))).reset_index(drop=True)

    # 샘플링된 데이터셋 저장 (파일 형식에 따라)
    if file_extension == '.xlsx':
        df_resampled.to_excel(input_file, index=False)
    elif file_extension == '.csv':
        df_resampled.to_csv(input_file, index=False, encoding='utf-8-sig')
    elif file_extension == '.json':
        df_resampled.to_json(input_file, orient='records', force_ascii=False, indent=4)
    elif file_extension == '.parquet':
        df_resampled.to_parquet(input_file, index=False)
    else:
        raise ValueError("저장할 수 없는 파일 형식입니다.")

    # 샘플링 결과에 대한 설명 출력
    logging.info("샘플링이 성공적으로 완료되었습니다.")
```

## 논의 내용

## 참고문서

- [OpenAssistant Conversations Dataset (OASST1)](https://huggingface.co/datasets/OpenAssistant/oasst1)
- [Anaconda Documentation](https://www.anaconda.com/docs/main#miniconda-latest-installer-links)
- [webharvy](https://www.webharvy.com/)
- [duckdb Documentation](https://duckdb.org/)
- [OpenVINO](https://github.com/openvinotoolkit/openvino)
- [Datumaro](https://github.com/openvinotoolkit/datumaro)
- [poetry](https://python-poetry.org/docs/)
- [pre-commit](https://pre-commit.com/)
- [gitlint](https://github.com/jorisroovers/gitlint)
- [pytest](https://docs.pytest.org/en/stable/)
