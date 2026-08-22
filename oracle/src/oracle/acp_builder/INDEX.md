# `basic.py`

## Summary
- AIコーディングエージェント呼び出しに必要な論理モデルクラス、推論強度、ファイルアクセスモード、プロンプト、Structured Output schema、作業ディレクトリなどのパラメータ契約を定義する。`ModelClass`、`ReasoningEffort`、`FileAccessMode` の選択肢と、その意味・バックエンド解決責務を確認したい場合の入口となる。

## Read this when
- agent call builder の戻り値や呼び出しパラメータの契約を確認・変更するとき
- モデル選択、reasoning effort、ファイルアクセス制御、prompt、Structured Output schema、agent call の cwd を扱う実装を調査するとき
- indexing preflight の実行要否を含む agent call 設定を確認するとき

## Do not read this when
- 実際のモデル名やバックエンド固有の解決処理を確認したいときは realization src を直接読む
- Codex CLI sandbox における各ファイルアクセスモードの正本仕様を確認したいときは指定された oracle 文書を読む
- 個別の builder 関数による prompt 構築や、呼び出し実行そのものだけを調べるとき

## hash
- 16da7aac62b6eb20427359ba16f1b4d49c15b57ef69f966a83830852c2177673

# `feedback`

## Summary
- feedback issue の同一性判定と現在状態の検証に使う AgentCallParameter 定義および Structured Output schema の入口。normalize_issue は観測と既存 issue candidate の同一性を判定し、verify_issue は report cut 時点の evidence に基づき issue candidate の verdict を決める。各 JSON schema は対応する判定結果の出力契約を定義する。

## Read this when
- feedback issue の同一性判定、既存・新規 issue の選択、normalize issue の prompt や起動設定を確認するとき
- report cut 時点における issue candidate の unresolved / resolved / not_actionable / inconclusive 判定と、その prompt・起動設定を確認するとき
- normalize issue または verify issue の Structured Output の必須項目や許容構造を確認するとき

## Do not read this when
- issue の生成・報告・状態管理など、同一性判定や現在状態の検証以外の feedback 処理を確認するとき
- 個別 issue の内容、report cut reference、raw log など具体的なデータを確認するとき
- AgentCallParameter や prompt rendering の共通仕様を確認するときは、対応する共通実装を直接読むべき場合
- 一般的な JSON Schema の仕様や検証方法だけを確認したいとき

## hash
- 5590d9d2830eee29d4d65228294663495f1e457dce6ef35a7855f5235abe15b7

# `indexing`

## Summary
- cmoc indexing における INDEX.md エントリー生成を扱うディレクトリ。index_entry.py は対象本文を含む agent call 用 prompt、Structured Output、読み取り専用アクセス、cwd、経済性重視の起動設定を構築する。index_entry.json は生成結果の JSON Schema を定義する。
- agent の prompt や起動パラメータを確認するときは index_entry.py を、エントリー生成結果の構造や必須項目を確認するときは index_entry.json を読む入口になる。

## Read this when
- cmoc indexing の INDEX.md エントリー生成 agent の prompt、モデル・推論・preflight・アクセスモード・cwd・Structured Output 設定を変更または確認するとき
- INDEX.md エントリー生成結果の JSON Schema と必須項目を確認するとき

## Do not read this when
- 既存の INDEX.md のルーティング内容だけを確認したいとき
- prompt の一般的な組み立て規則だけを確認したいときは、index_entry.py から参照される prompt builder 実装を直接読む

## hash
- 135668dd576a398378b1cdd3367127a2632d45f8a4f2d7bb54ca21ee5494fd58

# `oracle`

## Summary
- oracle 用 agent call の起動パラメータ、完全 prompt、oracle 読み書き範囲、作業ディレクトリ、モデル・推論設定、インデックス事前処理を構築するディレクトリ。
- edit は oracle file の編集と仕様削減、investigation は oracle file の読み取り専用調査、review は所見の列挙・擁護・反証・採否判定・統合を扱う下位入口である。review 配下には各処理の Structured Output schema も対応して置かれている。

## Read this when
- oracle に対する edit・investigation・review の agent call の prompt、アクセス制約、起動設定、または Structured Output 契約を確認・変更するとき
- 対象の処理が edit、investigation、review のどの下位ディレクトリに属するかを判断するとき
- review の所見列挙、妥当性検証、採否判定、重複・矛盾の統合に関する agent call の入口を確認するとき

