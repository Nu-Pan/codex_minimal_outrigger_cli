# `apply_review.py`

## Summary
- oracle file に対する realization file の追従要否・所見・修正を判断するためのポリシー集合を構築する。共通の権威・所見根拠ポリシーに加え、修正対象の判断と既解決事項の扱いに関する個別ポリシーをまとめる入口である。

## Read this when
- oracle file と realization file の適合性をレビューし、追従要否や所見、修正対象を判断するとき
- apply review に使用するポリシー構成や、共通ポリシーと個別ポリシーの組み合わせを確認するとき

## Do not read this when
- 個別ポリシーの具体的な判定条件だけを確認したいとき
- oracle file の権威規則や所見の根拠規則だけを確認したいときは、それぞれの定義元を直接読む

## hash
- 582e08e689f0db05b39b5f50ee038fd889d36f03f30ef8b56c5323344d272e3e

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
- 複数用途で共有する PolicyGroup の構成定義をまとめる。oracle・realization file の扱いに関する oracle authority policy group と、所見・修正対象の判断に関する finding basis policy group を提供する。各ポリシーの具体的内容を確認する必要がある場合は、同じ定義元へ進む前段の構成入口となる。

## Read this when
- oracle・realization file を扱う作業で、適用する oracle authority policy group の構成を確認するとき
- 所見や修正対象の判断で、finding basis policy group の適用範囲を確認するとき
- 共有ポリシーグループの構成や、基本グループと追加制約を含むグループの関係を確認するとき

## Do not read this when
- 個別ポリシーの本文や判定根拠を確認したい場合は、各ポリシー定義を直接読むとき
- PolicyGroup の一般的なデータ構造や実装仕様だけを確認する場合

## hash
- f4930ce3e972ef2675e299235f3c44771251d79bc4f9556e0f8dfd5831e9eeac

# `conflict_resolution.py`

## Summary
- `cmoc session join` で conflict marker を解消する際に適用する instruction 文面の構築定義。oracle / realization の権威関係を含む標準ポリシー群へ進む入口であり、conflict 解消方針の選択や変更を確認するときに読む。

## Read this when
- `cmoc session join` の conflict 解消規定を調査・変更するとき
- conflict 解消時に両ブランチを保持する方針、または oracle / realization の意味を保つ instruction 構成を確認するとき

## Do not read this when
- session join の conflict 解消以外の instruction 構築を調査するとき
- 個別ポリシーの定義や共通のポリシー構造を直接確認したいときは、それぞれの定義元を読む場合

## hash
- bd99ef59375838b8e633fa322b2ae022cfe9b80a453d6fbd2e6340daea0f80c0

# `definitions.py`

## Summary
- oracle file と realization file の関係、正本仕様の優先、仕様の未定義部分、実装適合性、レビュー、conflict 解消、editor handoff、および INDEX.md ルーティングに関する全用途の Policy 定義を一元管理する。各 Policy は識別子・題名と、必要に応じた required、prohibited、permitted の規則を持つ。Policy の定義や適用規則を変更・追加するときの入口であり、個別の Policy 実装や基本型の詳細を確認する場合は、より直接的な定義元を読む。

## Read this when
- oracle file を正本仕様として扱う規則、realization file の適合規則、仕様レビューや修正対象の判定規則を確認するとき
- 仕様間の優先関係、未定義事項の扱い、実装から仕様を逆算しない制約を確認するとき
- conflict 解消、editor handoff、INDEX.md エントリー生成に関する共通 Policy を確認するとき
- 全用途で共有される Policy の追加・変更や、Policy 定義の責務分担を調査するとき

## Do not read this when
- 単一の Policy の具体的な実装や Policy 基本型の仕様だけを確認する場合
- 対象の Policy 群に関係しない realization 実装、test、または個別 oracle file の内容を調査する場合

