# `apply_review.py`

## Summary
- 対象は、oracle file と realization file の適合性を評価する agent 向けポリシー集合を構築する関数を定義する。共通の oracle 権威・所見根拠ポリシーに加え、realization の追従要否、既解決事項、修正対象の判断に関する専用ポリシーを束ねる入口である。

## Read this when
- oracle file に対する realization file の追従要否、所見、修正対象の判断ルールを確認するとき
- apply review 用のポリシー集合がどの共通ポリシーと専用ポリシーから構成されるかを確認するとき

## Do not read this when
- 個別ポリシーの具体的な判定内容だけを確認したいときは、各ポリシー定義を直接読む
- apply review 以外の agent 文面構築規定を確認するときは、対象となる別の policy builder を読む

## hash
- 84938a66449ecd32dcca980f4da6b1d3c5e5dd9d5633142705c9ed2494f4aecd

# `basic.py`

## Summary
- agent 向け instruction の基本ポリシーを表す immutable な値オブジェクト群と、PolicyCollection を衝突検査・決定的順序で合成し、StructDoc の instruction 文面へ変換する処理を扱う。ポリシーの定義、group 単位の適用範囲、ID 衝突時の挙動、render 形式を確認または変更するときの入口となる。

## Read this when
- 複数の policy collection を合成する規則や、Policy/PolicyGroup の不変性・入力検証を確認するとき
- agent 向け instruction のポリシー文面を StructDoc へ変換する見出し・ラベル・順序を確認するとき
- policy ID または group ID の衝突、重複配置、決定的な出力順の挙動を変更・検証するとき

## Do not read this when
- 個別の agent prompt の動的生成手順や、Policy 以外の prompt 構成要素だけを確認するとき
- StructDoc 自体の仕様やレンダリング実装を直接確認する必要があるとき
- 実行時の CLI 処理や realization 層の責務を調査するとき

## hash
- 354778fdd844f394f06749ab576373fb6ea2368b8b8a8d9d5cb85abfcb4fad71

# `common.py`

## Summary
- 複数用途で共有する PolicyGroup の構成定義を担う。oracle・realization file を扱うときに適用する oracle authority 系ポリシー群と、所見・修正対象を判断するときに適用する finding basis 系ポリシー群を組み立てる。各ポリシーの本文や PolicyGroup の実装を確認する場合は、それぞれの定義元または実装へ進む入口となる。

## Read this when
- oracle・realization file を扱う作業で、適用する oracle authority policy group の構成を確認するとき
- 所見や修正対象の判断で、finding basis policy group の適用範囲を確認するとき
- oracle authority policy に逆方向の流れを防ぐ規則を加えた共有グループの構成を確認するとき

## Do not read this when
- 個別ポリシーの具体的な規則を確認したいときは、各ポリシー定義を直接読む場合
- PolicyGroup のデータ構造や動作を確認したいときは、PolicyGroup の実装を直接読む場合
- 対象ファイルと無関係な作業や、既存の INDEX.md の内容を確認する場合

## hash
- 0c1842670da7005c600d865872db0eb0a72ed6758bca43fe1fc8fbea11b01039

# `conflict_resolution.py`

## Summary
- `cmoc session join` で発生した conflict marker の解消に使う policy collection を構築する。oracle と realization の意味を保つ共通 authority policy に加え、両ブランチを保持する conflict resolution policy を選択する処理を扱う。conflict 解消時の instruction 文面生成を確認・変更するときの入口。

## Read this when
- `cmoc session join` の conflict 解消動作や、conflict 解消用 policy の選択・適用を確認するとき。
- oracle / realization の意味を維持しつつ、両ブランチを残す conflict 解消規則を変更するとき。

## Do not read this when
- session join の conflict 解消以外の policy 構築を調べるとき。
- conflict resolution policy の個別定義そのものを確認する場合は、まず policy 定義側の対象を読むとき。

## hash
- 49ff3b83ca17b01987ea79372cd2f9b848f1101363fccdfea36ba1ac8ac7ae15

