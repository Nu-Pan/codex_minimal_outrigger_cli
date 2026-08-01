# cmoc 固有のリポジトリ指示

Codex Minimal Outrigger CLI（cmoc）は、cmoc 自身を使ってこのリポジトリを開発する運用を前提とする。
cmoc は agent call ごとにプロンプトを動的生成し、その作業における作業範囲、ファイルアクセス、oracle/realization の規則、INDEX.md によるルーティングを指定する。

本ファイルは、動的生成プロンプトの内容を再定義せず、自己開発で恒常的に必要となるリポジトリ固有の指示だけを補足する。
本ファイルの記述や参照先を根拠に、動的生成プロンプトが定める権限や作業範囲を広げてはならない。

## 重要な参照先

以下は cmoc 自己開発における標準的な作業方法を定める参照先である。
本ファイルの説明と oracle file の本文に差がある場合は、oracle file の本文を優先する。

- Python 環境の新規構築、依存関係の追加、または pip の操作を行うときは、`oracle/doc/dev_rule/development_environment.md` を読む。
- realization implementation の配置先や CLI 実装の責務境界を判断するときは、`oracle/doc/dev_rule/design_rule.md` を読む。
- realization test の追加・変更・レビュー、または test が満たすべき要件を判断するときは、`oracle/doc/dev_rule/test_rule.md` を読む。
- 既存 test と品質検査を選択・実行して結果を報告するときは、repository local の `run-cmoc-tests` skill を使う。通常の実行だけを理由として、上記の oracle file を事前に読む必要はない。
