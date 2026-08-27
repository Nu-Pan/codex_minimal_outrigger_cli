# cmoc
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import SDHeader
from oracle.prompt_builder.basic import PlaceholderMap


def build_oracle_and_realization_basic(
    path_context: AgentCallPathContext,
) -> tuple[PlaceholderMap, SDHeader]:
    """oracle, realization についての基本知識の説明文章を構築する。

    NOTE
        意味仕様は `oracle/doc/app_spec/oracle_and_realization.md` の
        「oracle file と realization file の責務」と
        `oracle/doc/app_spec/oracle_and_realization_file_enumeration.md` の
        「分類結果」を参照。
    """
    root_definitions = path_context.root_placeholder_definitions()
    return (
        {"work-root": root_definitions["work-root"]},
        SDHeader(
            "oracle and realization basic",
            SDHeader(
                "oracle file",
                SDHeader(
                    "役割",
                    """
                    - oracle file は人間が所有し 100% の責任を負う正本仕様断片である
                    - oracle file の内容に対する主たる編集者は人間であり、agent は補助のみを行う
                    - oracle file を正本として realization file が生成されるものとし、その逆は禁止である
                    """,
                ),
                SDHeader(
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
                SDHeader(
                    "分類方法",
                    """
                    以下の条件をすべて満たすものを oracle file とする

                    - regular file である
                    - uncategorised file ではない
                    - `{{work-root}}/oracle` ツリー内である
                    """,
                ),
            ),
            SDHeader(
                "realization file",
                SDHeader(
                    "役割",
                    """
                    - oracle file で述べられた人間意図を具体化したものである
                    - realization file を編集するのは AI であり、人間ではない
                    - realization file は正本仕様を述べるものではない
                    """,
                ),
                SDHeader(
                    "下位概念",
                    """
                    - realization code
                        - realization file のうち、実装またはテストのソースコードを指す
                    - realization implementation
                        - realization code のうち、実装ファイルを指す
                        - 純粋なソースコードだけでなく、プロダクトの挙動を記述する設定ファイル類も含む
                        - 通常は `{{work-root}}/src` に配置されている
                    - realization test
                        - realization test とは、realization code のうち、テストのソースコードを指す
                        - 通常は `{{work-root}}/test` に配置されている
                    - realization ancillary
                        - realization ancillary とは、realization file のうち、補助的なファイルを指す
                        - e.g. `{{work-root}}/.gitignore`, `{{work-root}}/bin/**/*`, ...
                    """,
                ),
                SDHeader(
                    "分類方法",
                    """
                    以下の条件をすべて満たすものを realization file とする

                    - regular file である
                    - uncategorised file ではない
                    - `{{work-root}}` ツリー内である
                    - `{{work-root}}/oracle` ツリー外である
                    """,
                ),
            ),
            SDHeader(
                "uncategorised file",
                SDHeader(
                    "説明",
                    """
                    oracle, realization どちらにも該当しない、分類対象外のファイルを指す
                    """,
                ),
                SDHeader(
                    "分類方法",
                    SDHeader(
                        "パスによる分類",
                        """
                        以下のディレクトリツリー内のファイルはすべて uncategorised file とする。

                        - `{{work-root}}/.agents`
                        - `{{work-root}}/.codex`
                        - `{{work-root}}/.cmoc`
                        - `{{work-root}}/memo`

                        以下の名前を持つファイルはすべて uncategorised file とする。

                        - `INDEX.md`
                        - `AGENTS.md`
                        """,
                    ),
                    SDHeader(
                        "git ignore による分類",
                        """
                        以下の条件をすべて満たすものを uncategorised file とする。

                        - regular file である
                        - git 未追跡である
                        - git ignore 判定で無視される

                        ただし、

                        - `{{work-root}}` 内にネストした git working tree がある場合、最も内側の git repository を owning repository として git ignore 判定を行う
                        - git ignore 判定は `git -C <owning-repository-root> check-ignore --quiet -- <repository-relative-path>` と意味的に等価であれば良い
                        """,
                    ),
                    SDHeader(
                        ".git による分類",
                        """
                        以下の条件、

                        - regular file or regular directory である
                        - 名前が `.git` である
                        - 実際に git repository metadata である (たまたま名前が一致しただけではない)

                        をすべて満たすものについて、
                         
                        - `.git` file なら、それを uncategorised file とする
                        - `.git` directory なら、そのツリー内全体を uncategorised file とする
                        """,
                    ),
                ),
            ),
        ),
    )
