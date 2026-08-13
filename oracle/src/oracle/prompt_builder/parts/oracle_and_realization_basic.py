# cmoc
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_oracle_and_realization_basic(
    path_context: AgentCallPathContext,
) -> tuple[PlaceholderMap, StructDoc]:
    """
    oracle, realization についての基本知識の説明文章を構築する
    """
    # この part の文面が参照する root 定義を call-scoped context から取得する
    root_definitions = path_context.root_placeholder_definitions()
    return (
        {"work-root": root_definitions["work-root"]},
        StructDoc(
            "oracle and realization basic",
            StructDoc(
                "分類",
                """
                `{{work-root}}` 配下の regular file を、次の境界で oracle file と realization file に分類する。

                **常時対象外 root**

                次の exact path は、`{{work-root}}` 直下にある場合だけ、その path 自身と全 descendant を常時対象外にする。nested の同名 path は、名前だけで対象外にしない。

                - `{{work-root}}/.git`
                - `{{work-root}}/.agents`
                - `{{work-root}}/.codex`
                - `{{work-root}}/.cmoc`
                - `{{work-root}}/memo`

                **Git repository と ignore 判定**

                - nested Git working tree の `.git` path は、実際の repository metadata であると確認できた場合だけ、その path 自身と全 descendant を対象外にする
                - 候補 path を含む最内側の検証済み Git working tree を owning repository とする
                - owning repository の root と nested の `.gitignore`、repository-local exclude、および global exclude を使用する、通常の index-aware な Git ignore 判定を適用する
                - tracked な regular file は、ignore pattern に一致しても分類対象に含める
                - Git ignore によって除外するのは、untracked かつ ignored な regular file だけとする
                - untracked かつ unignored な regular file は分類対象に含める

                **分類結果**

                - `{{work-root}}/oracle` ツリー内にあり、ファイル名が `INDEX.md` と `AGENTS.md` のいずれでもない regular file を oracle file とする
                - `{{work-root}}` ツリー内かつ `{{work-root}}/oracle` ツリー外にあり、ファイル名が `INDEX.md` と `AGENTS.md` のいずれでもない regular file を realization file とする
                """,
            ),
            StructDoc(
                "oracle",
                StructDoc(
                    "oracle file",
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