## Do not read this when
- oracle file 自体の正本仕様、調査対象の内容、編集方針を確認するとき
- 共通の AgentCallParameter、パス解決、prompt builder、構造化文書レンダリングの実装を確認するとき
- oracle review 全体の実行制御や、判定後の所見適用処理を確認するとき
- 特定の処理の詳細な prompt、実装、出力 schema を確認できる場合に、ディレクトリ全体を読む必要があるとき
- realization 側の CLI 動作やテストを確認するとき

## hash
- 4c10fbaa2a42f5a95f11de046d45c57b6dbc3f64574279b08b97cebe82cd371a

# `quota_probe.py`

## Summary
- Codex CLI の quota 回復確認用 agent call を構築する定義。quota availability probe の完全 prompt と起動パラメータを、probe 用 cwd を基準に生成する。
- probe は追加の調査や作業を行わず短い応答を 1 回返す用途で、読み取り専用・最小モデル・低 reasoning effort の実行条件を定める。

## Read this when
- Codex CLI の quota 回復確認や利用可能性確認用 agent call の prompt・起動パラメータを確認するとき
- quota probe の cwd、読み取り専用設定、モデル・reasoning effort、preflight 実行有無を確認するとき

## Do not read this when
- quota availability probe 以外の agent call の prompt や起動パラメータを確認するとき
- quota probe の実装処理や quota 判定ロジックそのものを確認するときは、該当する実装・判定対象を直接読む場合

## hash
- 9ff86001f27931a401580a7a0587b29d10a439c30dbc964a278980d85d3bc2b1

# `realization`

## Summary
- realization file を oracle file の変更へ追従させる agent call 群の定義をまとめたディレクトリ。
- apply は oracle file の差分を realization file へ反映する追従処理、refactor は変更要約とファイル単位のレビュー・修正処理への入口である。
- 各処理の具体的な prompt 構築、起動パラメータ、作業モード、検証条件を確認する際に、下位の apply または refactor へ進む。

## Read this when
- oracle file の変更を realization file へ反映する apply 処理の起動条件や作業範囲を確認するとき
- refactor fork の変更要約、レビュー、修正の agent call 群を横断して責務や入口を確認するとき
- realization file の差分追従、レビュー、修正に関する下位定義の所在を判断するとき

## Do not read this when
- apply の差分追従処理の具体的な prompt や実装だけを確認したい場合は apply 配下を直接読むとき
- refactor の変更要約またはファイル単位レビュー・修正の具体的な契約を確認したい場合は refactor 配下を直接読むとき
- 通常の realization 実装、テスト、補助成果物の内容を調査するときは、それぞれの realization file を直接読むとき

## hash
- cd380d62730fac413c9130ae3800ec3ed16d4b4c063c26e287012515944c1a0e

# `session`

## Summary
- `cmoc session join` における Git merge conflict marker 解消エージェントの起動パラメータ構築を担う実装。conflict 対象のパス解決、対象ファイルと編集方針を含む prompt、作業ディレクトリ、書き込み権限、モデル・推論設定をまとめる。

## Read this when
- `cmoc session join` の conflict marker 解消処理を変更・調査するとき
- conflict 解消エージェントへ渡す対象ファイル、prompt、作業ディレクトリ、モデルまたは推論設定を確認するとき

## Do not read this when
- `session join` の通常処理や conflict marker 解消以外の処理を確認するとき
- 共通 prompt 生成処理の仕様を確認するとき
- AgentCallParameter の一般的な型や設定値の仕様だけを確認するとき

## hash
- 29c7ea98c4901662e98d3787aa34c0707c422e366a1353cad734ba5db7a77359

# `tui`

## Summary
- `cmoc tui` の起動に必要なプロンプトと AgentCallParameter を構築する入口。作業パス、モデル・推論設定、ファイルアクセスモード、インデックス事前実行などの固定パラメータを扱う。

## Read this when
- `cmoc tui` の起動パラメータや完全プロンプトの構築を確認・変更するとき
- TUI 起動時のモデル、推論、ファイルアクセス設定を確認・変更するとき

## Do not read this when
- TUI の画面表示や対話ループそのものを調べるとき
- プロンプト生成の詳細や構造化文書の定義を直接確認したいとき

## hash
- cb678f004fe8cb4c3438e11aace22439c05a14d71dba1c4a4a85d0458f5157a7
