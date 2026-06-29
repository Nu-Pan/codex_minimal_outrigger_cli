"""`<work-root>/oracle/src/oracle/acp_builder/indexing/index_entry.py` を再公開する。

既存の `acp.builder.indexing.index_entry` 参照を維持するために残す互換入口。
削除条件は realization 側と利用者向け公開面から同参照がなくなること。
"""

from oracle.acp_builder.indexing.index_entry import *  # noqa: F403
