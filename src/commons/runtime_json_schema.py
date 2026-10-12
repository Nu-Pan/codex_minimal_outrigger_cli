"""Structured Output 検証用の JSON Schema 準備を内容ごとに共有する。"""

import json
from functools import lru_cache
from typing import NoReturn

from jsonschema import validators
from jsonschema.protocols import Validator


def reject_non_json_constant(value: str) -> NoReturn:
    """JSON 仕様外の非有限数リテラルを schema と出力の解析から拒否する。"""
    raise ValueError(f"non-standard JSON constant: {value}")


@lru_cache(maxsize=4)
def checked_schema_validator(schema_text: str) -> Validator:
    """同じ schema 本文の解析・定義検査・検証器構築を再利用する。

    呼び出し側で現在の本文を読み、出力ごとの検証を行う。保持数を制限して、
    schema の更新で過去の本文と検証器を蓄積しない。
    """
    schema = json.loads(schema_text, parse_constant=reject_non_json_constant)
    validator_class = validators.validator_for(schema)
    validator_class.check_schema(schema)
    return validator_class(schema)
