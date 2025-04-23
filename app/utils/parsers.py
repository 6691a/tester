import json
import re
from typing import Any


def parse_json_from_llm_response(response: str) -> dict[str, Any]:
    """LLM 응답에서 JSON 부분을 추출하고 파싱합니다."""
    # JSON 부분 추출
    json_match = re.search(r"```json\n(.*?)\n```", response, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        # JSON 형식이 아닌 경우 전체 문자열을 사용
        json_str = response

    # JSON 파싱
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        raise ValueError("응답을 JSON으로 파싱할 수 없습니다.")
