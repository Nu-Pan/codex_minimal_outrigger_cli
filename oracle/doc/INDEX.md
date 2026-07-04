# `app_spec`

## Summary
- cmoc アプリケーション全体の正本仕様断片を集めた領域。CLI 自動補完、Codex CLI 呼び出し、ログ、共通前処理、エラー処理、索引生成、実行隔離、セッション状態、利用者ワークフロー、サブコマンド群など、複数機能にまたがる外部挙動と共通境界を確認する入口になる。
- 個別の実装構造ではなく、利用者に見えるコマンド挙動、状態・ログ・索引の扱い、agent call との接続、run や session のライフサイクルに関する仕様断片へ進むためのルーティング対象。

## Read this when
- cmoc の公開 CLI 挙動、サブコマンド、使用手順、セッションや apply の流れに関わる正本仕様を探すとき。
- Codex CLI 呼び出し、Structured Output、プロンプト受け渡し、動的 profile、quota・retry・resume、ファイルアクセス制限など agent call 周辺の仕様を確認したいとき。
- ログ、エラー処理、doctor preprocess、Ollama によるローカル SLM、インデクシング、run 隔離、セッション状態など、複数サブコマンドから参照される共通処理を実装・変更・テストするとき。
- 補完プローブ時の副作用抑制、通常実行前処理のタイミング、stdout/stderr へ出してよい内容など、CLI 起動経路の境界を判断するとき。
- path keyword 以外の横断的な前提、git 管理対象の扱い、作業用状態領域、タイムスタンプ、管理ブランチ上の変更範囲などを確認したいとき。

## Do not read this when
- oracle file、realization file、INDEX.md エントリー、品質基準など、リポジトリ全体の一般原則だけを確認したいとき。
- path keyword や root 種別そのものの定義だけを確認したいときは、パスモデルの正本へ直接進む。
- 実装ファイルやテストの具体的な関数、クラス、内部 helper、既存コード構造だけを調べたいとき。
- 特定サブコマンドや特定共通処理の読むべき仕様断片が既に分かっており、その詳細だけを確認したいとき。
- Codex CLI や Ollama など外部ツール自体の一般的な使い方だけを調べたいとき。

## hash
- 788112208220b6db2162c8c8366371f7c3ce529897f389b451fffe94163e8a62

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
- cmoc の開発時に参照する規則群をまとめた正本仕様断片への入口。Python コーディング規則、CLI 構成と共通処理の配置、開発環境、pytest を中心とした自動テスト規約を扱う。
- 機能ごとの外部仕様ではなく、realization code と realization test をどのように書き、どの環境・設計方針・テスト方針に従うかを判断するための開発ルールを束ねている。

## Read this when
- Python の実装またはテストを追加・修正する前に、型ヒント、import、docstring、コメント、ログ、命名、非公開識別子の共通規則を確認したいとき。
- CLI 引数解釈、エントリーポイント、サブコマンド本体、複数サブコマンドで使う共通処理の配置方針を判断したいとき。
- cmoc の開発環境、仮想環境、pip、依存追加、ファイルエンコード、ファイル名・ディレクトリ名の規則を確認したいとき。
- realization test を追加・修正する際に、pytest、tmp_path、テスト用リポジトリ、Codex CLI や LLM を伴うテストの扱いを確認したいとき。

## Do not read this when
- 個別サブコマンドの利用者向け仕様、出力 schema、保存状態、エラー条件など、具体的な機能仕様を確認したいとき。
- oracle file と realization file の関係、正本仕様断片の扱い、仕様と実装の関係、INDEX.md エントリー生成基準など、リポジトリ全体の仕様管理原則を確認したいとき。
- 対象コードの具体的な実装場所、既存関数のシグネチャ、内部ロジック、テスト期待値を調べたいとき。
- path キーワードの意味や実行時のパスモデルなど、開発規約ではなく基礎概念や個別実装の詳細を確認したいとき。

## hash
- d72ad5bf8c257deb9f3f86ae63c5917592a2bdf239f91616db6699cc13987078
