"""oracle src の basic 互換 import 入口。

`{{work-root}}/oracle/src/oracle/other` と ACP 基本型を複製せず既存の
`basic.*` 参照を保つために残す。削除条件は realization 側と利用者向け
公開面から `basic.*` 参照がなくなり、正本側または実体 module へ移行済み
になること。
"""
