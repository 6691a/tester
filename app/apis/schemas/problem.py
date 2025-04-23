from typing import List

from pydantic import BaseModel, Field


class ProblemSchema(BaseModel):
    """
    Pydantic model for coding test problem description
    """

    level: int = Field(ge=1, le=10, description="Problem difficulty level (1-10)")
    title: str = Field(description="Problem title")
    description: str = Field(description="Detailed problem description")
    constraints: List[str] = Field(description="Input constraints and limitations")
    input_example: str = Field(description="Example input format")
    output_example: str = Field(description="Example output format")
    explanation: str = Field(description="Explanation of the example")
    concepts: List[str] = Field(description="Concepts tested by this problem")
    approach_hints: List[str] = Field(description="Hints for approaching the problem")
    test_case: str = Field(description="Test case for the problem")
    code_skeleton: str = Field(description="Skeleton code for the problem")

    class Config:
        json_schema_extra = {
            "example": {
                "level": 2,
                "title": "문자열 압축",
                "description": """주어진 문자열을 압축하는 함수를 작성하세요. 
                압축은 동일한 문자가 연속적으로 나타나는 경우,
                해당 문자와 반복 횟수를 연결하여 표현합니다.
                """,
                "constraints": [
                    "입력 문자열의 길이는 1 이상 100,000 이하입니다.",
                    "입력 문자열은 영문 소문자로만 구성됩니다.",
                ],
                "input_example": "aaabbbccc",
                "output_example": "a3b3c3",
                "explanation": """입력 문자열 \"aaabbbccc\"는 'a'가 3번, 'b'가 3번, 'c'가 3번 반복됩니다. 
                따라서 압축 결과는 \"a3b3c3\"입니다.""",
                "concepts": ["문자열 처리", "반복문", "조건문", "문자열 연결"],
                "approach_hints": [
                    "문자열을 순회하면서 동일한 문자의 연속 횟수를 계산합니다.",
                    "연속 횟수가 1보다 크면 해당 문자와 횟수를 연결하여 새로운 문자열을 만듭니다.",
                    "연속 횟수가 1이면 해당 문자를 그대로 유지합니다.",
                ],
                "test_case": """def test_compress_string():
                assert compress_string("aaabbbccc") == "a3b3c3"
                assert compress_string("abc") == "abc"
                assert compress_string("aabbcc") == "a2b2c2"
                assert compress_string("aaaaaa") == "a6"
                assert compress_string("") == ""
                """,
                "code_skeleton": '''def compress_string(s):
                """
                문자열을 압축하는 함수
    
                Args:
                    s: 압축할 문자열
    
                Returns:
                    압축된 문자열
                """
                result = ""
                count = 1
                if not s:
                    return ""
    
                for i in range(len(s)):
                    if i + 1 < len(s) and s[i] == s[i+1]:
                        count += 1
                    else:
                        result += s[i]
                        if count > 1:
                            result += str(count)
                        count = 1
                return result''',
            }
        }
