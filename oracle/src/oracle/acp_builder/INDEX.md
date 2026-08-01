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
- AI コーディングエージェント呼び出しに必要なモデルクラス、推論強度、ファイルアクセスモード、プロンプト、Structured Output schema、作業ディレクトリ、索引事前処理フラグを定義する。ACP 関連の呼び出しパラメータや論理 enum の意味を確認する入口。

## Read this when
- ACP の呼び出しパラメータ構造を変更・利用するとき
- モデル選択、推論強度、ファイルアクセスモード、プロンプト、作業ディレクトリの表現を確認するとき
- agent call 前の indexing preflight 制御を確認するとき

## Do not read this when
- 実際のバックエンドモデル名への解決や Codex CLI の実行規則を確認したいとき
- ファイルアクセス規則の詳細や app specification を確認したいとき
- ACP パラメータ以外のビルダー実装や呼び出し処理を調べるとき

## hash
- d2680fbd43595b5fe00108bf30e2a6937ae8d68a22e6f8906e54e7766b7339f7

# `indexing`

## Summary
- INDEX.md エントリー生成用の正本実装と、その Structured Output schema を扱うディレクトリ。`cmoc indexing` が対象パスの本文からルーティング情報を生成するための prompt・agent call 設定の入口を含む。

## Read this when
- `cmoc indexing` の INDEX.md エントリー生成 prompt、Structured Output schema、対象パス解決、モデル・推論・アクセスモード設定を変更・調査するとき。

## Do not read this when
- INDEX.md の一般的なルーティング規則や記述方針だけを確認したいとき。
- `cmoc indexing` 以外の prompt 構築や agent call パラメータを調査するとき。

## hash
- 6114f70e885a1247cd290b3397cb56f6fc8c2691ee81127b8b2be381cf58a6cf

# `oracle`

## Summary
- `cmoc oracle` 系サブコマンド向けの agent call 構築実装を分類するディレクトリです。`edit` は oracle 編集 TUI の起動処理、`investigation` は調査用 TUI の prompt・起動パラメータ生成、`review` はレビュー所見処理の prompt builder と Structured Output schema を扱います。各サブディレクトリが担当機能の実装確認への入口です。

## Read this when
- `cmoc oracle` の edit、investigation、review のいずれかに関する agent call prompt、起動パラメータ、Structured Output schema、またはログ保存処理を調査・変更するとき。

## Do not read this when
- oracle の正本仕様やレビュー判定基準そのものを確認するとき。
- 共通の agent call 型・prompt 構築・実行設定、または各サブコマンドの具体的な実装を直接確認するとき。

## hash
- c8d881f5fe2278734de3aae15024a8150f4b5e966b64ccf8c9c3c4899152cc27

# `realization`

## Summary
- Oracle の変更を realization 全体へ反映する agent call の起動設定と、refactor fork の変更要約・レビュー・修正用 agent call パラメータを扱うディレクトリ。

## Read this when
- oracle の変更を realization implementation・test・ancillary へ反映する agent call の条件や prompt を変更するとき。
- refactor fork の変更要約、レビュー、修正に関する出力 schema や agent call パラメータを確認するとき。

## Do not read this when
- 通常の realization 実装やテストの内容を変更するとき。
- oracle の仕様、共通 prompt 構築処理、実際の realization code の挙動を調査するとき。
- 個別の Structured Output schema の定義や、レビュー・修正 agent call の実処理だけを確認するとき。

## hash
- ca27df97fb419a4c0b24a7336b3516490b74f2f0b5186c96d8c58788a3e9ad13

# `session`

## Summary
- `cmoc session join` の merge conflict marker 解消用 agent call 設定を扱う。対象ファイルの実パス解決、専用 prompt、リポジトリ書き込み権限、最高品質のモデル・推論設定、実行 cwd、indexing preflight 無効化を確認する入口。

## Read this when
- `session join` の conflict 解消 agent call における対象パス、prompt、ファイルアクセス権限、モデル、推論設定、cwd、preflight 設定を変更または調査するとき。

## Do not read this when
- 通常の `session join` 処理や merge 操作そのものを調査するとき。
- 共通の agent call パラメータ、prompt 生成、パス解決の仕様だけを調査するとき。

## hash
- bd3443e6c0860f9001070a192885b30f18fc92d0ba9e3b4540b7fd0aef225b01

# `tui`

## Summary
- TUI 起動の実行パラメータ解決と AgentCallParameter 構築に関する oracle src を扱うディレクトリ。起動用パラメータ、完全プロンプト、モデル・推論設定、アクセスモード、作業ディレクトリ、構造化出力判定スキーマを確認する入口。

## Read this when
- `cmoc tui` の起動処理や AgentCallParameter の設定を調査・変更するとき
- TUI 用プロンプトの構成、保存先、パスコンテキスト、実行条件を確認するとき
- AI Agent CLI/TUI の標準文書参照要否や入力スキーマを確認するとき

## Do not read this when
- TUI 以外のサブコマンドのプロンプト生成や AgentCallParameter を調査するとき
- TUI の呼び出し元、ユーザー入力受付、画面表示を調べるとき
- 構造化出力スキーマや共通プロンプト・パス解決仕様だけを確認するときは、対応する直接のファイルを読むとき

## hash
- 54a7d588fc2f8e0881d24e319e6dd6325e156e1f714e1b15aad41cb9364e8cd8
