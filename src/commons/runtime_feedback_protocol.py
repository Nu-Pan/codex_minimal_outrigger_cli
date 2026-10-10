"""collector と stdio reporter が共有する接続情報と正本 schema の読み取り。

reporter の discovery で保存処理や JSON Schema validator を読み込まない。
schema 自体の検査は collector と doctor、submission の検査は collector が行う。
"""

import importlib.util
import json
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import Any

FEEDBACK_CAPABILITY_ENV = "CMOC_FEEDBACK_CAPABILITY"
FEEDBACK_COLLECTOR_HOST = "127.0.0.1"
FEEDBACK_COLLECTOR_PORT_ENV = "CMOC_FEEDBACK_COLLECTOR_PORT"
FEEDBACK_PROTOCOL_ENV = "CMOC_FEEDBACK_PROTOCOL_VERSION"
REPORTER_PROTOCOL_VERSION = "1"


@lru_cache(maxsize=1)
def load_reporter_input_schema() -> dict[str, Any]:
    """oracle package resource の JSON object を読み、discovery と検査で共有する。"""
    # schema field を realization へ複製しない。
    try:
        schema_text = (
            resources.files("oracle.feedback")
            .joinpath("reporter_input.json")
            .read_text(encoding="utf-8")
        )
    except NotADirectoryError:
        # source/editable の namespace package を resources が表現できない場合は、
        # package の具体的な検索先から同じ正本 resource を読み取る。
        spec = importlib.util.find_spec("oracle.feedback")
        locations = (
            spec.submodule_search_locations
            if spec is not None and spec.submodule_search_locations is not None
            else ()
        )
        for location in locations:
            candidate = Path(location) / "reporter_input.json"
            if candidate.is_file():
                schema_text = candidate.read_text(encoding="utf-8")
                break
        else:
            raise
    loaded = json.loads(schema_text)
    if not isinstance(loaded, dict):
        raise TypeError("feedback reporter schema must be a JSON object")
    return loaded
