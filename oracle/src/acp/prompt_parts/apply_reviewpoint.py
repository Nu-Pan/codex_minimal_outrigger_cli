# std
from pathlib import Path

# cmoc
from basic.struct_doc import StructDoc
from basic.standard import (
    Requirement,
    Standard,
    standard_to_struct_doc,
)


def build_apply_reviewpoint() -> StructDoc:
    """
    oracle file の内容を realization file に適用する際に発生する「所見（要修正点）を列挙する作業」のレビュー観点を構築する

    TODO ちゃんとコード化する

    - oracle file と実装との明確な不整合
        - 「oracle file 上で記述されている仕様」と「実装」とが明確に不整合している点を指す
        - oracle は仕様断片であるから、明記されていない仕様の隙間は AI の裁量であり、原則として不整合とはみなさない
        - しかしながら、仕様文言から推測可能な意図と実装とが著しく乖離する場合は要修正点とみなす
    - 実装上の明確な問題点
        - 実装だけから見た成果物の品質としての問題を指す
        - バグのような致命的な問題だけを対象とする
        - 「こうした方が良い」のようなクオリティアップ的な話は対象としない
        - 当然ながら、修正後の実装は oracle file 上で記述されている仕様を満たしている必要がある
    """
    ...
