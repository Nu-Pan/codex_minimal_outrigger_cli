# `conflict_resolution.py`

## Summary
- session join で merge conflict を解消する agent call 用の規定を構築する定義。
- 両マージ元ブランチの oracle file の両立する意図・挙動を保持し、両立不能な場合は一方を推測で破棄せず未解消事項として報告する方針を扱う。
- realization file の都合による oracle file の意味変更と、conflict marker 解消に不要な変更を禁止する。

## Read this when
- session join の conflict marker 解消に用いる規定、またはその prompt policy の責務を確認するとき。
- 両 branch の oracle file の意味を保持する conflict 解消方針の入口を探すとき。

## Do not read this when
- session join コマンド全体の実行手順や merge 対象の仕様を確認したい場合は、session_join の仕様を直接読む。
- conflict 解消用 agent call の prompt part 選択や起動パラメータを確認したい場合は、session/join の conflict resolution parameter 定義を直接読む。
- realization file の実装や一般的な merge 処理を確認したい場合。

## hash
- 86b797de0ed040e404ca997830d4b0bd872a47496e6b3a3364029a8e57262e3d

# `feedback_reporting.py`

## Summary
- 全 agent call に共通する、人間向け feedback 報告規定を構築するポリシー実装。SDHeader と SDPolicy を使って、報告対象・必須手段・禁止事項を定義する。feedback 報告ポリシーのプロンプト構築処理を確認する際の入口となる。

## Read this when
- agent call 共通の human feedback reporting ポリシーを確認・変更するとき。
- feedback 報告ポリシーの SDHeader／SDPolicy 構成や、関連するプロンプト構築処理を確認するとき。

## Do not read this when
- feedback 報告の詳細な仕様を確認したいときは、本文が案内する feedback_observation.md を直接読む。
- PlaceholderMap や一般的なプロンプト構築の仕様だけを確認したいときは、該当する実装・仕様書へ直接進む。

## hash
- a32f521e78df82d76259454f98f6577ac82d94bf18bc486d60fef5421ef6195b

# `file_access.py`

## Summary
- cmoc エージェント向けのファイルアクセス制限ポリシー文面を、FileAccessMode と AgentCallPathContext に基づいて構築する。リポジトリ外、管理用ディレクトリ、AGENTS.md・INDEX.md、memo、oracle/realization file などの読み書き禁止範囲をモード別に定義し、PlaceholderMap と SDHeader を返す。アクセス規定の生成ロジックやモード別の制約を確認・変更するときの入口である。

## Read this when
- エージェント呼び出し時のファイルアクセス規定がどのように生成されるか確認するとき
- FileAccessMode ごとの禁止範囲、oracle file・realization file の扱い、パスプレースホルダーの定義を変更するとき
- NO_POLICY を含むアクセス制約ポリシーの構築結果を調査するとき

## Do not read this when
- アクセス制約そのものではなく、実際の CLI 実装やプロンプト全体の組み立てを確認したいとき
- ファイルアクセス規定を利用する側の処理だけを調査し、生成ルールの変更や確認が不要なとき

## hash
- 4fcdfb27bf7b640d7684ad9a3d0b11c0d53bf7e02140f50696a1500c6902590b

# `index_entry.py`

## Summary
- INDEX.md エントリーを生成する agent 向けの構築定義。ルーティング情報に含めるべき判断材料と、避けるべき記述を SDPolicy として定める。INDEX.md のエントリー生成方針を組み立てる処理の入口である。

## Read this when
- INDEX.md エントリー生成用のプロンプト方針を確認・変更するとき。
- ルーティング情報に記載する責務、読む条件、境界、禁止事項の定義を確認するとき。

## Do not read this when
- 個別の対象を案内する既存 INDEX.md エントリーを確認するとき。
- INDEX.md エントリー生成方針の根拠となる関連仕様を直接確認するとき。

## hash
- d1308402ec3ede69802fd23f408bc77c7ecb7e3723d5bac8cbc5cb67319a2a92

# `oracle.py`

## Summary
- oracle file を扱う agent call 向けの instruction 文面を構築する定義。
- oracle file と realization file の役割境界、仕様断片の goal・non-goal、実装差の許容範囲、関連 oracle file の参照要件などを SDPolicy としてまとめる。
- oracle policy の構築入口であり、oracle file の規定を変更・確認する作業ではこの定義から確認する。

## Read this when
- oracle file の規定を構築または変更するとき。
- oracle と realization の要件、指示の優先順位、実装差の許容境界、goal・non-goal の記述方針を確認するとき。
- oracle file 間の参照、仕様断片の疎性、定義済み事項と未定義事項の区別を確認するとき。

