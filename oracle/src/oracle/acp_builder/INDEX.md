# `basic.py`

## Summary
- AI コーディングエージェント呼び出しのパラメータ型と、ファイルアクセスモードを定義する。
- エージェント呼び出し種別、アクセスモード、prompt、Structured Output schema、実行 cwd、editor input MCP の有効化、indexing preflight の設定をまとめる入口。

## Read this when
- Agent Call Parameter の構造や生成・受け渡し項目を確認するとき
- cmoc の論理的なファイルアクセスモードの列挙を確認するとき
- agent call の editor input MCP または indexing preflight の設定を確認するとき

## Do not read this when
- 各ファイルアクセスモードの詳細な意味や Codex CLI sandbox への対応を確認したいときは、本文が参照する正本仕様を読む
- agent call の具体的な構築処理や file access policy の生成処理を確認したいとき
- Structured Output schema の機械的な受理条件を確認したいとき

## hash
- 23a9f8d92cc7f3453214b8f5042ba4a495fb3427ffa5434bb5113e25bed1200e

# `feedback`

## Summary
- feedback issue の同一性判断と remediation に関する agent call の入出力契約、および起動パラメータ定義への入口。

## Read this when
- feedback issue の正規化・同一性判断・remediation agent call の出力形式や起動条件を確認するとき
- 同一性判断用 schema、prompt 構築、remediation の安全な修正・検証条件を横断して確認するとき

## Do not read this when
- feedback observation の受付・送信や候補 issue の収集・絞り込みそのものを確認したいとき
- remediation 対象の realization 実装、oracle file、または同一性判断ロジックの本体を直接確認したいとき
- INDEX.md のルーティング情報だけを確認したいとき

## hash
- 4233d6d48e0e4c6bc63d9fdfbba2e91b914293377ca8a3d4812ec56c032d7723

# `indexing`

## Summary
- 対象ディレクトリは、INDEX.md 用エントリー生成 agent call に関する実装と、その出力形式を定義するスキーマを扱う。
- スキーマ定義は、要約・読む条件・読まなくてよい条件を必須の文字列配列として指定する。
- 実装は、対象パスや完全な読み取り専用 prompt、構造化出力スキーマ、agent の作業ディレクトリ、indexing preflight 設定を組み立てて呼び出しパラメータを返す。

## Read this when
- INDEX.md 用エントリー生成の仕組みを変更・追跡するとき。
- 生成 agent call の prompt 構成、対象パス解決、読み取り専用設定、構造化出力スキーマ、作業ディレクトリ、preflight 設定の関係を確認するとき。
- 生成結果の JSON 構造や必須項目、および指定された出力形式への適合を確認するとき。

## Do not read this when
- 対象ファイルやディレクトリそのものの実際の責務を調べるとき。
- INDEX.md のルーティング内容やエントリー生成用 prompt の規則を確認するとき。
- 一般的な prompt 完成処理や path context の実装だけを確認したいときは、対応する共通実装を直接読む。

## hash
- 4d4c2433d75dca8bbb16c25f34731f6b7bd567719a957176b6c409d81f98ffc8

# `oracle`

## Summary
- `cmoc oracle edit` の編集 agent call と、編集後の仕様削減 call の起動パラメータを構築する。
- `cmoc oracle investigation` の完全プロンプトと Codex CLI TUI 起動パラメータを構築し、ユーザー指示を読み取り専用の oracle 調査経路へ組み込む。
- 対象ディレクトリ本文が提示されていないレビュー用要素については、現時点で具体的な責務を判断できない。

## Read this when
- `cmoc oracle edit` の agent call 起動条件、prompt 構成、起動パラメータ、または編集後の仕様削減 call への責務分担を確認・変更するとき。
- `cmoc oracle investigation` の調査用完全プロンプト、ユーザー指示の埋め込み、TUI 起動時設定、読み取り専用アクセス、エディタ入力の引き継ぎ、またはインデックス事前処理を確認・変更するとき。
- レビュー用要素の本文が追加され、その担当範囲を確認するとき。

