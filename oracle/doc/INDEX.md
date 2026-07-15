# `app_spec`

## Summary
- cmoc のアプリケーション仕様断片をまとめたディレクトリ。CLI 補完、Codex 呼び出し、ログ、doctor 前処理、プロンプト、run isolation、session 状態、サブコマンドなどの仕様文書への入口となる。

## Read this when
- cmoc の個別機能やサブコマンドの正本仕様を確認・変更するとき。
- CLI 補完、Codex CLI 呼び出し、ログ、前処理、プロンプト生成、実行隔離、session 状態の仕様を調べるとき。
- 目的に応じて app_spec 内の具体的な仕様文書またはサブコマンド仕様を選ぶとき。

## Do not read this when
- INDEX.md の自動生成・更新規則だけを確認したいときは、インデクシング仕様を直接読む。
- リポジトリ全体の共通運用前提だけを確認したいときは、共通運用仕様を直接読む。
- 特定文書の本文や実装の詳細が既に明らかな単純な作業では、このディレクトリ全体を入口として読む必要はない。

## hash
- af159c9011f9397322018e7eda9b288875cd3133867bb38c2e52b4040d9186dd

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
- `cmoc` の設計で採用しなかった代替案と、その不採用理由を記録した設計判断メモ群。apply の orchestration、事後検査、permission profile 連携、AI-generated memory、作業計画レビューなどの背景を確認するための入口であり、現行仕様や実装そのものを扱う場所ではない。

## Read this when
- `cmoc apply` の不採用 orchestration 案や、所見調査・並列化・作業計画・状態管理を避けた理由を確認するとき。
- file access rule の事後検査案や `.gitignore` と permission profile の連携案の採否を調べるとき。
- AI-generated kaizen や継続的 memory の自動注入を採用しない設計意図を確認するとき。
- AI 作業計画を人間がレビューする workflow ではなく、人間が oracle を編集し AI が実装を追従させる方式を採用した背景を確認するとき。

## Do not read this when
- `cmoc apply` などの現行の実行手順、CLI 入出力、状態ファイル、テスト期待値を確認するとき。
- 現在の file access rule、差分検査、permission profile の仕様や実装を調べるとき。
- oracle file・realization file・INDEX.md の一般的な定義や記述規則を確認するとき。
- 採用済み workflow の操作方法や、個別機能の実装・テスト仕様を直接確認したいとき。

## hash
- 2eaef6ba625b805a5335e7f4ed166148fe03f84fac754f6e59a849b6ed892226

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
