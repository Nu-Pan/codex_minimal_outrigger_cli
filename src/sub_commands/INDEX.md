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

- `src/sub_commands/apply` は `cmoc apply` 系サブコマンド実装の入口ディレクトリです。
- ここには `__init__.py`、`abandon.py`、`fork.py`、`join.py` があり、apply 系のパッケージ宣言、破棄、調査・修正ループ、取り込み処理をまとめています。
- 個別の apply サブコマンド実装へ進む前に、このディレクトリ全体の責務分担を確認したいときに読む目次です。

## Read this when

- `cmoc apply` 系の実装・修正・レビュー・テストを始める前に、どのモジュールを開くべきか整理したいとき。
- apply のパッケージ入口と、`abandon` / `fork` / `join` の役割分担を素早く把握したいとき。
- apply state、worktree、merge 後始末、レポート生成など、`cmoc apply` 周辺の処理を横断して確認したいとき。

## Do not read this when

- `cmoc apply` の利用手順や正本仕様だけを確認したいときは、`oracles/docs/app_specs/sub_commands/` 側を読むべきです。
- 個別の `cmoc apply abandon`、`cmoc apply fork`、`cmoc apply join` の詳細だけを確認したいときは、対応する実装モジュールを直接読むべきです。
- `cmoc session` や `cmoc review` など、apply 以外のサブコマンドを確認したいときはこのディレクトリは対象外です。

## hash

- e7a7e8e4bf2ba44d32af75d4428bb5198a0bf52801e617836676afe6ed4eba28

# `init.py`

## Summary

- `src/sub_commands/init.py` は `cmoc init` の本体処理を持つモジュールです。
- `repo_root` が未指定なら共通 runner に委譲し、指定済みなら `.cmoc` の ignore 確認と初期化変更の commit という 2 段階で処理します。
- `.cmoc` の ignore 保証、既存 tracked `.cmoc` の追跡解除、初期化に伴う差分 commit と結果表示をまとめて扱います。

## Read this when

- `cmoc init` の実装・修正・テスト・レビューを行いたいとき。
- `.cmoc` を git 追跡対象外にする処理、`.gitignore` 更新、tracked file の解除、初期化差分の commit 規則を確認したいとき。
- `run_command()` 経由で repo root を解決しつつ、`StepTimer` と `start_step()` で 2 段階の初期化フローをどう実行するかを把握したいとき。

## Do not read this when

- `cmoc init` 以外のサブコマンドの入口や CLI 登録だけを確認したいとき。
- `.cmoc` の ignore 保証や初期化 commit の流れが論点に入っていないとき。
- 初期化後の session / apply の運用仕様だけを追いたいとき。

## hash

- d521f2e6b339670dceeea2ae04fae5971c16a7ac9760586977de57e4f82240e6

# `review`

## Summary

- `src/sub_commands/review` は `cmoc review` 系サブコマンドの入口ディレクトリです。
- `__init__.py` はパッケージ宣言だけを担う最小モジュールです。
- `oracles.py` は `cmoc review oracles` の本体処理を担い、スナップショット固定、評価、改善、レポート出力までを実行します。

## Read this when

- `src/sub_commands/review` が Python パッケージとして宣言されていることを確認したいとき。
- `cmoc review` 系サブコマンドの入口構造や、`oracles.py` の役割を把握したいとき。
- `cmoc review oracles` の本体処理、開始時点の `oracles` スナップショット固定、評価、改善、レポート出力の流れを確認したいとき。

## Do not read this when

- `cmoc review oracles` の利用手順や引数だけを確認したいときは、`oracles/docs/app_specs/sub_commands/review_oracles.md` を読むべきです。
- `cmoc review` の CLI 登録や hidden alias だけを確認したいときは、`src/main.py` を読むべきです。
- `INDEX.md` の生成・更新ルールや、`oracles` 全体のルーティング方針だけを確認したいときは、このディレクトリを読む必要はありません。

## hash

- 85794ff51a4f9a190c00cedff044aa30985d0fa29a59ff9ca6121f5d889e709d

# `session`

## Summary

- src/sub_commands/session は `cmoc session` 系サブコマンドをまとめる実装ディレクトリです。
- ここにはパッケージ宣言用の `__init__.py` と、`session fork`、`session join`、`session abandon` の本体実装が入っています。
- session の開始、統合、破棄に関する処理の入口を、このディレクトリからたどれます。

## Read this when

- cmoc session fork / join / abandon の実装、修正、レビュー、テストを行うとき。
- このディレクトリ全体の役割と、どの実装ファイルを開くべきかを整理したいとき。
- cmoc session 系サブコマンドのパッケージ構造を確認したいとき。

## Do not read this when

- cmoc session ではなく、cmoc apply や cmoc review など別系統のサブコマンドを確認したいとき。
- 個別実装ではなく、`oracles/docs/app_specs/sub_commands/` 側の利用手順や仕様断片を直接確認したいとき。
- このディレクトリの入口構造ではなく、一般的な git の使い方や他ディレクトリの目次だけを確認したいとき。

## hash

- 6619157a18baa06475373c808120a90c431dd600ab58df9ce87cefd960382d38
