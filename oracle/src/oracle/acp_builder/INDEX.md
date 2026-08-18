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
- oracle の各サブディレクトリにおける agent call の起動構成と review・investigation・edit の責務分担を把握するための入口。edit は oracle 編集 call、investigation は oracle 調査用 TUI 起動設定、review は所見レビューの呼び出し・出力契約・統合処理を扱う。

## Read this when
- cmoc oracle edit、investigation、review の agent call 起動条件、prompt 構成、アクセス制約、モデル・推論設定、Structured Output schema を確認または変更するとき
- oracle 関連の agent call 定義や、所見レビューの入出力契約の担当箇所を特定するとき

## Do not read this when
- oracle file 自体の正本仕様、編集方針、調査対象の内容を確認するとき
- agent call の共通型・パス解決・prompt builder・構造化文書レンダリングなど、oracle 配下の個別用途に依存しない基盤を確認するとき
- realization 側の CLI 動作やテスト、または review の具体的な所見内容を直接確認するときは、該当する下位対象へ進むとき

## hash
- 1e437bf59c4d8f96e329d6a17a4c35b383ee256bc1cab224d0f87ea117b69e7a

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
- oracle 差分の realization 反映、refactor fork の差分要約・レビュー・修正に使う AgentCallParameter 構築定義の入口。apply と refactor の起動条件、作業範囲、完了条件、出力契約を扱う。

## Read this when
- `cmoc realization apply fork` の prompt、起動設定、作業範囲、権限、完了条件を確認・変更するとき。
- refactor fork の差分要約またはファイル単位レビュー・修正に関する prompt、起動パラメータ、出力契約、JSON schema と実装の対応を調査・変更するとき。

## Do not read this when
- realization の具体的な実装・テスト・補助ファイルを確認・変更するときは、対象の realization file を直接読む。
- 一般的な prompt 構築や apply/refactor 以外の realization 起動経路を調査するときは、対応する別の builder 定義を直接読む。
- 変更差分の取得・要約処理や、Structured Output の具体的な項目・形式だけを確認するときは、それぞれの対応実装・JSON schema を直接読む。

## hash
- a7ab5166ebc156ccb9f02cec6618b0db5c01026e31428d7efdb36164c761751e

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
- `cmoc tui` サブコマンド向けに、オリジナルプロンプトを埋め込んだ完全プロンプトと、TUI 実行用の固定 `AgentCallParameter` を構築する。TUI の作業ディレクトリ、リポジトリ書き込み権限、モデル・推論設定、各種ポリシー適用、インデックス事前処理を確認・変更する際の入口となる。

## Read this when
- `cmoc tui` の起動パラメータ、完全プロンプト、オリジナルプロンプトの埋め込み、または TUI 呼び出し時のモデル・推論強度・ファイルアクセス・作業ディレクトリ設定を変更・確認するとき。

## Do not read this when
- TUI 以外の AgentCallParameter 構築を扱うとき。
- 完全プロンプトの共通生成規則を確認するときは、`build_complete_prompt` の定義を直接読むべき場合。
- CLI のサブコマンド解析や TUI の画面・対話処理を変更するとき。

## hash
- 269e7272d0ef5f8a3aaab19515e3aa6669a1831413e10288ecd9e15c11fa59dc
