"""cmoc 上の論理的なファイルアクセス権限についての基本コンポーネントを定義する"""

# std
from enum import StrEnum, auto
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


# ファイル・ディレクトリに適用するアクセス属性
# deny: 読み書き共に不可
# write: 読み書き共に可能
# read: 読み取りのみ可能
type FAAttr = Literal["deny", "write", "read"]


@dataclass(frozen=True)
class FARule:
    """cmoc 上の論理的なファイルアクセスルール"""

    # このルールが適用されるファイル・ディレクトリパスのパターン
    # `<work-root>` からの相対パス形式で記述する
    # e.g. `<work-root>` そのものなら `.`
    # e.g. `<work-root>/memo` なら `memo`
    # e.g. リポジトリ上の `.bin` ファイルすべてなら `**/*.bin`
    pattern: Path | str

    # pattern にマッチしたファイル・ディレクトリに適用されるアクセス属性
    attr: FAAttr


# cmoc 上の論理的なファイルアクセスプロファイル
#
# より広いルールは、より狭いルールによって上書きされる
# e.g. [(".", "read"), ("memo", deny)]
#   `<work-root>` 内は原則読み取りのみ可能（広いルール）
#   例外的に `<work-root>/memo` は読み書き共に不可（狭いルールで上書き）
#
# 同一のファイル・ディレクトリに対して複数のルールが適用された場合、 deny > write > read の優先順位で適用される。
# e.g. [("oracle", "read"), ("**/INDEX.md", "write")]
#   `<work-root>/oracle` ツリー内の `INDEX.md` に対して read, wirte が同時に指定される。
#   この場合 `("INDEX.md", "write")` として解釈される
type FAProfile = list[FARule]


class FAPProfilePreset(StrEnum):
    """cmoc 上の論理的なファイルアクセスプロファイルのプリセット"""

    READONLY = auto()
    PURE_ORACLE_READ = auto()
    REALIZATION_WRITE = auto()
    ORACLE_WRITE = auto()
    REPO_WRITE = auto()


def build_faprofile(
    oracle_faattr: FAAttr,
    realization_faattr: FAAttr,
    index_faattr: FAAttr,
) -> FAProfile:
    """プリセット値を元に具体的なファイルアクセスプロファイルを構築する

    `AgentCallParameter` を構築する時は基本的に `build_faprofile` 経由で生成する。
    oracle src, realization src 各所での独立した `FAProfile`

    oracle_faattr: FAAttr,
        oracle file に対するファイルアクセス属性

    realization_faattr: FAAttr,
        realization file に対するファイルアクセス属性

    index_faattr: FAAttr,
        index file に対するファイルアクセス属性

    return:
        具体的なファイルアクセスプロファイル
    """
    # 基本ルール
    # NOTE
    #   一番弱い基礎設定として `<work-root>` 全体に対する read を設定する
    #   どんな場合でも `<work-root>/memo` はアクセス全面禁止
    basic_rule = [
        FARule(".", "read"),
        FARule("memo", "deny"),
    ]
    # TODO 
    #   oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py の定義に従う
    #   oracle file, realization file のパターンを動的に生成する
    #   __pycache__ とかの非トラック対象は自由に読み書き出来るようにしたい

    match preset:
        case FAPProfilePreset.READONLY:
            # body = ntqs(f"""
            # - `<work-root>` ツリー外は読み書き禁止
            # - `<work-root>` ツリー内は書き込み禁止
            # - `<work-root>/memo` は読み書き禁止
            # """)
            return [

                FARule(".", "read"),
                FARule("memo", "deny"),
                FARule("**/INDEX.md", "write"),
            ]
        case FAPProfilePreset.PURE_ORACLE_READ:
            # body = ntqs(f"""
            # - `<work-root>` ツリー外は読み書き禁止
            # - `<work-root>/oracle` ツリー内は書き込み禁止
            # - `<work-root>/oracle` ツリー外は読み書き禁止
            # """)
            return [
                FARule("**/INDEX.md", "write")
            ]
        case FAPProfilePreset.REALIZATION_WRITE:
            # body = ntqs(f"""
            # - `<work-root>` ツリー外は読み書き禁止
            # - `<work-root>/oracle` ツリー内は書き込み禁止
            # - `<work-root>/memo` は読み書き禁止
            # """)
        case FAPProfilePreset.ORACLE_WRITE:
            # body = ntqs(f"""
            # - `<work-root>` ツリー外は読み書き禁止
            # - `<work-root>/oracle` ツリー外は書き込み禁止
            # - `<work-root>/memo` は読み書き禁止
            # """)
        case FAPProfilePreset.REPO_WRITE:
            # body = ntqs(f"""
            # - `<work-root>` ツリー外は読み書き共に禁止
            # - `<work-root>/memo` は読み書き禁止
            # """)

def _build_oracle_file_farule(attribute: FAAttr) -> list[FARule]:
    """oracle file に対するファイルアクセスルールを生成する"""

    # TODO 
