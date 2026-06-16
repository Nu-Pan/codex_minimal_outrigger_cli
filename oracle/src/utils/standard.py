from dataclasses import dataclass
from typing import Literal
from utils.struct_doc import StructDoc


class Standard:
    """
    何らかの事柄について、標準的に従うべき事項
    - `<cmoc-root>` の oracle file 上には cmoc 成果物 (e.g. oracle, realization, ...) に対する  が存在する
    - これら  の記述は一定のフォーマットに従うものとする
    - このフォーマット規則は `<cmoc-root>` 上の oracle file に適用されるものであり、`<repo-root>` 上の oracle file は対象外である
    """

    def __init__(
        self,
        title: str,
        targets: list[str],
        backgrounds: list[str],
        requirements: list["Requirement"],
        criteria: list[str] = list(),
        examples: list[str] = list(),
    ):
        # title
        # - この standard の見出し
        self._title = title
        # targets
        # - この standard が適用される対象
        # - 必須フィールド
        # - e.g.
        #     - oracle file
        #     - realization file
        #     - realization code
        #     - ...
        if (
            isinstance(targets, list)
            and len(targets) > 0
            and all(isinstance(i, str) for i in targets)
        ):
            self._targets = targets
        else:
            raise ValueError(f"Invalid targets (targets={targets})")
        # backgrounds
        # - この standard が必要になる理由・前提
        # - 必須フィールド
        # - 規範は書かない
        #     - ～しなければならない、～すべきである、禁止、許容、のような判断は「背景」には書かない
        # - e.g. 良い背景の書き方
        #     - file の規模が大きいほど、人間または AI が読む文脈量が増える
        #     - 同じ責務の記述が複数箇所にあると、どちらを正とみなすべきか判断しにくくなる
        # - e.g. 良くない背景の書き方
        #     - file の規模は小さくしなければならない
        if (
            isinstance(backgrounds, list)
            and len(backgrounds) > 0
            and all(isinstance(i, str) for i in backgrounds)
        ):
            self._backgrounds = backgrounds
        else:
            raise ValueError(f"Invalid backgrounds (backgrounds={backgrounds})")
        # requirements
        # - この  が要求する規範
        # - 必須フィールド
        if (
            isinstance(requirements, list)
            and len(requirements) > 0
            and all(isinstance(i, Requirement) for i in requirements)
        ):
            self._requirements = requirements
        else:
            raise ValueError(f"Invalid requirements (requirements={requirements})")
        # criteria
        # - この standard を満たしているかをレビューする際の判定基準を述べる
        # - ここに要求を書いてはいけない
        # - 省略可能
        # - e.g. 良い判定の書き方
        #     - 同じ責務を持つ記述・実装・テストが複数箇所に残っていない
        #     - 削除済み仕様に対応する記述・分岐・テストが残っていない
        if (
            isinstance(criteria, list)
            and len(criteria) > 0
            and all(isinstance(i, str) for i in criteria)
        ):
            self._criteria = criteria
        elif isinstance(criteria, list) and len(criteria) == 0:
            pass
        else:
            raise ValueError(f"Invalid criteria (criteria={criteria})")
        # example
        # - 「要求」フィールドで言いたいことを補足するための例示を書く
        # - ここに新しい要求を書いてはいけない（例示内で要求を増やしてはいけない）
        # - e.g. 良い例示の書き方
        #     - OK: 同じ説明を複数箇所に書かず、1 箇所にまとめて参照する
        #     - NG: 似た仕様説明を各サブコマンド仕様に少しずつコピーする
        if (
            isinstance(examples, list)
            and len(examples) > 0
            and all(isinstance(i, str) for i in examples)
        ):
            self._examples = examples
        elif isinstance(examples, list) and len(examples) == 0:
            pass
        else:
            raise ValueError(f"Invalid example (example={examples})")

    @property
    def title(self) -> str:
        return self._title

    @property
    def targetgs(self) -> list[str]:
        return self._targets

    @property
    def backgrounds(self) -> list[str]:
        return self._backgrounds

    @property
    def requirements(self) -> list["Requirement"]:
        return self._requirements

    @property
    def criteria(self) -> list[str]:
        return self._criteria

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
    # 必須: 破ると  違反になる
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
            "対象",
            ".\n".join(f"- {t}" for t in standard.targetgs),
        ),
        StructDoc(
            "背景",
            ".\n".join(f"- {b}" for b in standard.backgrounds),
        ),
        StructDoc(
            "要求",
            ".\n".join(f"- [{r.label}] {r.body}" for r in standard.requirements),
        ),
    ]
    if standard.criteria:
        fields.append(
            StructDoc(
                "判定基準",
                ".\n".join(f"- {c}" for c in standard.criteria),
            ),
        )
    if standard.examples:
        fields.append(
            StructDoc(
                "例示",
                ".\n".join(f"- {e}" for e in standard.examples),
            ),
        )
    return StructDoc(standard.title, *fields)
