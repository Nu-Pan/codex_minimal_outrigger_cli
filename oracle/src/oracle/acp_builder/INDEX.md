# `apply`

## Summary
- このディレクトリには、参照可能な正本ソース本文がない。正本ソースの有無を確認するための入口である。

## Read this when
- このディレクトリの内容や、参照可能な正本ソースの有無を確認するとき。

## Do not read this when
- 実装仕様や処理内容を確認したいとき。

## hash
- 0af302f7be7ef5db5b5b3790733cdc5b9d23e3de43be05b57a4287af7ea9be0d

# `basic.py`

## Summary
- AI コーディングエージェント呼び出し用の論理パラメータを定義する oracle src。モデルクラス、推論強度、ファイルアクセスモードの列挙と、プロンプト・cwd・Structured Output 設定・indexing preflight 指定をまとめる不変データ構造を扱う。

## Read this when
- Agent call のパラメータ項目、モデル選択区分、推論強度、ファイルアクセスモード、indexing preflight の既定動作を確認するとき。
- Agent call parameter を生成・検証する実装の正本定義を確認するとき。

## Do not read this when
- 具体的な agent call builder の生成ロジックや prompt 構築規則を確認したいとき。
- Codex CLI sandbox や permission profile の詳細なアクセス規則を確認したいとき。

## hash
- 1c637587b1fc7c500c21c3ac412fbb9d47bb80714478ba0421882b003f8a53d8

# `feedback`

## Summary
- feedback observation を既存 issue へ統合するか新規 issue とするかを判断する、正規化処理の oracle src と JSON Schema を扱うディレクトリ。正規化結果の契約確認には schema、agent call の prompt・参照範囲・設定確認には実装へ進む入口となる。

## Read this when
- feedback observation の issue 正規化処理、統合判断、入出力契約を確認・変更するとき
- 正規化結果の必須項目、列挙値、文字数制約、関連 issue ID の扱いを確認するとき
- feedback 正規化 agent call の参照範囲、入力形式、モデル・推論設定、Structured Output 制約を確認するとき

## Do not read this when
- feedback observation の収集・送信だけを扱うとき
- feedback issue の保存形式や human disposition の運用を確認するとき
- 正規化処理の具体的なテスト内容だけを確認するとき
- 一般的な prompt 構築や別の agent call parameter の実装を確認するとき

## hash
- 11ff759448ed5a50db841a7ec879e9b5ecf5d802515d6f431820c0cacfb81167

# `indexing`

## Summary
- `cmoc indexing` における INDEX.md エントリー生成用の agent call パラメータを構築する実装を収める。対象内容を含む prompt、読み取り専用アクセス、モデル・推論設定、Structured Output schema の参照、実行コンテキストを定義する。
- indexing 用の prompt 構築と agent call 設定を確認する際の入口であり、出力形式の詳細は同階層の schema 定義から確認できる。

## Read this when
- `cmoc indexing` の INDEX.md エントリー生成 prompt を変更・調査するとき。
- indexing 用 agent call のモデル、推論強度、ファイルアクセス権限、実行コンテキスト、Structured Output schema の指定元を確認するとき。

## Do not read this when
- 実際の INDEX.md 生成処理や indexing サブコマンド全体の実行フローを調査するときは、呼び出し側や実行フローの対象を直接読む。
- Structured Output の JSON Schema 自体の定義だけを確認するときは、schema 定義を直接読む。
- 一般的な prompt 構築処理や indexing 以外の agent call 種別を調査するときは、共通 prompt 実装や該当する agent call の対象を直接読む。

## hash
- 1dd8a883f7a42a61b5eaa5537221aa9a875de4ea75f11bfb6003d148a04f9317

# `oracle`

## Summary
- oracle 向け ACP 呼び出しのサブコマンド別ビルダーを配置する領域です。oracle review の所見列挙・採否判定・統合・妥当性検証と、oracle investigation の調査起動設定を扱います。各実装の prompt、出力契約、起動条件を確認する入口です。

## Read this when
- oracle review の所見列挙、採否判定、重複・矛盾の統合、妥当性検証に関する ACP 呼び出し契約や prompt 構築を確認・変更するとき。
- oracle investigation の調査用 ACP 起動設定、調査 prompt、モデル、アクセスモード、作業ディレクトリを確認・変更するとき。
- この領域にある oracle 向け ACP builder の用途や呼び出し条件を確認するとき。

