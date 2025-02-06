import random

# 유니코드 상에서 '가'의 코드 포인트
BASE_CODE = 0xAC00

# 초성, 중성, 종성 리스트
CHOSEONG_LIST = [
    'ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'
]

JUNGSEONG_LIST = [
    'ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ'
]

# 종성(받침) 리스트, index 0은 받침 없음
JONGSEONG_LIST = [
    '', 'ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ',
    'ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'
]

def is_hangul(char: str) -> bool:
    """
    한글(가~힣) 범위인지 판별하는 함수.
    """
    return '가' <= char <= '힣'

def decompose(char: str):
    """
    한 글자를 초성, 중성, 종성 인덱스로 분해한다.
    한글이 아닐 경우 None을 반환한다.
    """
    if not is_hangul(char):
        return None
    code = ord(char) - BASE_CODE
    jongseong_index = code % 28
    jungseong_index = (code // 28) % 21
    choseong_index = code // (28 * 21)
    return (choseong_index, jungseong_index, jongseong_index)

def compose(c_idx: int, j_idx: int, jo_idx: int) -> str:
    """
    초성, 중성, 종성 인덱스를 합쳐 한글 음절(문자)을 만든다.
    """
    code = BASE_CODE + (c_idx * 21 * 28) + (j_idx * 28) + jo_idx
    return chr(code)

def drop_final_consonant(sentence: str) -> str:
    """
    문장 전체에서 한 번만, 받침(종성)이 있는 임의의 한글 음절을 골라
    그 받침을 제거한다.
    """
    candidates = []
    for i, ch in enumerate(sentence):
        dec = decompose(ch)
        if dec is not None:
            # 종성이 있으면 후보에 추가
            if dec[2] != 0:
                candidates.append(i)
    
    if not candidates:
        return sentence  # 받침 있는 음절이 없다면 변화 없음
    
    idx = random.choice(candidates)
    c_idx, j_idx, jo_idx = decompose(sentence[idx])
    # 받침을 0으로 설정
    new_ch = compose(c_idx, j_idx, 0)
    
    return sentence[:idx] + new_ch + sentence[idx+1:]

def replace_consonant(sentence: str) -> str:
    """
    문장 전체에서 한 번만, 임의의 한글 음절 초성을 다른 초성으로 치환한다.
    """
    candidates = []
    for i, ch in enumerate(sentence):
        if is_hangul(ch):
            candidates.append(i)
    
    if not candidates:
        return sentence
    
    idx = random.choice(candidates)
    c_idx, j_idx, jo_idx = decompose(sentence[idx])
    
    # 현재 초성을 제외한 임의의 초성 인덱스 중 하나 선택
    possible_choseongs = [x for x in range(len(CHOSEONG_LIST)) if x != c_idx]
    new_c_idx = random.choice(possible_choseongs)
    
    new_ch = compose(new_c_idx, j_idx, jo_idx)
    return sentence[:idx] + new_ch + sentence[idx+1:]

def replace_final_consonant(sentence: str) -> str:
    """
    문장 전체에서 한 번만, 임의의 한글 음절 받침을 다른 받침으로 치환한다.
    (없던 받침을 추가하거나 기존 받침을 바꿀 수 있음)
    """
    candidates = []
    for i, ch in enumerate(sentence):
        if is_hangul(ch):
            candidates.append(i)
    
    if not candidates:
        return sentence
    
    idx = random.choice(candidates)
    c_idx, j_idx, jo_idx = decompose(sentence[idx])
    
    # 현재 종성을 제외한 임의의 종성 인덱스 중 하나 선택
    possible_jongseongs = [x for x in range(len(JONGSEONG_LIST)) if x != jo_idx]
    new_jo_idx = random.choice(possible_jongseongs)
    
    new_ch = compose(c_idx, j_idx, new_jo_idx)
    return sentence[:idx] + new_ch + sentence[idx+1:]

def replace_vowel(sentence: str) -> str:
    """
    문장 전체에서 한 번만, 임의의 한글 음절 모음을 다른 모음으로 치환한다.
    """
    candidates = []
    for i, ch in enumerate(sentence):
        if is_hangul(ch):
            candidates.append(i)
    
    if not candidates:
        return sentence
    
    idx = random.choice(candidates)
    c_idx, j_idx, jo_idx = decompose(sentence[idx])

    # 현재 중성을 제외한 임의의 중성 인덱스 중 하나 선택
    possible_jungseongs = [x for x in range(len(JUNGSEONG_LIST)) if x != j_idx]
    new_j_idx = random.choice(possible_jungseongs)
    
    new_ch = compose(c_idx, new_j_idx, jo_idx)
    return sentence[:idx] + new_ch + sentence[idx+1:]

def double_error_in_one_word(sentence: str) -> str:
    """
    문장 전체에서 임의로 한 단어를 택해,
    두 가지 오류 함수를 연속 적용한다.
    """
    words = sentence.split()
    if not words:
        return sentence
    
    error_functions = [
        drop_final_consonant,
        replace_consonant,
        replace_final_consonant,
        replace_vowel
    ]
    
    # 단어를 하나 선택
    word_idx = random.randrange(len(words))
    chosen_word = words[word_idx]
    
    # 두 가지 오류를 연속 적용
    func1 = random.choice(error_functions)
    func2 = random.choice(error_functions)
    new_word = func2(func1(chosen_word))
    
    words[word_idx] = new_word
    return " ".join(words)

if __name__ == "__main__":
    # 테스트 예시
    test_sentence = "안녕하세요 저는 파이썬을 공부합니다."
    
    print("원문: ", test_sentence)
    print("받침 탈락 예시: ", drop_final_consonant(test_sentence))
    print("자음 치환 예시: ", replace_consonant(test_sentence))
    print("받침 치환 예시: ", replace_final_consonant(test_sentence))
    print("모음 치환 예시: ", replace_vowel(test_sentence))
    print("한 단어에 연속 2개 오류: ", double_error_in_one_word(test_sentence))
