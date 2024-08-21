import pytest
# import 

## https://docs.pytest.org/en/stable/


def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be less than 0")


def test_validate_age_valid_age():
    validate_age(10)


def test_validate_age_invalid_age():
    with pytest.raises(ValueError, match="Age cannot be less than 0"):
        validate_age(-1)

# class undersample:
# def test_undersample_1_5():
# def test_undersample_1_5_binary():
# def test_undersample_1_5_multiclass3():
# def test_undersample_1_5_multiclass5():
def test_undersample():
    """
    분류기준 최소 데이터의 1.5
    데이터 삭제 기준: 각 라벨 데이터 별 가장 적은 라벨 값의 최대 n배 까지만 남기고, 전부 삭제(최소값 1배) 
    —undersample 1.5 최소 데이터의 1.5배 까지만
    —undersample 1.0 최소 데이터의 1.0배 까지만
    100개 짜리 testdata 2 class | 100개 짜리 testdata 3 class | 100개 짜리 testdata 5 class
    
    —undersample 1.5 실행시 [true 15개, false 85개] 이진분류 case 작동검증 -> 작동시 [true 15개, false 23개]
    —undersample 1.0 실행시 [true 15개, false 85개] 이진분류 case 작동검증 -> 작동시 [true 15개, false 15개]
    [형사, 민사, 이혼] 같은 3개 이상의 라벨 case 작동검증 -> 5개도 넣어 봐야됨
    
    """
    with pytest.raises(ValueError, match="Age cannot be less than 0"):
        validate_age(-1)

    # assert calculator.add(1, 2) == 3
    # assert calculator.add(2, 2) == 4