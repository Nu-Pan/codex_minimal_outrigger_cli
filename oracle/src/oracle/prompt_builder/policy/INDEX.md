# `conflict_resolution.py`

## Summary
- session join の merge conflict 解消時に埋め込む専用 instruction 文面を構築する関数を定義する。両方の oracle file の意図・挙動を保ち、両立不能時は未解消事項として報告する規定と、oracle の意味変更や不要変更を禁じる規定を返す。
- session join の conflict 解消ポリシーの責務・適用条件を確認するときに読む。
- 通常の edit、review、refactor 用 policy の内容を確認するだけなら、この対象ではなく各専用 policy の定義を直接読む。

## Read this when
- session join の merge conflict 解消処理が従うべき instruction 文面を確認・変更するとき
- conflict resolution policy の require / prohibit の構築元を特定するとき

## Do not read this when
- session join のドメイン上の意味や挙動を確認する場合は、正本である app_spec の session_join 仕様を直接読む
- edit、review、refactor policy の規定を確認する場合は、それぞれの専用 policy 定義を直接読む

## hash
- 9afdb49dfba340bc80e8bb98bb4c8473f30d60230639edd59f433a404e282da6

# `feedback_reporting.py`

## Summary
- 対象は、全 agent call に共通する人間向け feedback 報告規定を、固定の SDHeader/SDPolicy として構築する関数を定義するポリシー実装です。問題を人間へ報告する際の必須手段と、報告してはならない条件を prompt に組み込む責務を担います。
- 全 call 共通の feedback reporting policy の生成・配置を変更または確認するときに、この対象を入口として読みます。

## Read this when
- 全 agent call に共通する人間向け問題報告ポリシーの構築、文言、必須事項、禁止事項を変更・確認するとき。
- complete prompt に feedback 報告規定を組み込む経路を調査し、固定のポリシー構造を確認するとき。

## Do not read this when
- feedback 観測の報告基準そのものの正本仕様を確認する場合は、対象本文ではなく oracle/doc/app_spec/feedback_observation.md を直接読みます。
- prompt 全体の生成処理や、AgentCallPathContext・PlaceholderMap などの型定義だけを確認する場合。

## hash
- bc6ec2cb81ddce92a750ff11eb9ddda019ad91d05fc40b64ff1ecf0b23d3a60b

# `file_access.py`

## Summary
- ファイルアクセスモードと呼び出し対象パスの文脈から、エージェント向けのファイル読み書き禁止規定とプレースホルダー定義を構築する。READONLY、PURE_ORACLE_READ、REPO_WRITE、PURE_ORACLE_WRITE、REALIZATION_WRITE、NO_POLICY の各モードに応じた制約文面の入口。

## Read this when
- エージェント呼び出し用のファイルアクセス規定を生成・変更・確認するとき
- ファイルアクセスモードごとの oracle file・realization file の読み書き制約を確認するとき
- repo-root と work-root の関係に応じた禁止パスやプレースホルダー定義の生成を確認するとき

## Do not read this when
- アクセス規定の正本である Codex 実行ルールや、実際の sandbox 設定を確認したいとき
- 個別の oracle file・realization file の内容や配置責務を確認したいとき
- 生成済みプロンプト全体の構成を確認したいときは、プロンプト構築側の対象を直接読む

## hash
- b546bfb326e651e4241d6e89a658e539cba8947a6a4ffb368b4de57d5bb04dce

# `index_entry.py`

## Summary
- INDEX.md 用エントリー生成 agent に渡す、専用の構築定義を提供する。
- エントリー作成時の必須条件と禁止事項を SDPolicy として保持し、SDHeader にまとめる。
- プロンプト置換用の PlaceholderMap は空で返す。

## Read this when
- INDEX.md 用エントリー生成のルーティング条件や禁止事項を構築する処理を変更するとき。
- エントリー生成用の SDHeader と SDPolicy の組み立て方を確認するとき。

## Do not read this when
- INDEX.md のインデックス処理全体や生成タイミングを確認するとき。
- SDHeader、SDPolicy、PlaceholderMap 自体の汎用仕様を確認するとき。
- 生成された INDEX.md エントリーの内容や既存インデックスを確認するとき。

## hash
- 8a03c969c0fddd70f602d897d56aadaacb4bf2693db6d083a0804bd2e7deddc2

# `oracle.py`

## Summary
- oracle file を扱う agent call 向けの instruction 文面を構築する関数を定義する。oracle policy の適用対象と、関連する指示の優先順位・仕様断片の扱いを agent call へ渡す入口である。

## Read this when
- oracle file 用の agent call に適用する共通 policy の構築方法を変更・調査するとき。
- oracle policy の instruction 文面を prompt builder に組み込む経路を確認するとき。

