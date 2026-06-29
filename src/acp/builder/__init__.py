"""oracle.acp_builder を acp.builder として公開する互換入口。

`<work-root>/oracle/src/oracle/acp_builder` を正本に保ったまま既存の
`acp.builder.*` 参照を成立させるために残す。削除条件は realization 側と
利用者向け公開面から `acp.builder.*` 参照がなくなること。
"""
