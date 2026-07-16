# `app_spec`

## Summary
- cmoc のアプリケーション仕様断片をまとめたディレクトリ。CLI の補完、通常実行、サブコマンド、ログ、エラー処理、セッション状態、run 隔離、Codex CLI 呼び出し、managed ollama などの個別仕様への入口となる。

## Read this when
- cmoc の利用者向け挙動、CLI 実行条件、状態遷移、ログ・エラー処理、agent call、managed ollama の仕様を確認するとき。
- 複数のアプリケーション仕様候補から、対象機能に対応する正本仕様断片を選ぶとき。

## Do not read this when
- INDEX.md の自動生成・更新規則だけを確認したいときは、インデクシング仕様を直接読む。
- Python 実行環境、設計ルール、テスト手順など開発規則だけを確認したいときは、対応する dev_rule 文書を読む。
- 個別仕様が明らかで、対象ファイルへの直接アクセスで足りるとき。

## hash
- 21655a2e18d73bf1f641e5310508385c004428c4ee1b2c11b1e787dafe618806

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
- cmoc の開発規則に関する正本ドキュメント群。Python コーディング、CLI の設計・配置、開発環境、realization test の方針を確認するための入口。

## Read this when
- Python 実装の書き方や命名・型ヒント・import 方針を確認するとき。
- CLI のエントリーポイント、サブコマンド、共有処理の配置を判断するとき。
- Python/venv、依存関係、ファイル命名など開発環境の運用を確認するとき。
- pytest、Real Codex CLI 結合、テスト環境隔離、検証範囲など realization test の方針を確認するとき。

## Do not read this when
- 個別機能やコマンドの挙動仕様を確認したいときは、対象機能の oracle doc を直接読む。
- 個別モジュールの実装詳細を確認したいときは、その実装本文を読む。
- INDEX.md の読み方やルーティング方針を確認したいときは、専用の routing 文書を読む。

## hash
- 2eadee0de716c3689527ae67aef5aeae48aedf5689c90b9bc197be8d5fa9cc60
