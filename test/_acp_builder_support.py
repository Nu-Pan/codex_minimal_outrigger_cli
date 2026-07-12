from pathlib import Path


def oracle_schema_path(*parts: str) -> Path:
    # Keep schema expectations in the oracle tree instead of copying them into tests.
    return Path(__file__).parents[1].joinpath(
        "oracle", "src", "oracle", "acp_builder", *parts
    )
