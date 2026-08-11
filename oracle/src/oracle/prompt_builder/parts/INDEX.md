# `apply_review_standard.py`

## Summary
- oracle file に対する realization file の追従要否とレビュー所見を判断するための規範を構築する。明確な仕様不整合または realization 側だけで説明できる致命的な実装問題を修正対象とし、根拠となる対象を具体的に示す。

## Read this when
- oracle file の要求に realization file が適合しているか確認するとき
- 仕様不整合や実行不能、明白な致命的バグを修正対象として扱うか判断するとき

## Do not read this when
- 仕様に記述がないことだけを理由に改善案を検討するとき
- 複数の妥当解、好み、推測、一般的なベストプラクティスに基づくコード品質改善を検討するとき

## hash
- 6c2eb183509fcd3e15f0b5975e995b75756e68379bb87996431b4c48b7c9e9e5

# `conflict_resolution_standard.py`

## Summary
- session join の conflict marker 解消に適用する instruction 文面の構築定義。両 branch と関連 oracle file の意味を保つ conflict 解消規範を組み立てる、prompt builder の部品。

## Read this when
- `cmoc session join` の conflict marker 解消用 instruction の内容や適用条件を確認するとき
- conflict 解消規範の requirements と、それを構造化文書へ変換する流れを調べるとき

## Do not read this when
- 通常の session join 処理や conflict 解消の実装動作を調べるとき
- prompt builder の別の instruction 部品を直接調べるとき

## hash
- 2053e0baa0a518f506d48450a8c6b0beafd477bc076577519abb05283d51fcc8

# `feedback_reporting_standard.py`

## Summary
- 全 agent call に共通する、人間向け feedback 報告規範の prompt 部分を構築する。作業外の人間対応で再発防止・浪費削減・意図確定につながる問題だけを報告対象とし、専用 MCP tool による報告後も本来の作業を継続するための標準文面を提供する。

## Read this when
- 全 agent call 共通の feedback 報告ルールや、人間への問題報告用 prompt の生成処理を確認・変更するとき。

## Do not read this when
- 個別 agent call の作業内容や、feedback 保存先の実装を直接確認したいとき。通常の作業内で解決済みの問題や、単なる改善提案を扱うとき。

## hash
- b8637771d4871133e4db01d49c7e6d05f105f213e4d5b819003338d42385066c

# `file_access_rule.py`

## Summary
- agent のファイルアクセスモードに応じた読み書き制限文面を構築する。リポジトリ外、予約領域、oracle/realization file などの禁止規則を共通規則とモード別に組み立て、パス用プレースホルダー定義と構造化文書を返す。
- アクセス規則の生成ロジックや FileAccessMode ごとの制限を確認・変更するときの実装入口であり、実際のファイルアクセス設定や各 oracle/realization file の内容を確認する対象ではない。

## Read this when
- ファイルアクセスモードの追加・変更・検証が必要なとき
- agent 向けの読み書き制限文面、パス境界、oracle/realization file の扱いを調査するとき
- file access rule の戻り値やプレースホルダー定義の生成元を確認するとき

## Do not read this when
- 特定の oracle file や realization file の本文・仕様・実装を調査するとき
- Codex CLI の sandbox 実行規則そのものを確認するときは、対応する正本仕様を読むべきである
- INDEX.md のルーティング情報だけを更新・確認するとき

## hash
- 74be481ba7fd0c5e8a88245c84d926f1893af482cffed83164591005ff59be85

# `index_entry_standard.py`

## Summary
- INDEX.md エントリーが満たすべき規範を構造化して生成する。対象を読むべき条件、対象固有の責務、適切な入口、対象外となる境界を定義する。
- エントリーには対象本文から根拠を持って言える情報だけを含め、推測による責務の拡張や詳細説明を避ける。
- 機械的に補える識別情報や出力形式の説明を除き、ルーティング判断に必要な意味情報だけを提供する。

## Read this when
- INDEX.md エントリーの規範や生成基準を確認・変更するとき。
- 対象を読むべき条件、責務、他の対象ではなく対象へ進む理由を判断するとき。
- エントリーに含める情報の範囲や、対象を読まなくてよい境界を確認するとき。

## Do not read this when
- 具体的な対象の実装内容や個別仕様を直接確認することが目的のとき。
- 既存の INDEX.md のルーティングだけで目的の対象を特定でき、エントリー生成規範を確認する必要がないとき。
- Structured Output の形式や機械的な識別情報だけを確認したいとき。

## hash
- 871f8990511d3d804e6ce7e1763bf3eefd5ae27f3f63c1e68d19b2624b3adaa3

# `oracle_and_realization_basic.py`

## Summary
- 対象ファイルは、oracle と realization の定義・役割・下位分類を、動的な work-root 定義を用いて構築するプロンプト部品です。呼び出し元へは PlaceholderMap と StructDoc の組を返し、oracle/realization の基本説明を組み立てる入口になります。

