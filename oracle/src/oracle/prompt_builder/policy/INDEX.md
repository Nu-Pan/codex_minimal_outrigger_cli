# `conflict_resolution.py`

## Summary
- session join の merge conflict 解消結果に適用する policy を構築する関数。両方のマージ元ブランチの oracle file の意図・挙動の保持、両立不能時の未解消事項としての報告、oracle file の意味変更と不要な変更の禁止を定義する。

## Read this when
- session join の conflict 解消用 instruction の内容や、解消結果に求められる規定を確認するとき
- merge conflict 解消における oracle file の意図・挙動の保持方針を確認するとき

## Do not read this when
- session join の意味仕様や oracle file 規定と conflict 解消の優先順位そのものを確認するとき
- realization file の実装や挙動、または conflict 解消処理の具体的な実装を確認するとき

## hash
- 24db424d4c6fa917aeda82cd22244160d78e7ae3c487fa3a40e8bef4855c8ae8

# `feedback_reporting.py`

## Summary
- 全 agent call に共通する、人間向け feedback 報告規定のプロンプトポリシーを構築する。報告時の必須手段と禁止事項を SDHeader／SDPolicy として提供する。

## Read this when
- agent call 共通の human feedback 報告ルールを確認・変更するとき
- 人間へ報告すべき問題の扱いや、feedback 報告ポリシーのプロンプト構築責務を調べるとき

## Do not read this when
- feedback 報告の意味仕様そのものを確認するときは、参照先の app specification を直接読む
- feedback 報告とは無関係な prompt builder や個別 agent call の仕様を調べるとき

## hash
- a9912c718fc712efad38e202f9ebb1bcdc96dedc19ea3a5e55d107ab71b28543

# `file_access.py`

## Summary
- ファイルアクセスモードとパスコンテキストから、エージェント向けのファイル読み書き規定とプレースホルダー定義を構築する。
- リポジトリ境界、保護対象ディレクトリ、AGENTS.md・INDEX.md・memo、および oracle／realization file の扱いをモード別に組み立てる処理の入口。
- アクセス制御ポリシーの生成条件や、READONLY・PURE_ORACLE_READ・REPO_WRITE・PURE_ORACLE_WRITE・REALIZATION_WRITE・NO_POLICY の差異を確認するときに参照する。

## Read this when
- エージェント呼び出しで適用されるファイルアクセス規定の生成ロジックを調べるとき
- FileAccessMode ごとの oracle file／realization file の読み書き制限を確認するとき
- リポジトリルートと作業ルートが異なる場合の境界規定や、NO_POLICY の特殊扱いを確認するとき

## Do not read this when
- 個別の oracle file や realization file の内容・仕様を確認したいとき
- 生成済みプロンプト全体の構成や他のプレースホルダーの生成を調べるときは、該当する prompt builder の対象へ直接進む場合
- 実際のサンドボックス設定や Codex CLI の実行規則そのものを確認したいとき

## hash
- 9ce25523f13f5aee9d24c28d1232c1d323d36266e33b2e8c359511dd9cd320d4

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
- oracle file が満たすべき基本規定と、oracle doc・oracle src の正本責務、委譲、優先関係を agent call 向け指示として構築する関数。
- `SDHeader`、`SDPolicy`、`PlaceholderMap` を用い、oracle policy として要求事項・禁止事項・許可事項・補足事項を返す。
- oracle doc の意味仕様と oracle src の明示委譲された正確な詳細を区別し、仕様断片の未定義部分や実装差を扱う際の境界を示す。

## Read this when
- oracle file の作成・変更・レビューで、oracle doc と oracle src の責務分担、優先関係、委譲先の特定方法を確認する場合。
- agent call 向けに oracle policy、実装差の許容範囲、goal・non-goal、仕様断片の未定義事項を確認する場合。
- oracle file 間の矛盾、誤記、重複、実現不能な仕様を調査する場合。

## Do not read this when
- oracle policy の内容に関係しない prompt builder の実装詳細や、他の agent call 向け policy だけを確認する場合。
- realization file の具体的な実装配置や CLI の責務境界を確認する場合は、design_rule など該当する oracle file を直接読む。
- oracle file のテスト実行方法や品質検査だけを確認する場合は、test_execution の指示を直接読む。

## hash
- b6d9fbf08611868a289a1eacd3ce0c71e5de186b37c9a2b69c9fc5dad045c686

# `oracle_findings.py`

## Summary
- oracle file に対する所見の判定基準を共通ポリシーとして構築する。
- 所見として扱える問題の根拠と、fatal・minor の分類基準を定める。
- 各 review ステップで共通利用する所見ポリシーへの入口となる。

## Read this when
- oracle file の具体的記述に基づく問題の判定基準を確認するとき。
- 正本仕様の矛盾、実装者裁量で解決できない問題、表記上の問題を fatal・minor に分類するとき。
- 所見の根拠にしてよい事項や、既解消問題の重複報告禁止を確認するとき。

## Do not read this when
- 個別の oracle review の意味仕様や「所見」の定義そのものを確認する必要があるとき。
- 所見ポリシーではなく、構造化文書の一般的なヘッダーやポリシー型の構築方法を確認するとき。

## hash
- 222577ede357976761a308e4a059785a1b0bb703c6c2671b5a5d9c222adafa51

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
- `AgentCallPathContext` からルートのプレースホルダー定義を取得し、`work-root` を含む置換マップと routing policy 用の `SDHeader` を構築する関数。
- `SDHeader` と `SDPolicy` を使って、`INDEX.md` による routing の基本方針をプロンプトへ組み込む。
- routing の意味仕様そのものは `oracle/doc/app_spec/indexing.md` を参照する前提で、対象ファイルはその規定文面を動的に構成する入口となる。

## Read this when
- `INDEX.md` による routing policy のプロンプト生成や、そのヘッダー・ポリシー構築を変更または確認するとき。
- `AgentCallPathContext` のルートプレースホルダー定義を routing policy の入力へ渡す処理を追うとき。

## Do not read this when
- `INDEX.md` の routing 意味仕様を確認したいときは、対象ファイルではなく `oracle/doc/app_spec/indexing.md` を直接読む。
- `PlaceholderMap`、`SDHeader`、`SDPolicy` の一般的な実装詳細だけを確認したいとき。

## hash
- 908d29e185249c4aa4fecb62b09429a1b55e4022db7bd7c28d5d2ee749daebf3
