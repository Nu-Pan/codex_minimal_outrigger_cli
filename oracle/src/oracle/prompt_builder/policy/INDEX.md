# `apply_review.py`

## Summary
- oracle file に対する realization file の追従要否、所見、修正対象を判断する policy 定義の構築入口。oracle を正本仕様として扱い、oracle の明示要求と realization の具体的挙動の不整合、または realization 単独で説明できる実行不能・明白な致命的バグを修正対象とする判断基準を扱う。
- 所見や修正対象には具体的な oracle file または realization file の記述・挙動を示し、realization の都合で oracle の意味を変更せず、仕様の隙間や好みだけで問題を作らないための制約を提供する。

## Read this when
- oracle file と realization file の適合性をレビューするとき
- realization file の追従要否、所見の成立、または修正対象を判断するとき
- oracle の要求と realization の挙動の不整合を根拠付きで評価するとき

## Do not read this when
- oracle・realization file の適合性判断を行わず、別の prompt builder policy の責務を確認するとき
- 一般的なコード品質、好み、推測だけに基づく改善を検討するとき
- 対象の具体的な oracle file または realization file を直接確認すべき作業

## hash
- 7c8804f3be697c446d0ad53c2bf1abe218be59fe66fc7677270afae328381d24

# `basic.py`

## Summary
- 現在のファイルは空で、定義・処理・設定を担っていません。内容を確認する必要がある場合の最小限の入口です。

## Read this when
- 対象ファイルが空であることや、内容が存在しないことを確認するとき

## Do not read this when
- prompt_builder のポリシー挙動を調査・変更するとき
- 実装や仕様を確認するときは、内容を持つ該当ファイルを直接読む

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `conflict_resolution.py`

## Summary
- `cmoc session join` で conflict marker を解消する際の instruction 文面を構築する定義。oracle file を人間所有の正本仕様断片として扱い、conflict 両側と関連 oracle file の意図・挙動を両立させる解消方針、および両立不能時に未解消事項として報告する制約への入口。

## Read this when
- `cmoc session join` の conflict marker 解消方針や、その instruction 文面の構築内容を確認・変更するとき。
- oracle・realization file を含む conflict の扱いにおける、oracle authority と未解消事項の報告条件を確認するとき。

## Do not read this when
- conflict marker の解消ではなく、通常の prompt 構築や別の session join 動作を確認するとき。
- oracle または realization の具体的な正本仕様・実装内容を確認する場合は、この方針ではなく該当する oracle・realization file を直接読むとき。

## hash
- f9b1b2a7cdbe39fb8ea933e26507d27ddbe14f488b2c1280e7d132dfb6eec487

# `editor_handoff.py`

## Summary
- このファイルは、任意の agent call から editor work file へ handoff する際の instruction 文面を構築する定義を担う。handoff 時にも選択済みの file access mode と Codex CLI sandbox を維持し、handoff file への書き込みとは別に agent call が要求する正式な成果物を満たす規定を扱う。

## Read this when
- agent call から editor work file への handoff 規定を確認・変更するとき
- handoff 時の file access mode、Codex CLI sandbox、正式な成果物の扱いを確認するとき

## Do not read this when
- editor work file への handoff を行わず、通常の agent call の prompt 構築規定だけを扱うとき
- handoff の具体的な書き込み処理や、他の prompt policy の内容を直接確認する必要があるとき

## hash
- c8def0a7d551f710d98f812d7fb6d54a21dc319700ec732d14d1f23fc5876222

# `feedback_reporting.py`

## Summary
- 全 agent call に共通する、人間向け feedback 報告規定を構築するポリシー実装。未解決問題の MCP 報告要件、報告対象外の条件、報告結果による継続判断の禁止を SDHeader として定義する。feedback 報告ポリシーの生成処理を確認・変更する際の入口となる。

## Read this when
- 全 agent call に適用する human feedback reporting の規定を確認・変更するとき
- 解決できなかった問題の MCP tool 報告要件や、報告対象外・継続判断の扱いを確認・変更するとき

## Do not read this when
- feedback 報告以外の prompt policy を確認・変更するとき
- 生成済みプロンプトの利用側の挙動だけを確認するとき

## hash
- 1570460431e1bb37b4d66142a9c594245e6a1976b48b4d58f0d2b7de13a66ec1

# `file_access.py`

## Summary
- FileAccessMode と AgentCallPathContext に基づき、agent 向けのファイルアクセス制限文面を構築する関数を定義する。リポジトリ外、管理用ディレクトリ、AGENTS.md・INDEX.md・memo、oracle file・realization file などへの読み書き禁止を mode ごとに組み立て、NO_POLICY では空の規定を返す。
- ファイルアクセス権限の生成規則や、READONLY・PURE_ORACLE_READ・REPO_WRITE・PURE_ORACLE_WRITE・REALIZATION_WRITE・NO_POLICY の差異を確認するための実装上の入口であり、下位のパス文脈・構造化文書型と連携する。

## Read this when
- agent 呼び出し向けのファイルアクセス制限文面を変更・調査するとき
- FileAccessMode ごとの oracle file または realization file の読み書き制約を確認するとき
- repo-root と work-root が異なる場合の .cmoc/g*/ar への扱い、または NO_POLICY の挙動を確認するとき

## Do not read this when
- INDEX.md のルーティング構成やエントリー形式だけを確認したいとき
- 具体的な oracle file・realization file の内容や、CLI の実際のアクセス処理を直接確認したいとき
- SDHeader・SDPolicy・PlaceholderMap・AgentCallPathContext の型定義や一般的な構造化文書の仕様を確認したいとき

## hash
- 7fdbde495952a7d90e41aa71ed13525fdbd428ee3d05b492e124cc68c433d504

