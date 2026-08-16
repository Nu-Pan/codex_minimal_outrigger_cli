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
- oracle 関連の agent call 起動定義を扱うディレクトリ。oracle の edit・investigation・review 各フローについて、起動パラメータ、prompt、読み取り制約、モデル設定、Structured Output などの個別定義へ進むための入口。

## Read this when
- oracle edit・investigation・review の agent call 起動条件や固定パラメータを確認・変更するとき
- oracle 用 prompt の構成、アクセス範囲、モデル・推論設定、作業ディレクトリ、Structured Output 設定を調査するとき
- レビュー所見の出力契約、妥当性検証、採否判定、統合に関する個別定義を確認するとき

## Do not read this when
- oracle file の内容や正本仕様そのものを確認・変更するとき
- realization 実装の責務や配置を確認するとき
- 通常の agent call 起動処理、共通設定、共通 prompt 生成規則を確認するとき
- 対象フローの具体的なファイルを直接確認できる場合

## hash
- 5da42aa4c7d53ae949fd20c1189d4b325e13fee9991030fb711251bfb3db6530

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
- realization apply fork と refactor fork の agent call 定義をまとめる入口です。apply fork は oracle file の変更を realization file 全体へ追従させる起動処理を扱い、refactor fork は変更差分の要約およびファイル単位のレビュー・修正を扱います。
- apply fork の起動 prompt、commit 範囲と raw git diff の埋め込み、run worktree、アクセス権限、各種 policy、モデル・推論設定を確認するときの入口です。
- refactor fork の変更要約では、差分分類の Structured Output schema と readonly の起動設定を扱います。ファイルレビュー・修正では、対象 path を起点とした調査、realization file の修正、検証、所見と変更 path の整合、および出力契約を扱います。
- apply fork の具体的な起動実装を確認する場合は apply 配下へ、refactor fork の変更要約またはファイルレビュー・修正を確認する場合は refactor 配下へ進みます。共通 prompt builder、共通 AgentCallParameter、個別の oracle・realization 実装やテストを調べる場合は、それぞれの定義元または対象ファイルを直接読みます。

## Read this when
- realization apply fork の追従 agent の prompt、作業範囲、完了条件、run worktree、起動パラメータを変更または確認するとき。
- oracle file の変更を realization file 全体へ反映する apply agent call と、commit 範囲・raw git diff の prompt 埋め込みを調査するとき。
- refactor fork の変更差分を構造化要約する agent call の prompt、実行設定、linked worktree、Structured Output schema を確認または変更するとき。
- refactor fork のファイル単位レビュー・修正における対象 path、調査範囲、修正権限、oracle・realization 参照方針、検証条件、所見出力契約を確認または変更するとき。

## Do not read this when
- apply fork 以外の apply 処理や、refactor fork 以外の agent call builder を調査するとき。
- 完全 prompt の共通生成規則を調査するときは、共通 prompt builder を直接読むとき。
- AgentCallParameter の共通データ構造や列挙値だけを調査するときは、基礎定義を直接読むとき。
- 実際の変更差分、個別の oracle file、realization implementation、realization test の仕様や挙動を確認するときは、該当する対象を直接読むとき。

## hash
- 523e8efe8df254f06c95c2d2ea22ec711701c1b186e6eea3b094fa475c0beb32

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
