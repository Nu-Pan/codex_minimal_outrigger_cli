# `doc`

## Summary
- cmoc の利用者向け挙動と主要な共通契約を定義する正本仕様群。自動補完、Codex 実行、ログ、doctor 前処理、feedback、prompt、run/session lifecycle、サブコマンド、通知などの個別仕様へ進むための入口。

## Read this when
- cmoc の CLI、workflow、agent call、feedback、ログ、通知など、利用者向け挙動や複数機能にまたがる正本仕様を確認するとき
- 個別仕様が未特定で、サブコマンド、session/run、prompt、feedback、Codex 呼び出し、実行前処理を横断して調べるとき
- 個別機能の実装・変更・レビューに先立ち、対応する仕様書の責務境界と参照先を把握するとき

## Do not read this when
- 対象となる個別仕様書が既に特定でき、その本文だけで確認できるとき
- realization implementation や realization test の具体的な実装・テスト手順だけを調べるとき
- INDEX.md の生成処理、開発環境、テスト実行手順など、専用の仕様・手順が直接の入口となるとき

## hash
- b8eaea2d519ab512af88b4f825c150318e8390f363bec1cc840e0273158ddd4e

# `src`

## Summary
- oracle 側の agent call 構築と prompt 構築を担う実装群への入口。論理的な agent call パラメータ、モデル・推論・ファイルアクセス設定、quota probe、indexing 用呼び出し定義を扱う。prompt の組み立て、共通 Standard、ファイルアクセス規則、routing 規則、Structured Markdown、パスモデル、feedback reporter 入力契約も含む。用途別の agent call を調べる場合は acp_builder、完全 prompt や instruction の合成を調べる場合は prompt_builder、共通設定・パス・Standard・文書レンダリングを調べる場合は other、feedback 入力契約を調べる場合は feedback へ進む。

## Read this when
- cmoc の oracle 側で agent call の論理パラメータ、モデルクラス、Reasoning effort、ファイルアクセスモード、cwd、Structured Output schema の設定を調査・変更するとき。
- agent call の用途別 builder、indexing、quota availability probe、oracle・realization 間の呼び出し構築経路を調査するとき。
- 完全 prompt の構成、placeholder の統合、共通 Standard の選択・合成、file access rule、routing rule、feedback reporting の注入を調査・変更するとき。
- Structured Markdown の構造化・レンダリング、agent call のパスコンテキスト、cmoc 設定、feedback reporter の入力スキーマを調査するとき。

## Do not read this when
- CLI の実行処理、realization implementation、realization test、個別 oracle file の正本仕様を直接確認したいとき。
- agent call 構築、prompt 構築、oracle 共通モデル、構造化文書、feedback 入力契約と無関係な永続化処理や実行時制御だけを調査するとき。
- 既存の INDEX.md によるルーティング情報だけを確認したいとき。

## hash
- cc3b335ec2283bf9773a7d833bdca34a2b7b8e556b6c0c9efaf4dbeb4a72ca10
