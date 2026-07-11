# `app_spec`

## Summary
- `cmoc` のアプリ仕様群をまとめる入口。サブコマンド、起動前処理、補完、ログ、状態、実行隔離、プロンプト、外部 provider 連携など、利用者向け挙動や実装境界を決めるときにここから必要な個別仕様へ進む。
- 個別機能の正本仕様断片を探すための案内であり、ここ自体は詳細仕様の代替ではない。対象の責務がどの文書に属するかを切り分けるために読む。

## Read this when
- `cmoc` の CLI 挙動、サブコマンド、実行フロー、ログ、状態管理、補完、インデクシング、外部 model 連携のどれを実装・修正・検証するか判断したいとき。
- 起動前の共通処理、エラー処理、run/session の隔離や状態更新、プロンプト受け渡しなど、複数機能にまたがる仕様の入口を探したいとき。
- どの個別仕様文書を読むべきか迷っていて、責務境界で候補を絞りたいとき。

## Do not read this when
- oracle file と realization file の一般的な役割分担や編集規則だけを確認したいとき。
- 個別仕様がすでに分かっていて、その文書本文だけで判断できるとき。
- cmoc 以外の一般的な CLI 設計や、ここに属さない別機能の仕様を探したいとき。

## hash
- 2f54c6008e5920a79e4b330d1f714d952705fca8b1212e6daa54ec2664f830cb

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
- Python 実装・テストを書くときの共通コーディング規則をまとめる入口。型ヒント、import、docstring、コメント、ログ、非公開識別子など、実装差を避けたい書き方の基準を確認する。
- CLI の構成や共通処理の配置ではなく、コード全体に共通する記法・記述方針を確認したいときに読む。

## Read this when
- Python の実装またはテストを追加・修正し、型ヒント、import、docstring、コメント、ログメッセージ、非公開識別子の書き方を確認したいとき。
- コードレビューや実装修正で、コメントの粒度、日本語コメントと英語ログの使い分け、NOTE を付けるべき補足の扱いを判断したいとき。
- 新しい関数・クラス・モジュールを作る前に、命名、責務、入出力を明確に保ち、過剰な実装を避けるための共通規則を確認したいとき。
- 相対 import、循環参照、TYPE_CHECKING の使い方など、モジュール間参照の書き方を判断したいとき。

## Do not read this when
- CLI の具体的なコマンド仕様、出力 schema、保存状態、エラー条件など、利用者に見える個別機能の正本仕様を確認したいとき。
- oracle file と realization file の役割、正本仕様断片の扱い、仕様と実装の関係など、リポジトリ全体の仕様管理原則を確認したいとき。
- ファイル分割、重複削減、依存追加、テスト肥大化抑制など、realization file の保守量や構成判断に関する一般原則を確認したいとき。
- 対象コードの具体的な実装場所や既存実装の現在の構造を探したいとき。

## hash
- bfbb73fd94dd2b748b8d08b8cd6c2d64351a217ea93d72282d9411013623a388
