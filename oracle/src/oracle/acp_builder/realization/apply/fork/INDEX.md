# `launch_exec.py`

## Summary
- `cmoc realization apply fork` が oracle file の差分を realization file へ追従適用する AgentCallParameter を構築する定義。commit 範囲と raw git diff を構造化して完全 prompt に埋め込み、run worktree、realization 書き込み権限、最高品質のモデル設定、全体調査・検証方針を起動パラメータへ固定する。

## Read this when
- `cmoc realization apply fork` の prompt 内容、差分追従の完了条件、または AgentCallParameter の起動設定を確認・変更するとき。
- oracle file の変更を realization 全体へ反映する agent call の作業範囲、権限、パスコンテキストを調査するとき。

## Do not read this when
- realization の具体的な実装・テスト・補助ファイルを直接確認または変更する場合は、生成された prompt の定義ではなく対象の realization file を直接読む。
- 一般的な prompt 構築や他の realization 起動経路を調査する場合は、それぞれの builder 定義を直接読む。

## hash
- a94dca14044b22a403f70cdb124d19177755e285ad3705b2b10b4e3c8bbafdba