## hash
- 8e37a3b2131d3fe3ed676964bda2ff107fd0c0b92266d5950b3623fd683fc254

# `editor_handoff.py`

## Summary
- agent call から editor work file へ handoff する際の instruction policy を構築する定義。handoff 用の policy group を作成し、結果保持ポリシーを選択した PolicyCollection を返す。

## Read this when
- agent call から editor work file への handoff 規定を変更または確認するとき
- editor handoff 用 policy group の適用範囲や選択ポリシーを確認するとき

## Do not read this when
- editor work file 自体の内容や handoff 後の処理を確認するとき
- editor handoff 以外の policy group の構築を確認するとき

## hash
- 9ad2ffbcdcfeaacc19f6d5b239be98d2fdb3a56b560b102c155f19c41280d42e

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
- `INDEX.md` 用エントリー生成時に適用する規定群を選択し、ルーティング、根拠、意味情報に関する方針をまとめて返す。個別の規定本文ではなく、エントリー生成へ適用する方針集合の構築入口である。

## Read this when
- `INDEX.md` 用エントリー生成の適用規則や、生成時に組み合わせる方針群を確認するとき。

## Do not read this when
- 個々の方針の具体的な要求文を確認するときは、方針定義側を直接読む。エントリーの対象本文や既存の `INDEX.md` の内容を確認するときは、この方針構築定義を読む必要はない。

## hash
- 9fe09b68fee30b5286ff7aa6c9b46823dc762f328f5eb3c26ed5105eff5df86b

# `oracle.py`

## Summary
- oracle file を扱う agent call 向けの規定セットを構築するポリシービルダー。作成・変更・レビュー向けと、読み取り専用調査向けで適用するポリシー群を分け、共通の権限ポリシー群と組み合わせて返す。

## Read this when
- oracle file に関する agent call の指示へ、作成・変更・レビューまたは読み取り専用調査の規定を組み込む必要があるとき
- oracle 用ポリシーの適用範囲や、用途別の規定選択を確認するとき

## Do not read this when
- 個別ポリシーの定義本文や共通ポリシー群の内容だけを確認したいとき
- oracle file 以外の agent call 向けポリシー構成を調べるとき

## hash
- 8dcd1265c093ba94527d12284caf3735581d2c3d18a24d5da26232d2a63735c8

# `oracle_review.py`

## Summary
- oracle review の全段階で共有する所見判定ポリシー集合を構築する関数。
- 所見の成立根拠を定める共通ポリシー群に加え、重大所見・軽微所見・oracle file 限定所見の判定規定をまとめる。
- oracle review の所見列挙・統合・検証・採否判定に関するポリシー選択の入口となる。

## Read this when
- oracle review の複数段階で共通する所見判定規定の選択箇所を確認するとき。
- oracle review 用のポリシー集合に含める判定カテゴリや適用範囲を変更するとき。

## Do not read this when
- 個々の所見判定規定の具体的な内容だけを確認したいとき。
- oracle review 以外のポリシー集合や、共通ポリシー群の定義を直接確認するとき。

## hash
- ce4f333e7a805b91b275d8e5b2f62b47a1eb0dc5cb78b9d0e07ad97678014ce8

# `realization.py`

## Summary
- realization file の作成・変更・リファクタ・レビュー時に適用するポリシー群を構築する。oracle authority 共通規定に加え、oracle 準拠、現行仕様限定、リポジトリ検証の規定をまとめ、instruction 文面生成側の realization 向け入口となる。

## Read this when
- realization file に対する agent call の instruction 規定を追加・変更・レビューするとき
- realization 作業へ適用するポリシーの選定や構成を確認するとき

## Do not read this when
- oracle authority 共通規定そのものを確認するとき
- 個別ポリシーの本文や、realization 以外の作業向けポリシー構成を直接確認するとき

## hash
- af7fa05eb288adf86352cdf3f2afb85be8905d97cc2b578215ede6a1d586499c

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
