# `app_spec`

## Summary
- cmoc の実行仕様をまとめる oracle/doc 配下の入口。CLI の起動前後の共通規則、出力・ログ・エラー処理、run 隔離、状態管理、外部 model provider 境界、補完、利用手順を横断して確認したいときに読む。
- 個別サブコマンド仕様へ進む前の上位ルーティングとして使い、必要に応じて sub_command 配下の各仕様へ分岐する。

## Read this when
- cmoc 全体の実行仕様を横断して把握したいとき。
- CLI 補完、ログ、エラー処理、run 隔離、状態管理、prompt、外部 model provider との責務分担をまたいで確認したいとき。
- どの個別サブコマンド仕様へ進むべきか判断したいときの入口として使うとき。

## Do not read this when
- 個別サブコマンドの挙動だけを確認したいときは、対応する sub_command 側を直接読む。
- oracle file と realization file の一般的な役割分担や編集規則だけを確認したいとき。
- この配下にない別領域の仕様や実装を調べたいとき。

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
- cmoc の開発・実装・テストで参照する共通ルール群をまとめた入口。Python の書き方、CLI 設計、開発環境、テスト方針という異なる観点を分けて案内し、必要な規則だけに進めるための上位ルーティングに使う。
- ここは個別機能の仕様ではなく、realization code と realization test をどう書くか、どの環境前提で作業するかを決めるための規則集である。

## Read this when
- Python 実装やテストの書き方を確認したいときは `coding_rule.md` へ進む。
- CLI の構成、エントリーポイントとサブコマンドの責務分離、共通処理の置き場所を判断したいときは `design_rule.md` へ進む。
- 開発環境の前提、Python や pip の使い方、ファイルやディレクトリの命名・エンコード方針を確認したいときは `development_environment.md` へ進む。
- 決定論的な制御ロジックのテスト方針や、Real Codex CLI 経路で cmoc managed ollama を使うべき条件を確認したいときは `test_rule.md` へ進む。

## Do not read this when
- CLI の個別コマンド仕様、出力形式、状態更新条件などの正本仕様を確認したいときは、機能別の仕様断片を読むべきで、この案内は不要である。
- oracle file と realization file の役割や、仕様と実装の関係そのものを確認したいときは、この配下ではなくリポジトリ全体の仕様管理原則を読むべきである。
- 特定の実装ファイルやテストファイルの現在の中身を探したいときは、このルーティング文書ではなく対象本文を直接読むべきである。

## hash
- bfbb73fd94dd2b748b8d08b8cd6c2d64351a217ea93d72282d9411013623a388
