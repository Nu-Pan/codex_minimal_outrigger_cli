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
- feedback issue の同一性判定と現在状態の検証に使う prompt・AgentCallParameter・Structured Output schema をまとめたディレクトリ。normalize_issue は observation と既存候補の同一性判定、verify_issue は report cut 時点の evidence に基づく issue 状態の検証を担う。feedback 処理における判定・検証契約の入口として各実装と schema を確認する。

## Read this when
- feedback observation が既存 issue と同一か新規かを判定する処理の入力範囲、起動条件、出力契約を確認するとき
- issue candidate の unresolved、resolved、not_actionable、inconclusive 判定や report cut reference に基づく検証処理を確認するとき
- 判定・検証用の prompt と Structured Output schema の対応関係を調べるとき

## Do not read this when
- feedback issue の記録・送信や observation の状態管理を確認するとき
- summary、impact、原因、actionability、human action、verification verdict、relation など issue 内容の生成を確認するとき
- 候補の絞り込み、feedback state、raw log、共通の agent call 型や JSON Schema の一般仕様を直接確認するとき

## hash
- 1c048dbe9a0dd3c046d2d1dac1961d00bed3bce1b2b7b9073d0a46e8992f2128

# `indexing`

## Summary
- `cmoc indexing` の INDEX.md エントリー生成に使う agent call の定義をまとめたディレクトリ。対象内容を埋め込んだプロンプト、読み取り専用設定、モデル・推論設定、Structured Output schema の参照を扱う。
- 下位の Python 実装が agent call パラメータ構築を担い、JSON schema が生成結果の形式を定義するため、indexing 用の起動条件や出力契約を確認する入口となる。

## Read this when
- `cmoc indexing` の INDEX.md エントリー生成処理を変更または確認するとき。
- 生成 agent call のプロンプト、対象ファイルの渡し方、読み取り専用アクセス、モデル・推論設定、実行 cwd を確認するとき。
- エントリー生成結果の Structured Output schema と、その参照方法を確認するとき。

## Do not read this when
- INDEX.md エントリーの出力項目や JSON schema だけを確認したい場合は、下位の schema ファイルを直接読むとき。
- agent call の一般的な実行フローや共通プロンプト生成処理を確認したい場合は、呼び出し側または共通の prompt builder を直接読むとき。
- 実際の INDEX.md のルーティング内容や対象ディレクトリの責務を調べる場合は、この agent call 定義ではなく対象となる実装・文書を読むとき。

## hash
- 6518c41131b96ae2b13601d14faed245828a107756d5bfc17a8c5565c26c6798

# `oracle`

## Summary
- oracle investigation・edit・review 各処理の agent call 用 prompt と起動パラメータを定義するディレクトリです。調査・編集・レビューの起動条件、読み書き権限、モデル、推論強度、作業ルート、indexing 設定を確認する入口です。
- review 配下では、所見の列挙、擁護・反証理由の生成、採否判定、重複や矛盾の統合に使う prompt 構築実装と Structured Output schema を扱います。

## Read this when
- oracle investigation・edit・review の agent call prompt、権限、起動設定を調査または変更するとき。
- oracle review の所見処理や出力 schema の構成を確認するとき。
- 配下の investigation、edit、review のどの処理を入口にすべきか判断するとき。

## Do not read this when
- 完全 prompt の共通生成規則だけを確認したいときは prompt 構築側を直接読む。
- ACP の基本パラメータ型やパス解決だけを確認したいときは、それぞれの定義元を直接読む。
- 対象 oracle file の仕様や realization の実装内容を確認したいときは、対象ファイルを直接読む。
- 個別レビュー処理の実装または schema だけを確認したいときは、review 配下の対応ファイルを直接読む。

## hash
- b244a105674b3576453f483a8c847360ff1d72caf2bc15e84958296c89d480d0

# `quota_probe.py`

## Summary
- quota availability probe 用 agent call の prompt 文面と起動パラメータを構築する関数を定義する。quota 回復確認用の専用設定を確認する入口である。

## Read this when
- Codex CLI の quota 利用可能性確認用 agent call の構築内容を確認・変更するとき
- probe の cwd、読み取り専用設定、モデル・推論設定、prompt 生成、indexing preflight の指定を確認するとき

