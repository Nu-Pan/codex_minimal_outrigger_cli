# `apply_review.py`

## Summary
- oracle file と realization file の適合性を判定する agent 向け policy を構築する関数を定義する。oracle の正本性、所見・修正対象の根拠、不整合や明白な致命的バグの扱い、修正後の適合条件を指定する。apply review policy の実装内容を確認・変更するときの入口となる。

## Read this when
- oracle file に対する realization file の追従要否、所見、修正対象を判断するとき
- oracle と realization の具体的な要求・挙動の不整合を評価するとき
- apply review policy の構築内容を変更または検証するとき

## Do not read this when
- oracle file や realization file の個別仕様そのものを確認する必要があるときは、それぞれの対象を直接読む
- 一般的なレビュー方針や、apply review policy と無関係な prompt builder の挙動を確認するとき

## hash
- d9d6867951f6ca8c82b7227bccbaaa7bbe7ab36fe465a0332368a7dfbd58c71d

# `conflict_resolution.py`

## Summary
- `cmoc session join` の conflict marker 解消時に適用する instruction 文面の構築定義。
- oracle file を人間所有の正本仕様断片として扱い、conflict 両側と関連 oracle file の意図・挙動を保つ解消方針を示す。
- 両立不能な場合の未解消事項報告と、realization を根拠にした oracle の変更禁止を定める。

## Read this when
- `cmoc session join` の conflict marker 解消方針を確認・変更するとき
- oracle と realization にまたがる conflict の解消手順や判断基準を確認するとき
- conflict 解消時に仕様変更・実装都合の変更を避ける制約を確認するとき

## Do not read this when
- conflict marker 解消を伴わない通常の oracle・realization の仕様確認や実装変更を行うとき
- 個別の conflict 対象ファイルの意味や変更内容を確認するときは、その対象ファイルを直接読む方が適切な場合
- prompt builder の共通構造や構造化文書型の定義だけを確認したいとき

## hash
- af4b2fb532f942e41d2828bb6868b2da5b6ecf41d7f126331931465bcd0e8a9d

# `editor_handoff.py`

## Summary
- 日本語の editor work file handoff 用 instruction 文面を構築する関数を定義する。agent call の file access mode と Codex CLI sandbox を維持しつつ、正式な成果物も満たす handoff ポリシーを返す。
- handoff file への書き込みについては、対象パスと理由を限定した sandbox escalation の許可を定義する。

## Read this when
- agent call から editor work file へ handoff する際のポリシーや instruction 文面を確認・変更するとき。
- handoff 時のアクセスモード、sandbox 維持、正式成果物の扱い、書き込みに伴う escalation の境界を確認するとき。

## Do not read this when
- editor handoff 以外の prompt policy を確認・変更するとき。
- handoff ポリシーの定義ではなく、実際の editor work file の内容や別の prompt builder の基本構造を直接確認すべきとき。

## hash
- 8d2cadc492c24b25da7b026158934bd6167cb3685e35c5e0676ed49f16535eba

# `feedback_reporting.py`

## Summary
- このモジュールは、全 agent call に共通する人間向け feedback 報告ポリシーを構築する。問題報告の対象、必須の報告手段、報告結果をセッション継続判断に使わない制約を、生成されるポリシー見出しとして定義する。
- feedback 報告に関する prompt policy の生成責務を確認したいときの入口であり、他の prompt policy の実装ではなく、この共通ポリシーの内容を確認・変更する場合に読む。

## Read this when
- 全 agent call に適用する human feedback reporting policy の内容や生成方法を確認・変更するとき
- 解決できない問題の報告方法、報告対象、報告結果の扱いに関する prompt policy を調査するとき

## Do not read this when
- 個別の agent call の prompt 全体や、feedback 以外の policy を確認したいとき
- 問題報告ポリシーの利用箇所だけを確認したいときは、呼び出し元または生成された prompt の定義を直接読む

## hash
- 2e55d4370b9b2fb1cc44c56918ab5617a32e14db2a7c9c3fdb73752c170cb951

# `file_access.py`

## Summary
- FileAccessMode と AgentCallPathContext に基づき、エージェント向けのファイルアクセス規定を構築する。リポジトリ外、特定の管理用ディレクトリ、AGENTS.md・INDEX.md・memo、oracle file・realization file などの読み書き制限をモード別に組み立て、パス置換定義と SDHeader を返す。NO_POLICY では空の規定を返す。

## Read this when
- agent prompt に埋め込むファイルアクセス規定の生成・変更条件を確認するとき
- FileAccessMode ごとの oracle file・realization file のアクセス境界を確認するとき
- AgentCallPathContext に応じた repo-root・work-root の制限文面や placeholder 定義の扱いを確認するとき

## Do not read this when
- 個別の oracle file や realization file の内容・仕様を確認するだけのとき
- このポリシーを利用する prompt builder の全体構成を確認したいときは、まずその呼び出し側を読むべきとき
- Structured Output の出力項目や形式だけを確認したいとき

## hash
- 59ab6b0a5b2fe145daa79f1ecfb6009be968f2113ee379f1b4de80f50bb697aa

# `index_entry.py`

