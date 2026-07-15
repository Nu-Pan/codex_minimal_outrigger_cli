# `app_spec`

## Summary
- cmoc のアプリケーション仕様断片を集約するディレクトリ。CLI の補完、Codex 実行、ログ、前処理、モデルプロバイダー、プロンプト、run 隔離、session 状態、サブコマンド仕様などへの入口を提供する。各機能の詳細確認では、該当する個別文書または `sub_command` 配下へ進む。

## Read this when
- cmoc のアプリケーション仕様から、読むべき機能別文書やサブコマンド仕様を選びたいとき。
- CLI 共通基盤、実行環境、ログ、状態管理、プロンプト、run 隔離など複数領域にまたがる仕様の入口を確認したいとき。
- 補完、Codex 実行、doctor 前処理、managed Ollama、session、interruption などの個別仕様文書を探すとき。

## Do not read this when
- 実装コードやテストコードの具体的な挙動を直接確認したいときは、対応する `src` または `test` 配下を読む。
- 特定機能の仕様が明確なときは、このディレクトリ全体ではなく該当する個別文書へ直接進む。
- INDEX.md の生成・更新規則だけを確認したいときは、インデクシング仕様を直接読む。

## hash
- 9dbb26a0e3e115f4556fac1af2de99ab354698f1a57f00a48a430d3ceb851c1b

# `branch_model.md`

## Summary
- cmoc が session と run の境界をどう切るかを定める。どの branch や worktree が誰の作業領域か、session fork/join と各サブコマンドの run fork/join を扱う文脈で読む。

## Read this when
- session の開始・終了で branch の生成や merge の扱いを決めたいとき
- apply や review などの run がどの branch と worktree を使うか確認したいとき
- cmoc 管理対象の branch 名や commit 名の責務境界を確認したいとき

## Do not read this when
- 個別サブコマンドの入出力や実行手順だけを知りたいとき
- branch 名や worktree 名の具体的な生成規則ではなく、内部実装の詳細を詰めたいとき
- cmoc 以外の通常の git 運用やリポジトリ本流の方針だけを確認したいとき

## hash
- e48fc3d9371ee9b4c447d06cdcb12a96f006afa581263ea87bd285118a7a60ed

# `considered_alternative`

## Summary
- `cmoc` の採用しなかった設計案と、その不採用理由を集めた文書群への入口。`apply` 系の進め方、事後検査の位置づけ、権限例外の扱い、永続記憶の可否、作業計画レビューの責務分担など、実装方針の分岐点を確認するときに読む。

## Read this when
- `cmoc` の実行フローや状態管理で、採用案ではなく却下案の背景を確認したいとき。
- `apply` の段取り、調査の並べ方、復旧方針、計画レビュー、記憶の引き継ぎ方など、設計判断の根拠を比較したいとき。
- 権限プロファイルや事後検査の扱いについて、なぜ別案を採らなかったかを確認したいとき。

## Do not read this when
- 現在採用している `cmoc` の具体的な CLI 手順、出力形式、保存先、テスト期待値だけを確認したいとき。
- 個別機能の実装手順や現行仕様そのものを探していて、不採用案の背景は不要なとき。
- `oracle` と `realization` の一般定義や記述標準だけを確認したいとき。

## hash
- cad9fc4f61a6f59d4a593a1ed5039859c760c986de217d8b353dbe12520073a0

# `dev_rule`

## Summary
- Python の実装規則・CLI 構成方針・テスト規約をまとめる入口。型や import などの書き方、サブコマンドや共有処理の配置、pytest を使った検証方針を確認したいときにここから下位文書へ進む。
- 個別機能の挙動仕様や実装詳細ではなく、開発時の共通ルールを確認するための案内である。

## Read this when
- Python 実装の書き方やレビュー基準を揃えたいとき。
- CLI の責務分担や共通処理の置き場所を決めたいとき。
- テストの作り方や検証対象の境界を確認したいとき。

## Do not read this when
- 機能の正本仕様を知りたいときは、対象機能の oracle doc を直接読む。
- 個別モジュールの実装内容を知りたいときは、そのモジュール本文を読む。
- 開発ルーティングそのものを確認したいときは、別の routing 文書を読む。

## hash
- 8d16bc2046ed83543190cd8757ee292c53d8890d3f778dc679543a747d3fb6a5
