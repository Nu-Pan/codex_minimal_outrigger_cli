# `__init__py`

## Summary

- この `agent_call_parameter` パッケージのルーティング文書で、`base.py`、`prompt_builder/`、`apply/`、`review/`、`indexing/`、`session/` への入口です。
- `base.py` は `AgentCallParameters` などの共通型を定義し、`prompt_builder/` は prompt 組み立て、`apply/`、`review/`、`indexing/`、`session/` は各サブコマンドで発生する Codex CLI 呼び出し仕様をまとめます。
- `__init__py` はこのパッケージの Python モジュール入口として、他モジュールからの参照点になります。

## Read this when

- `AgentCallParameters`、`ModelClass`、`ReasoningEffort` の定義場所を確認したいとき。
- AI エージェント向け prompt の組み立てと、`apply` / `review` / `indexing` / `session` のどの入口を読むべきか迷ったとき。
- `agent_call_parameter` 配下で共有される呼び出しパラメータや、サブコマンド別の構成をまとめて把握したいとき。
- このパッケージ配下の `INDEX.md` を追加・修正する前に、全体の役割分担を整理したいとき。

## Do not read this when

- すでに `base.py`、`prompt_builder/complete_prompt.py`、`apply/fork/file_audit_finding.py`、`review/oracles/` など目的のファイルが分かっていて、直接開くとき。
- `cmoc apply fork`、`cmoc review oracle`、`cmoc indexing`、`cmoc session join` の個別手順だけを確認したいとき。
- このパッケージではなく、`oracle` 全体の自然言語仕様や別系統の Structured Output schema を探しているとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `apply`

## Summary

- この `apply` ディレクトリのルーティング文書で、`fork/` への入口です。
- `fork/` は `cmoc apply fork` の 4 つの主要段階である、ファイル単位監査、要修正点の整理、要修正点 1 件の実装修正、変更要約生成を案内します。
- Structured Output schema を使う読み取り中心の呼び出しと、schema を使わず realization file を修正する書き込み中心の呼び出しをまとめる目次です。

## Read this when

- `cmoc apply fork` の各段階で、どの prompt と Structured Output schema が使われるかをまとめて確認したいとき。
- ファイル単位監査、要修正点リスト改善、要修正点 1 件の実装修正、作業レポート用変更要約のどれに進むべきか迷ったとき。
- この階層の `INDEX.md` を追加・修正する前に、役割分担と分岐先を整理したいとき。

## Do not read this when

- `cmoc apply fork` 以外のサブコマンドや、`review` / `indexing` / `session` 系の agent call parameter を探しているとき。
- 対象ファイルがすでに分かっていて、`file_audit_finding.py`、`file_audit_finding.json`、`fixing_point_refinement.py`、`fixing_point_refinement.json`、`fixing_point_application.py`、`change_summary.py`、`change_summary.json` を直接開くとき。
- この階層ではなく、`apply/` 全体の入口や `oracle` 全体の共通規約だけを確認したいとき。

## hash

- 524d2efd90b5dbc242410b717b481bfc84eb2d0ac17d4f5fb91d858ac9974791

# `base.py`

## Summary

- `<cmoc-root>/oracle/src/agent_call_parameter/base.py` は、AI コーディングエージェント呼び出し用の基本データ型をまとめる入口です。
- `BackendType`、`ModelClass`、`ReasoningEffort`、`AgentCallParameters` を案内し、バックエンド種別、モデル選択、推論強度、プロンプト本文、Structured Output schema パスの所在を示します。
- `agent_call_parameter` 配下の各サブコマンド実装が共通して参照する、呼び出しパラメータ基盤の目次です。

## Read this when

- `<cmoc-root>/oracle/src/agent_call_parameter/base.py` にある共通の呼び出しパラメータ定義を確認したいとき。
- `AgentCallParameters` の項目や、`ModelClass` / `ReasoningEffort` / `BackendType` の役割を把握したいとき。
- AI エージェント呼び出しの共通基盤が `apply/` や `review/` からどう使われるかをたどりたいとき。

## Do not read this when

- すでに `AgentCallParameters`、`ModelClass`、`ReasoningEffort`、`BackendType` の定義を把握していて、この `base.py` を直接確認するとき。
- `prompt_builder/` の個別実装や Structured Output schema だけを確認したいとき。
- `apply/` や `review/` の個別フローを追いたくて、この共通基盤を経由する必要がないとき。

## hash

- 53c98b7504d0479951bc685266fb54b0c3235daa936ca0330498239084893732

# `indexing`

## Summary

- 目次情報を生成するための呼び出し仕様と出力形式をまとめた入口である。
- 対象の内容に対して、要約・読むべき条件・読む必要がない条件を整理して返す。
- 目次作成の前提となる自然言語の案内を、機械判定しやすい形で定義している。

## Read this when

- 目次情報の生成ルールと出力形式を確認したいとき。
- 対象に何を書けばよいか、要約と利用条件の切り分け方を確認したいとき。
- この領域の呼び出し仕様をたどって、目次生成の入口を把握したいとき。

## Do not read this when

- すでに目次情報を生成するための入力仕様と出力形式が分かっていて、細部を確認する必要がないとき。
- 別の呼び出し仕様や別のサブコマンド向けの案内を探しているとき。
- 対象の列挙やコミット処理だけを確認したいとき。

## hash

- 03e13fe2a47153731cd221834f546e4ef8fd46914c0e8f6a192708336301a140

# `review`

## Summary

- `cmoc review oracle` の Codex CLI 呼び出し仕様への入口です。
- `oracles/` を案内し、所見の列挙・統合・妥当性検証・採否判定に使う prompt と schema へ分岐します。
- `agent_call_parameter/review` 配下の目次として、レビュー用 agent call parameter をたどる起点です。

## Read this when

- `cmoc review oracle` 用の prompt と schema の入口をまとめて確認したいとき。
- `oracles/` に進む前に、レビュー用 Codex CLI 呼び出しの役割分担を把握したいとき。
- どのレビュー用 Python 関数または JSON schema を開くべきか迷ったとき。

## Do not read this when

- 対象の関数名や JSON schema 名がすでに分かっていて、`oracles/INDEX.md` や個別ファイルを直接開くとき。
- `cmoc review oracle` の run isolation やレポート生成だけを確認したいとき。
- `apply/`、`indexing/`、`session/` など別の agent call parameter を探しているとき。

## hash

- 6e0ae7bb9c4e178d3b24748fade429bde7d2421ca17ead15095464c9880ee54f

# `session`

## Summary

- `cmoc session` 系サブコマンドで発生する Codex CLI 呼び出し仕様への入口です。
- このディレクトリは `join/` を案内し、merge conflict marker 解消用 agent call parameter をまとめます。
- Structured Output を要求しない、ファイル編集を伴う `session join` の呼び出し仕様を扱います。

## Read this when

- `cmoc session join` で conflict 発生時に Codex CLI へ何を依頼するか確認したいとき。
- session 系サブコマンドの agent call parameter を探しているとき。
- `cmoc session join` の conflict 解消用 prompt と、その入口となる `join/` の所在を把握したいとき。

## Do not read this when

- apply、review、indexing の agent call parameter を探しているとき。
- session 状態ファイル更新や branch 削除など、Codex CLI 以外の制御処理だけを確認したいとき。
- すでに目的のファイルが `join/conflict_resolution.py` だと分かっていて、この目次を経由せず直接開くとき。

## hash

- ff3d38e390bec92af9577a9892a9aab03f86562682cdfa52b2e3c29099a37b7d
