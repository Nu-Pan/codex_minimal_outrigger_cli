# `acp`

## Summary

- AI コーディングエージェント呼び出しに関する realization 実装への入口です。
- `prompt_parts/` は共通 prompt 断片、`builder/` はサブコマンド別の `AgentCallParameter` と Structured Output schema を扱います。
- oracle/src/acp の正本断片に対応する prompt 生成と agent call parameter 生成を確認する起点です。

## Read this when

- prompt 断片や agent call parameter builder の実装・テストを確認したいとき。
- `cmoc apply fork`、`cmoc review oracle`、`cmoc indexing`、`cmoc session join` の Codex CLI 呼び出し境界を追いたいとき。
- Structured Output schema の配置や prompt への標準断片注入を確認したいとき。

## Do not read this when

- CLI サブコマンドの実行制御や git 状態遷移だけを確認したいとき。
- path model、StructDoc、config など共通基盤だけを直接確認したいとき。
- 既に読むべき builder や prompt part のファイル名が分かっているとき。

## hash

- e70a5cb210b709aa9114717790e2671973ec8c72f0984ba2ef72d43c44c9cd02

# `basic`

## Summary

- cmoc の共通基盤 realization 実装への入口です。
- `acp.py`、`path_model.py`、`standard.py`、`struct_doc.py` の論理型、path token 解決、標準文書、Markdown レンダリングを扱います。
- oracle/src/basic の正本断片と対応する基盤 API を確認する起点です。

## Read this when

- `ModelClass`、`ReasoningEffort`、`FileAccessMode`、`AgentCallParameter` の定義を確認したいとき。
- `<cmoc-root>` / `<repo-root>` / `<run-root>` / `<work-root>` の path model を追いたいとき。
- `StructDoc` や `Standard` から prompt 用 Markdown を生成する処理を確認したいとき。

## Do not read this when

- CLI のサブコマンド実装や git 操作だけを確認したいとき。
- prompt 断片の具体的な文言や builder の引数だけを確認したいとき。
- config の既定値だけを直接確認したいとき。

## hash

- 69954679dba159a9b9c60034de86c2380953a718fe5f8862597af9835c21bf28

# `cmoc_runtime.py`

## Summary

- `commons.cmoc_runtime` への compatibility shim です。
- 既存の `import cmoc_runtime` やテストの monkeypatch 境界を保ちながら、shared runtime helper の本体を `src/commons/cmoc_runtime.py` に置きます。

## Read this when

- 旧来の `cmoc_runtime` import path がどこへ接続されているか確認したいとき。
- compatibility shim と shared runtime 実体の関係を確認したいとき。

## Do not read this when

- runtime helper の実装内容を確認したいときは `commons/cmoc_runtime.py` を読むべきです。
- Typer のコマンド登録や subcommand implementation を確認したいとき。

## hash

- 81ecd7098ca82b3aab203450f5599ed486313c7b477ea88f527c4b7356c81e04

# `commons`

## Summary

- cmoc の shared helper 実装を置く realization ディレクトリです。
- `cmoc_runtime.py` は git 操作、状態ファイル、config 永続化、Codex CLI 呼び出し、エラー整形、ログなど複数 subcommand が共有する runtime helper を担当します。
- design rule の shared functionality 配置に対応する入口です。

## Read this when

- subcommand 間で共有される runtime helper や状態管理処理を確認したいとき。
- `src/main.py` や `src/sub_commands/` から呼ばれる共通処理を修正したいとき。
- `cmoc_runtime` compatibility shim の実体を確認したいとき。

## Do not read this when

- Typer の command 登録や個別 subcommand の本命処理だけを確認したいとき。
- prompt builder、path model、config dataclass など oracle/src と同形の基盤実装だけを直接確認したいとき。
- `cmoc_runtime.py` shim の import 互換性だけを確認したいとき。

## hash

- 0ab928ec9cb3833bbeda9b9958192819a51463cd85380c97ebb1202939464a32

# `config`

## Summary

- cmoc の設定 dataclass realization 実装への入口です。
- `CmocConfig` と Codex CLI 向け model/reasoning effort の既定マッピングを扱います。
- oracle/src/config の正本断片に対応する設定構造を確認する起点です。

## Read this when

- `CmocConfig`、`CmocConfigCodex`、apply/review ループ回数の既定値を確認したいとき。
- logical model class から Codex CLI 用モデル名への対応を確認したいとき。
- 設定永続化や config schema の実装を追加する前に既存構造を把握したいとき。

## Do not read this when

- CLI のサブコマンド処理や git 状態遷移だけを確認したいとき。
- prompt 文面や Structured Output schema を確認したいとき。
- path token 解決や StructDoc 生成だけを追いたいとき。

## hash

- 9ca7b05b582423349733cdbae07a437d02f7020041c8d919648dea04f6f9a917

# `main.py`

## Summary

- Typer による `cmoc` CLI の realization 実装です。
- `init`、`indexing`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracle` のコマンド登録、completion probe 用 program name 固定、work root 実行検査、config 同期、Codex 呼び出し前 indexing、INDEX entry 並列生成、apply fork 編集禁止差分検査、apply worktree の動的解決、apply join 差分判定、review report 生成、実行制御を扱います。
- `bin/cmoc` から起動される Python 側エントリーポイントです。

## Read this when

- CLI サブコマンドの引数、事前条件、stdout、状態遷移を確認したいとき。
- `cmoc init` の config 同期、completion probe、work root 実行検査、Codex 呼び出し前 indexing、INDEX entry 並列生成、apply fork の編集禁止差分検査、apply worktree の動的解決、apply join の想定外差分判定、review report の frontmatter、session/apply/review/indexing の実装を修正したいとき。
- shell entrypoint から呼ばれる `main()` の流れを追いたいとき。

## Do not read this when

- git helper や session state dataclass の詳細だけを確認したいとき。
- prompt builder の文言や schema だけを確認したいとき。
- oracle/src と同形の基盤実装だけを直接確認したいとき。

## hash

- 4ffeaada81485fe023bf4515f2466e0f5dc722731ac506c5125e5d9290553f6b

# `sub_commands`

## Summary

- cmoc の各 subcommand の本命処理を置く realization ディレクトリです。
- 現時点では `init.py` が `cmoc init`、`session.py` が `cmoc session fork/join/abandon`、`indexing.py` が `cmoc indexing` と indexing preflight、`apply.py` が `cmoc apply fork/join/abandon`、`review.py` が `cmoc review oracle` の実処理を担当します。
- `src/main.py` の Typer callback から呼び出される subcommand implementation の移管先です。

## Read this when

- design rule に沿った subcommand implementation の配置を確認したいとき。
- `cmoc init`、`cmoc session`、`cmoc indexing`、`cmoc apply`、`cmoc review oracle` の本命処理を確認したいとき。
- Typer callback と実処理の責務分離を修正したいとき。

## Do not read this when

- Typer の command 登録や引数解釈だけを確認したいとき。
- prompt builder、path model、config dataclass など oracle/src と同形の基盤実装だけを直接確認したいとき。
- `cmoc_runtime.py` の git helper や状態ファイル dataclass の詳細だけを確認したいとき。

## hash

- afdc4a515c6de9407c4b6d7fa279cd534d26f12a76801b9836522df3effc418c
