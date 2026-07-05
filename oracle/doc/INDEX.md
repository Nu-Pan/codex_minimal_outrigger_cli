# `app_spec`

## Summary
- cmoc のアプリケーション仕様断片を集めた領域。CLI 補完、Codex CLI 呼び出し、ログ、doctor preprocess、managed ollama、run 隔離、session 状態、サブコマンド、インデクシング、利用手順など、実装差を避けたい外部挙動や共通境界の正本仕様へ進む入口になる。
- 個別ファイルは、共通処理、永続状態、外部 provider 境界、サブコマンド仕様、利用者向けワークフローなどの責務ごとに分かれており、対象機能の仕様断片を選ぶための上位ルーティング情報として使う。

## Read this when
- cmoc の CLI 挙動、共通前処理、ログ、状態管理、Codex CLI 呼び出し、run 隔離、インデクシング、managed ollama、サブコマンド仕様のどの正本仕様断片を読むべきか判断したいとき。
- 新しい実装やテストの前に、対象機能が共通仕様、個別サブコマンド仕様、外部 provider 境界、利用手順のどこで定義されているかを探すとき。
- 複数の仕様領域にまたがる変更で、通常実行前処理、補完時の例外、ログ出力、状態更新、agent call、git worktree 隔離などの入口を切り分けたいとき。

## Do not read this when
- oracle file と realization file の一般的な定義、編集責務、品質基準、INDEX.md エントリー生成規則だけを確認したいとき。
- <cmoc-root>、<repo-root>、<work-root>、<run-root> などのパス語彙そのものの定義だけを確認したいとき。
- 実装ファイルの内部 helper、モジュール分割、具体的なコード構造だけを調べたいとき。
- 対象のサブコマンドや共通処理が既に特定できており、その個別仕様ファイルを直接読めば足りるとき。

## hash
- ca0cdc761c4c072cf5075fcd206a603de54cc28e18bcb1764369b6d838b88ce1

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
- cmoc の開発作業全体に適用する正本仕様断片群への入口。Python コーディング規則、CLI 実装の責務分離と共通処理配置、開発環境、テスト作成方針を扱う。
- 個別機能の仕様ではなく、realization code と realization test をどの作法・設計・環境・検証方針で作るかを判断するための基準をまとめる。

## Read this when
- Python の実装またはテストを追加・修正する前に、型ヒント、import、docstring、コメント、ログ、命名、非公開識別子の共通作法を確認したいとき。
- CLI 引数解釈、エントリーポイント、サブコマンド本体、複数サブコマンドで使う共通処理の配置方針を判断したいとき。
- cmoc の開発環境、Python 仮想環境、pip、依存追加、ファイルエンコード、ファイル名・ディレクトリ名の規則を確認したいとき。
- realization test を追加・変更し、pytest、テスト用リポジトリ環境、Real Codex CLI と Fake Codex CLI の使い分け、検証対象の境界を確認したいとき。

## Do not read this when
- 個別サブコマンドの外部仕様、出力 schema、状態更新条件、エラー条件など、利用者に見える機能仕様を確認したいとき。
- oracle file と realization file の役割、正本仕様断片の扱い、INDEX.md エントリー生成基準など、リポジトリ全体の仕様管理原則を確認したいとき。
- 既存実装の具体的な関数シグネチャ、内部ロジック、テスト期待値、実装場所を直接調べたいとき。
- 実行時の path キーワードやパスモデルの詳細を確認したいとき。

## hash
- e78945d712f4434505b2dce59f66f1a76c04fc9880c1d374320e3d043e894067
