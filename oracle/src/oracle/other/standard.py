from dataclasses import dataclass
from typing import Literal

from oracle.other.struct_doc import StructDoc


class Standard:
    """agent 向け instruction の要求文面を構造化する。"""

    def __init__(
        self,
        title: str,
        requirements: list["Requirement"],
        examples: list[str] = list(),
    ):
        # title
        # - この standard の見出し
        self._title = title
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
    #     - 必須: 対象を読むべき条件を判断できる意味情報を書く
    #     - 禁止: 対象外の責務を推測で追加してはいけない
    body: str


def standard_to_struct_doc(standard: Standard) -> StructDoc:
    """agent 向け instruction 文面へ変換する。"""
    fields = [
        StructDoc(
            "要求",
            ".\n".join(f"- [{r.label}] {r.body}" for r in standard.requirements),
        )
    ]
    if standard.examples:
        fields.append(
            StructDoc(
                "判断例",
                ".\n".join(f"- {e}" for e in standard.examples),
            ),
        )
    return StructDoc(standard.title, *fields)
