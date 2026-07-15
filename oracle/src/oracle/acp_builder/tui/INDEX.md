# `launch_tui.py`

## Summary
- `cmoc tui` で編集後の元プロンプトを共通プロンプトに束ね、完全プロンプトを書き出したうえで起動用 `AgentCallParameter` を組み立てる入口。起動時に固定されるモデル選択、推論強度、ファイルアクセス方針、保存先の扱いを確認したいときに読む。
- TUI 本体や入力編集の流れではなく、TUI 起動前に決まる呼び出し条件と保存済みプロンプトの扱いに関心があるときの案内になる。

## Read this when
- `cmoc tui` の起動パラメータ、保存される完全プロンプト、または起動時に固定されるモデル・推論強度・ファイルアクセス方針を変えたいとき。
- 元プロンプトをどう共通プロンプトへ束ねて、どのファイルへ保存してからエージェント呼び出しに渡すかを確認したいとき。
- `cmoc tui` の実行フローのうち、TUI 起動用の `AgentCallParameter` を生成する部分だけを追いたいとき。

## Do not read this when
- `cmoc tui` の実行本体、エディタ選択、対話 UI の制御を追いたいだけのとき。
- 実行パラメータ解決の別経路や、共通プロンプト生成の個別部品を見たいとき。
- `AgentCallParameter` 型そのものや共通のモデル定義だけを確認したいとき。

## hash
- b1566b81149ccfc58e08edd5eea264b2f5474fa3e340826aa45b282fce7527ef

# `resolve_parameter.json`

## Summary
- role: AI Agent CLI/TUI が `cmoc tui` の実行パラメータ解決を担う前提で、この schema の目的に合う。
- summary: TUI の実行パラメータ選定と、その出力 schema に関わるため、対象の役割を一言で示す必要がある。
- goal: Structured Output schema に従って TUI のパラメータ解決結果を返す、というこのファイルの用途に一致する。
- file_access_mode: このファイルは oracle src の正本仕様断片なので、読むだけで足りる。
- oracle_and_realization_basic: oracle file と realization file の境界を前提にしたルーティングなので、これを読む必要がある。
- oracle_standard: この schema は oracle file を読むかどうかの判定項目を持つため、oracle file の扱いを確認する必要がある。
- realization_standard: この schema は realization file を読むかどうかの判定項目を持つため、realization file の扱いを確認する必要がある。
- review_oracle_standard: この schema は review 用の standard 読み込み判定を持つため、レビュー観点の基準を確認する必要がある。
- apply_review_standard: この schema は apply 用の standard 読み込み判定を持つため、所見反映側の基準を確認する必要がある。
- index_entry_standard: この作業自体が INDEX.md エントリー生成なので、書式と境界条件の基準を確認する必要がある。

## Read this when
- TUI の実行パラメータ解決の正本を変えたいとき。
- TUI が選ぶファイルアクセスモードや、どの標準文書を読み込むかの判定を変えたいとき。
- TUI resolve-parameter の Structured Output schema を確認・更新したいとき。
- この処理がどの標準文書を前提にしているかをたどりたいとき。

## Do not read this when
- TUI 以外の別サブコマンドのパラメータ生成を変えたいときは、該当サブコマンドの正本を見る。
- TUI の起動や転送だけを確認したいときは、resolve-parameter ではなく起動側の正本を見る。
- 個別の standard 本文そのものを直したいときは、この schema ではなく各 standard の正本を見る。

## hash
- 42b774d0c3675155a6008849266f1c43e76dd4baa2ef6fced307bab6b216ee1a

# `resolve_parameter.py`

## Summary
- `cmoc tui` の実行に渡す AI Agent 呼び出し条件を組み立てる正本。実行モデル、推論強度、ファイルアクセスモード、出力先 JSON、固定プロンプト本体の組み立て方を確認したいときに読む。

## Read this when
- `cmoc tui` の実行時に、どのモデル वर्ग・推論強度・アクセス制約でエージェントを起動するかを変える必要がある。
- オリジナルプロンプトを受けて、実行用プロンプトと返却パラメータの対応を追いたい。
- プロンプトに含める固定文言や、参照させる作業ルート・リポジトリルートの扱いを確認したい。

## Do not read this when
- `cmoc tui` の画面操作や入出力そのものの実装を見たい場合は、呼び出し側の実装を直接読む。
- ファイルアクセスルールの個別内容だけを見たい場合は、ここではなくそのルール定義側を読む。
- 他サブコマンドのパラメータ解決を探している場合は、このファイルではなく該当サブコマンドの解決ロジックを読む。

## hash
- 81bbc66ac758546192770b38bcbf7810c5b1cdc5b58c1ef1087f6bb5259662b9
