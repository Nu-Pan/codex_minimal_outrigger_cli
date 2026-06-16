# cmoc
from oracle.src.utils.struct_doc import StructDoc
from utils.path_model import (
    resolve_cmoc_root,
    resolve_repo_root,
    resolve_run_root,
    resolve_work_root,
)


def build_oracle_and_realization_basic() -> StructDoc:
    """
    oracles, realization についての基本知識の説明文章を構築する
    """
    # エイリアス
    work_root = resolve_work_root()
    return StructDoc(
        "oracle and realization basic",
        StructDoc(
            "oracle",
            StructDoc(
                "oracle file",
                StructDoc(
                    "定義",
                    f"""
                    以下の条件をすべて満たしたファイルの事を指す
                    - `{work_root}/oracle` ツリー内である
                    - `{work_root}/.gitignore` の対象ではない
                    - `INDEX.md` ではない
                    """,
                ),
                StructDoc(
                    "役割",
                    """
                    - oracle file は人間が所有し 100% の責任を負う正本仕様断片である
                    - oracle file の内容に対して AI は提案を行うことは出来るが、実際の編集を行うのは必ず人間である
                    - oracle file を正本として realization file が生成されるものとし、その逆は禁止である
                    """,
                ),
                StructDoc(
                    "下位概念",
                    f"""
                    - oracle doc
                        - oracle file のうち、自然言語の markdown ドキュメント形式で記述されたもの
                        - `{work_root}/oracle/doc` に配置されている
                    - oracle src
                        - oracle file のうち、プログラミング言語・設定ファイルで記述された実装
                        - `{work_root}/oracle/src` に配置されている
                    - oracle test
                        - oracle file のうち、プログラミング言語で記述されたテスト
                        - `{work_root}/oracle/test` に配置されている
                    """,
                ),
            ),
        ),
        StructDoc(
            "realization file",
            StructDoc(
                "定義",
                f"""
                以下の条件をすべて満たしたファイルの事を指す
                - `{work_root}` ツリー内である
                - `{work_root}/oracle` ツリー内ではない (i.e. oracle file ではない)
                - `{work_root}/.gitignore` の対象ではない
                - `INDEX.md` ではない
                """,
            ),
            StructDoc(
                "役割",
                """
                - oracle file で述べられた人間意図を具体化したものである
                - realization file を編集するのは AI であり、人間ではない
                - realization file は正本仕様を述べるものではない
                """,
            ),
            StructDoc(
                "下位概念",
                f"""
                - realization code
                    - realization file のうち、実装またはテストのソースコードを指す
                - realization implementation
                    - realization code のうち、実装ファイルを指す
                    - 純粋なソースコードだけでなく、プロダクトの挙動を記述する設定ファイル類も含む
                    - `{work_root}/src` に配置されている
                - realization test
                    - realization test とは、realization code のうち、テストのソースコードを指す
                    - `{work_root}/test` に配置されている
                - realization ancillary
                    - realization ancillary とは、realization file のうち、補助的なファイルを指す
                    - e.g. `{work_root}/.gitignore`, `{work_root}/bin/**/*`
                """,
            ),
        ),
    )
