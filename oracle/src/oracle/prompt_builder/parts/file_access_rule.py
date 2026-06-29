# cmoc
from oracle.other.path_model import resolve_work_root
from oracle.other.struct_doc import StructDoc, ntqs
from oracle.other.file_access_profile import FAProfile
from oracle.prompt_builder.basic import PlaceholderMap


def build_file_access_rule(
    faprofile: FAProfile,
) -> tuple[PlaceholderMap, StructDoc]:
    """
    AI エージェントによるファイル読み書き規則のプロンプトを構築する

    mode:
        ファイルアクセスプロファイル
    """
    # TODO
    #   このルールの読み方の説明が必要
    #   Codex CLI 特有の `:root` みたいなのは何らかの対応が必要
    body = "\n".join(f"- `{rule.pattern}` is `{rule.attr}`" for rule in faprofile)
    # 正常終了
    return (
        {
            "work-root": resolve_work_root(),
        },
        StructDoc(
            f"file access profile",
            body,
        ),
    )