# `index_entry.py`

## Summary
- INDEX.md 用エントリー生成 agent に適用するルーティング記述の規定を構築する。対象を読む条件、責務、入口、対象外との境界を意味情報として記述し、推測や過剰な詳細、機械的情報の記載を禁じる。

## Read this when
- INDEX.md のエントリーを新規生成・更新する作業や、その記述方針を確認する場合
- 対象の責務と、同階層の別対象ではなく対象へ進む条件を定める場合

## Do not read this when
- INDEX.md エントリーを扱わない通常のプロンプト方針や実装を読む場合
- 対象ファイルそのものの機能実装や構造を確認することが目的の場合

## hash
- 6a61edcbfad76363c8e720c8adc03d08e60ba7e5208abb0d5407f8e6756e674b

# `oracle.py`

## Summary
- oracle file の作成・変更・レビュー時に適用する instruction 構築規定を定義する。oracle と realization の要件、指示の優先順位、仕様から読み取るべき実装差の境界や goal・non-goal、関連 oracle file への参照、既存意味の維持、用語統一、未定義事項の扱いを要求事項として整理し、realization からの仕様逆算や根拠のない修正、仕様矛盾・重複・誤りを禁止する。oracle file の問題調査に限り実装制約を判断材料として許容する。

## Read this when
- oracle file の作成・変更・レビューで、適用すべき要求・禁止・許容事項を確認するとき
- oracle file における実装差の許容範囲、goal・non-goal、未定義事項の扱いを確認するとき
- oracle file 間の参照、用語、既存意味の維持に関する規定を確認するとき

## Do not read this when
- realization file の実装配置や具体的な実装挙動を確認するとき
- oracle file 以外の prompt builder policy の構築規定を確認するとき
- oracle file の個別仕様そのものではなく、oracle と realization basic の詳細要件を確認するとき

## hash
- db22873b969681521bffa92c8bb4c0790c5b3d18710723e5b57f79d8601a1b6f

# `oracle_review.py`

## Summary
- oracle review の所見が fatal または minor として成立する条件を構築する定義。正本仕様間の明確な矛盾、実装で解消不能な問題、表記上の明確な誤りを区別し、それぞれに必要な根拠と説明を求める。oracle review の所見の列挙・統合・検証・採否判定における共通ポリシーへの入口となる。

## Read this when
- oracle file に対する所見の列挙、統合、検証、採否判定を行うとき
- fatal と minor の所見成立条件や、所見に必要な根拠を確認するとき

## Do not read this when
- 所見を扱わず、oracle review policy の構築や判定条件を変更しない作業をするとき
- 具体的な oracle file の内容や realization への適合性を直接確認する場合

## hash
- ebd4bcaece98af9856432caf672c962433f998142275a99f8a8c059639e04f95

# `realization.py`

## Summary
- 対象は realization file を扱う agent call 向け instruction 文面を構築する関数を定義する。パス由来の placeholder 定義と、realization の作成・変更・レビュー時に従うべき SDPolicy を組み合わせて返すため、realization policy の規定や prompt builder の挙動を確認したい作業の入口になる。

## Read this when
- realization file の作成・変更・リファクタ・レビューに必要な instruction 文面の生成規則を確認するとき
- AgentCallPathContext から placeholder 定義を取得し、SDHeader と SDPolicy で policy を組み立てる処理を変更・検証するとき
- oracle file を正本仕様として扱うこと、既存実装の再利用、YAGNI、重複整理、検証・テスト要件を確認するとき

## Do not read this when
- realization file 本体の実装やテスト内容を直接確認したいときは、対象の realization file または対応する test を直接読む
- prompt builder 全体の共通仕様や PlaceholderMap の詳細だけを確認したいときは、対応する共通定義を直接読む
- INDEX.md の既存ルーティングや他対象の案内を確認したいときは、この対象ではなく許可された INDEX.md の情報源を読む

## hash
- 3bea8a3a959d7f60b0d8a79ba457f4fb67514cd86a54f7185ed612490a74050f

# `realization_oracle_reference.py`

## Summary
- realization code から参照する oracle file のパス記載規定を構築する関数。パスコンテキストから work-root の定義を取得し、PlaceholderMap と、対応する oracle file が存在する場合に realization code のコメントへ work-root 起点のパスを記載する SDHeader を返す。

## Read this when
- realization code の作成・変更時に、参照すべき oracle file path のコメント規定を確認したいとき
- oracle 参照ポリシー用の PlaceholderMap や SDHeader の構築方法を確認したいとき

## Do not read this when
- realization code の具体的な実装責務や配置規則だけを確認したいとき
- oracle file 自体の内容や、一般的な prompt builder の仕様を直接確認したいとき

## hash
- f5e984540c2c3d95e21b1cef839a32c90ee26c64b31037bb8afa3d0d49fe4e5d

# `routing.py`

## Summary
- 対象ファイルは、cmoc の各階層にある INDEX.md を起点として、作業対象に近い routing policy 文書へ進むための規定文面を構築する。call-scoped context から work-root を解決し、INDEX.md の利用規則を SDHeader と SDPolicy として返す入口である。

## Read this when
- INDEX.md の routing policy 文面を生成・変更するとき
- 各階層の INDEX.md の起点や、本文と INDEX.md の優先関係を確認するとき
- routing policy が参照する work-root の placeholder 定義を確認するとき

## Do not read this when
- INDEX.md の個別エントリーや対象ファイルの責務を特定することが目的のとき
- routing policy 以外の prompt builder の仕様・実装を直接確認すれば足りるとき

## hash
- e371d8744a622d9f5ef60d663f523a2561202a4c52a06ab524de80bb8bdfdc7c
