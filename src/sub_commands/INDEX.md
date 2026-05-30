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

- `src/sub_commands/apply` は `cmoc apply` 系サブコマンドの実装パッケージで、`__init__.py`、`abandon.py`、`fork.py`、`join.py` をまとめています。
- apply の開始、調査・修正ループ、成果物の取り込み、破棄に関する処理へ進むための入口です。
- apply branch、worktree、state file をどう扱うかを、実装ファイル単位でたどるための目次です。

## Read this when

- `src/sub_commands/apply` 配下にどの実装ファイルやパッケージがあるかを整理したいとき。
- `cmoc apply` 系の開始、調査・修正、マージ、破棄の流れを実装・修正・レビューしたいとき。
- apply branch、apply worktree、session state file の役割分担を実装側から確認したいとき。

## Do not read this when

- `cmoc apply` の利用手順や引数の意味だけを確認したいときは、`oracles/app_specs/sub_commands/` 側の仕様を読むべきです。
- `cmoc session` 系サブコマンドや `review oracles` など、別機能の実装を探しているときは対象外です。
- 個別の `fork.py`、`join.py`、`abandon.py` の実装内容が既に分かっていて、そのファイルを直接読みたいときは、この目次を経由する必要はありません。

## hash

- e3c5b18f31260c26afec51183a7fbf3afc3ffdb4cbc80500f150e907b50030d3
<!-- cmoc-index-kind: directory -->

# `eval_oracles.py`

## Summary

- `src/sub_commands/eval_oracles.py` は `cmoc review oracles` の本体実装です。
- oracles ファイルの列挙、部分評価/全体評価の分岐、並列評価、問題点リスト改善、Markdown レポート保存をまとめています。
- 評価前の `INDEX.md` 事前メンテナンス、Structured Output の検証、error report と stderr フォールバックも担っています。

## Read this when

- `cmoc review oracles` の実行順、部分評価/全体評価の切り替え、評価対象ファイルの選定を確認したいとき。
- `referenced_paths` や `specification_only_basis` を含む Structured Output の検証条件、問題点リストの改善ロジックを追いたいとき。
- レポート生成先、error report の出力、stderr フォールバックまで含めて実装・修正・レビューしたいとき。

## Do not read this when

- `cmoc review oracles` の CLI 引数やサブコマンド登録だけを確認したいとき。
- `cmoc` の他サブコマンドや共通処理だけを確認したいとき。
- `oracles` 配下の個別仕様断片そのものを読みたいとき。

## hash

- a4b4cedd92e397a119d16e0e938acce3a3c1e85a2d1379d7e85aa24105973cdb

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

- `src/sub_commands/session` は `cmoc session` 系サブコマンドのパッケージ入口で、`__init__.py`、`fork.py`、`join.py`、`abandon.py` に各コマンド本体を持つディレクトリです。
- `fork.py` は session branch の作成と session state の記録を担当し、`join.py` は session branch の merge と conflict 解消、`abandon.py` は session branch の破棄を担当します。
- この配下は session の開始・統合・破棄を扱う実装の入口であり、個別の処理詳細は各モジュールへ分かれています。

## Read this when

- `cmoc session` 系サブコマンドの実装入口と、`fork` / `join` / `abandon` の配置を把握したいとき。
- session パッケージ全体の役割や、どのモジュールがどのコマンドを担当しているかを確認したいとき。
- `src/sub_commands/session` 配下の実装・修正・レビュー・テストを始める前に、関連ファイルの入口を整理したいとき。

## Do not read this when

- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` のうち 1 つだけの詳細仕様、状態遷移、例外条件を確認したいとき。
- `cmoc apply` 系の開始・統合・破棄の流れだけを確認したいとき。
- `src/sub_commands/session` のパッケージ宣言だけを確認したいときは `__init__.py` を直接見れば足ります。

## hash

- 46d18610eaf7078ce833fde501e8f6a852139ac98e1c549e8a3cdfff815e38c1
