# `apply_review_policy.py`

## Summary
- oracle file に対する realization file の追従要否、所見、修正を判断するためのポリシー群を構築する。oracle の権威、所見の根拠、修正対象、既に解消済みの扱いをまとめた判断の入口である。

## Read this when
- oracle file と realization file の適合性を確認し、追従要否や修正対象を判断するとき
- 適合性レビューで所見の根拠や、既に解消済みの問題の扱いを確認するとき

## Do not read this when
- oracle file の内容そのものや realization の実装を直接確認するとき
- 適合性レビュー以外のポリシー構築や一般的なプロンプト生成を調べるとき

## hash
- 76d59c19789a3f142a281c2ce5c51b525138b0270d45c540f931bf00a231ce93

# `common_policy.py`

## Summary
- 複数用途で共有する PolicyGroup の構成定義を担う。oracle・realization file の扱いに関する authority policy 群と、所見・修正対象の判断に関する finding basis policy 群を、共通利用可能なグループとして構成する。

## Read this when
- oracle・realization file を扱う作業で、oracle authority policy または reverse flow 禁止 policy をまとめて適用する入口を確認したいとき
- 所見や修正対象の判断で、finding basis policy を適用する PolicyGroup の構成を確認したいとき

## Do not read this when
- 個々の policy の具体的な規則や根拠を確認したいときは、参照されている policy 定義を直接読む
- PolicyGroup の型や一般的な構造を確認したいときは、PolicyGroup の定義を直接読む

## hash
- 750f753b1a644bdaa719660f3a83a2de532243bfed707f1a011260f6dfea5acd

# `conflict_resolution_policy.py`

## Summary
- `cmoc session join` で conflict marker を解消する際に適用する policy collection の構築定義。oracle / realization の意味を保つ共通権威ポリシーと、両ブランチを保持する conflict 解消ポリシーをまとめる。conflict 解消 instruction の選択・構成を確認する入口。

## Read this when
- `cmoc session join` の conflict 解消時に、適用される policy group や instruction の構成を確認・変更するとき。
- conflict 解消で両ブランチを保持する規定がどのように選択されるかを確認するとき。

## Do not read this when
- session join の conflict 解消以外の policy 定義を調べるとき。
- 個別の conflict 解消ポリシー本文を確認する場合は、直接そのポリシー定義を読むとき。

## hash
- dfb25321733ba824a259f636374abfcf9f3b154c66c579e65c139b0f2fde4ae5

# `editor_handoff_policy.py`

## Summary
- 日本語の技術文書として、対象が担う editor work file への handoff 規定の構築責務と、agent call から handoff する規定を確認・変更するときの入口を示す。
- 対象は policy group を組み立ててポリシーコレクションを返す実装であり、個別ポリシー本文やポリシー定義そのものを読む作業の直接の入口ではない。

## Read this when
- agent call から editor work file への handoff 規定を選択・構成する処理を確認または変更するとき。
- editor handoff 用の policy group の scope、識別子、含めるポリシーの組み立てを確認するとき。

## Do not read this when
- editor handoff の個別ポリシー内容だけを確認または変更するときは、対象の policy definition を直接読む。
- 一般的な prompt builder の構成や、editor work file 以外の handoff 規定を確認するときは、該当する別の構成対象へ進む。

## hash
- 70192e603c87c595aa2e011dd4d65defd6e14f0ec98e619541ea4396a7720ea7

# `feedback_reporting_policy.py`

## Summary
- 全 agent call に共通する、人間向け feedback 報告規定の構築を担当する。作業外の人間対応が必要で、再発防止・反復的浪費の削減・外部挙動に関わる意図確定につながる問題だけを報告対象とし、通常 workload 内で解決した問題などは対象外とする。feedback は指定 MCP tool で報告し、報告後も本来の作業を継続するための共通プロンプト断片を提供する。

## Read this when
- agent call 共通の human feedback reporting 方針を確認・変更するとき
- feedback 報告対象の範囲、報告手段、報告後の継続動作を確認するとき
- prompt builder が共通の feedback reporting ポリシーを組み立てる責務を調査するとき

## Do not read this when
- 特定 workload の個別仕様や実装上の問題だけを調査するとき
- feedback 報告方針ではなく、プロンプトの別の構成要素を直接調査するとき
- 通常の作業内で解決済みの問題や、根拠のない改善案を扱うとき

## hash
- d310455d79a8cb591f50a86e582d583ed7ab886f7e88729221b1d28d388ec067

