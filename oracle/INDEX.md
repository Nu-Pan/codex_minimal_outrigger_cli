# `doc`

## Summary
- cmoc の正本ドキュメント群への入口。アプリケーション仕様、サブコマンド仕様、開発規則、ブランチモデル、採用しなかった設計案を分類して収録する。
- app_spec は cmoc の利用者向け挙動、状態管理、ファイル分類、Codex 呼び出し、ログ、feedback、各サブコマンドの正本仕様を扱う。
- app_spec/sub_command は個別サブコマンドの引数、前提条件、実行手順、結果報告、終了処理を扱うため、特定コマンドの仕様確認時の直接の入口となる。
- dev_rule は cmoc 自体の開発環境、設計、コーディング、テスト実装、テスト実行に関する開発者向け規則を扱う。
- branch_model は session、run、worktree とそれらに対応する branch・commit の概念と関係を定義する。
- considered_alternative は採用しなかった設計や運用案と、その判断理由を記録する。現行仕様の確認ではなく、設計判断の背景を調べるための資料である。

## Read this when
- cmoc の正本仕様を横断的に探す必要があるとき。
- 利用方法、状態遷移、ファイル分類、Codex agent call、feedback、ログ、編集 run などのアプリケーション挙動を確認するときは app_spec 以下を読む。
- 特定の cmoc サブコマンドの契約や処理手順を確認するときは app_spec/sub_command 以下から該当仕様を読む。
- cmoc の実装・テスト・開発環境に関する規則を確認するときは dev_rule 以下を読む。
- session/run の Git branch、commit、worktree の関係を確認するときは branch_model.md を読む。
- 過去に不採用となった設計案の理由や代替方針を確認するときは considered_alternative 以下を読む。

## Do not read this when
- 対象が実装コードやテストコードに限定され、正本仕様を確認する必要がないとき。
- 特定の仕様ファイルが既に判明しており、その本文を直接読めば目的を満たせるとき。
- 現行仕様ではなく、過去の不採用案だけを調査する場合は app_spec や dev_rule 全体へ進まず considered_alternative 以下を直接読む。
- 個別サブコマンドの仕様だけが必要な場合は、このディレクトリ全体を読み込まず app_spec/sub_command 以下の該当ファイルへ直接進む。

## hash
- 16dbe6a4768bfcc2387263bec48817d3eaab402c9ad894cd25c64b18766de0a0

# `src`

## Summary
- cmoc の正本ソースコードを集約するルート。設定・パス解決・文書参照・構造化文書レンダリングなどの共通モデル、agent 呼び出し用パラメータ生成、プロンプトと各種ポリシーの組み立てを含む。
- `oracle/prompt_builder` は基本プロンプト、完全なプロンプト、エディタ入力、oracle／realization／ファイルアクセス／ルーティング等のポリシーを組み立てる入口。プロンプト内容や指示文の構成を確認するときに進む。
- `oracle/acp_builder` は session join、oracle 編集・調査、realization 適用・リファクタリング、feedback、TUI、indexing、quota probe など、個別の agent 呼び出しパラメータを生成する入口。特定の処理フローの agent 呼び出し条件を確認するときに進む。
- `oracle/editor_input_handoff` はエディタ入力の引き継ぎ本文・ガイドを生成する。エディタとの入力受け渡しや、その案内文を確認するときに進む。
- `oracle/other` は設定値、パスモデル、文書参照、構造化文書の共通データ構造とレンダリングを担う。複数の処理領域にまたがる値の表現・パス解決・Markdown 生成を確認するときに進む。
- `oracle/feedback` は feedback 報告に渡す入力データを保持する補助領域で、feedback の agent 処理そのものは `oracle/acp_builder/feedback` から確認する。

## Read this when
- cmoc の正本実装全体の構成や、どのサブシステムが対象の責務を担うかを確認したいとき
- プロンプト生成、agent 呼び出しパラメータ生成、共通モデルのいずれかを変更・調査するとき
- 特定の agent 呼び出し処理へ進む前に、その処理を含む上位カテゴリを判断したいとき

## Do not read this when
- 正本仕様の意味や利用者向け要件だけを確認したいときは `oracle/doc` を直接読む
- 実装に対応する正本テストだけを確認したいときは `oracle/test` を直接読む
- 対象が明確に `prompt_builder`、`acp_builder`、`editor_input_handoff`、または `other` の下位要素に限定されているときは、このルート全体ではなく該当サブディレクトリへ直接進む

## hash
- 64377c1b873afe3e8e349087943c8c341a276bde8c9cf39bd66727a60f998996
