import pandas as pd
import random
from error_functions import (
    drop_final_consonant,
    replace_consonant,
    replace_final_consonant,
    replace_vowel,
    double_error_in_one_word
)

# 입력 파일 및 출력 파일 경로 설정
input_file_path = "../data/train.csv"  # 원본 데이터 파일
output_file_path = "../data/augmented_trivial_error.csv"  # 변형된 데이터를 저장할 CSV 파일

# CSV 파일 읽기
df = pd.read_csv(input_file_path)

# 적용할 오류 변형 함수 목록
error_functions = [
    drop_final_consonant,
    replace_consonant,
    replace_final_consonant,
    replace_vowel,
    double_error_in_one_word
]

# 변형된 데이터를 저장할 리스트
processed_data = []

# 데이터 처리 시작
for _, row in df.iterrows():
    sentence = row['output']  # 원본 문장
    sentence_id = row['ID']  # 원본 데이터의 ID 값

    # 현재 처리 중인 데이터의 ID를 출력하여 진행 상태 확인
    print(f"Processing ID: {sentence_id}")

    # 1. 오류가 없는 올바른 문장 추가 (원본 문장을 그대로 저장)
    processed_data.append([sentence_id, sentence, sentence])  # error와 original 동일

    # 2. 각 오류 변형을 적용한 문장 추가
    for func in error_functions:
        modified_sentence = func(sentence)
        processed_data.append([sentence_id, modified_sentence, sentence])  # error: 오류 문장, original: 원본 문장

# 결과를 DataFrame으로 변환
columns = ["original_id", "error", "original"]
processed_df = pd.DataFrame(processed_data, columns=columns)

# CSV 파일로 저장 (UTF-8 인코딩 사용)
processed_df.to_csv(output_file_path, index=False, encoding="utf-8-sig")

# 처리 완료 메시지 출력
print(f"Processed data saved to: {output_file_path}")
