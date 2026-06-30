# cmoc
from oracle.other.path_model import resolve_work_root
from oracle.other.struct_doc import StructDoc, ntqs
from oracle.acp_builder.basic import FileAccessMode
from oracle.prompt_builder.basic import PlaceholderMap


def build_file_access_rule(mode: FileAccessMode) -> tuple[PlaceholderMap, StructDoc]:
    """
    AI エージェントによるファイル読み書き規則のプロンプトを構築する

    mode:
        読み書きモードプリセット
    """
    # 本文を構築
    rules = list()
    match mode:
        case FileAccessMode.READONLY:
            rules += [
                "`<work-root>` ツリー外は読み書き禁止",
                "`<work-root>` ツリー内は書き込み禁止",
                "`<work-root>/memo` は読み書き禁止",
            ]
        case FileAccessMode.PURE_ORACLE_READ:
            rules += [
                "`<work-root>/oracle` ツリー外は読み書き禁止",
                "`<work-root>/oracle` ツリー内は書き込み禁止",
            ]
        case FileAccessMode.REALIZATION_WRITE:
            rules += [
                "`<work-root>` ツリー外は読み書き禁止",
                "`<work-root>/oracle` ツリー内は書き込み禁止",
                "`<work-root>/memo` は読み書き禁止",
            ]
        case FileAccessMode.ORACLE_WRITE:
            rules += [
                "`<work-root>` ツリー外は読み書き禁止",
                "`<work-root>/oracle` ツリー外は書き込み禁止",
                "`<work-root>/memo` は読み書き禁止",
            ]
        case FileAccessMode.REPO_WRITE:
            rules += [
                "`<work-root>` ツリー外は読み書き禁止",
                "`<work-root>/memo` は読み書き禁止",
            ]
        case _:
            raise ValueError(f"Invalid mode (mode={mode})")
    rules += [
        "上記に対する例外として `git check-ignore --stdin` で git 追跡対象外と判定されたファイル・ディレクトリは読み書き許可",
    ]
    # 正常終了
    return (
        {
            "work-root": resolve_work_root(),
        },
        StructDoc(
            f"file read write rule - {mode.value}",
            "\n".join(f"- {r}" for r in rules),
        ),
    )
