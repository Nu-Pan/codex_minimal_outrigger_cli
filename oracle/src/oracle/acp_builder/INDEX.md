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
- 日本語技術文書のルーティング情報として、フィードバック issue の正規化・検証に関する prompt、agent call parameter、Structured Output 契約への入口を示すディレクトリです。
- 観測と既存 issue candidate の同一性判定、report cut 時点の evidence に基づく issue 状態検証を扱う対象へ進むための中間入口であり、個別の schema や実装の詳細は各対象を直接確認します。

## Read this when
- feedback issue の正規化または検証フローの prompt・agent call 設定・Structured Output 契約を確認するとき
- 観測を既存 issue と新規 issue のどちらとして扱うか、または issue candidate の現在状態を判定する処理の入口を探すとき

## Do not read this when
- issue の発見・保存・送信や候補の絞り込みなど、正規化・検証以外の feedback 処理だけを確認するとき
- 個別 schema のフィールド定義、個別 issue の内容、または一般的な JSON Schema の仕様を直接確認するとき

## hash
- 2a1c1e0a32408b4c81297fe9a1ffca49fd81799d343a2c6ec9a07d5ae0fffd8e

# `indexing`

## Summary
- `cmoc indexing` が対象本文から INDEX.md エントリーを生成するための agent call 構築と、その Structured Output schema を扱うディレクトリ。prompt、読み取り専用設定、モデル・推論設定、出力形式を確認する入口となる。

## Read this when
- `cmoc indexing` の index entry 生成処理について、prompt の構成、対象本文の埋め込み、path context、読み取り専用設定、モデル・推論設定を変更・確認するとき。
- 生成される INDEX.md エントリーの JSON schema、必須項目、出力制約を確認するとき。

## Do not read this when
- indexing サブコマンド全体の実行フローや agent call の起動処理を確認するときは、呼び出し側または agent 実行処理を直接読む。
- 目次対象となる個別ファイルやディレクトリの責務・ルーティング内容を判断するときは、対象本文とその対象側の INDEX.md を読む。
- INDEX.md エントリー生成とは無関係な agent call や prompt 構築を確認するとき。

## hash
- 12a6b41b525d92f82af506b3953916dcba6df7a401c93a2cb0cafb30d337361c

# `oracle`

## Summary
- `cmoc oracle` 配下の agent call 起動定義を扱う領域です。oracle file の編集・調査・レビューそれぞれについて、prompt、読み取り制約、モデルや推論設定、作業ディレクトリ、Structured Output、起動前処理などの実行パラメータを構築する入口です。

## Read this when
- `cmoc oracle edit` の起動条件、prompt 構成、仕様削減時の参照境界、アクセス範囲、モデル設定、作業ディレクトリ、索引事前処理を確認・変更するとき
- `cmoc oracle investigation` でユーザー指示を完全プロンプトへ組み込む方法や、oracle-only 読み取り制約、構造化出力、起動前処理を確認・変更するとき
- `cmoc oracle review` の所見列挙・妥当性検証・採否判定・統合に関する Structured Output schema と agent call builder の接続を確認・変更するとき

## Do not read this when
- realization 実装の責務や配置を確認するとき
- 個別の oracle file の内容や正本仕様そのものを確認・変更するとき
- 一般的な agent call 起動処理、共通設定、agent call パラメータ型の定義だけを確認するとき
- prompt の共通生成規則だけを確認するとき
- oracle review の実行制御、所見の永続化、レビュー結果の後処理だけを調査するとき
- 配下の具体的なファイルを直接確認でき、ディレクトリ全体の起動定義を読む必要がないとき

## hash
- b2a2991c70d7722f983ea45b4e4e1fd597749e55ecf673d712d5113bbaf99c15

# `quota_probe.py`

## Summary
- Codex CLI の quota 回復確認用 agent call を構築する定義。quota availability probe の prompt 文面、読み取り専用設定、モデル・推論 effort、agent call の作業ディレクトリ、構築時の実行オプションを確認する入口となる。

## Read this when
- quota availability probe の agent call の prompt や起動パラメータを変更・確認するとき
- quota 回復確認用 agent call がどのような実行設定で構築されるかを調べるとき

## Do not read this when
- quota availability probe の実行結果だけを確認したいとき
- 一般的な prompt 構築処理や他の agent call の設定を調べるときは、対応する構築定義を直接読む

## hash
- d51c05853344f75c4bd0785ecbf8cd6e568ab694affcdb993a99e6669ac21d41

# `realization`

## Summary
- `apply` は realization apply fork の AgentCallParameter を構築し、oracle diff の追従条件、prompt、worktree・権限・モデル設定、indexing preflight を確認する入口です。
- `refactor` は refactor fork の変更要約およびファイル単位レビュー・修正用の AgentCallParameter と Structured Output 契約を扱い、差分分類、対象範囲、参照・書込規則、検証条件を確認する入口です。

## Read this when
- realization apply fork の起動パラメータ、oracle diff の prompt 組み込み、実行環境や indexing preflight を確認・変更するとき。
- refactor fork の変更要約・レビュー・修正 agent call の prompt、差分入力、モデル・権限・検証条件、Structured Output 契約を確認・変更するとき。

## Do not read this when
- apply または refactor の realization 実装・テスト・補助ファイル自体を調査するとき。
- oracle の仕様や一般的な AgentCallParameter 定義を確認するとき。
- Structured Output のフィールド定義だけを確認する場合や、実際の refactor 差分・レビュー対象を調査する場合。

## hash
- d89c1deed2370a70e8d04b32040bf12f825a3fe36da973ee305418336dc5d30f

# `session`

## Summary
- `cmoc session join` における Git merge conflict 解消用 agent call の構築定義を扱うディレクトリ。競合対象の実体パス、解消専用 prompt、ファイルアクセス方針、モデル・推論設定、実行コンテキストを確認する入口であり、具体的な prompt と起動パラメータは下位の conflict 解消定義から確認する。

## Read this when
- `cmoc session join` の merge conflict 解消処理で、agent call の prompt、対象パスの渡し方、アクセス制約、モデル・推論設定、作業ディレクトリまたは事前 indexing の設定を変更・確認するとき

## Do not read this when
- session join の通常の結合処理や conflict 解消以外の prompt 構築を調べるとき
- 競合対象ファイルの内容、merge conflict の検出、Git 操作そのものを直接確認したいとき

## hash
- ad0c630057477ef04b29b5fbccd219a7b1ba59c4888d826f884b5894c93f64f5

# `tui`

## Summary
- `cmoc tui` サブコマンド用の AI Agent CLI/TUI 起動設定と完全プロンプト構築の入口。起動時の固定パラメータ、リポジトリ作業用のパス・権限、oracle/realization 方針、ルーティング情報を組み込む処理を確認するための対象。

## Read this when
- `cmoc tui` の起動パラメータ、モデル・推論設定、作業ディレクトリ、ファイルアクセス権限を変更または確認するとき。
- TUI 起動時に渡す完全プロンプトへ、構造化された補助情報やリポジトリ固有の作業方針を組み込む経路を追跡するとき。

## Do not read this when
- 完全プロンプトの共通生成ロジック自体を変更または確認する場合は、その生成処理の定義を先に読むとき。
- `cmoc tui` 以外のサブコマンドや、TUI 実行後の対話・エージェント処理を調べるとき。

## hash
- e7e8614b77341d81a60b8defc793c97d638f42e4130c62478ac28bee76bf078f
