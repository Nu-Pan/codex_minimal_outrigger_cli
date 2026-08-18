# `oracle`

## Summary
- oracle/src/oracle は、agent call の用途別定義、feedback 入力契約、共有設定・パス・文書化ヘルパー、完全 prompt 構築処理をまとめる oracle 実装領域である。各下位ディレクトリは、agent 呼び出し設定、feedback 構造化、共有モデル、prompt 構成という異なる責務への入口になる。

## Read this when
- agent call の用途別設定や出力契約を調査・変更するときは acp_builder から確認を始めるとよい。
- feedback reporter の入力契約や問題情報の構造化を確認するときは feedback から確認を始めるとよい。
- 共有設定、パス解決、構造化 Markdown 生成の責務を確認するときは other から確認を始めるとよい。
- agent call に渡す完全 prompt の構成、placeholder、共通規範や policy の組み込み経路を確認するときは prompt_builder から確認を始めるとよい。

## Do not read this when
- agent call の共通型や共通 prompt 生成、パス解決など、oracle 配下の特定用途に固有でない処理だけを確認したい場合は、該当する共通実装を直接読む方が適切である。
- realization の具体的な実装・テスト、oracle file 自体の仕様内容、collector 側の保存や集約だけを確認したい場合は、このディレクトリを入口にする必要はない。
- 既存の INDEX.md のルーティング内容や文書全体のナビゲーションだけを確認したい場合は、このディレクトリを読む必要はない。

## hash
- 14e076dd0067685ad4fba2155ce7b7e94aa54e69bb6ae95c6722e9eda5b02a90
