# `apply_review.py`

## Summary
- oracle file と realization file の適合性を評価する agent 向け方針を定義する。oracle を正本仕様として扱い、realization の挙動から oracle の意味を変更しない原則、具体的根拠に基づく所見・修正判断、明確な不適合や致命的問題のみを修正対象とする基準をまとめる。oracle と realization の追従要否やレビュー所見を判断する際の入口となる。

## Read this when
- oracle file に対する realization file の適合性、追従要否、レビュー所見、修正対象を判断するとき
- oracle と realization の権威関係や、所見の根拠・修正基準を確認するとき

## Do not read this when
- oracle または realization file の適合性判断を行わず、通常の実装・テスト・文書作成だけを行うとき
- 具体的な挙動仕様そのものを確認する必要があり、対象の oracle file または realization file を直接読むべきとき

## hash
- 719b5288852db477c8084e43ae647eab9feb3b3fb301ab91b673f49b97c5df55

# `conflict_resolution.py`

## Summary
- `cmoc session join` の conflict marker 解消時に適用する conflict resolution policy の定義。oracle file を正本仕様断片として扱い、realization file から oracle file へ意味を逆流させない原則と、両 branch の意図・挙動を保って解消するための判断基準をまとめた入口。

## Read this when
- `cmoc session join` で conflict marker を解消するとき
- oracle file と realization file の関係を保ったまま conflict を解消するとき
- 両 branch の意味を両立できず、人間による意図の選択が必要か判断するとき

## Do not read this when
- conflict marker の解消を伴わない通常の oracle／realization の編集や実装を行うとき
- `cmoc session join` 以外の conflict 解消方針を確認するとき
- oracle file の個別仕様や realization の実装挙動そのものを確認するとき

## hash
- e105db670ccdba7ced07a4c7e54bda543fccb86dba6d9f5c2b06a0ed67eb3a5a

# `editor_handoff.py`

## Summary
- agent call から editor work file へ handoff する際の instruction 文面を構築する定義。agent call の file access mode と Codex CLI sandbox を維持しつつ、正式な結果・成果物も満たすという handoff policy の入口。

## Read this when
- agent call と editor work file 間の handoff 規定を確認・変更するとき
- handoff 時の権限維持、成果物要件、sandbox escalation の許容範囲を確認するとき

## Do not read this when
- editor work file への handoff policy ではなく、一般的な prompt 構築や PlaceholderMap の仕様だけを確認するとき
- agent call の正式な成果物そのものを実装・検証するとき

## hash
- 5a4459cb2bece8488288dc27153178b949e0acbe6a3c7cb3199573299ca6c098

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
- INDEX.md 用エントリー生成 agent 向けの文面構築定義。対象の責務は、INDEX エントリー作成時に適用する必須事項・禁止事項を構造化された文書として提供すること。
- 対象を読むべきなのは、INDEX.md のルーティング情報を生成・変更・レビューし、記載すべき判断条件や対象への導線を確認するとき。
- 対象本文の詳細な実装内容や、INDEX.md 以外の通常のプロンプト構築規則を確認する目的では、より直接的な対応文書を読むべきで、この対象は入口にしない。

## Read this when
- INDEX.md 用エントリーの生成規定を確認するとき。
- エントリーに含める責務・読む条件・境界・禁止事項の根拠を確認するとき。
- エントリー生成 agent 向けの構造化された方針文面を変更するとき。

## Do not read this when
- INDEX.md 用エントリーではなく、対象機能そのものの実装や通常のプロンプト構築を調べるとき。
- すでに別の正本文書から、機械的な識別情報や Structured Output の形式を確認できるとき。

## hash
- ea372cb54937e7ba38fc019ebd1feab047c3a2a11ec953271c98d29287377333

# `oracle.py`

## Summary
- oracle file を扱う agent call の instruction 文面を構築する定義。oracle を正本仕様断片として扱う権限規則、判断根拠、実装からの意味逆流禁止、仕様の隙間の扱い、整合性・検索性の維持を定める。oracle file の作成・変更・レビュー時と、読み取り専用調査時の規定をそれぞれ構築するための下位要素への入口となる。

## Read this when
- oracle file の作成・変更・レビューに必要な agent call 向け policy の構築規則を確認するとき
- oracle file の読み取り専用調査に必要な policy の構築規則を確認するとき
- oracle と realization の権限境界、正本仕様の扱い、未定義事項の扱いを instruction に反映するとき

## Do not read this when
- oracle file の具体的な仕様本文や realization の実装内容を確認することが目的のとき
- prompt builder の一般的な placeholder 処理や StructDoc の実装を直接確認すべきとき
- INDEX.md の更新手順やエントリー形式だけを確認するとき

## hash
- 0a290a69ba9b649af4612085efc3e7d232b5cfa1008071c68c6582ba10ff8267

# `oracle_review.py`

## Summary
- oracle review 全段階で共有する所見判定規定を構築する定義。所見・修正対象に具体的な oracle file または realization file の根拠を求め、実装者の裁量で解消できない矛盾や問題だけを fatal、文意または検索性を損なう表記上の誤りだけを minor として扱う。realization file や外部事情を追加しなければ成立しない事項を所見にしないための判断基準を提供する。

## Read this when
- oracle review の所見を列挙、統合、検証、擁護・反証、採否判定するとき。
- oracle review の所見成立条件、fatal/minor の分類条件、根拠の要件を確認または変更するとき。

## Do not read this when
- oracle review の所見判定規定を扱わず、別の prompt builder の構築定義だけを確認するとき。
- realization file の実装挙動や外部事情を個別に調査するとき。

## hash
- e3bb0ca58b9c3143b00d99af89da11d1cfbbb1da79378a09eda9f3fb54eb734f

# `realization.py`

## Summary
- 対象は、realization file を扱う agent call に与える instruction 文面を構築する定義である。oracle を正本仕様として扱い、realization を現行 oracle に適合させること、必要な実装だけを保つこと、リポジトリ固有手順で検証することを要求するポリシー断片を組み立てる。realization の作成・変更・リファクタ・レビュー時に、関連する規定の入口として読む。

## Read this when
- realization file の作成、変更、リファクタ、またはレビューを行うとき
- oracle と realization の責務分離、仕様適合、実装の最小性、検証手順に関する agent call 向け policy を確認するとき

## Do not read this when
- oracle file 自体の意味や prompt 文面を変更する作業
- realization file を扱わず、一般的な prompt builder の実装や別ポリシーだけを確認するとき

## hash
- 927a7c1af72b03fc0618d9c34c90ecd21971bf039c583c9d59ca4645957daf0c

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
