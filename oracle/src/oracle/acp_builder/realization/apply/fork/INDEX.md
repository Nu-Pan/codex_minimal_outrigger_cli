# `launch_exec.py`

## Summary
- このファイルは、`cmoc realization apply fork` における差分追従 Agent Call の起動パラメータを構築する実装です。追従対象の commit 範囲と oracle file の raw git diff を構造化し、完全な prompt に埋め込みます。関連する prompt 構築定義や Agent Call の設定を確認・変更するときの入口です。

## Read this when
- `cmoc realization apply fork` が生成する prompt の文面、追従対象変更の渡し方、または起動時のモデル・推論・ファイルアクセス設定を確認するとき。
- 差分追従処理の完了条件、oracle/realization の参照方針、リポジトリ全体を対象とする routing 設定を確認するとき。

## Do not read this when
- realization の具体的な実装・テスト・補助ファイルそのものを変更または確認するときは、対象の realization file を直接読む。
- 一般的な prompt 構築や共通の AgentCall 型・パス型・構造化文書の仕様だけを確認するときは、この起動定義ではなく各共通モジュールを直接読む。

## hash
- 4a0a7e18286f4877ca2aa90b149adc4eae191e11213c73fbabbba1869a2d3156
