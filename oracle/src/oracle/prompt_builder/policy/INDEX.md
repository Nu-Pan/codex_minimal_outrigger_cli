# `conflict_resolution.py`

## Summary
- session join で merge conflict を解消する結果が満たすべき規定を定義する instruction 文面の構築入口
- conflict の両側と関連する oracle file の確認、両 branch の意図・挙動の保持、人間による選択が必要な場合の未解消報告、および解消に伴う編集判断を扱う

## Read this when
- session join の merge conflict 解消方針や、その結果を完了扱いにする条件を確認・変更するとき
- conflict 解消用の instruction 文面を構築する責務の所在を確認するとき

## Do not read this when
- session join の意味仕様そのものや oracle file 規定と conflict 解消の優先順位を確認するとき
- conflict 解消以外の prompt policy、または具体的な conflict の個別判断を直接確認するとき

## hash
- 2e420cbd70c8ef4ee3cc3c0a0f0e12c4051faf31e4f861e3b61286f0ba351c56

# `editor_input_handoff.py`

## Summary
- `build_editor_input_handoff_policy` は、明示的に選択された editor input handoff 規定を構築する関数です。
- active target への handoff 条件、tool 引数への情報分離、oracle 参照、結果報告、禁止事項を `SDHeader` と `SDPolicy` として定義します。

## Read this when
- editor input handoff の要求条件・引き渡す情報・禁止事項を確認するとき。
- prompt builder が handoff 規定をどのような構造で生成するか確認するとき。

## Do not read this when
- handoff の意味仕様そのものを確認したいとき。doc の「agent の責務と権限」を直接読むべきです。
- prompt builder の別の policy や、editor work file の実装を確認したいとき。

## hash
- 2e8a6979680b6eb147b94752fc3dfe4a711bb817c1a104f35a7ddb302fd212aa

# `feedback_reporting.py`

## Summary
- 対象は、全 agent call に共通する feedback observation 報告規定の構築処理であり、報告の必須条件、具体的根拠の基準、禁止事項、後続処理との関係を定義する。
- feedback observation の報告ポリシーを変更・確認するとき、または agent call 共通のプロンプト規定への入口を探すときに読む。

## Read this when
- feedback observation の問題報告要件や禁止事項を変更・確認する場合
- 全 agent call に共通する報告規定がどこで構築されるかを調べる場合
- 報告ポリシーを prompt builder の出力へ組み込む処理を追跡する場合

## Do not read this when
- feedback observation の意味仕様そのものを確認する場合は、参照先の報告基準文書を直接読む
- AgentCallPathContext や SDPolicy などの型・構造定義だけを確認する場合は、それぞれの定義元を直接読む
- 対象と無関係な agent call のプロンプト構築や別のポリシーを調べる場合

## hash
- 203fbeb6ca169491ad48cfd61c5d95aeff6128d33632b7b0d70e95f9e3ddf1c5

# `file_access.py`

## Summary
- FileAccessMode ごとの共通ファイルアクセス制限文面を構築する定義。各モードの deny list と、MCP・Structured Output 経由の書き込み例外をプロンプトへ反映する入口。

## Read this when
- FileAccessMode に応じた agent 向け file R/W policy の生成規則を確認・変更するとき
- 共通の禁止対象、oracle/realization file のモード別制限、または外部ツールによる書き込み例外の扱いを確認するとき

## Do not read this when
- ファイルアクセス制限の意味仕様そのものを確認するときは、参照先として示される正本仕様を直接読むとき
- 特定の agent prompt 全体の構成や FileAccessMode の定義自体を確認するとき

## hash
- 2024227edecd081482ba2bc22f0eace6067cc3c7a3d4df39292d91c4f77837ad

# `index_entry.py`

## Summary
- INDEX.mdエントリー生成時のルーティング情報に、対象を読むべき作業・質問・変更の条件と、この対象が担う責務を示すための規定を定義する。
- 対象内容を根拠に、過度な詳細や推測を避けつつ、対象へ進むべき境界と進まなくてよい境界を判断できるようにする。

## Read this when
- INDEX.md用エントリーを生成・改訂するとき
- 対象の責務、読むべき条件、または同階層の別対象との境界を整理するとき