# `editor_handoff.py`

## Summary
- agent call の結果を editor work file へ handoff する際に適用する policy collection を構築する定義。handoff の対象範囲を示す policy group を、既存の preserve-result policy とともにまとめる。
- prompt builder の policy 定義で、editor work file への handoff 規則を確認・変更するときの入口となる。

## Read this when
- agent call から editor work file へ結果を handoff する挙動や適用 policy を確認・変更するとき。
- handoff 用 policy collection の group 構成や、結果保持 policy の組み込み方を確認するとき。

## Do not read this when
- editor work file への handoff 以外の policy group を確認・変更するとき。
- handoff policy の個別内容そのものを確認する場合は、参照される policy 定義を直接読むとき。

## hash
- d040f3242479acc63a63b1b745b863fc325c9b31958790cee7c7ca9ae7adc7e2

# `feedback_reporting.py`

## Summary
- 全 agent call に共通する、人間向け feedback 報告規定のプロンプト構築を担う。現在の workload 外の人間対応が再発防止・反復的な浪費削減・外部挙動に関わる意図の確定に必要な問題だけを報告対象とし、報告時の MCP tool 利用、継続方針、報告対象外の境界を定義する。agent call の feedback 報告ルールやそのプロンプト生成処理を確認・変更するときの入口となる。

## Read this when
- agent call に共通する human feedback reporting policy の内容または生成処理を確認・変更するとき
- feedback 報告対象の判定、MCP による報告、報告後の workload 継続方針を確認するとき

## Do not read this when
- 個別 workload の実装や、feedback 規定を利用するだけで共通ポリシー自体を確認する必要がないとき
- feedback 保存 file の内容や、別の prompt policy の責務を直接確認するとき

## hash
- d310455d79a8cb591f50a86e582d583ed7ab886f7e88729221b1d28d388ec067

# `file_access.py`

## Summary
- file access mode に応じた agent 向けの読み書き禁止ポリシー文面を構築する。リポジトリ境界、予約ディレクトリ、oracle／realization file などのアクセス制約を mode 別に組み立て、prompt builder が利用するプレースホルダー定義と構造化文書を返す。

## Read this when
- agent prompt に埋め込む file access policy の内容や、FileAccessMode ごとの禁止事項を変更・確認するとき
- repo-root と work-root の関係に応じたアクセス制約の生成規則を変更・確認するとき
- oracle／realization file の読み書き可否を mode 別に調整するとき

## Do not read this when
- Codex CLI の sandbox 設定や path 単位の権限を変更・確認するときは、該当する実行規則を直接読む
- prompt 内のアクセス制約ではなく、実際の CLI 実装やファイル操作処理の責務を変更・確認するときは、その実装の入口を直接読む

## hash
- 71e275db327577997bd71e5920ae3e8552d2b9c5ab094888c9ef78bcc5866f20

# `index_entry.py`

## Summary
- `INDEX.md` 用エントリー生成時に適用するポリシー群を構築する定義。エントリー生成規則の選択範囲を確認する入口であり、個別ポリシーの文面を確認するときは `policy_definitions.py` を直接読む。

## Read this when
- `INDEX.md` 用エントリー生成で、どのポリシー群を適用するかを変更・確認するとき
- エントリー生成向けのポリシー構成や適用範囲を調査するとき

## Do not read this when
- 個別ポリシーの具体的な要求・禁止事項を確認するとき
- `PolicyCollection` や `PolicyGroup` のデータ構造・合成処理を確認するとき

## hash
- d6b09b0e2558bfbf4b9ad3d1777bb37cd9ec0e7d1ecbc47df62db0139f91c1f1

# `oracle.py`

## Summary
- 対象は oracle file を扱う agent call 向けの policy collection 構築定義であり、oracle file の作成・変更・レビュー時に適用する規定群と、読み取り専用調査時に適用する限定的な規定群を選択する。oracle 関連の動的 prompt 方針や調査方針の入口として読む。

