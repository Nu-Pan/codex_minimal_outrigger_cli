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

- `src/sub_commands/apply` は `cmoc apply` 系サブコマンドの実装ディレクトリで、パッケージ宣言と `fork` / `join` / `abandon` の 3 実装をまとめています。
- 各モジュールは apply run の開始・統合・破棄を分担し、session state と worktree / branch の管理を扱います。

## Read this when

- `cmoc apply` 系サブコマンド全体の構成と役割分担を把握したいとき。
- `fork` / `join` / `abandon` のどのモジュールを読むべきか切り分けたいとき。
- apply ランの state、branch、worktree の扱いを横断的に確認したいとき。

## Do not read this when

- `cmoc session` 系サブコマンドの開始・終了・破棄だけを確認したいときは、このディレクトリではなく `src/sub_commands/session` 側を読むべきです。
- `cmoc apply` の個別実装を深く追いたいときは、このディレクトリの INDEX ではなく `__init__.py` / `abandon.py` / `fork.py` / `join.py` を直接読むべきです。
- `cmoc apply` の仕様断片や利用手順だけを確認したいときは、`oracles/docs/app_specs/sub_commands/` 側を読むべきです。

## hash

- 06668229fdc63ff42b6b9db42f6377fb4542e8f311c5e9dce6abd771ab6fd44c

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

# `review`

## Summary

- `src/sub_commands/review` は `cmoc review` 系サブコマンド実装の入口ディレクトリです。
- `__init__.py` はパッケージ宣言だけを担い、公開 API や実行ロジックは持ちません。
- `oracles.py` は `cmoc review oracles` の本体で、oracle スナップショットの評価、問題点リストの改善、レポート生成をまとめて担当します。

## Read this when

- `src/sub_commands/review` が Python パッケージとして成立しているか確認したいとき。
- `cmoc review` 系サブコマンドの入口構造や、どの実装ファイルを読むべきか整理したいとき。
- `cmoc review oracles` の実行フロー、Structured Output 検証、レポート出力を追いたいとき。

## Do not read this when

- `cmoc apply`、`cmoc session`、`cmoc init` など別サブコマンドの実装や仕様を確認したいとき。
- `cmoc review oracles` ではなく、`oracles` 配下の個別仕様断片そのものを直接確認したいとき。
- パッケージ宣言だけで足りるときは、`src/sub_commands/review/__init__.py` を直接読めば十分なとき。

## hash

- cc328a945dfaf540b67c56e07743800e886c70d8bacdee6a9914cd59811c5ad8

# `session`

## Summary

- `src/sub_commands/session` は `cmoc session` 系サブコマンド実装の入口で、`__init__.py`、`fork.py`、`join.py`、`abandon.py` をまとめるディレクトリです。
- この配下では `fork` が session 開始、`join` が merge による完了、`abandon` が merge せず破棄を担当します。
- 個別実装に進む前に、session 系の責務分担と入口構造を俯瞰するための目次です。

## Read this when

- `cmoc session` 系サブコマンドの入口と、`fork`・`join`・`abandon` の役割分担を把握したいとき。
- `src/sub_commands/session` 配下のどの実装ファイルを読むべきか整理したいとき。
- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` の実装・修正・レビュー・テストを始める前に、関連ファイルの位置関係を確認したいとき。

## Do not read this when

- `cmoc session` ではなく `cmoc apply` や `cmoc init` の実装・仕様を確認したいとき。
- `fork`、`join`、`abandon` のいずれか個別の詳細手順、状態遷移、例外条件だけを確認したいとき。
- このディレクトリのパッケージ宣言だけで足りるときは、`__init__.py` を直接読むべきです。

## hash

- 9e2cc6b6956e50ab829d89272a5d947af60efa4d505d364991fda2fcc79ac1e4
