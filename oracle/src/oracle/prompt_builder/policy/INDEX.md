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
- oracle file を扱う agent call 向けの instruction 文面を構築する定義。`build_oracle_policy` は、oracle file の要件・禁止事項・許容事項・補足方針を `SDHeader` と `SDPolicy` としてまとめ、プレースホルダー map とともに返す。
- oracle と realization の基本要件、指示の優先順位、実装差の許容境界、goal・non-goal の可読性、関連 oracle file の参照、既存意味の維持、用語統一、定義済み事項と未定義事項の区別を oracle file の必須条件として扱う。
- realization file による仕様の逆算、一般論による仕様修正、未定義事項の断定、仕様矛盾や重複、誤記を禁じ、oracle file の問題調査時に限り実装上の制約を判断材料として許容する。oracle file は認知負荷を抑えた疎な仕様断片であるべきだと補足する。

## Read this when
- oracle file を扱う agent call 向けの policy 文面や構造を確認・変更するとき
- `build_oracle_policy` が生成する oracle file の必須条件、禁止事項、許容事項を確認するとき
- oracle と realization の関係、仕様断片の未定義範囲、実装差の許容境界をプロンプトへ反映するとき

## Do not read this when
- oracle file の具体的な仕様内容や個別の開発ルールを確認する場合は、対象となる oracle file を直接読むとよい
- prompt builder の一般的なプレースホルダー処理や `SDHeader`・`SDPolicy` の実装を確認するだけの場合は、対応する定義ファイルを直接読むとよい

## hash
- 42688aed3b7d0513ce6e25e9d2028ef5111b209e4b42d9f9fba8bbbd6a3762dc

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
- realization file を扱う agent call 向けの instruction 文面を構築する。パス文脈からプレースホルダー定義を取得し、realization file の責務・要求・禁止事項・許容事項を構造化した policy header として返す。
- realization file に関する作業方針や agent call のプロンプト生成規則を確認したい場合の入口であり、具体的な oracle と realization の判断基準そのものは参照先の仕様を確認する。

## Read this when
- realization file を対象とする agent call の instruction 内容を変更・検討するとき
- realization file に適用する要求、禁止事項、許容される実装範囲を prompt policy として構築するとき
- パス文脈由来のプレースホルダー定義と、構造化文書の policy header を組み合わせる処理を確認するとき

## Do not read this when
- realization file の具体的な実装やテスト内容を確認したいとき
- oracle と realization の判断基準そのものを確認したいときは、本文中で指定された関連仕様を直接読む
- realization file 以外の agent call 向け instruction を構築する場合

## hash
- c32816ad468392a8d41ad064ec9dc797dbae4ca74284c6576bfa289e96cbeb57

# `realization_findings.py`

## Summary
- realization file に対する所見が満たすべき規定を定義するポリシー構築関数。所見の根拠、修正対象となる不整合・致命的問題、一貫した適用基準を示し、oracle file 自体の問題や必須でない事項、既に解消済みの問題を対象外とする。

## Read this when
- realization file の oracle file への適合性を調査・レビューするとき
- realization file に対する所見の作成規定や、修正対象・対象外の判断基準を確認するとき

## Do not read this when
- oracle file の仕様そのものを定義・レビューするとき
- realization file の実装内容を直接確認するとき
- 所見ポリシー以外のプロンプト構築規定を確認するとき

## hash
- 053b9a74fc9b62a0ead9ba0b3a8a8a4347ff72a1da1f0eb36400943105ae4847

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
