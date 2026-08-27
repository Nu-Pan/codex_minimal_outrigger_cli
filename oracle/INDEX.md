# `doc`

## Summary
- cmoc の正本ドキュメント群を集約するディレクトリ。アプリケーション仕様、session/run の branch model、採用しなかった代替案、開発規則を扱い、実装・変更・調査の開始時に該当する下位文書へ進むための入口となる。
- app_spec は CLI・agent call・lifecycle・feedback・ログ・通知などのアプリケーション挙動仕様、branch_model.md は session/run の git 隔離モデル、considered_alternative は不採用案の背景、dev_rule は実装・環境・テスト・品質検査の開発規則を案内する。

## Read this when
- cmoc の正本仕様、git による session/run 隔離モデル、不採用となった設計案、または開発規則の入口を確認するとき
- アプリケーション挙動、branch・worktree、実装配置、開発環境、テスト要件、品質検査に関する作業へ着手するとき
- 下位の個別仕様書や開発規則へ進む前に、対象文書の責務と参照境界を確認するとき

## Do not read this when
- 単一の仕様書や開発規則だけで確認事項が完結し、ディレクトリ全体の案内が不要なとき
- 具体的な CLI 契約、個別機能の詳細挙動、実装コード、テスト、schema、prompt builder など、下位対象を直接読むべきとき
- 採用済み仕様の操作方法や現在の実行結果だけを確認する場合で、検討資料群を読む必要がないとき

## hash
- 8432d98a6e0f1820a1f31c6139f95bff617371671424dd7c3840c84ef71d264e

# `src`

## Summary
- cmoc の agent call 構築と prompt 生成を担う Python ソースおよび Structured Output schema の領域です。
- 共通データモデルは `oracle/acp_builder`、prompt の組み立てと policy は `oracle/prompt_builder`、パス・構造化文書・設定などの共通処理は `oracle/other` から確認できます。
- feedback、indexing、oracle、realization、session、tui、quota probe など、各機能の agent call 定義と出力契約への入口を提供します。

## Read this when
- agent call のモデル、推論強度、ファイルアクセスモード、cwd、prompt、Structured Output schema、indexing preflight の構築定義を調査・変更するとき
- 特定機能の agent call が使用する prompt、起動パラメータ、または Structured Output 契約を確認するとき
- agent call 共通のデータモデル、パス解決、構造化文書レンダリング、prompt policy、placeholder の連携を確認するとき
- feedback、indexing、oracle、realization、session join、tui、quota probe の実装上の呼び出し定義へ進む必要があるとき

## Do not read this when
- Codex CLI の実際の実行処理、agent call の実行結果、またはバックエンドモデル名への変換規則を確認したいとき
- agent call が参照する oracle file、realization file、feedback state、既存の INDEX.md の本文を確認したいとき
- cmoc の意味仕様や開発規定そのものを確認したいときは、対応する `oracle/doc` 配下を直接読む方が適切なとき
- 実行時の CLI サブコマンド処理や realization 側の実装・テストを直接確認すれば足りるとき

## hash
- d44dd41f4575d50f27295a5c90ffa2324c4e220f1061e79339a99cf370ede101
