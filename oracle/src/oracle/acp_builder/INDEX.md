# `basic.py`

## Summary
- cmoc の論理エージェント呼び出しパラメータを定義するデータモデルと、モデル種別・推論強度・ファイルアクセスモードの列挙型を提供する。エージェント呼び出し構築処理で、呼び出し種別、モデル選択、アクセス制約、プロンプト、Structured Output schema、実行ディレクトリなどの設定をまとめて扱う入口。

## Read this when
- エージェント呼び出しのパラメータ構造、論理モデルクラス、推論強度、ファイルアクセスモードを確認・変更するとき。
- エージェント呼び出しに渡すプロンプトや schema パス、cwd、indexing preflight の既定値の契約を確認するとき。

## Do not read this when
- 実際のバックエンドモデル名や推論強度への変換規則を確認したいとき。
- Codex CLI の具体的なファイルアクセス制約の正本や、realization 側のエージェント実装を確認・変更するとき。

## hash
- f8bf61c9a692c82b0c01f3922a0b00946ae526d4e949797512d74dd5565ab990

# `feedback`

## Summary
- feedback 配下で、観測の issue 同一性判定と issue candidate の現在状態検証に関する Structured Output schema および agent call 構築処理を扱う。normalize_issue は既存 issue か新規 issue かの判定入口、verify_issue は report cut 時点の参照情報に基づく検証入口であり、各 schema は対応する出力契約を定義する。

## Read this when
- feedback observation と既存 issue candidate の同一性判定に関する出力契約、agent call、prompt 構成を確認するとき
- issue candidate の report cut 時点の状態検証、verdict ごとの出力条件、検証用 agent call の prompt や起動パラメータを確認するとき

## Do not read this when
- issue の絞り込み、feedback state、raw log、過去 session の参照など、候補収集や feedback state 管理を確認するとき
- issue の summary、impact、原因、actionability、human action、verification verdict、relation の生成・評価そのものを確認するとき
- 実際の verification 実装やテストの挙動、個別 issue の内容、一般的な JSON Schema の仕様だけを確認するとき

## hash
- 9bce1e990942a31cc1e94025a412eb86c1562be17539e2152ff673046379cbdd

# `indexing`

## Summary
- `cmoc indexing` の INDEX.md エントリー生成を定義するディレクトリ。生成結果の Structured Output schema と、対象本文・パス文脈・実行設定を含む agent call 構築実装を扱う。
- `index_entry.json` はエントリーの出力契約を定義し、`index_entry.py` は生成用 prompt と agent call パラメータの入口となる。

## Read this when
- INDEX.md エントリーの必須項目や JSON 出力形式を確認するとき。
- INDEX.md エントリー生成用 agent call の prompt、対象パス解決、モデル・推論設定、読み取り専用設定を確認・変更するとき。

## Do not read this when
- 既存の INDEX.md のルーティング内容だけを確認したいとき。
- 生成結果の形式だけを確認したい場合は `index_entry.json` を直接読む。
- 共通 prompt の構築規則や、エントリー生成以外の agent call を調べるとき。

## hash
- 135668dd576a398378b1cdd3367127a2632d45f8a4f2d7bb54ca21ee5494fd58

# `oracle`

## Summary
- oracle 関連の agent call 起動定義を扱うディレクトリで、edit・investigation・review の各処理へ進むための入口を提供する。
- oracle 編集・調査・レビューにおける prompt、アクセス範囲、起動パラメータ、Structured Output 契約の確認対象を含む。

## Read this when
- oracle edit の本命処理または仕様削減処理の起動条件、prompt、アクセスモード、モデル・推論設定、作業ディレクトリ、indexing 実行有無を確認・変更するとき。
- oracle investigation の TUI 起動パラメータ、完全 prompt、読み取り専用範囲、モデル設定、indexing 事前処理を確認・変更するとき。
- oracle review の所見生成、妥当性検証、採否判定、重複・矛盾の統合に関する入力・出力契約や agent call 起動条件を確認するとき。

## Do not read this when
- oracle の仕様本文や編集内容そのものを確認するときは、該当する oracle file を直接読む。
- 共通の agent call パラメータ構築、prompt 生成、パス解決、アクセス制御を確認するときは、上位の共通定義を直接読む。
- 個別の Structured Output schema の項目・型・形式だけを確認するときは、該当する schema ファイルを直接読む。