## Do not read this when
- oracle file の編集内容や realization 側の実装だけを確認する場合。
- サブコマンドに依存しない共通 prompt 構築ロジックを確認する場合は、共通 prompt builder を直接読むべきです。
- 個別のレビュー所見や、その根拠となる oracle 仕様を確認する場合は、該当する対象を直接読むべきです。

## hash
- fade59eb8c125fb938f45e5bb72de7fcdd5641c325e8dd5c21f992c851cc0173

# `realization`

## Summary
- `cmoc realization apply fork` の追従処理に向けた起動パラメータと codex exec 用プロンプトを構築する実装入口です。oracle file の差分、対象コミット範囲、linked worktree、実行モデル・推論設定・ファイルアクセス権限の対応を扱い、apply fork の prompt 構築を調べる際の入口になります。
- refactor fork の変更差分要約、およびファイル単位の実装レビュー・修正・検証に向けた AgentCallParameter と prompt を構築します。Structured Output の契約、変更 path、モデル・権限・作業ディレクトリ設定を扱い、refactor fork の prompt や出力契約を確認・変更する際の入口になります。

## Read this when
- `cmoc realization apply fork` の追従用 AgentCallParameter や codex exec prompt の構築方法を確認するとき
- apply fork で oracle file の差分、対象コミット範囲、linked worktree、実行条件がどのように prompt へ組み込まれるか調べるとき
- refactor fork の変更差分要約、ファイルレビュー、修正、検証の prompt または AgentCallParameter を確認・変更するとき
- refactor fork の Structured Output の項目や対応条件、モデル・権限・作業ディレクトリ設定を確認するとき

## Do not read this when
- `cmoc realization apply fork` 以外の prompt 構築を調べるときは、各用途に対応する prompt builder を直接確認してください
- 実際にレビューされる個別の oracle file や realization file の内容を調査するときは、対象ファイルを直接確認してください
- 通常の realization 実装・テストの挙動を確認するときは、対応する realization implementation または realization test を直接確認してください
- refactor fork を呼び出す上位の運用を調査するときは、上位の prompt builder を直接確認してください

## hash
- 0362bbd63b78a44f0eee34b5486855e6967264eff4548b0f49bc3d9a71957335

# `session`

## Summary
- `cmoc session join` の Git merge conflict marker 解消用 agent call パラメータを構築する実装を含む。競合対象ファイルの実パス解決、専用 prompt の生成、リポジトリ書き込み権限、最高品質のモデル・推論設定、事前 indexing 無効化をまとめて指定する下位実装への入口。

## Read this when
- `cmoc session join` の conflict marker 解消用 agent call 設定や prompt を変更・確認するとき。
- 競合対象パスの解決、モデル・推論設定、ファイルアクセス権限、agent call の作業ディレクトリ、実行前 indexing 設定を調査するとき。

## Do not read this when
- 通常の merge conflict 解消処理や Git 操作そのものを調査するとき。
- `session join` と無関係な prompt builder や agent call パラメータを調査するとき。

## hash
- 4052f74c94d2c7069dec6d6443a4de00cec4703a801960b6880c8b8fdedd9aec

# `tui`

## Summary
- `cmoc tui` の TUI 起動用 `AgentCallParameter` を構築する実装。オリジナルプロンプトから完全プロンプトを生成して保存し、リポジトリ書き込み権限、作業ディレクトリ、モデル、推論強度、インデックス事前処理などの起動条件を固定する。下位の起動処理を確認するための入口。

## Read this when
- `cmoc tui` の起動パラメータ、完全プロンプトの保存、エディタ入力の埋め込み、TUI 呼び出し時のモデル・推論強度・作業ディレクトリ・アクセスモードを確認または変更するとき。

## Do not read this when
- TUI 以外のサブコマンドや起動方式のパラメータを調べるとき。
- 完全プロンプトの共通構造やレンダリング仕様だけを調べるときは、プロンプト生成側の実装を直接読む。

## hash
- 9b2c3cf92ffd59d90024b24e9c1320332c4d1f24636b15d102c777df6ac56149
