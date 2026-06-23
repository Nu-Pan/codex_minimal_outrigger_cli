from dataclasses import dataclass
from typing import Literal
from basic.struct_doc import StructDoc


class Standard:
    """
    「何らかの事柄が従うべき規範」のフォーマットを定義するクラス
    e.g. oracle file は oracle standard に従うし、oracle standard は `Standard` を元に生成される
    `Stnadrd` は `<cmoc-root>` ツリー内に対して適用されるものであり、`<work-root>` ツリー内は対象外である
    """

    def __init__(
        self,
        title: str,
        backgrounds: list[str],
        requirements: list["Requirement"],
        criteria: list[str] = list(),
        examples: list[str] = list(),
    ):
        # title
        # - この standard の見出し
        self._title = title
        # backgrounds
        # - この standard が必要になる背景・前提
        # - 必須フィールド
        # - requirements と内容が重複しないように注意
        if (
            isinstance(backgrounds, list)
            and len(backgrounds) > 0
            and all(isinstance(i, str) for i in backgrounds)
        ):
            self._backgrounds = backgrounds
        else:
            raise ValueError(f"Invalid backgrounds (backgrounds={backgrounds})")
        # requirements
        # - この standard が要求する規範
        # - 必須フィールド
        if (
            isinstance(requirements, list)
            and len(requirements) > 0
            and all(isinstance(i, Requirement) for i in requirements)
        ):
            self._requirements = requirements
        else:
            raise ValueError(f"Invalid requirements (requirements={requirements})")
        # examples
        # - requirements フィールドだけからは汲み取り切れない意図を補足するための判断例を書く
        # - requirements フィールドだけからわかるようなことを examples で冗長に補足することはしない
        # - requirements フィールドに書いていない事を examples フィールドに新しく書いてはいけない
        # - 典型的には、状況例、判断の根拠・判断結果の３段構成で書く
        if (
            isinstance(examples, list)
            and len(examples) > 0
            and all(isinstance(i, str) for i in examples)
        ):
            self._examples = examples
        elif isinstance(examples, list) and len(examples) == 0:
            self._examples = list()
        else:
            raise ValueError(f"Invalid example (example={examples})")

    @property
    def title(self) -> str:
        return self._title

    @property
    def backgrounds(self) -> list[str]:
        return self._backgrounds

    @property
    def requirements(self) -> list["Requirement"]:
        return self._requirements

    @property
    def examples(self) -> list[str]:
        return self._examples


@dataclass(frozen=True)
class Requirement:
    """
    Standard の要求フィールド
    Standard が要求する規範
    """

    # ラベル
    # 必須: 破ると standard 違反になる
    # 禁止: してはいけない
    # 推奨: 原則として従うが、理由があれば外してよい
    # 許容: 禁止ではないことを明示する
    label: Literal["必須", "禁止", "推奨", "許容"]

    # 要求の本文
    # １文で簡潔に書く
    # - e.g. 良い要求の書き方
    #     - 許容: oracle file の隙間に未定義部分が残ることは許容する
    #     - 必須: 実装差が許されない事項は、人間が oracle file に明示する
    #     - 推奨: AI 裁量で補う仕様の規模は小さく保つ
    body: str


def standard_to_struct_doc(standard: Standard) -> StructDoc:
    """
    standard を StructDocs に変換する。
    """
    fields = [
        StructDoc(
            "背景",
            ".\n".join(f"- {b}" for b in standard.backgrounds),
        ),
        StructDoc(
            "要求",
            ".\n".join(f"- [{r.label}] {r.body}" for r in standard.requirements),
        ),
    ]
    if standard.examples:
        fields.append(
            StructDoc(
                "判断例",
                ".\n".join(f"- {e}" for e in standard.examples),
            ),
        )
    return StructDoc(standard.title, *fields)