## hash
- de31f57c2a295c45c48f41bb600e91fff6f92ea7eb09c999df6e602e66a2f01b

# `quota_probe.py`

## Summary
- Codex CLI の quota 回復確認用 agent call を構築する定義。probe 用 prompt の内容、読み取り専用のアクセス設定、最小モデル・低推論強度、agent call の作業ディレクトリ、preflight 無効化などの起動パラメータをまとめる。quota 可用性確認の agent call 構築処理への入口となる。

## Read this when
- Codex CLI の quota 回復確認 probe の prompt や起動パラメータを確認・変更するとき
- quota 可用性確認用 agent call のモデル、推論強度、アクセスモード、preflight 設定を調べるとき

## Do not read this when
- quota probe の実行結果や quota 状態そのものを確認したいとき
- 一般的な prompt 生成処理や agent call の基本型を確認したいときは、それぞれの prompt builder または ACP 基本定義を直接読む

## hash
- d8aef551b3064c128af79d8831de5a0ac8d87610f17cc52351b9f8d777bec991

# `realization`

## Summary
- oracle の変更を realization に反映する apply 処理と、refactor 差分の要約・ファイル単位レビューおよび修正を起動する定義をまとめたディレクトリ。各 fork の prompt、ファイルアクセス権限、モデル・推論設定、Structured Output schema、起動前 indexing を確認する入口。
- apply/fork は oracle file の commit 範囲と raw git diff を受け取り、realization file へ差分を反映する AgentCallParameter と prompt を構築する。
- refactor/fork は refactor 差分の変更要約、および指定した oracle file または realization file を起点とするレビュー・修正の AgentCallParameter、prompt、Structured Output schema を定義する。

## Read this when
- oracle の変更を realization に追従させる Agent の起動定義や prompt を調査・変更するとき
- refactor 差分の要約処理、またはファイル単位の realization レビュー・修正処理の起動条件、権限、モデル設定を確認するとき
- refactor の変更要約またはレビュー・修正結果の Structured Output 契約を確認するとき

## Do not read this when
- 個別の oracle file や realization file の実装内容、要求、差分そのものを調査するとき
- AgentCallParameter の共通仕様、prompt の共通生成、パス解決、構造化文書レンダリング、Agent 呼び出し基盤を確認するときは、それぞれの共通定義を直接読む
- 変更要約またはレビュー・修正の出力項目だけを確認したいときは、対応する JSON schema を直接読む

## hash
- 8f550d26c23019668c4ac9730476ec5249615a7dd59d7c761d37b38923b857cf

# `session`

## Summary
- `session/join` は、`cmoc session join` における merge conflict marker 解消用 agent call の構築定義への入口。conflicted paths の実パス解決、対象ファイルの prompt への埋め込み、conflict 解消専用 policy、REPO_WRITE 権限、最高品質の model・reasoning 設定、preflight 無効化を扱う。

## Read this when
- `cmoc session join` の conflict 解消 agent call に渡す対象ファイル、prompt、アクセス権限、適用 policy、model・reasoning、preflight 設定を確認・変更するとき

## Do not read this when
- merge conflict marker を含む対象ファイルを直接確認・編集するとき
- 通常の prompt 生成や session join の別処理を調べるとき。該当する prompt builder または session join 実装を直接読む。

## hash
- 373ae33e1a529b56c51bf23e18583cac2b27ffa5e0bf734f9997254aa7e55799

# `tui`

## Summary
- `cmoc tui` の TUI 起動に使う AgentCallParameter と完全プロンプトを構築する実装。オリジナルプロンプトを埋め込み、リポジトリ書き込みモード、リポジトリルートの作業コンテキスト、モデル・推論設定、oracle/realization と routing policy、起動前 indexing を含む固定パラメータを定義する。

## Read this when
- `cmoc tui` の起動パラメータまたは完全プロンプト skeleton の構築を確認・変更するとき。
- オリジナルプロンプトの埋め込み方、作業ディレクトリ、ファイルアクセスモード、モデル・推論設定、起動前 indexing の設定を確認するとき。

## Do not read this when
- 完全プロンプトの共通レンダリング規則を確認する場合は、`build_complete_prompt` の実装を直接読むとき。
- TUI 起動パラメータの呼び出し元や、別サブコマンドの設定を調べる場合。

## hash
- fe0c844b30d4c5106f83b0c9c65ecff5f2898928445521fb06d060f8f97b8f09