## Do not read this when
- domain 固有の判断基準や仕様内容を確認するときは、参照先の oracle 仕様を直接読む。
- realization の配置や CLI 実装の責務を確認するときは、対応する design rule または realization file を読む。
- oracle file そのものの個別仕様を確認するときは、この policy 構築定義ではなく対象の oracle file を直接読む。

## hash
- 781c6dc48af85816722155ca49dec32822685f4cf53afc735f7fc420262a6aa8

# `oracle_findings.py`

## Summary
- oracle file に対する所見の成立条件と分類基準を定義するポリシー。レビュー全段階で共有され、oracle file と realization file を根拠に所見の重大度を判定するための入口となる。
- 正本仕様間の明確な矛盾や実装者裁量で解決できない問題を fatal、仕様の意味を変えない表記上の問題や初歩的な文言上の問題を minor とする基準、および重複・根拠不足の所見を禁止する条件を扱う。

## Read this when
- oracle file や realization file に対する所見の成立条件・重大度分類を確認するとき。
- レビュー段階をまたいで共有される所見判定基準の一貫性を確認するとき。
- fatal または minor として報告できる問題の範囲、禁止される所見の根拠を確認するとき。

## Do not read this when
- 個別の oracle file または realization file の内容自体を確認することが目的のとき。
- oracle review の対象仕様や実装の適合性を直接確認する必要があるとき。
- 所見の分類ではなく、レビュー手順やレビュー対象の責務を確認するとき。

## hash
- 6a9a9380a1785ff645a98b4bc78b0b5e007fc66938b7135627d042ef80d77f6a

# `realization.py`

## Summary
- realization file を扱う agent call 向けの instruction 文面を構築する関数を定義する。呼び出し元のパス文脈から placeholder 定義を取得し、realization policy の要求・禁止・許可事項を SDHeader/SDPolicy として返す。
- oracle file を正本仕様として扱い、関連仕様との整合、既存実装の活用、必要最小限の実装、重複整理、検証可能性を realization file に求めるポリシーを保持する。

## Read this when
- realization file に対する agent call の instruction や policy の構築を変更・確認するとき
- realization policy の要求事項、禁止事項、許可される実装範囲を確認するとき
- AgentCallPathContext 由来の placeholder 定義と SDHeader/SDPolicy の組み立てを確認するとき

## Do not read this when
- oracle の正本仕様そのものを確認したいとき
- realization file の具体的な実装内容やテストを確認したいとき
- 一般的な prompt builder の共通処理を確認したいときは、該当する共通実装を直接読む

## hash
- 5a825613b34f35f839b64fb48c2d1c7670c4bd87b2f3bb5928dc7773c41d7e6c

# `realization_findings.py`

## Summary
- oracle file と realization file の不整合や realization file 上の明確な致命的問題を、所見として修正対象にするための適用基準を定義する。所見の根拠を両ファイルの具体的記述・挙動に限定し、基準の一貫性を求める。realization findings に関するポリシー構築の入口となる。

## Read this when
- oracle file と realization file の適合性を評価する所見ポリシーを確認・変更するとき
- realization の不整合や致命的問題を修正対象とする判定基準を確認するとき

## Do not read this when
- oracle file 自体の不足や未定義を検討するとき
- 個別の oracle file または realization file の内容・挙動そのものを直接確認するとき

## hash
- a3e4a305f704e4b3c220177b547eadf6b538fcdb5cdf4aa44996aeb2fc0a6715

# `routing.py`

## Summary
- 作業対象に近い階層の INDEX.md を起点に、{{work-root}} ツリー内で読むべきファイルやディレクトリを特定するための routing policy を構築する。対象領域を推定できない場合の root 起点、INDEX.md と本文が異なる場合の本文優先、INDEX.md を本文の代替にしない原則を、PlaceholderMap と SDHeader/SDPolicy の形で提供する。

## Read this when
- リポジトリ内で次に読むべきファイルやディレクトリを INDEX.md に基づいて判断する必要があるとき
- 作業対象に近い階層を起点とする routing policy の文面や構造を変更・確認するとき
- work-root の定義を call-scoped context から取得して routing 用 placeholder に渡す処理を確認するとき

## Do not read this when
- INDEX.md の具体的な意味要件やエントリー形式を確認したいときは、正本である oracle/doc/app_spec/indexing.md を直接読む
- 個別のファイルやディレクトリの責務・内容を確認したいときは、対応する本文または近い階層の INDEX.md を直接読む
- routing policy を使わない prompt builder の別のポリシーや、SDHeader・SDPolicy 自体の仕様を確認するとき

## hash
- a24ac521eab9fed233e643c8ab79085fc194429e7209bc09981368d73e982a35