## Do not read this when
- INDEX.mdエントリー以外の一般的な文書編集を行うとき
- Structured Outputの出力項目や型だけを確認したいとき
- 対象ファイルの実装内容を直接調査・変更する必要があるとき

## hash
- 6bf595b53b34a59a30230606ab87ee397ff028ac5e22c6136c02e9d6c7a62baa

# `oracle.py`

## Summary
- oracle file を扱う agent call 向け instruction 文面の構築定義。oracle の正本責務・委譲関係・優先順位と、仕様断片の作成・修正時に守るべき境界を agent 向け規定として組み立てる。

## Read this when
- oracle file を扱う agent call の指示文面、正本仕様と実装詳細の責務分担、oracle file 間の優先関係を確認するとき。
- oracle file に記述できる実装差の許容範囲、goal・non-goal、未定義事項の扱い、関連 oracle file の参照方法を判断するとき。

## Do not read this when
- oracle file の具体的な意味仕様そのものを確認したいときは、指定された oracle doc を直接読む。
- oracle src が所有する正確な詳細や実装内容だけを確認したいときは、その委譲先の oracle src を直接読む。
- realization file の内容や実装のみを確認し、oracle の作成・修正規定を必要としないとき。

## hash
- 4e4de41de95647dfcd55ce5e4287127cd05c7c08f0e5a399c7ba06cf9b39419d

# `realization.py`

## Summary
- realization file を扱う agent call 向け instruction 文面を構築する入口。oracle file を正本仕様断片として扱い、既存実装の活用、最小限の補完、不要な実装整理、検証・テストの扱いに関する realization policy を定義する。

## Read this when
- realization file の変更・追加・整理に伴い、agent call に渡す作業規定の構築内容を確認したいとき
- oracle file と realization file の関係、実装者の裁量範囲、YAGNI、既存実装の活用、検証要件を含む方針の入口を探しているとき

## Do not read this when
- realization file 自体の具体的な実装内容や、個別の oracle file の正本仕様を確認したいとき
- agent call の基本的な instruction 構築や realization file 以外の policy を確認したいときは、該当する prompt builder の定義へ直接進むべき

## hash
- 36a10fbf5477337cdb240ee63c42952b7161f28c1d08a218325c8afe3881f510

# `realization_findings.py`

## Summary
- oracle file と realization file の適合性を判断する agent 向けに、所見の適用ポリシーを構築する。所見の根拠、修正対象となる不整合・致命的問題、適用基準の一貫性を定義する。
- realization file に対する所見の規定を生成する入口であり、oracle と realization の適合性調査用プロンプトを組み立てる処理へ進む起点となる。

## Read this when
- oracle file と realization file の具体的な記述・挙動に基づいて適合性の所見を作成するとき。
- 明確な要求と挙動の不整合、または realization file 上の明確な致命的問題を修正対象として扱う基準を確認するとき。
- 所見の適用基準を一貫させる必要があるとき。

## Do not read this when
- oracle file 自体の仕様不足や定義上の問題を検討するときは、このポリシーではなく oracle file の仕様定義を直接読む。
- 規定上必須でない事項の改善提案や、調査開始時点ですでに解消された問題の確認だけを行うとき。
- oracle と realization の適合性ではなく、別の prompt builder policy の責務を調べるときは、該当する policy ファイルを直接読む。

## hash
- b531825f8f44927871a9b987eb21d9d6aef981e1207d9d654edfe6030b464f3e

# `routing.py`

## Summary
- INDEX.md による routing 規定文面を構築する関数。作業対象に近い INDEX.md を起点に、必要なファイルやディレクトリを特定するためのプロンプト定義への入口。

## Read this when
- INDEX.md を使った文書 routing の規定文面を変更・確認するとき
- 作業対象の階層や root placeholder を routing policy に組み込む必要があるとき
- INDEX.md の位置づけや本文優先の方針をプロンプトへ反映する処理を調べるとき

## Do not read this when
- INDEX.md の実際の配置内容や個別ファイルの責務を確認したいとき
- routing policy の意味仕様そのものを確認したいときは、先に指定された index routing の正本仕様を読むべき場合
- INDEX.md を使わないプロンプト文面や、別の policy header の構築だけを扱うとき

## hash
- dcaa865be45b4a4daf2a6c19e7e4706655ea8fd54e91ff1dff23acc0577c7118
