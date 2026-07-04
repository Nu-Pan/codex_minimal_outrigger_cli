# `app_spec`

## Summary
- cmoc の横断仕様とサブコマンド仕様へ進むための oracle doc 群。Codex CLI 呼び出し、補完、ログ、事前検証、エラー処理、INDEX 生成、実行隔離、セッション状態、Ollama/SLM、利用手順など、複数の実装領域から参照される正本仕様断片を扱う。
- 利用者向け CLI 挙動、agent call 境界、永続状態、ログ、作業隔離、インデクシングなどについて、実装差を避けたい外部挙動や共通前提を確認する入口となる。

## Read this when
- cmoc の CLI 起動経路、サブコマンド、共通前処理、ログ、エラー処理、状態管理、作業隔離、インデクシング、Codex CLI 呼び出しのいずれかに関わる実装・テスト・設計判断を始めるとき。
- 補完プローブ、doctor preprocess、Ollama/SLM、Structured Output、quota/retry/resume、セッションや apply の状態遷移、利用者の標準ワークフローなど、複数機能にまたがる正本仕様断片を探すとき。
- 個別サブコマンドの詳細仕様へ進む前に、対象コマンドや関連する共通処理の読む先を絞りたいとき。

## Do not read this when
- oracle file と realization file の一般的な役割分担、編集責任、品質基準、INDEX.md エントリー作成規則だけを確認したいとき。
- パスキーワードやルート種別の定義だけを確認したいときは、パスモデルを扱う正本仕様へ直接進む。
- 実装ファイルの関数構造、内部 helper、既存テスト、具体的なコード上の挙動だけを調べたいときは、対象の realization code または realization test を読む。
- Codex CLI や外部ツールそのものの一般的な利用方法だけを調べたいとき。

## hash
- 56625cdd5e46022c2972df2a33b30ce9661980b8ef22769fb146d2635f09575e

# `branch_model.md`

## Summary
- cmoc が通常の local branch から session branch を作り、run ごとに subcommand-specific な managed branch と linked worktree へ作業を隔離する branch/worktree モデルを定義する。
- repository default branch、local branch、remote-tracking branch、cmoc-managed branch、session/run 系 branch、fork/join commit、run worktree の意味と命名規則を扱う。

## Read this when
- cmoc の session fork/join や apply/review などの run が、どの git branch・commit・worktree を作成または利用するかを確認したいとき。
- `<cmoc-session-branch>`、`<cmoc-session-home-branch>`、`<cmoc-run-branch>`、`<cmoc-run-worktree>` などの用語の意味や命名規則を確認したいとき。
- repository default branch を特別扱いするか、session の home branch をどの時点の branch とみなすかを判断したいとき。

## Do not read this when
- oracle file と realization file の責務境界、編集権限、追跡対象判定などを確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` のパス概念そのものを確認したいとき。
- git branch/worktree ではなく、oracle 文書構成、INDEX.md エントリー規則、または realization code の品質基準を確認したいとき。

## hash
- 4c44301943a5bf0f9213b6720b0852c2f85bd0b69b2967ab72baf1cda109e4b9

# `considered_alternative`

## Summary
- cmoc で採用しなかった設計案と、その不採用理由を集めた設計判断メモ群。apply orchestration、file access rule 違反の事後検査、gitignore と permission profile の変換、AI-generated memory/kaizen の自動注入、AI 作業計画の人間レビュー方式について、再検討時の入口になる。
- 採用済み仕様そのものではなく、過去に検討して退けた案の背景、避けるべき理由、設計判断の境界を確認するための領域。

## Read this when
- cmoc の現行設計に対して、過去に不採用となった代替案を再検討しているとき。
- cmoc apply の作業計画立案、所見リストアップ、並列 agent call、所見単位修正、調査対象管理方式を変更する根拠を探しているとき。
- file access rule 違反を agent call 後の差分検査や別 agent call による回復で扱う案を検討しているとき。
- git 追跡対象外ファイルを読み書き規則や permission profile の例外として扱う案、または .gitignore を permission profile へ変換する案を検討しているとき。
- AI-generated kaizen、memory、振り返り結果、改善案、継続的指示を後続の Codex CLI 実行へ自動注入する状態管理を検討しているとき。
- AI に作業計画を書かせて人間がレビューする workflow と、oracle を人間が編集し AI が実装可能性を評価する方式を比較したいとき。

## Do not read this when
- 採用済みの詳細仕様、CLI 入出力、状態ファイル仕様、テスト期待値、実装経路を確認したいとき。
- oracle file と realization file の一般的な定義、責務境界、記述標準、INDEX.md エントリー生成規則を確認したいとき。
- Codex CLI 本体の memory 機能、git ignore の一般仕様、permission profile の現在の実装方法など、外部または現行採用仕様の詳細を調べたいとき。
- 不採用案の背景ではなく、個別コマンドの操作方法、現在の workflow の具体的挙動、または実装・テスト対象を探しているとき。

## hash
- 7767be4a4c27a93b3358c7b521d7f73444e4557bc421c8899dca1dcddd2e6e29

# `dev_rule`

## Summary
- cmoc の開発時に適用する共通ルールを集めた正本仕様断片群。Python コーディング規則、CLI 実装の責務配置、開発環境、realization test の方針を確認する入口になる。
- 個別機能の外部仕様ではなく、実装・テスト・環境構築・共通設計を進める際に守るべき横断的な作法と判断基準を扱う。

## Read this when
- Python の実装やテストを追加・修正する前に、型ヒント、import、docstring、コメント、ログ、命名、テスト配置、検証対象の共通基準を確認したいとき。
- CLI のエントリーポイント、サブコマンド本体、複数サブコマンドで使う共通機能の配置を判断したいとき。
- 開発環境の準備、Python 仮想環境、pip、依存追加、ファイルエンコード、ファイル名・ディレクトリ名の規則を確認したいとき。
- Codex CLI を伴うテストで、課金回避、ローカル実行、Fake Codex CLI の使い分けを判断したいとき。

## Do not read this when
- CLI の個別コマンド仕様、利用者向けの入出力形式、状態更新条件、エラー条件などを確認したいとき。
- oracle file と realization file の役割、正本仕様断片の扱い、仕様管理原則、INDEX.md エントリー生成基準を確認したいとき。
- path キーワードや実行時パスモデルの詳細を調べたいとき。
- 既存実装の具体的な関数シグネチャ、内部ロジック、テスト期待値、対象コードの現在の配置を探したいとき。

## hash
- 0759d8cb5ffd743c0bf74b515c9ebc687ba96beec80fdce5d7458a2ac0aae77c
