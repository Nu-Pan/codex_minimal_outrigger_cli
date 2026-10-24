"""oracle file と realization file の基本知識を説明する文面の構築定義。"""

# cmoc
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import SDHeader
from oracle.prompt_builder.basic import PlaceholderMap


def build_cmoc_basic_instruction(
    path_context: AgentCallPathContext,
) -> tuple[PlaceholderMap, SDHeader]:
    """cmoc が仮定するワークフローについての基本知識の説明文章を構築する。"""
    root_definitions = path_context.root_placeholder_definitions()
    return (
        {"work-root": root_definitions["work-root"]},
        SDHeader(
            "cmoc basic instruction",
            SDHeader(
                "decision",
                SDHeader(
                    "説明",
                    """
                    - decision は人間意図であり、人間が判断を下した決定事項であり、正本仕様断片である
                    - GitHub Flavored Markdown で記述する
                    """,
                ),
                SDHeader(
                    "分類方法",
                    """
                    以下の条件をすべて満たすものを decision file とする

                    - regular file である
                    - uncategorised file ではない
                    - `{{work-root}}/decision/**/*.md` とマッチする

                    decision file 内の、見出し 1 件を decision 1 件とする
                    """,
                ),
                SDHeader(
                    "ID の形式",
                    """
                    - decision の見出しの先頭には `\\[DECI-\\d{6}\\]` の形式で ID が付与される
                    - decision に対する参照は「... については [DECI-XXXXXX] を参照」の形式で記述すること
                    """,
                ),
            ),
            SDHeader(
                "reference",
                SDHeader(
                    "説明",
                    """
                    - reference は decision から参照される補足資料である
                    """,
                ),
                SDHeader(
                    "分類方法",
                    """
                    以下の条件をすべて満たすものを reference file とする

                    - regular file である
                    - uncategorised file ではない
                    - `{{work-root}}/reference` ツリー内である

                    reference file, reference は概念的には同じものを指す
                    """,
                ),
            ),
            SDHeader(
                "spec",
                SDHeader(
                    "説明",
                    """
                    - spec は decision, reference を正本として AI エージェントが生成する仕様文章である
                    - GitHub Flavored Markdown で記述する
                    """,
                ),
                SDHeader(
                    "分類方法",
                    """
                    以下の条件をすべて満たすものを spec file とする

                    - regular file である
                    - uncategorised file ではない
                    - `{{work-root}}/spec/**/*.md` とマッチする

                    spec file 内の、見出し 1 件を spec 1 件とする
                    """,
                ),
                SDHeader(
                    "ID の形式",
                    """
                    - spec の見出しの先頭には `\\[SPEC-\\d{6}\\]` の形式で ID が付与される
                    - spec に対する参照は「... については [SPEC-XXXXXX] を参照」の形式で記述すること
                    """,
                ),
            ),
            SDHeader(
                "realization",
                SDHeader(
                    "役割",
                    """
                    - realization は decision, reference, spec を正本として AI エージェントが生成する実体 (実装、テスト、補助ファイル) である
                    """,
                ),
                SDHeader(
                    "分類方法",
                    """
                    以下の条件をすべて満たすものを realization file とする

                    - regular file である
                    - uncategorised file ではない
                    - `{{work-root}}` ツリー内である
                    - decision file, reference file, spec file, memo file のいずれでもない

                    realization file, realization は概念的には同じものを指す
                    """,
                ),
            ),
            SDHeader(
                "memo",
                SDHeader(
                    "役割",
                    """
                    - memo は人間専用のメモである
                    """,
                ),
                SDHeader(
                    "分類方法",
                    """
                    以下の条件をすべて満たすものを memo file とする

                    - regular file である
                    - uncategorised file ではない
                    - `{{work-root}}/memo` ツリー内である

                    memo file, memo は概念的には同じものを指す
                    """,
                ),
            ),
            SDHeader(
                "uncategorised file",
                SDHeader(
                    "説明",
                    """
                    decision, reference, spec, realization, memo のいずれにも該当しない、分類対象外のファイルを指す
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

                        以下の名前を持つファイルはすべて uncategorised file とする。

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
