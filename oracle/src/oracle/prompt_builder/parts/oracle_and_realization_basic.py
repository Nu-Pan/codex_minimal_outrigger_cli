# cmoc
from oracle.other.path_model import resolve_work_root
from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_oracle_and_realization_basic() -> tuple[PlaceholderMap, StructDoc]:
    """
    oracle, realization についての基本知識の説明文章を構築する
    """
    # エイリアス
    work_root = resolve_work_root()
    return (
        {
            "work-root": str(work_root),
        },
        StructDoc(
            "oracle and realization basic",
            StructDoc(
                "oracle",
                StructDoc(
                    "oracle file",
                    StructDoc(
                        "定義",
                        """
                        以下の条件をすべて満たしたファイルの事を指す
                        - `{{work-root}}/oracle` ツリー内である
                        - ファイル名が `INDEX.md`, `AGENTS.md` のいずれでもない
                        - `git check-ignore` で git 追跡対象外ではないと判定された
                        """,
                    ),
                    StructDoc(
                        "役割",
                        """
                        - oracle file は人間が所有し 100% の責任を負う正本仕様断片である
                        - oracle file の内容に対する主たる編集者は人間であり、agent は補助のみを行う
                        - oracle file を正本として realization file が生成されるものとし、その逆は禁止である
                        """,
                    ),
                    StructDoc(
                        "下位概念",
                        """
                        - oracle doc
                            - oracle file のうち、自然言語の markdown ドキュメント形式で記述されたもの
                            - `{{work-root}}/oracle/doc` に配置されている
                        - oracle src
                            - oracle file のうち、プログラミング言語・設定ファイルで記述された実装
                            - `{{work-root}}/oracle/src` に配置されている
                        - oracle test
                            - oracle file のうち、プログラミング言語で記述されたテスト
                            - `{{work-root}}/oracle/test` に配置されている
                        """,
                    ),
                ),
            ),
            StructDoc(
                "realization file",
                StructDoc(
                    "定義",
                    """
                    以下の条件をすべて満たしたファイルの事を指す
                    - `{{work-root}}` ツリー内である
                    - `{{work-root}}/oracle` ツリー内ではない
                    - `{{work-root}}/memo` ツリー内ではない
                    - `{{work-root}}/.git` ツリー内ではない
                    - `{{work-root}}/.agents` ツリー内ではない
                    - `{{work-root}}/.codex` ツリー内ではない
                    - `{{work-root}}/.cmoc` ツリー内ではない
                    - ファイル名が `INDEX.md`, `AGENTS.md` のいずれでもない
                    - `git check-ignore` で git 追跡対象外ではないと判定された
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
                    """
                    - realization code
                        - realization file のうち、実装またはテストのソースコードを指す
                    - realization implementation
                        - realization code のうち、実装ファイルを指す
                        - 純粋なソースコードだけでなく、プロダクトの挙動を記述する設定ファイル類も含む
                        - `{{work-root}}/src` に配置されている
                    - realization test
                        - realization test とは、realization code のうち、テストのソースコードを指す
                        - `{{work-root}}/test` に配置されている
                    - realization ancillary
                        - realization ancillary とは、realization file のうち、補助的なファイルを指す
                        - e.g. `{{work-root}}/.gitignore`, `{{work-root}}/bin/**/*`
                    """,
                ),
            ),
        ),
    )
