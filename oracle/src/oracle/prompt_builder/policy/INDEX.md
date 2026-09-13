# `conflict_resolution.py`

## Summary
- session join の merge conflict 解消結果に適用する規定を構築する。conflict の両側と関連する oracle file の意図を保持し、両立不能な場合は未解消事項として報告するための instruction 文面への入口。

## Read this when
- session join の merge conflict 解消方針を確認・変更するとき
- conflict 解消結果に求める oracle file 優先の規定や、未解消事項の報告条件を確認するとき

## Do not read this when
- session join 全体の意味仕様や conflict 解消の優先順位を確認したいときは、まず正本仕様を読むべき場合
- conflict 解消の具体的な実装挙動や realization file 自体を調べるとき

## hash
- 939087b46316af049646fb574af9178fbd8b70bae62508db39c4ac9167c8d5a0

# `editor_input_handoff.py`

## Summary
- 明示的に選択された editor input handoff の規定文面を構築する定義。active な prompt editor input への完成済み content の handoff 条件、入力内容、結果報告、失敗時の対応を扱う。

## Read this when
- 人間から active target への handoff を明示的に要求され、target ID が提示された場合の editor input handoff 規定を確認するとき。
- editor work file への直接書き込み禁止や、handoff 失敗時の回答上の扱いを確認するとき。

## Do not read this when
- editor input handoff 以外の prompt 構築規定を確認する場合。
- handoff の実行結果そのものや、editor work file の内容を確認する場合。

## hash
- 603b78cf401b4dc637877b582e0fe330f35d6e00d63d626106a975615e455832

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
- realization file を扱う agent call 向けの instruction 文面を構築する関数。
- path context から placeholder 定義を取得し、realization policy の見出しと、oracle file を正本仕様断片として扱うための require・prohibit・allow 規定を組み立てる。
- realization policy の意味仕様自体は別の oracle file を参照する前提で、prompt builder における realization policy の生成入口となる。

## Read this when
- realization file を対象とする agent call の instruction 生成経路を確認したいとき。
- realization policy に含める placeholder 定義、見出し、要求・禁止・許可規定の構築元を調査または変更するとき。
- prompt builder の policy 構築処理から realization file 向け規定がどのように組み立てられるかを確認したいとき。

## Do not read this when
- realization file を扱わない agent call の policy 構築を確認するとき。
- realization file の意味仕様や判断基準そのものを確認したいときは、対象ファイルではなく doc/app_spec 側の oracle 仕様を直接読むべきである。
- policy 構築後の agent call 実行や、PlaceholderMap・SDHeader・SDPolicy の一般的な実装を確認したいときは、それぞれの定義元を直接読むべきである。

## hash
- f469ec0b2fb4ad1f8863fb6db277c5653d6cbf4b900fa85caa69e93541d61410

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