## Do not read this when
- oracle file の編集処理そのものや仕様削減の判断基準を確認するとき。
- oracle の調査結果や個別の oracle file の内容を確認するとき。
- session の join・競合解決、または `cmoc oracle edit` と `cmoc oracle investigation` 以外の agent call 起動処理を調べるとき。
- 本文が提示されていないレビュー用要素から、具体的なレビュー作業へ進むとき。

## hash
- 8e63542424c486e8830235fcf7d9e025f8593acfeac6bf392e77b95216cd07e6

# `quota_probe.py`

## Summary
- Codex CLI の利用可能性を確認する quota availability probe の prompt と agent call パラメータを構築する定義。
- 読み取り専用・短い単発応答・追加調査なしの probe 条件を設定し、再帰的な indexing preflight を無効化する。

## Read this when
- Codex CLI の quota 回復確認用 agent call の prompt、アクセスモード、起動条件を確認または変更するとき。
- quota probe が実行する最小限の確認内容や indexing preflight の扱いを確認するとき。

## Do not read this when
- 通常の quota 管理ロジックや利用量計算を調べるとき。
- 一般的な agent call パラメータや prompt 構築の仕様を確認する場合は、共通の builder 定義を直接読むとき。

## hash
- 1ac746647bce56257d4ec7e41e2b7113802e8e2926f32e10699b404067da3ad6

# `realization`

## Summary
- `apply` は、指定した commit 範囲の oracle file 変更を realization file に追従させる agent call の起動条件・権限・差分判定を確認する入口。
- `refactor` は、refactor fork の commit 差分の要約と、指定 realization file の調査・修正・検証を行う agent call の契約と実行条件を確認する入口。

## Read this when
- oracle file の commit 間変更を realization に反映する agent call の prompt、起動パラメータ、linked worktree、実行前 indexing、差分取得失敗時の扱いを確認するとき。
- refactor fork の差分要約、変更分類、レビュー対象の調査、realization の修正・検証、または各 agent call の出力契約を確認するとき。

## Do not read this when
- 実際の Git 差分取得、fork の実行、realization file の具体的な編集、または個別の変更内容・レビュー結果を調べるとき。
- 共通 prompt 構築、AgentCallParameter の一般仕様、oracle 要求・realization 実装そのもの、または構造化文書レンダリングを直接調査するとき。

## hash
- 31b82bb17ffbff96848c92cef4fdbb63127a7fd62e30023fe68f1a68d6bd01ad

# `session`

## Summary
- session join の merge conflict marker 解消に使うエージェント呼び出し定義。競合対象ファイルの実パス、編集権限、適用するポリシー、indexing preflight の扱いをまとめる。

## Read this when
- session join の競合解消で、対象ファイルの prompt への渡し方や、解消エージェントの実行条件を確認するとき。
- conflict 解消後にも oracle・realization などの規定を適用する呼び出し設定を確認するとき。

## Do not read this when
- 通常の merge 処理や session join 以外のサブコマンドにおけるエージェント呼び出し条件を確認するとき。
- 共通の prompt 構築規則や共通パラメータの定義を確認するとき。

## hash
- 458cbb17539bf5bea207315042fa9cc6c0cfdb291d43cc29b17d06e511cd52cc

# `tui`

## Summary
- `cmoc tui` の TUI 起動パラメータと、ユーザーのオリジナルプロンプトを埋め込んだ完全プロンプトを構築する入口。
- TUI 起動時のリポジトリ書き込み、作業ディレクトリ、エディター入力引き継ぎ、インデックス事前処理の設定を担う。

## Read this when
- `cmoc tui` の起動パラメータや起動時ポリシーを変更・調査するとき。
- オリジナルプロンプトを完全プロンプトへ組み込む処理を確認するとき。
- TUI 起動時の作業ディレクトリ、ファイルアクセスモード、エディター入力引き継ぎ、インデックス事前処理の設定を確認するとき。

## Do not read this when
- 完全プロンプトの共通構造や各種ポリシーの定義自体を変更・調査するときは、完全プロンプト構築側の定義を直接読む。
- TUI 以外の agent call の起動パラメータだけを変更・調査するとき。

## hash
- fc6c0e67b291d5ff02434b89c61162777dfc6ec518ce6add34859b818545ae13