## Summary
- INDEX.md 用エントリー生成 agent に適用するルーティング記述規定を構築する。対象の責務・読む条件・適切な境界を意味情報として記述し、推測や本文の過剰展開、機械的情報の記載を避けるための入口となる。

## Read this when
- INDEX.md のエントリーを新規作成・改訂するとき
- 対象を読む条件、責務、同階層の別対象との境界を定めるとき

## Do not read this when
- INDEX.md エントリーではなく、対象ファイル自体の実装内容を理解したいとき
- Structured Output の項目・型・形式だけを確認したいとき

## hash
- 158237fbec2dccc0d98bb33797a17ed819ee5dfd398f77ecfa35d84612ad4303

# `oracle.py`

## Summary
- oracle file を扱う agent call 向け instruction 文面の構築定義。oracle file の作成・変更・レビューに必要な規定を、要求・禁止・許容・補足から成る `SDPolicy` として定義する。
- `build_oracle_policy` は oracle policy 用の `PlaceholderMap` と `SDHeader` の組を返す構築入口である。

## Read this when
- oracle file の作成・変更・レビューに関する instruction の規定を確認するとき。
- oracle policy の要求・禁止・許容・補足や、その構造化文書ヘッダーへの組み立てを確認するとき。

## Do not read this when
- 個別 oracle file の具体的な仕様内容を確認するとき。
- `PlaceholderMap`、`SDHeader`、`SDPolicy` の定義や、プロンプト全体の組み立て順を確認するとき。

## hash
- 5800098e4d5d434167abff89929c70f2751bb450aa20ad8fe6ff801488d0fa65

# `oracle_findings.py`

## Summary
- oracle review の全段階で共有する所見判定ポリシーを構築する関数を定義する。正本仕様間の明確な矛盾や実装者裁量で解決できない問題を fatal とし、誤字・脱字・用語不統一など意味を変えない表記上の問題を minor とする判定基準を、oracle file と realization file を根拠に適用するための入口である。

## Read this when
- oracle file または realization file のレビューで、所見を fatal／minor に分類する基準を確認するとき
- oracle review の各段階に共有される所見判定規定の構築内容や禁止事項を変更・調査するとき

## Do not read this when
- 個別の oracle file や realization file の具体的な仕様・挙動を確認することが目的のとき
- 所見判定ポリシーを使わず、別の prompt builder や構造化文書の定義を直接確認すれば足りるとき

## hash
- f61fa13989fef2784b43119f8af7fd3af7783accec9f16376d640dde5c7ecfb1

# `realization.py`

## Summary
- realization file の作成・変更・レビュー時に、oracle file を人間意図を具体化した正本仕様断片として扱うための規定を構築する。関連仕様との整合、YAGNI、責務重複の整理、検証・テスト、不足時の報告に関する要求・禁止事項・例外を定義し、agent call 用の placeholder 定義とポリシーヘッダーを返す入口となる。

## Read this when
- realization file の実装方針、作成・変更・レビュー規定、oracle file との関係を確認するとき
- realization policy を agent call の instruction に組み込む処理を変更するとき
- realization の検証・テスト、不足報告、YAGNI や重複整理の要求を確認するとき

## Do not read this when
- oracle file 自体の正本仕様を確認するとき
- realization file の具体的な実装内容やテスト実装を直接確認するとき
- agent call の経路情報や placeholder の一般的な定義だけを確認するとき

## hash
- a529650c8990148de613b85bf6468348660c407a88bed594a8be2f24c12ff863

# `realization_oracle_reference.py`

## Summary
- realization code から oracle file path を参照する規定を構築する関数を定義する。realization code の作成・変更時に、対応する oracle file が存在する場合は、コメントへ work-root 起点の oracle file path を記載するためのポリシーと、work-root のプレースホルダー定義を返す。

## Read this when
- realization code に対応する oracle file 参照コメントの記載ルールを確認するとき
- realization code 用の oracle reference policy やプレースホルダー設定を変更・利用するとき

## Do not read this when
- realization code 自体の実装責務や配置規則を確認したいとき
- oracle file の内容や一般的な構造化文書ポリシーを直接確認したいとき

## hash
- 3b5639efb1bd3149ce3b41ca4c00861887207a698f60482363d7db691601645c

# `routing.py`

## Summary
- `build_routing_policy` は、エージェント呼び出しのパスコンテキストから root 定義を取得し、`work-root` をプレースホルダーとして routing policy 文面へ注入する構築処理。`SDHeader` と `SDPolicy` により、INDEX.md の利用目的、起点、本文優先、本文代替禁止などのルーティング規定を定義する。

## Read this when
- INDEX.md による文書・ファイルの探索規定を確認または変更するとき
- `build_routing_policy` の生成する routing policy、root placeholder、`SDPolicy` 構成を調査するとき

## Do not read this when
- 特定の実装ファイルやディレクトリの具体的な責務を確認したいだけで、INDEX.md の利用規定自体を扱わないとき
- `AgentCallPathContext` の root 定義や `PlaceholderMap` の仕様を直接確認する必要があるときは、それぞれの定義元を読む

## hash
- 5900b089dc7c25a67250309c108a0d000e39d6f4fee42bc83e571bcb13b4379d
