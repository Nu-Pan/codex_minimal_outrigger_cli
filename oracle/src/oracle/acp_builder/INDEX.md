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
- feedback issue の同一性判断と verification を行う agent call の出力契約・実装をまとめた入口。normalize_issue は observation と既存候補の同一性判定、verify_issue は report cut 時点の参照に基づく候補検証を担う。

## Read this when
- feedback issue を既存候補と同一か新規か判定する出力形式または prompt・起動パラメータを確認するとき
- issue candidate の現在状態を検証する出力形式、verdict、evidence、人間対応または理由の契約を確認するとき
- 同一性判定や検証の入力範囲、候補・参照 ID の制約を確認するとき

## Do not read this when
- feedback issue の内容、候補生成、候補絞り込み、report cut reference の作成など、判定前のデータ準備を確認したいとき
- summary、impact、原因、actionability、relation など issue の詳細評価を確認したいとき
- raw log、過去の Codex session、feedback state、候補外 issue の探索を行いたいとき
- normalize_issue または verify_issue 以外の agent call の出力契約を確認したいとき

## hash
- 673ee6efa708d1d4917d73695b4218a703ae4d931b53baaac092e1d5e10f9447

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
- oracle 編集では、ユーザー指示を oracle file へ反映する本命 call と、反映後の仕様を簡素化する削減 call の prompt・アクセス制約・起動条件を構築する。
- oracle 調査では、ユーザー指示を埋め込んだ完全 prompt と、oracle file の読み取り専用調査および TUI 起動条件を構築する。
- oracle review では、所見の列挙、妥当性の擁護・反証、採否判定、重複・矛盾の統合に用いる prompt・Structured Output 契約・起動条件を扱う。

## Read this when
- oracle の編集 call が変更対象、ユーザー指示、仕様削減、読み書き制約をどう扱うか確認するとき。
- oracle の調査 call が調査範囲、根拠とする oracle file、読み取り専用アクセス、TUI への入力引き継ぎをどう構成するか確認するとき。
- oracle review で新規所見を列挙する、所見の妥当性を支持または反証する、採否を判定する、または重複・矛盾を編集操作へ整理する条件を確認するとき。

## Do not read this when
- oracle file の編集処理そのもの、仕様削減の判断基準、調査結果、または個別所見の具体的な妥当性を確認するとき。
- session の join・競合解決や、oracle 以外の agent call の起動処理を確認するとき。
- 所見の保存・表示・判定結果の適用処理、または共通の prompt・agent call 基盤の責務だけを確認するとき。

## hash
- 53464cf52b33ca194a1d59f8100c9adca3c6bfcee1f71cee0be0fdecaef02f0d

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
- `cmoc tui` のTUI起動用パラメータと、オリジナルプロンプトを埋め込んだ完全プロンプトを構築する入口。
- 作業コンテキスト、書き込み権限、oracle・realization・routing規則、エディタ入力引き継ぎ、インデックス事前処理を起動設定へ反映する。

## Read this when
- `cmoc tui` の起動パラメータやagent call設定を変更・調査するとき。
- オリジナルプロンプトから完全プロンプトを構築する経路を確認するとき。
- TUI起動時の作業ディレクトリ、ファイルアクセスモード、エディタ入力引き継ぎ、インデックス事前処理を確認するとき。

## Do not read this when
- 完全プロンプトの一般的なレンダリング規則だけを確認したいとき。
- agent callパラメータの型やアクセスモードの基本定義だけを確認したいとき。

## hash
- 5c3a5e4bd169fa627acf9e0690c04d3dbacfbe37d6374016beda4e22a1909c83