## Do not read this when
- oracle file の個別仕様本文を確認したいときは、直接対象の oracle file を読む。
- realization の実装配置や具体的な実行時挙動を確認したいとき。
- oracle policy と無関係な prompt builder の機能を確認したいとき。

## hash
- ea7cfac6f60ac401fa398b8bbbc0912c123cd42cb31225044a8809309b2de5c4

# `oracle_findings.py`

## Summary
- oracle file に対する所見の判定基準を共通化して構築する関数。所見の根拠、fatal/minor の分類条件、禁止事項を SDPolicy として定義し、レビュー手順から利用できる oracle findings policy の入口となる。

## Read this when
- oracle file や realization file に対するレビュー所見の妥当性・重大度・根拠の規定を確認または変更するとき
- レビュー各ステップで共通利用する所見ポリシーの構築箇所を確認するとき

## Do not read this when
- oracle_review のレビュー手順そのものを確認する場合
- 所見ポリシーの具体的な適用結果や個別の oracle file の内容を確認する場合

## hash
- 529216e264dd19deae04126b0d7f25a8ff38ecdb287567894a13bbd598b32744

# `realization.py`

## Summary
- realization file を扱う agent call 向けの instruction 文面を構築する。パス由来の placeholder 定義と、realization file の実装方針を示す SDHeader を返す。
- oracle file を正本仕様断片として扱うこと、仕様の補完範囲、関連 oracle file の確認、既存実装の優先、YAGNI、重複整理、検証要件などの realization policy を定義する。
- realization file 側で禁止される仕様複製・oracle file の変更・不要実装の残存・根拠のない複雑化などを明示し、必要な場合に限り最小限の同等実装を許可する。
- realization policy の関連仕様として misc_spec を参照するため、realization file 向け agent call の規定や prompt policy を確認・変更するときの入口となる。

## Read this when
- realization file を対象とする agent call の instruction policy を確認・変更するとき。
- oracle file と realization file の責務境界、実装方針、禁止事項、検証要件を prompt に反映するとき。
- realization policy の placeholder 定義や構造化された prompt header の構築方法を調べるとき。

## Do not read this when
- realization file 自体の具体的な実装内容やテストを確認する場合は、対象の realization file または対応する test を直接読む。
- realization に関する正本仕様の内容を確認する場合は、本文が参照する misc_spec などの oracle file を直接読む。
- agent call の一般的な prompt 構築や realization 以外の policy を扱う場合は、対応する prompt_builder の対象ファイルを読む。

## hash
- f201c872904970a3af61a8aaeabb6ccb29585aa7655c3948efa80834297268d4

# `realization_findings.py`

## Summary
- realization file に対する所見の判定基準を構築する関数を定義する。所見は oracle file と realization file の具体的な記述・挙動を根拠とし、明確な仕様不整合または realization file 上の致命的問題を修正対象とする一方、oracle file 自体の問題や必須でない事項は対象外とする。
- 返却内容は、所見方針を表す空のプレースホルダーマップと、要求事項・禁止事項を含む構造化されたポリシーヘッダーである。関連する仕様確認や所見判定の入口として利用する。

## Read this when
- oracle file と realization file の適合性を判定する際の所見基準を確認したいとき
- 明確な仕様不整合や realization file の致命的問題を修正対象とするか判断するとき
- 所見に適用する要求事項・禁止事項を構築または変更するとき

## Do not read this when
- realization file の実装内容そのものを調査するときは、対象の realization file を直接読む
- oracle file の仕様定義や関連仕様の内容を確認するときは、該当する oracle file を直接読む
- 所見判定やポリシー構築と無関係な prompt builder の処理を調査するとき

## hash
- 11923872158d5007ae726acea0ff9ebd0449c723eb5a6f7dc67cb3e67207393b

# `routing.py`

## Summary
- 作業対象に近い文書へ INDEX.md から到達するための routing policy を構築する実装です。パス文脈から work-root を解決し、プレースホルダー定義と SDHeader/SDPolicy の組を返します。

## Read this when
- INDEX.md の routing 規定の文面や構築処理を確認・変更するとき
- AgentCallPathContext から work-root を取得し、routing policy を組み立てる処理を確認するとき

## Do not read this when
- PlaceholderMap、SDHeader、SDPolicy、AgentCallPathContext 自体の定義を確認するとき
- routing policy 以外の prompt_builder 処理を確認するとき

## hash
- ad13498f719a62e6463d66bb9994aa662fbc3f787238b0a5e7ac01092efb3cf2
