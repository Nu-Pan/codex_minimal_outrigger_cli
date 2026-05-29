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
- 配下には `__init__.py`、`fork.py`、`join.py`、`abandon.py` があり、各処理が役割ごとに分かれています。
- `fork.py` は調査・修正ループ、`join.py` は merge、`abandon.py` は破棄と cleanup を担当します。

## Read this when

- `cmoc apply` 系サブコマンドの実装・修正・レビュー・テストを始めるときに、配下の役割分担を把握したい場合に読む。
- apply branch や worktree の生成、merge、破棄の役割分担を整理して、どのモジュールへ進むべきか確認したいときに読む。
- この配下の各モジュールへの参照先を確認して、必要な実装へ素早く移動したいときに読む。

## Do not read this when

- `cmoc apply fork`、`cmoc apply join`、`cmoc apply abandon` のうち 1 つだけの詳細仕様を確認したいときは、この目次ではなく該当モジュールを直接読むべきです。
- `cmoc apply` ではなく `cmoc session` 側の開始・統合・破棄仕様を確認したいときは、このディレクトリを読む必要はありません。
- このディレクトリではなく、`__init__.py` だけでパッケージ宣言を確認すれば足りるときは、ここを読む必要はありません。

## hash

- cba266b9f501269aed36dc737b3c3f8f0d94e8bef3beb58afd10123198188287

# `eval_oracles.py`

## Summary

- `src/sub_commands/eval_oracles.py` は `cmoc review oracles` の本体実装です。
- `oracles` 配下の仕様断片を対象に、部分評価・全体評価の切り替え、Codex CLI による評価、問題点リストの改善、レポート保存までをまとめて担当します。
- 評価前の `INDEX.md` メンテナンスを含み、エラー時には `.cmoc/reports/review_oracles` に失敗レポートを残します。

## Read this when

- `cmoc review oracles` の処理順や、部分評価・全体評価の切り替え条件を確認したいとき。
- Structured Output の検証、問題点リストの改善、レポート生成の実装やテストを追いたいとき。
- `INDEX.md` の保守や、評価エラー時の保存先・出力内容を確認したいとき。

## Do not read this when

- cmoc review oracles のユーザー向け仕様だけを確認したいときは、`oracles/app_specs/sub_commands/review_oracles.md` を読むべきです。
- cmoc のコマンド登録や引数定義だけを確認したいときは、`src/main.py` を読むべきです。
- review oracles 以外のサブコマンド実装を追いたいときは、このファイルではなく該当モジュールを読むべきです。

## hash

- e2599e319d010c28c8a41ed34f3a24ca43229caa3303b1d8ab17420ac4f82b52

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
- `fork.py` は session branch の作成と session state 記録を担当し、`join.py` は session branch の merge と conflict 解消、`abandon.py` は session branch の破棄を担当します。
- この配下は session の開始・統合・破棄を扱う実装の入口であり、個別の処理詳細は各モジュールへ分かれています。

## Read this when

- `cmoc session` 系サブコマンドの実装入口と、`fork` / `join` / `abandon` の配置を把握したいとき。
- session パッケージ全体の役割や、どのモジュールがどのコマンドを担当しているかを確認したいとき。
- `src/sub_commands/session` 配下の実装・修正・レビュー・テストを始める前に、関連ファイルの入口を整理したいとき。

## Do not read this when

- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` のうち 1 つだけの詳細仕様を確認したいときは、この目次ではなく該当モジュールを直接読むべきです。
- `cmoc apply` 系の開始・終了や破棄の仕様だけを確認したいときは、このディレクトリではなく apply 側の仕様を読むべきです。
- `src/sub_commands/session` のパッケージ宣言だけを確認したいときは `__init__.py` を直接見れば足ります。

## hash

- 04c4167bf332c2a23f8df6d21a00c5d6aa4c922a2819c8be47cb004013df583c