## Do not read this when
- quota probe 以外の通常の agent call パラメータを確認したいとき
- 共通の prompt 構築処理や quota 利用可能性の判定・実行結果を直接確認したいとき

## hash
- a9b61224964c68973387f08c74a880a32cc82006572ed1896ec78b6de99b8d65

# `realization`

## Summary
- `cmoc realization apply fork` による oracle の変更差分追従を担う Agent Call 構築群への入口。fork 配下の prompt、起動設定、参照・routing 方針を確認するための上位ルートであり、具体的な prompt 実装は `fork/launch_exec.py` に進む。
- refactor fork の変更差分要約と、ファイル単位のレビュー・修正を担う prompt builder および Structured Output schema への入口。変更分類、oracle/realization 要求に基づく所見・修正・検証、変更 path の対応を確認する際に利用する。

## Read this when
- `cmoc realization apply fork` の差分追従処理で、prompt、oracle diff の渡し方、commit 範囲、Agent Call の実行設定を確認または変更するとき。
- 差分追従の完了条件、oracle/realization の参照方針、リポジトリ全体を対象とする routing の入口を探すとき。
- refactor fork の変更差分を意味論的に要約する prompt と起動設定を調べるとき。
- ファイル単位レビュー・修正の対象 path、worktree、ファイルアクセス、oracle/realization policy、検証条件を調べるとき。
- 変更要約またはレビュー結果の Structured Output 契約、変更 path・根拠・対応状態の関係を確認するとき。

## Do not read this when
- 具体的な `apply` の prompt 構築や `AgentCallParameter` 実装を確認するときは、`fork/launch_exec.py` を直接読む。
- realization の個別実装・テスト・補助ファイル、または共通 prompt・Agent Call・パス・構造化文書仕様を確認するときは、対応する対象を直接読む。
- 具体的な refactor の変更要約またはファイル単位レビュー・修正の prompt 構築処理を調査するときは、対応する Python 定義を直接読む。
- Structured Output の項目、型、`status` 値だけを確認するときは、対応する JSON schema を直接読む。
- レビュー対象の実装内容、oracle/realization の個別要求、実際の差分を調査するときは、対象ファイルや diff を直接読む。

## hash
- 0e8d94799cd9ffb4e87e6c1998f917e0fa6789729a8004c18b1bad9884149350

# `session`

## Summary
- `cmoc session join` における Git merge conflict 解消用の AgentCallParameter 構築実装を扱う。conflict 対象パスの解決、対象ファイルと編集方針を含む prompt、リポジトリ書き込みやモデル・推論・indexing の起動設定を確認するための入口。

## Read this when
- `cmoc session join` の merge conflict marker 解消処理を変更または調査するとき。
- conflict 対象パスの解決、解消用 prompt、または AgentCallParameter の起動設定を確認するとき。

## Do not read this when
- 通常の `session join` 処理や、merge conflict 解消以外の prompt 構築を確認するとき。
- AgentCallParameter の共通定義や prompt の一般的な組み立て規則を確認するとき。

## hash
- 90d92477182050877451c189867d94dc41240dd0819a7efdf06d4de179c72c93

# `tui`

## Summary
- `cmoc tui` の起動パラメータ構築を担うディレクトリ。`launch_tui.py` を入口として、オリジナルプロンプトを組み込んだ完全プロンプト、リポジトリ作業ディレクトリ、書き込み権限、モデル・推論設定、インデックス前処理を確認できる。

## Read this when
- `cmoc tui` の TUI 起動設定や起動時プロンプトを調査・変更するとき。
- TUI 用 agent call の作業ディレクトリ、ファイルアクセスモード、モデル・推論強度、ルーティングおよび oracle/realization ポリシーの組み込みを確認するとき。

## Do not read this when
- 完全プロンプトの共通生成規則だけを調査するときは、`build_complete_prompt` の定義を直接読む。
- プロンプトの構造化ドキュメント表現だけを調査するときは、`SDTagBlock`、`SDHeader`、`render_sd_node_as_markdown` の定義を直接読む。
- agent call の基本パラメータ型や列挙値だけを調査するときは、`oracle.acp_builder.basic` を直接読む。
- エディタ入力のコメント除去や strip など、呼び出し側の前処理だけを調査するときは、該当する呼び出し側を直接読む。

## hash
- 2080d687222ab435ae8739a793214b23069feb1fe4d66cd5aa57ad00ddec77c8
