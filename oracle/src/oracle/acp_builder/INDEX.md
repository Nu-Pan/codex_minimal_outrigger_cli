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
- oracle 向け agent call の用途別実装をまとめるディレクトリ。編集、調査、レビューの各サブディレクトリが、専用の prompt 構成・起動パラメータ・出力契約を確認する入口となる。

## Read this when
- oracle edit、investigation、review のいずれかに関する agent call の prompt、起動条件、アクセス制約、出力契約を確認・変更するとき
- oracle 向けの用途別実装の入口を特定し、対応するサブディレクトリへ進むとき

## Do not read this when
- oracle file 自体の正本仕様や編集方針を確認するとき
- 一般的な agent call の基底型、パス解決、prompt builder、構造化文書レンダリングを確認するとき
- realization 側の CLI 動作やテスト、または oracle review 全体の実行制御を確認するとき
- 特定の出力形式や個別の agent call 実装を直接確認できる場合

## hash
- 84c71a6d28a4352f3d2d7a7db92917ad60e90a7b04f29f11c74259f25db41094

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
- realization apply fork 用の AgentCallParameter 定義。追従対象 commit 範囲や oracle file の raw git diff を prompt に組み込み、run worktree、モデル、権限、調査・検証・routing 方針などの起動条件を構築する。oracle file の変更を realization file 全体へ追従させる Agent call を確認・変更するときの入口。
- refactor fork の agent call 定義。変更差分要約およびファイル単位のレビュー・修正について、出力契約、prompt、実行コンテキスト、アクセスモード、モデル、Structured Output schema、調査・修正・検証要件、AgentCallParameter 構築を扱う。これらの起動設定や契約を確認・変更するときの入口。

## Read this when
- realization apply fork の Agent 起動パラメータ、prompt 構築、commit 差分の埋め込み、run worktree 設定を確認・変更するとき
- oracle file の変更を realization file 全体へ追従させる Agent call のモデル設定、権限設定、実行前 indexing 設定を確認するとき
- refactor fork の変更差分要約 agent call の出力形式、prompt、実行コンテキスト、アクセスモード、モデル、Structured Output schema を確認・変更するとき
- refactor fork のファイル単位レビュー・修正 agent call の出力契約、調査範囲、修正権限、検証要件、prompt、AgentCallParameter の構築方法を確認・変更するとき

## Do not read this when
- 通常の realization implementation、test、ancillary の具体的な実装内容を確認する場合
- Agent call の共通パラメータ型や prompt の共通生成規則を確認する場合は、各定義元を直接読む
- 変更差分の取得・要約生成ロジック自体、レビュー対象の実装や個別仕様、所見判定、レビュー・修正 agent の実行処理を調べる場合
- 構造化出力の項目・型・形式だけ、または一般的な prompt builder、path model、struct document の仕様だけを確認する場合は、それぞれの定義元を直接読む

## hash
- 10e38f667aa25e5fa57669551e8f91e676357826cf59792094a4c437c8479925

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
- `cmoc tui` の完全プロンプトと Codex CLI TUI 起動用 `AgentCallParameter` を構築する実装入口。オリジナルプロンプトを埋め込み、リポジトリルートを作業ディレクトリとして、モデル、推論強度、ファイルアクセス、起動前インデックス処理を固定する。

## Read this when
- `cmoc tui` の TUI 起動パラメータや固定設定を確認・変更するとき。
- オリジナルプロンプトの完全プロンプトへの埋め込み方と、その構築呼び出しを調査するとき。
- TUI 起動時の作業ディレクトリ、モデル、推論強度、ファイルアクセスモード、インデックス処理の設定根拠を確認するとき。

## Do not read this when
- 完全プロンプトの共通生成規則を確認したいときは、`build_complete_prompt` の定義を直接読む。
- TUI の画面表示や対話操作を確認したいときは、該当する TUI 実装を直接読む。
- `AgentCallParameter`、モデル、推論強度、ファイルアクセスモードの一般仕様を確認したいときは、各型の定義を直接読む。

## hash
- ea497a5a3579639bfc48b68831772a92cfcc173d73d196a7a9fd45371e72dc7b