## Read this when
- oracle file の作成、変更、レビューに伴って agent call の適用ポリシーを確認するとき
- oracle file を読み取り専用で調査する際に、調査用に選択される規定の範囲を確認するとき

## Do not read this when
- oracle file 以外の policy collection や一般的な prompt 構築の責務だけを確認するとき
- oracle file の本文や個別の規定内容を直接確認することが目的のときは、対象の oracle file または各 policy 定義へ直接進む

## hash
- 2f73a07bd4cba435413ae3c002f3df9350d7bc88f94854635e768b3e1d42bc1f

# `oracle_review.py`

## Summary
- oracle review の各段階で共有する所見判定ポリシー群を構築する関数を定義する。所見の根拠ポリシー群と、致命的・軽微・oracle file 限定の判定ポリシーをまとめた PolicyCollection を返す、prompt_builder のポリシー構成上の入口。

## Read this when
- oracle review における所見の列挙・統合・検証・採否判定に適用する共有ポリシーを確認または変更するとき。
- oracle review 用 PolicyCollection の構成や、所見判定ポリシーの選択を確認するとき。

## Do not read this when
- oracle review 以外のプロンプト構築ポリシーを確認するとき。
- 個別ポリシーの具体的な定義を確認する場合は、対応する policy_definitions の対象を直接読むとき。

## hash
- 8eb36dc0d73093ee1940406f47bd1013ce591385fb96e517570843a87be9086a

# `realization.py`

## Summary
- realization file の作成・変更・リファクタ・レビューに必要な instruction policy を構築する入口。oracle authority policy group と realization 固有の policy group をまとめ、realization の現行仕様準拠、oracle 準拠、リポジトリ検証に関する規定へ接続する。

## Read this when
- realization file の作成・変更・リファクタ・レビューに必要な agent call 向け instruction の構成を確認するとき。
- realization 固有の policy group と oracle authority policy group の適用範囲を確認するとき。

## Do not read this when
- realization 以外の対象に対する policy 構築定義を確認するとき。
- 個別 policy の具体的な規定や、PolicyCollection・PolicyGroup の実装を直接確認したいとき。

## hash
- 1823163573badda60bfca8e44c284ce6f4ad09f26ddc051180bcfb451201fbb2

# `realization_oracle_reference.py`

## Summary
- realization code から、対応する oracle file の参照規則を構築するポリシー定義。realization code の作成・変更時に適用され、対応する oracle file が存在する場合のコメント記載ルールを確認する入口となる。

## Read this when
- realization code の作成または変更にあたり、oracle file path をコメントへ記載する規則を確認するとき。
- realization code と oracle file の対応付けに関する prompt policy を変更・調査するとき。

## Do not read this when
- realization code 自体の実装責務や配置を確認したいとき。
- oracle file の本文や、個別の realization code の動作仕様を直接確認するとき。

## hash
- a72583769048b759b2d53f7ca62ecd97cffc25515bb5b1f3f72c1afd4b2bf1c3

# `routing.py`

## Summary
- INDEX.md を本文の代替ではなく、必要な文書へ絞り込む routing 情報として定義する。作業対象に近い INDEX.md、または対象領域を特定できない場合のリポジトリルートから読み始め、Summary・Read this when・Do not read this when で候補を絞る。下位階層では必要に応じて各階層の INDEX.md を使い、本文を意味の根拠とする。

## Read this when
- INDEX.md の読み始める位置や候補の絞り込み方を確認するとき
- 関連文書を総当たりせず、対象に近い階層から必要な本文へ進むとき
- INDEX.md と本文の内容が異なる場合の判断基準を確認するとき

## Do not read this when
- 特定の実装や仕様の意味を直接確認したいとき
- routing 以外の prompt builder の処理責務を調べるとき
- 対象文書がすでに特定されており、INDEX.md による候補選択が不要なとき

## hash
- 7f76ed23be7f3301d5ebe8a22987e9180e23c37e4a79bd47bb69b9ceff1509ee
