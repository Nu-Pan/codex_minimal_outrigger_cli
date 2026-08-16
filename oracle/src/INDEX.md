# `oracle`

## Summary
- cmoc の agent 呼び出し定義と、その prompt・policy・Structured Output schema を構成する Python パッケージ群。共通モデルや文書生成は other、完全 prompt と policy は prompt_builder、用途別の起動パラメータは acp_builder、feedback 入力 schema は feedback 以下へ進む入口となる。

## Read this when
- cmoc の agent 呼び出しに使う prompt、policy、アクセス設定、作業ディレクトリ、Structured Output の定義を調査・変更するとき
- 共通モデルや Markdown 文書生成、完全 prompt の構築、用途別 agent call の設定、feedback 入力契約の配置を確認するとき
- 複数の agent call 定義や policy にまたがる構成を確認し、対象用途の下位ディレクトリへ進む入口を探すとき

## Do not read this when
- 実際の CLI サブコマンドの実行処理や、agent call 後の Git・worktree 制御だけを確認するとき
- 特定の agent call、policy、Structured Output schema の詳細が明らかな場合は、このディレクトリ全体ではなく対応する下位要素へ直接進む
- oracle file や realization file の正本仕様そのものを確認するときは、対応する oracle または realization の文書を直接読む

## hash
- f01721b3a18c608a1c4783e510cb10e81092eea2c99e5400c5cd5596ef756328