## Read this when
- oracle と realization の基本概念を説明するプロンプト生成や、その文面・構造を変更または確認するとき。
- AgentCallPathContext からルート定義を取得し、StructDoc とプレースホルダーの組を返す処理を追跡するとき。

## Do not read this when
- 特定の oracle 文書や realization 実装の内容そのものを調べるとき。
- プロンプト部品の選択・組み合わせだけを調べるときは、該当する prompt builder の呼び出し元を直接読む。

## hash
- 3ebaefdba6473a30c6510a47642027979a34061132dd26b4472f8c5c11321d7d

# `oracle_review_standard.py`

## Summary
- oracle review の所見判定規範を構築する関数を提供する。oracle file のレビューで fatal・minor として扱える問題の成立条件、根拠の境界、適用条件を構造化文書としてまとめる。

## Read this when
- oracle review の所見を列挙・統合・検証・採否判定する agent 向けの共有基準を確認するとき。
- fatal と minor の判定条件や、oracle file の具体的記述に基づく所見の境界を確認するとき。

## Do not read this when
- レビュー基準そのものではなく、個別の oracle file の内容や実装適合性を確認したいとき。
- 構造化文書の一般的な構築方法や placeholder の扱いだけを確認したいとき。

## hash
- 245f8307112102d50bc9ed8fc79281a2823d0760048f6b57b48d0050b4d46b0a

# `oracle_standard.py`

## Summary
- oracle file を扱う agent call 向けの標準規範を構築する。oracle を正本仕様として扱い、実装からの逆算を避け、仕様間の整合性・優先関係・用語・検索性を保つための要求を StructDoc として返す。
- AgentCallPathContext から call-scoped な work-root 定義を取得し、標準文書とともに PlaceholderMap を生成する。oracle file の作成・変更・調査・レビューに関する instruction 文面へ組み込む入口である。

## Read this when
- oracle file に関する agent call の規範、作業条件、または instruction 文面の生成経路を変更・調査するとき
- build_oracle_standard が返す placeholder と StructDoc の構造、適用条件、要求項目を確認するとき
- oracle を正本仕様として扱うルールや、仕様の隙間・整合性・検索性に関する標準を確認するとき

## Do not read this when
- realization file の実装規範だけを確認する場合
- oracle 固有の標準文面ではなく、agent call のパス情報や一般的な prompt builder の構造だけを調査する場合
- 既存の INDEX.md エントリーやルーティング情報そのものを確認する場合

## hash
- a99341abd7ea1375fde6549f8cb8915b498fa4df392fb8087640ca802ff1de47

# `realization_oracle_reference_rule.py`

## Summary
- realization code から参照すべき oracle file path をコメントへ記載する規則を、agent call のパス文脈から構築する関数。placeholder map と構造化文書を返し、realization 実装時の oracle 参照ルールをプロンプトへ組み込む。

## Read this when
- realization code の作成・変更時に、対応する oracle file path をコメントへ記載する規則を確認したいとき。
- agent call の root placeholder 定義と、realization oracle reference rule の構造化文書生成方法を確認したいとき。

## Do not read this when
- realization code の具体的な実装内容やテスト方法を確認したいとき。
- oracle file の仕様本文や、プロンプト構築の別ルールを直接確認したいとき。

## hash
- 79789b9f78302eb267516c71cb34589e6f94c8b1408c4e2b2d5a691b9dbe0124

# `realization_standard.py`

## Summary
- realization file を作成・変更・レビューする agent call に適用する規範本文を、call-scoped な work-root 参照とともに構築する。oracle file への適合、不要な実装や公開面を増やさない最小実装、repository 固有手順による検証を扱う。realization 作業向け instruction 生成の入口となる。

## Read this when
- realization file の作成・変更・リファクタ・レビューに関する agent call の規範生成を確認するとき
- oracle と realization の責務分離、最小実装、repository 固有の検証手順を含む標準の構築元を確認するとき

## Do not read this when
- INDEX.md のルーティング情報だけを確認したいとき
- realization file 自体の具体的な実装や個別のテスト内容を確認したいときは、対象の実装またはテストへ直接進む

## hash
- b1829faebcfd080351d1b0f7625f49471a6e6d15f2ecc8aefe7caf4a0e52eba5

# `routing_rule.py`

## Summary
- INDEX.md を使った本文へのルーティング規則を構築するプロンプト部品。作業対象に近い INDEX.md から読み始め、Summary・Read this when・Do not read this when で候補を絞り、必要な本文へ進む手順を定義する。下位階層の INDEX.md の利用と、INDEX.md より本文を優先する判断も扱う。

## Read this when
- INDEX.md の読み進め方や、関連する本文を routing 情報で絞る仕組みを確認するとき。
- プロンプトへ埋め込む routing rule の内容や、work-root の参照方法を変更するとき。

## Do not read this when
- 特定の INDEX.md の既存エントリーや本文を確認したいとき。
- routing 以外のプロンプト部品の生成規則を確認したいとき。

## hash
- 2ebd20e0c920860904622c216abda854150d36a13101df2052f3da03e5389295
