# `app_spec`

## Summary
- cmoc のアプリケーション仕様断片を集めた領域。CLI 補完、Codex CLI 呼び出し、ログ、doctor preprocess、indexing、run 隔離、session state、managed ollama、外部 provider、利用手順、サブコマンド仕様など、複数機能にまたがる正本仕様へ進む入口になる。
- 個別ファイルは、公開 CLI 挙動、共通前処理、状態・ログ・インデックス生成、agent call 境界、実行環境管理など、実装差を避けたい外部挙動や責務境界を扱う。

## Read this when
- cmoc の CLI 実行フロー、サブコマンド、共通前処理、ログ、状態管理、インデックス生成、run 隔離、Codex CLI 呼び出し、provider 連携に関する正本仕様断片を探すとき。
- 個別実装やテストを変更する前に、対象機能の oracle doc がこの領域にあるか確認したいとき。
- 利用者が呼び出すコマンドの順序、実行前後の状態遷移、作業ブランチや worktree、agent call との境界を確認したいとき。

## Do not read this when
- oracle file と realization file の一般的な役割分担、品質基準、INDEX.md エントリー作成規則だけを確認したいとき。
- パスキーワードやルート種別の定義そのものを確認したいときは、パスモデルを定義する仕様または実装を読む。
- アプリケーション仕様ではなく、具体的な realization code の関数構造、内部 helper、既存テストの詳細だけを調べたいとき。

## hash
- fd6e1255ffedb7e9af5ffc24f3c87ae84d02614b4da031a9ebfda3d2fcc96036

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
- cmoc の開発時に参照する共通ルール群への入口。Python コードの書き方、CLI 実装の配置方針、開発環境、pytest による自動テスト方針など、realization code を追加・修正する前提条件を扱う。
- 個別機能の外部仕様ではなく、実装・テスト・環境構築にまたがって守るべき作法や責務分離の基準を確認するためのまとまり。

## Read this when
- Python の実装またはテストを追加・変更し、型ヒント、import、コメント、docstring、ログ、非公開識別子、命名、ファイルエンコードなどの共通作法を確認したいとき。
- CLI 引数解釈、エントリーポイント、サブコマンド本体、複数サブコマンドで共有する処理の配置を判断したいとき。
- 開発環境の前提、仮想環境、pip、依存追加、ファイル名・ディレクトリ名の命名規則を確認したいとき。
- pytest による自動テスト、テスト用一時ツリー、Codex CLI 呼び出しを伴うテスト、Fake Codex CLI やローカル SLM の利用境界を判断したいとき。

## Do not read this when
- 個別サブコマンドの利用者向け仕様、出力 schema、保存状態、エラー条件などを確認したいとき。
- oracle file と realization file の関係、正本仕様断片の扱い、INDEX.md エントリー作成基準など、仕様管理全体の原則を確認したいとき。
- 既存実装の具体的な関数、内部ロジック、テスト期待値、実行時のパスモデルを探したいとき。
- 実装やテストの共通ルールではなく、特定機能の挙動や状態更新条件だけを調べたいとき。

## hash
- 98119ed53c527c12ce712650db116284bea148e8eb5500c9a1997af243b19804
