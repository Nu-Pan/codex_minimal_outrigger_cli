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
- feedback issue の同一性判定と remediation を担う agent call の入口をまとめた対象。normalize_issue は観測結果と既存候補の同一性判定、remediate_issue は issue の存在確認・安全な修正・検証・結果分類を扱う。
- 同一性判定と remediation の出力契約、およびそれぞれの agent call の prompt・起動条件・対象範囲を確認するための入口。

## Read this when
- feedback observation が既存 issue と同一か新規かを判定する agent call の入力範囲、出力契約、起動パラメータを確認するとき
- remediation agent call の結果分類、realization file への変更範囲、検証条件、変更 path を確認するとき
- 同一性判定または remediation の Structured Output schema の必須フィールドと制約を確認するとき

## Do not read this when
- feedback observation の受付・構造化・送信、候補 issue の絞り込み、issue の生成・保存を確認するとき
- issue の内容・原因・summary・impact・remediation を生成する処理を確認するとき
- realization file 自体の実装や oracle file の内容、remediation の診断・修正手順を直接確認するとき

## hash
- c440a1f2961e419b90e901094ecc23af576b8470688769c351b76a749cc1419f

# `indexing`

## Summary
- `cmoc indexing` の INDEX.md エントリー生成処理と、その agent 呼び出しパラメータを定義する。
- INDEX.md エントリー生成結果の構造化出力スキーマを提供する。

## Read this when
- `cmoc indexing` のエントリー生成 prompt、対象本文の受け渡し、読み取り専用アクセス、agent call の cwd、Structured Output schema、indexing preflight 設定を確認・変更するとき。
- 生成結果に必要な項目や各項目の意味を確認するとき。

## Do not read this when
- 既存の INDEX.md の内容やルーティング規則そのものを確認するとき。
- エントリー生成後の INDEX.md 更新処理を確認するとき。

## hash
- e7df757d8890e511c5fe65777856c0ab09d293389dcbeb7919be9ba89f1db21d

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
- `cmoc realization apply fork` の realization 追従用 AgentCallParameter を構築する定義。commit 範囲と oracle file の raw git diff を追従対象として、oracle file と realization file の齟齬調査・反映作業への入口を提供する。

## Read this when
- `cmoc realization apply fork` の Agent call に作業範囲、完了条件、realization 書き込み権限、linked worktree、indexing preflight を設定する方法を確認するとき。
- commit 範囲と oracle file の raw git diff を追従対象変更として prompt に渡し、関連する oracle file と realization file をリポジトリ全体から調査させる条件を確認するとき。

## Do not read this when
- 追従対象となる oracle file の具体的な差分や、個々の realization file への反映内容を確認するとき。
- 共通の complete prompt 生成処理、構造化文書ノード、AgentCallParameter の一般仕様を確認するとき。

## hash
- a079e82e8258d856af2171fdcb4a2ae0fd6b6e3b681d5536e23edd520f6da873

# `session`

## Summary
- `cmoc session join` における merge conflict marker 解消用のエージェント呼び出し構築への入口。対象パスを解決し、conflict 解消用 prompt と起動パラメータを組み立てる下位要素を扱う。

## Read this when
- `session join` の merge conflict marker 解消に使うエージェント呼び出しの構築方法を確認・変更するとき。
- conflict 対象パスの扱いや、解消用の prompt・アクセス制御・起動条件の構成を確認するとき。

## Do not read this when
- merge conflict marker の具体的な解消処理や対象ファイルの内容を確認したいときは、conflict 対象ファイルを直接読む。
- 一般的な prompt 構築、共通 policy、または通常の `session join` 処理フローを確認したいときは、それぞれのより直接的な対象を読む。

## hash
- 47fcb891c8fda65984122c35dcab51fc85ba90bb4e1a6226eb2390001fc220f2

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
