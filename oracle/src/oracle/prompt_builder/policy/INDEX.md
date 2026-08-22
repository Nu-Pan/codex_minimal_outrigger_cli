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
- エージェント向けファイルアクセス方針の文面を、アクセスモードとパスコンテキストに基づいて構築する関数。リポジトリ外、特定の管理用ディレクトリ、oracle・realization file などの読み書き制限をモード別に定義し、プレースホルダー定義と構造化された方針ヘッダーを返す。

## Read this when
- エージェントへのファイルアクセス制限の生成・変更・検証が必要なとき
- FileAccessMode ごとの読み書き禁止範囲や、repo-root と work-root の扱いを確認するとき
- build_file_access_policy の戻り値やパスプレースホルダー連携を調べるとき

## Do not read this when
- 具体的な oracle builder や realization の実装責務だけを確認したいとき
- アクセス方針を利用するプロンプト生成全体の仕様を確認したいときは、まずそのプロンプト生成側の対象を直接読むとき
- ファイルアクセス制限と無関係な CLI 機能やデータモデルを調べるとき

## hash
- 06894151f163b3a7e05b1dc554b5d9e53fab67ba13230873213a3e67e7ff45ee

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
- oracle file を扱う agent call 向けの instruction 文面を構築する定義。oracle file の要件・禁止事項・許容事項を SDPolicy としてまとめ、oracle policy 用の SDHeader と PlaceholderMap を返す。oracle policy の構造や規定を変更・調査するときの入口となる。

## Read this when
- oracle file の作成・変更・レビューで、oracle file に適用する基本規定を確認するとき
- agent call 向けに oracle policy の instruction 文面を構築するとき
- oracle file と realization file の責務境界、goal・non-goal、未定義事項の扱いを確認するとき

## Do not read this when
- 個別の oracle file の内容や仕様断片を確認したいとき
- プロンプト構築全体や PlaceholderMap の一般的な扱いを確認したいとき
- realization file の実装責務だけを調査するとき

## hash
- 067b8c499d5b1986fe6da154a2bb0ce7df6b9d5bf82fdbf8422d0a23ac25b820

# `oracle_findings.py`

## Summary
- oracle file に対する所見の判定基準と禁止事項を構築する関数。所見の根拠、fatal・minor の分類条件、基準の一貫性を定義し、oracle と realization の記述を評価するルーティングの入口となる。

## Read this when
- oracle file や realization file に対する所見・レビューの妥当性を判定するとき
- fatal または minor 所見の分類基準、所見の根拠、禁止事項を確認するとき

## Do not read this when
- 所見の判定基準ではなく、個別の oracle file や realization file の内容を直接確認するとき
- プロンプト構築やプレースホルダーの一般的な実装を確認するとき

## hash
- 3a50423e45dc80af6c6ebe86c5be6c28dc9719ef8ce932457043afec1d5a83de

# `realization.py`

## Summary
- 対象は、realization file を扱う agent call 向けの instruction 文面を構築する関数を定義する。パス文脈から placeholder 定義を取得し、realization policy という見出しと、oracle file を正本仕様断片として扱う規定・実装上の裁量・YAGNI・重複整理・検証義務などの要求／禁止／許可事項をまとめた SDHeader を返す。

## Read this when
- realization file に関する agent call の instruction 文面、特に oracle と realization の責務境界や実装・テスト・検証の規定を確認または変更するとき。
- realization policy の要求・禁止・許可事項、または path placeholder の注入元を追跡するとき。

## Do not read this when
- realization file 自体の具体的な実装内容やテストを確認したいときは、該当する realization file や test を直接読む。
- oracle file の正本仕様そのものを確認したいときは、対応する oracle file を直接読む。
- agent call の一般的な prompt 構築や別種の policy を確認したいときは、該当する prompt builder／policy 対象へ直接進む。

## hash
- af7f068631559b63749e87c61c2bf35f09d18d986f357c5962c414a6a6b1ed2d

# `realization_findings.py`

## Summary
- oracle file と realization file の記述・挙動の適合性を判断するための所見ポリシーを構築する関数。所見の根拠、修正対象となる不整合・致命的問題、適用基準の一貫性を定義する。realization file に対するレビュー方針を組み立てる入口となる。

## Read this when
- oracle file の具体的な要求と realization file の具体的な挙動が不整合しているか確認するとき
- realization file 上に明確な致命的問題があるか判定するとき
- realization file に対する所見の根拠と適用基準を確認するとき

## Do not read this when
- oracle file 自体の定義不足や問題を検討するとき
- 規定上必須でない事項の改善点や一般的なコード品質を検討するとき
- realization file の実装内容を直接確認するときは、対象の realization file を先に読むべき場合

## hash
- 416190c9767555b83c10a4cb267bd07d1d4ceede09f2e680e425db2c7a359b3c

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
