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

- `src/sub_commands/apply` は `cmoc apply` 系サブコマンド実装の入口です。
- `__init__.py` はパッケージ宣言だけを担い、`abandon.py`、`fork.py`、`join.py` に本体ロジックが分かれています。
- この目次は、`cmoc apply` の開始・統合・破棄のどの実装モジュールへ進むべきかを素早く振り分けるためのものです。

## Read this when

- `cmoc apply` 系実装の入口をまとめて確認したいとき。
- `fork`、`join`、`abandon` のどの実装ファイルへ進むべきか整理したいとき。
- パッケージ入口と個別サブコマンド本体の対応関係を俯瞰したいとき。

## Do not read this when

- `cmoc apply fork` / `cmoc apply join` / `cmoc apply abandon` のうち 1 つだけの詳細仕様、状態遷移、例外条件を確認したいときは、各実装モジュールを直接読むべきです。
- `src/sub_commands/apply` のパッケージ宣言だけを確認したいときは、この目次ではなく `__init__.py` を直接読むべきです。
- `branch_model`、`codex_call`、`indexing`、`error_handling` などの共通仕様だけを確認したいときは、別の入口文書を読むべきです。

## hash

- 2fbe8bb64166350d4edd964e0d2071e81c24b938878c16a6f62c0b61353dce40
<!-- cmoc-index-kind: directory -->

# `eval_oracles.py`

## Summary

- `src/sub_commands/eval_oracles.py` は `cmoc review oracles` の本体実装です。
- 現在の oracles スナップショットの評価対象選定、部分/全体評価の分岐、並列評価、問題点リスト改善、Markdown レポート生成をまとめています。
- 評価前の `INDEX.md` メンテナンス、Structured Output 検証、Codex CLI 向けの prompt 構築とエラー時の報告処理も担います。

## Read this when

- `cmoc review oracles` の実行順、部分評価・全体評価の切り替え、評価対象ファイルの選定を確認したいとき。
- 評価前の `INDEX.md` メンテナンスや、評価対象の oracle スナップショットを固定する流れを追いたいとき。
- Structured Output の検証条件、問題点リストの改善反復、参照可能ファイルの制約を実装・修正・レビューしたいとき。
- レポート保存、error report、stderr フォールバックまで含めて `cmoc review oracles` の挙動を把握したいとき。

## Do not read this when

- `cmoc review oracles` の CLI 引数や `main.py` への登録だけを確認したいとき。
- `cmoc apply`、`cmoc session`、`cmoc init` など、別サブコマンドの実装や仕様を追いたいとき。
- `oracles` 配下の個別仕様断片そのものを読みたいときは、このファイルではなく `oracles/...` 側を直接読むべきです。

## hash

- 60ad6e60722435bd0a89328b07979425182f02d89b0731651b0b9da89cddb3ed
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

- src/sub_commands/session は `cmoc session` 系サブコマンドのパッケージ入口で、`__init__.py`、`fork.py`、`join.py`、`abandon.py` に各コマンド本体を持つディレクトリです。
- `fork.py` は session branch の作成と session state の記録を担当し、`join.py` は session branch の merge と conflict 解消、`abandon.py` は session branch の破棄を担当します。
- この配下は session の開始・統合・破棄を扱う実装の入口であり、個別の処理詳細は各モジュールへ分かれています。

## Read this when

- cmoc session 系サブコマンドの実装入口と、fork / join / abandon の配置を把握したいとき。
- session パッケージ全体の役割や、どのモジュールがどのコマンドを担当しているかを確認したいとき。
- src/sub_commands/session 配下の実装・修正・レビュー・テストを始める前に、関連ファイルの入口を整理したいとき。

## Do not read this when

- cmoc session fork、cmoc session join、cmoc session abandon のうち 1 つだけの詳細仕様、状態遷移、例外条件を確認したいとき。
- cmoc apply 系の開始・統合・破棄の流れだけを確認したいとき。
- src/sub_commands/session のパッケージ宣言だけを確認したいときは `__init__.py` を直接見れば足ります。

## hash

- 70e82e873e2b738c06c6f04f3ff8cc5914dfbbf60f8d27e5a899ca0ae5d1de11