# `file_access_policy.py`

## Summary
- cmoc の agent 向けファイル読み書きポリシー文面を、FileAccessMode とパスコンテキストに応じて生成する関数。リポジトリ外、管理対象ディレクトリ、oracle/realization file などのアクセス制限を deny-list として組み立て、プロンプト部品として返す。
- ファイルアクセス権限の生成規則、mode ごとの oracle/realization file の扱い、特殊な NO_POLICY の挙動を確認するための実装入口。ファイルアクセス制約や prompt builder の構成を変更・調査する際に読む。

## Read this when
- FileAccessMode ごとの読み書き制限や、agent prompt に埋め込むファイルアクセス規定を変更・検証するとき
- repo-root と work-root が異なる場合を含む、パスプレースホルダーとアクセス拒否文面の生成を調査するとき
- oracle file と realization file の編集可否を mode 別に確認するとき
- NO_POLICY が使われる特殊な prompt 構築経路を調査するとき

## Do not read this when
- INDEX.md のルーティングだけを確認したいとき
- ファイルアクセス規定ではなく、実際の Codex CLI sandbox 設定や正本の実行規則を確認するときは、対応する oracle 仕様を直接読む
- prompt builder の別部品や、oracle/realization file の具体的な内容だけを調査するとき

## hash
- 71e275db327577997bd71e5920ae3e8552d2b9c5ab094888c9ef78bcc5866f20

# `index_entry_policy.py`

## Summary
- 対象は、INDEX.md 用エントリー生成エージェントに適用するポリシー群を組み立てる入口です。INDEX_ENTRY_ROUTING_POLICY、INDEX_ENTRY_EVIDENCE_POLICY、INDEX_ENTRY_SEMANTIC_INFORMATION_POLICYを、専用グループとしてまとめて返します。

## Read this when
- INDEX.md 用エントリー生成時のポリシー構成や、どの規定群を適用するかを確認したいとき。
- index_entry_policy のポリシー選択・グループ化の責務を確認したいとき。

## Do not read this when
- INDEX.md エントリーの個別ルール本文を確認したいときは、各ポリシー定義を直接読む。
- 一般的なプロンプト構築や、INDEX.md 以外のポリシー構成を確認したいとき。

## hash
- 91fb91d6830bfd5a6f37952c9b71223b5ee195d496965449736ba0b64063fe79

# `oracle_and_realization_basic.py`

## Summary
- oracle と realization の分類境界、および両者の役割を定義する基本説明文を構築する。
- oracle 側では oracle doc・oracle src・oracle test、realization 側では realization code・implementation・test・ancillary の下位概念を整理する。
- call-scoped context から work-root の定義を取得し、説明文中のプレースホルダーへ渡す処理を含む。

## Read this when
- oracle file と realization file の分類規則や責務を確認するとき。
- oracle doc/src/test と realization implementation/test/ancillary の区分を確認するとき。
- oracle と realization に関する基本説明文の生成経路を変更・調査するとき。

## Do not read this when
- oracle と realization の分類や基本概念を扱わず、別の prompt_builder part を直接確認すべきとき。
- 具体的な分類アルゴリズムやテスト実装を確認する場合に、対応する実装・テスト対象へ直接進めるとき。

## hash
- 7d70bb60c470aff3275d9de18ec27d6b68d9da9fab51e7cf7a7608aa58964008

# `oracle_policy.py`

## Summary
- oracle file を扱う agent call に適用する PolicyCollection の構築定義。oracle file の作成・変更・レビュー向けと、読み取り専用調査向けに、適用する policy group を分けて提供する。

## Read this when
- oracle file の作成・変更・レビューを行う agent call に、適用する規定の集合を確認したいとき
- oracle file の読み取り専用調査を行う agent call に、調査用の規定の集合を確認したいとき
- prompt builder で oracle 向け policy collection の選択経路を確認したいとき

## Do not read this when
- oracle policy の個別規定の本文を確認したいとき
- oracle file 以外の作業に適用する policy collection を確認したいとき
- prompt builder の policy 選択ではなく、共通 authority policy や個別 policy 定義だけを確認したいとき

## hash
- 640e87ae96d06a65137ef8e0ebe21cf7a8ce301051c4f50d0fb1a2dcad0a0e65

# `oracle_review_policy.py`

## Summary
- oracle review の所見判定規定を構築する部品。所見の根拠に関する共通ポリシーと、oracle review 固有の致命的所見・軽微な所見・oracle file 限定の規定をまとめ、review の全段階で共有する PolicyCollection を提供する。oracle review の判定ポリシーの入口として扱う。

