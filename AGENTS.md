# cmoc 固有のリポジトリ指示

Codex Minimal Outrigger CLI（cmoc）は、cmoc 自身を使ってこのリポジトリを開発する運用を前提とする。
cmoc は agent call ごとにプロンプトを動的生成し、その作業における作業範囲、ファイルアクセス、oracle/realization の規則、INDEX.md によるルーティングを指定する。

本ファイルは、動的生成プロンプトの内容を再定義せず、自己開発で恒常的に必要となるリポジトリ固有の指示だけを補足する。
本ファイルの記述や参照先を根拠に、動的生成プロンプトが定める権限や作業範囲を広げてはならない。

## 重要な oracle file

以下は cmoc 自己開発における標準的な作業方法を定める重要な oracle file である。
本ファイルの説明と oracle file の本文に差がある場合は、oracle file の本文を優先する。

- Python 実行環境、環境構築、Python・pip の実行方法を確認するときは、`oracle/doc/dev_rule/development_environment.md` を読む。
- realization implementation の配置先や CLI 実装の責務境界を判断するときは、`oracle/doc/dev_rule/design_rule.md` を読む。
- realization test の実装・実行方法や、変更後の検証方法を判断するときは、`oracle/doc/dev_rule/test_rule.md` を読む。
