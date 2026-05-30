# `__init__.py`

## Summary

- `src/sub_commands/__init__.py` は `src.sub_commands` パッケージを宣言するだけの最小モジュールです。
- 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- `src.sub_commands` が Python パッケージとして宣言されていることを確認したいとき。
- `src/sub_commands` ディレクトリの入口として、最小限の役割だけを把握したいとき。
- パッケージとしての存在確認だけで足り、追加の公開 API や実行処理が不要なとき。

## Do not read this when

- `src.sub_commands` 配下の個別サブコマンド実装や実行フローを確認したいとき。
- `apply`、`session`、`init`、`eval_oracles` などの各モジュールの仕様を追いたいとき。
- `src.sub_commands` のパッケージ宣言ではなく、実際の業務ロジックや CLI 入口を見たいとき。

## hash

- ea4df02b820eba1ca77dfb1b2227c81dbff61cd7c4c2bf4d26d891369b57fa77

# `apply`

## Summary

- `src/sub_commands/apply` は `cmoc apply` 系サブコマンドの実装入口です。
- `__init__.py` はパッケージ宣言のみを担い、本体ロジックは `fork.py`、`join.py`、`abandon.py` に分かれています。
- この目次は、開始・統合・破棄のどの実装ファイルへ進むべきかを素早く振り分けるためのものです。

## Read this when

- `src/sub_commands/apply` の実装入口と各モジュールの担当範囲を確認したいとき。
- `cmoc apply fork`、`cmoc apply join`、`cmoc apply abandon` のどれを読めばよいか整理したいとき。
- 実装・修正・レビュー・テストを始める前に、関連ファイルの入口を把握したいとき。
- パッケージ宣言だけでなく、開始・統合・破棄の役割分担を俯瞰したいとき。

## Do not read this when

- 個別の `cmoc apply fork`、`cmoc apply join`、`cmoc apply abandon` の詳細仕様、状態遷移、例外条件を確認したいときは、それぞれのモジュールを直接読むべきです。
- `src/sub_commands/apply` のパッケージ宣言だけを確認したいときは、この目次ではなく `__init__.py` を直接読むべきです。
- 利用手順や仕様断片だけを確認したいときは、`oracles/app_specs/sub_commands/` 側の正本仕様を読むべきです。
- `branch_model`、`codex_call`、`indexing`、`error_handling` などの共通仕様だけを確認したいときは、別の入口文書を読むべきです。

## hash

- 0e95f4221090b4196421a7db9aa3fc4502cfff850e0661320277e889081ea30d
<!-- cmoc-index-kind: directory -->

# `eval_oracles.py`

## Summary

- `src/sub_commands/eval_oracles.py` は `cmoc review oracles` の本体実装です。
- oracles スナップショットの評価対象選定、部分/全体評価の分岐、並列評価、問題点リストの改善反復をまとめて扱います。
- 評価前の `INDEX.md` メンテナンス、Structured Output 検証、Codex CLI 用 prompt 構築、Markdown レポート生成と失敗時の報告処理も担います。

## Read this when

- `cmoc review oracles` の実行順、部分評価・全体評価の切り替え、評価対象の oracle ファイル選定を確認したいとき。
- 評価前の `INDEX.md` メンテナンス、開始時点の oracles tree の固定、参照可能ファイルの制約を実装・修正・レビューしたいとき。
- Structured Output の検証条件、問題点リストの改善反復、Codex CLI 向けの prompt 構築を確認したいとき。
- レポート保存、error report、stderr フォールバックまで含めて `cmoc review oracles` の挙動を把握したいとき。

## Do not read this when

- `cmoc review oracles` の CLI 引数や `main.py` への登録だけを確認したいとき。
- `cmoc apply`、`cmoc session`、`cmoc init` など、別サブコマンドの実装や仕様を追いたいとき。
- `oracles` 配下の個別仕様断片そのものを直接読みたいとき。

## hash

- 34c6e91d4fd996acd96b7440b5c556325973d9c961bb127bb6201f24864bedc8
<!-- cmoc-index-kind: file -->

# `init.py`

## Summary

- `cmoc init` の本体処理を実装している。
- 直接呼び出し時は共通 runner に委譲し、`.cmoc` の ignore 保証と初期化差分の commit を進める。

## Read this when

- `cmoc init` の実際の処理順や、`repo_root` 未指定時に共通 runner へ委譲する流れを確認したいとき。
- `.cmoc` を git 追跡対象外にする保証や、初期化時に発生した差分の commit 処理を実装・修正・レビューしたいとき。
- `src/sub_commands/init.py` の役割と、関連する共通処理の入口を把握したいとき。

## Do not read this when

- `cmoc init` 以外のサブコマンドの処理を見たいとき。
- `.cmoc` の git ignore 追加や tracked ファイル解除、初期化差分の commit が論点に含まれないとき。
- 初期化後の session/apply の運用仕様だけを確認したいとき。

## hash

- 766eb4ef5567a176766be2bb55dbc8f955c55af92c1ddc3f64043c1be4bda4ee

# `session`

## Summary

- `src/sub_commands/session` は `cmoc session` 系サブコマンドの実装入口です。
- `__init__.py` はパッケージ宣言のみで、実行ロジックは `fork.py`、`join.py`、`abandon.py` に分かれています。
- この目次は session の開始・統合・破棄のどの実装へ進むべきかを素早く振り分けるためのものです。

## Read this when

- `cmoc session` 系サブコマンドの入口と各モジュールの担当範囲を把握したいとき。
- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` のどれを読むべきか整理したいとき。
- `src/sub_commands/session` 配下の実装・修正・レビュー・テストを始める前に、関連ファイルの入口を整理したいとき。

## Do not read this when

- 個別の `cmoc session fork`、`cmoc session join`、`cmoc session abandon` の詳細仕様、状態遷移、例外条件だけを確認したいとき。
- `cmoc apply` 系の開始・統合・破棄の流れだけを確認したいとき。
- `src/sub_commands/session` のパッケージ宣言だけを確認したいときは、`__init__.py` を直接見れば足ります。

## hash

- c1b95ca54d632c67426b0117cbdb32b12c8861b7c6ef135d7fd4314f6ba1fd9f
<!-- cmoc-index-kind: directory -->