## Read this when
- oracle review における所見の列挙、統合、検証、採否判定の規則を確認するとき
- oracle review 用のポリシー集合を構築・変更するとき
- 所見の根拠に関する共通規定と oracle review 固有規定の組み合わせを確認するとき

## Do not read this when
- oracle review 以外のプロンプト構築ポリシーを確認するとき
- 個別ポリシーの具体的な判定内容を直接確認したいときは、各ポリシー定義を読む方が適切な場合

## hash
- 279b6203d95f0370ace4c4321df41d8f5dd2e282d24e3129050e49faed2709a0

# `policy_definitions.py`

## Summary
- 全用途で共有する Policy 定義を集約する入口。oracle と realization の扱い、仕様の優先関係・未定義領域、検証、レビュー、conflict 解消、editor handoff、INDEX.md ルーティングに関する方針を確認・変更するときに読む。個別の挙動仕様や実装そのものではなく、複数の作業領域に適用される共通ポリシーを扱う。

## Read this when
- 複数の prompt builder 部品で共有される policy の追加・変更・参照条件を判断するとき
- oracle と realization の責務境界、仕様適合、レビュー所見、conflict 解消、editor handoff の共通方針を確認するとき
- INDEX.md エントリー生成に関する共通方針を確認するとき

## Do not read this when
- 特定の oracle file や realization file の具体的な仕様・実装だけを確認する場合
- 共有 policy の適用結果や個別作業の実行手順を確認する場合は、対応する個別仕様または repository 固有手順を直接読む

## hash
- 51d10f9224c9acfdd3125419497d13a5f75afc509cdadf328ef26986216bd443

# `realization_oracle_reference_policy.py`

## Summary
- realization code から oracle file path を参照する規定を構築する関数を定義する。realization code の作成・変更時に、対応する oracle file が存在すれば、コメントへ work-root 起点の oracle file path を記載するための構造化された参照ポリシーと placeholder map を返す。

## Read this when
- realization code を作成または変更し、対応する oracle file への参照規定を確認する必要があるとき。

## Do not read this when
- realization code 自体の実装内容や配置規則を確認したいときは、対応する realization または設計規則を直接読む。
- oracle file の具体的な内容や個別の仕様を確認したいとき。

## hash
- a72583769048b759b2d53f7ca62ecd97cffc25515bb5b1f3f72c1afd4b2bf1c3

# `realization_policy.py`

## Summary
- realization file の作成・変更・リファクタ・レビュー時に適用する instruction policy 群を構築する定義。
- 共通の oracle authority policy group と、realization 向けの oracle conformance・current spec only・repository verification の各 policy を一つの PolicyCollection にまとめる。

## Read this when
- realization file を扱う agent call で、適用対象の policy group と個別 policy の構成を確認したいとき。
- realization 向け instruction 文面の policy 選択ロジックを変更・レビューするとき。

## Do not read this when
- realization file を扱わず、個別 policy の具体的な規定だけを確認したいとき。
- 個別 policy の本文や oracle authority policy group の定義を確認する場合は、それぞれの定義元を直接読むべきとき。

## hash
- a6b62a8f6e1658078e9536f7d7affc0bbe2056f1f4890085b6d50bf5cee26f86

# `routing_policy.py`

## Summary
- INDEX.md を用いた文書ルーティングの規定文面を構築する。作業対象に近い階層の INDEX.md から読み始め、候補を Summary・Read this when・Do not read this when で絞り、必要な本文や下位階層の INDEX.md へ進むための入口となる。INDEX.md は本文の代替ではなく、内容の意味は本文を根拠とする。

## Read this when
- INDEX.md の役割、読み始める位置、候補の絞り込み方を確認するとき
- 対象領域が不明で、リポジトリルートの INDEX.md を起点にしたルーティング規則を確認するとき
- 下位ディレクトリの INDEX.md を使う条件や、本文と INDEX.md が異なる場合の優先順位を確認するとき

## Do not read this when
- INDEX.md の具体的なエントリー内容や対象文書そのものを読む必要があるとき
- 特定の対象本文の責務や仕様を直接確認できる場合
- 候補の網羅的な探索ではなく、すでに対象本文が特定されている場合

## hash
- 7f76ed23be7f3301d5ebe8a22987e9180e23c37e4a79bd47bb69b9ceff1509ee
