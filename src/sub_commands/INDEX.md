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

- `cmoc apply` 系サブコマンドの実装・修正・レビュー・テストを始めるときに、配下の役割分担を把握したいとき。
- apply branch や worktree の生成、調査・修正、merge、破棄の流れを整理して、どのモジュールへ進むべきか確認したいとき。
- この配下の各モジュールへの参照先を確認して、必要な実装へ素早く移動したいとき。

## Do not read this when

- `cmoc apply fork`、`cmoc apply join`、`cmoc apply abandon` のうち 1 つだけの詳細仕様を確認したいときは、この目次ではなく該当モジュールを直接読むべきです。
- `cmoc apply` ではなく `cmoc session` 側の開始・統合・破棄仕様を確認したいときは、このディレクトリを読む必要はありません。
- このディレクトリではなく、`__init__.py` だけでパッケージ宣言を確認すれば足りるときは、ここを読む必要はありません。

## hash

- f2db376b0effa486033a2bcfd7fc22a5438467c3b9d6c4aeb1b26be3b0641986

# `eval_oracles.py`

## Summary

- `src/sub_commands/eval_oracles.py` は `cmoc review oracles` の本体実装で、対象 oracle の列挙、部分・全体評価モードの判定、Codex CLI による評価を担当します。
- 評価結果の問題点リストを severity 順に集約・改善し、`.cmoc/reports/review_oracles` へ Markdown レポートとして保存します。
- 評価前の `INDEX.md` メンテナンス、Structured Output の意味的検証、失敗時の error report 生成とフォールバック出力も扱います。

## Read this when

- `cmoc review oracles` の実行順、部分評価・全体評価の切り替え、対象 oracle の選び方を確認したいとき。
- Structured Output の検証、問題点の集約・改善、`referenced_paths` や `specification_only_basis` の検証を修正・レビューしたいとき。
- `INDEX.md` メンテナンス、レポート保存先、エラー時の error report や stderr へのフォールバックを追いたいとき。
- 評価用 prompt の組み立てや、検証 helper の役割分担を確認したいとき。

## Do not read this when

- `cmoc review oracles` のユーザー向け仕様や使い方だけを確認したいとき。
- コマンド登録や引数定義だけを確認したいとき。
- `review oracles` 以外のサブコマンド実装を追いたいとき。
- `oracles` 配下の個別仕様断片そのものを読む必要があるとき。

## hash

- 0cff3f03c64f2c7b75359d3bc701314f32bb42c01df01d954e75f9a4668936cb

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
