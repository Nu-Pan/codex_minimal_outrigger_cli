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
- `apply`、`session`、`review`、`init` などの各モジュールの仕様を追いたいとき。
- `src.sub_commands` のパッケージ宣言ではなく、実際の業務ロジックや CLI 入口を見たいとき。

## hash

- ea4df02b820eba1ca77dfb1b2227c81dbff61cd7c4c2bf4d26d891369b57fa77

# `apply`

## Summary

- このディレクトリは `cmoc apply` 系サブコマンドの実装入口で、`__init__.py` と `abandon.py`、`fork.py`、`join.py` をまとめて案内します。
- 各モジュールの役割は、`__init__.py` がパッケージ宣言、`abandon.py` が未 join の apply run の破棄、`fork.py` が調査・修正ループと report 生成、`join.py` が apply branch の merge と後始末です。
- 個別実装へ進む前に、どのファイルを読むべきかを素早く切り分けるための目次です。

## Read this when

- `src/sub_commands/apply` が `cmoc apply` 系パッケージとしてどう構成されているか確認したいとき。
- `cmoc apply fork`、`cmoc apply join`、`cmoc apply abandon` のどれを読むべきか整理したいとき。
- `apply.state` の遷移や、apply branch / worktree / report の責務分担を俯瞰したいとき。
- `__init__.py` のような最小パッケージ宣言と、各実装モジュールの入口をまとめて把握したいとき。

## Do not read this when

- 個別の `fork` / `join` / `abandon` の詳細な実行フローやエラー条件を直接追いたいとき。
- `cmoc apply` の利用手順や仕様断片そのものを確認したいときは、`oracles/docs/app_specs/sub_commands/` 側を読むべきです。
- `cmoc session` や `cmoc review` など、`apply` 以外のサブコマンドの入口だけを確認したいとき。
- `src/sub_commands/apply` 全体ではなく、特定の 1 ファイルだけの実装修正に集中したいとき。

## hash

- dacc724e792b8d0b0ac3af32891e2694ea2e97a411a2d21e76be63ade51a960d

# `init.py`

## Summary

- `cmoc init` の本体処理を定義する Python モジュールです。
- `run_command()` 経由で repo root を解決し、`.cmoc` の ignore 保証と tracked file の解除を行ったうえで、初期化に伴う変更をコミットします。
- `StepTimer` と `start_step()` を使って、`.cmoc` の ignore 確認から初期化変更の commit までを 2 段階で実行し、結果を標準出力に表示します。

## Read this when

- `cmoc init` の実装・修正・テスト・レビューを行いたいとき。
- `<repo-root>/.cmoc` を git 追跡対象外にする処理や、`.gitignore` 更新、`git ls-files` / `git check-ignore` による確認仕様を確認したいとき。
- 初期化後に続く session / apply 系コマンドの前提条件として、リポジトリ初期化の振る舞いを把握したいとき。

## Do not read this when

- `cmoc init` 以外のサブコマンドの実装や CLI 登録だけを確認したいとき。
- `.cmoc` の追跡解除や `.gitignore` 更新が論点に入っていないとき。
- 初期化後の session / apply の運用仕様だけを追いたいとき。

## hash

- 49282f4cf811268918e12479be371a9a72bb21ad66319b738e5d27f3a0a4d00c

# `review`

## Summary

- `src/sub_commands/review` は `cmoc review` 系サブコマンドの入口ディレクトリです。
- `__init__.py` はパッケージ宣言のみを担い、`oracles.py` は `cmoc review oracles` の本体処理を担います。
- この目次は、レビュー系の入口と oracles 評価本体の役割分担を整理するための案内です。

## Read this when

- `src/sub_commands/review` が Python パッケージとして宣言されていることを確認したいとき。
- `cmoc review` 系サブコマンドの入口構造を把握したいとき。
- `cmoc review oracles` の実行フロー全体を追いたいとき。
- oracles スナップショットの固定、`INDEX.md` のメンテナンス、部分評価・全体評価の切り替え、並列評価、レポート保存の流れを確認したいとき。

## Do not read this when

- パッケージ宣言だけを確認したいときは `__init__.py` を直接読むべきです。
- `cmoc review oracles` の本体ロジックや評価手順を追いたいときは `oracles.py` を直接読むべきです。
- `cmoc review` の CLI 登録や hidden alias だけを確認したいときは `src/main.py` を読むべきです。

## hash

- 22163c54c069ebfbd25baa83e33afd14a2deb11dbf27a06be7f3bd46a5539bb8

# `session`

## Summary

- `src/sub_commands/session` は `cmoc session` 系サブコマンドの実装をまとめるパッケージで、`__init__.py` と `fork.py`、`join.py`、`abandon.py` を含みます。
- session の開始・統合・破棄という 3 つの主要フローを、個別モジュールに分けて実装しています。
- このディレクトリの INDEX は、session 系の実装入口と各モジュールの役割分担を素早く把握するための案内です。

## Read this when

- `cmoc session fork/join/abandon` の実装・修正・レビュー・テストをするとき。
- `src/sub_commands/session` 配下のモジュール構成と責務分担を確認したいとき。
- session 系サブコマンドの入口がどのファイルにあるかを素早く把握したいとき。

## Do not read this when

- `cmoc apply` 系や、`session` 以外のサブコマンド実装を確認したいとき。
- session の利用手順や仕様断片そのものを確認したいときは、`oracles/docs/app_specs/sub_commands/session_*.md` を読むべきです。
- 一般的な git の操作や `cmoc` 全体の共通仕様だけを確認したいとき。

## hash

- f649cb2d0b8928c841bf7f88d6c30e9baf0ae130caaad6ba7fccd5d2cbb532f3
