from pathlib import Path


def oracle_schema_path(*parts: str) -> Path:
    """正本 schema の参照 path を返す。

    Args:
        *parts: `acp_builder` からの schema 相対 path。

    Returns:
        指定した oracle schema の path。
    """
    # 正本 schema をテストへ複製せず、<work-root>/oracle/src/oracle/acp_builder/ を参照する。
    return Path(__file__).parents[1].joinpath(
        "oracle", "src", "oracle", "acp_builder", *parts
    )
