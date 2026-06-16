# cmoc
from utils.struct_doc import StructDoc

# local
from .file_access_rule import build_file_access_rule, FileAccessMode
from .oracle_standard import build_oracle_standard
from .realization_standard import build_realization_standard
from .oracle_and_realization_basic import build_oracle_and_realization_basic


def build_complete_prompt(
    role: str,
    summary: str,
    goal: str,
    file_access_mode: FileAccessMode,
    *,
    oracles_and_realization_basic: bool = False,
    oracle_standard: bool = False,
    realization_standard: bool = False,
    structured_output: bool,
) -> list[StructDoc]:
    """
    実際に AI エージェントに渡すことができる完全なプロンプトを構築する
    """
    struct_doc = [
        StructDoc(
            "role",
            role,
        ),
        StructDoc(
            "sumary",
            summary,
        ),
        StructDoc(
            "goal",
            goal,
        ),
        build_file_access_rule(file_access_mode),
    ]
    if oracles_and_realization_basic or oracle_standard or realization_standard:
        struct_doc.append(build_oracle_and_realization_basic())
    if oracle_standard:
        struct_doc.append(build_oracle_standard())
    if realization_standard:
        struct_doc.append(build_realization_standard())
    if structured_output:
        struct_doc.append(
            StructDoc(
                "output format",
                """
                - 指定された Structured output schema に従う結果を返すこと
                """,
            )
        )
    return struct_doc
