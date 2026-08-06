# `apply_review_standard.py`

## Summary
- oracle file に対する realization file の適合性判定規範を構築する実装。明確な仕様不整合や実行不能な致命的バグを修正対象とし、根拠を具体化する。
- oracle file に明記されない実装詳細、好み、推測、一般的な改善案だけでは修正対象にせず、realization の挙動を oracle 仕様へ逆流させないための適用基準を定義する。
- oracle の要求に対する realization の追従要否、所見、修正内容を判断する処理を調べる際の入口。

## Read this when
- oracle file と realization file の適合性、追従要否、レビュー所見、修正対象の判定規範を確認するとき
- apply review standard の構造化文書や、その構築に使われる Requirement・Standard の扱いを変更または調査するとき

## Do not read this when
- 一般的なコード品質改善やベストプラクティスのレビューだけを行うとき
- oracle の適合性判定ではなく、別の prompt builder 部品や realization 実装そのものを直接調査するとき

## hash
- bf29bea4168dbc8d59d7d6c3d0e676ff93f39a6d6fc6dd2ed4465862df7f5c0c

# `conflict_resolution_standard.py`

## Summary
- session join における conflict marker 解消専用の規範を構築する oracle source。両 branch の意図と挙動を保ち、conflict 解消に不要な変更を禁止し、判断不能な場合は未解消事項として報告する要件を構造化文書へ変換する。

## Read this when
- `cmoc session join` の conflict marker 解消ルールや適用条件を確認するとき
- conflict 解消用の prompt または規範構造を変更・レビューするとき

## Do not read this when
- conflict 解消以外の session 処理を確認するとき
- 一般的な oracle / realization 規範の定義を確認するときは、対応する標準定義を直接読む

## hash
- c9e43334d126ed735a55807763442ee34292bfe17bfa2545c8e84e166b4d7c91

# `feedback_reporting_standard.py`

## Summary
- 全 agent call に共通する、人間向け feedback 報告規範のプロンプト断片を構築する。root の placeholder 定義から repo-root を取得し、報告条件・提出方法・報告後の継続方針を StructDoc として返す。

## Read this when
- agent call 共通の人間向け feedback 報告規範を変更・確認するとき
- prompt builder の feedback reporting 部分や、repo-root placeholder の受け渡しを調査するとき

## Do not read this when
- 個別の agent call の役割・作業概要・完了条件だけを確認したいとき
- feedback 保存 file の形式や reporter の具体的な入力方法を確認したいときは、reporter の describe を直接読むべき場合

## hash
- f094e8e7a6c495e5faca43d968f6a1eb2f0ad2dde7fe72fd6701a2ff681137f2

# `file_access_rule.py`

## Summary
- ファイルアクセスモードに応じた、AI エージェント向けの読み書き禁止規則を構築する。リポジトリ外、管理対象ディレクトリ、AGENTS.md・INDEX.md・memo、oracle file・realization file などのアクセス制約をモード別に組み立てる。
- ファイルアクセス規則の文面とプレースホルダー定義を生成する責務を持つ。アクセス権限の実行環境設定そのものではなく、プロンプトに使用する規則文面の入口である。

## Read this when
- AI エージェントのファイル読み書き規則を変更・確認するとき
- FileAccessMode ごとの oracle file・realization file のアクセス制約や、パスプレースホルダーの生成を調べるとき
- リポジトリ外アクセスや .git・.agents・.codex・.cmoc・memo への制約文面を調べるとき

## Do not read this when
- 特定のサブコマンドや機能の実装責務を調べるとき
- Codex CLI の sandbox 設定や実行権限の正本仕様を調べるときは、対応する oracle 文書を先に確認する
- INDEX.md の生成・更新処理そのものを調べるとき

## hash
- 16cc4569cb6d50750e5f0012d24a558b04cf8ffd01192ef3e51498a4e005b8f9

# `index_entry_standard.py`

## Summary
- INDEX.md エントリーが満たすべき規範文書を生成する。対象の責務、内容に基づくルーティング、機械的情報を含めない方針を定義する。

## Read this when
- INDEX.md のエントリーを新規作成・更新するとき
- 対象を読むべき条件、対象の責務、他対象との境界を判断するとき
- エントリーに含める情報の粒度や、対象内容に基づく根拠を確認するとき

## Do not read this when
- INDEX.md エントリー以外のプロンプト生成規範を確認するとき
- 対象ファイル固有の実装内容や、一般的な StructDoc の構造を確認するときは、対応する実装・定義を直接読む

## hash
- 942b23384c6e0468b807b626d94ad638b8898badc3a7dd37cd5cb0a8f771ddce

# `oracle_and_realization_basic.py`

## Summary
- oracle と realization file の定義・役割・下位概念を構築する prompt builder の一部。oracle file を人間所有の正本仕様断片、realization file をその具体化として整理し、doc・src・test・implementation・ancillary の分類と配置を説明する。

## Read this when
- oracle file と realization file の定義や責務境界を prompt に組み込む処理を変更するとき
- oracle、realization の分類・配置・正本性に関する説明文の生成元を確認するとき

## Do not read this when
- 個別の oracle 文書や realization 実装の内容を確認したいとき
- prompt builder 全体の構成や別の prompt part の仕様だけを調べるとき

## hash
- 46cac8d7867434199021d72041b4b1b9eea45f91fbb845ee3e177089d3dde021

# `oracle_review_standard.py`

## Summary
- oracle review 全段階で共有する所見判定規範を構築する正本実装。fatal・minor・所見なしの判定境界、根拠の要件、適用条件を定義する。

## Read this when
- oracle file の所見を列挙、統合、検証、擁護・反証理由の整理、または採否判定するとき
- fatal と minor の判定基準や、仕様の具体的記述に基づく所見の成立条件を確認するとき

## Do not read this when
- oracle review の所見判定を扱わず、一般的な仕様規範や別の prompt builder 部品だけを確認するとき
- 所見判定規範そのものではなく、Requirement・Standard・StructDoc のデータ構造や変換処理を確認するとき

## hash
- 831f63ed0ce47db11c675b76a03db06362fba62446e299ea7d6e6858f6d5a3e6

# `oracle_standard.py`

## Summary
- oracle file の作成・変更・調査・レビューに適用する規範を、call-scoped な work-root 定義とともに構築する。oracle file を正本仕様断片として扱うこと、仕様の隙間を過剰に埋めないこと、実装から仕様を逆算しないこと、仕様間の整合性・用語統一・検索性を保つことを定義する。

## Read this when
- oracle file に関する規範の構築・変更・適用条件を確認するとき
- oracle file と realization file、既存実装、installed skill の優先関係を判断するとき
- 正本仕様断片の追加・変更に伴う境界、整合性、用語統一を確認するとき

## Do not read this when
- realization file の実装やテスト自体の設計・変更だけを行うとき
- oracle file に関する規範ではなく、個別の oracle file の内容を確認するとき

## hash
- 4c37309fee606d2905ef28dca1322a86d786d78aa8c90e7211995a02079364ed

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
- realization file の作成・変更・レビュー時に適用する規範を、対象 repository の work-root 定義とともに構築する。
- oracle file への適合、不要な実装や公開面の抑制、repository 固有手順による検証という3領域を扱う。
- realization file の作業規範を注入する prompt builder 部品への入口である。

## Read this when
- realization file の作成、変更、リファクタ、またはレビューに適用される規範を確認するとき
- oracle file と realization file の責務境界、重複禁止、参照・生成・変換の扱いを確認するとき
- 対象 repository 固有の手順による検証要件を確認するとき

## Do not read this when
- oracle file 自体の仕様を作成・変更するとき
- INDEX.md のルーティング規則そのものを確認するとき
- realization file に関係しない prompt builder の部品を調査するとき

## hash
- 72ee123baa624d77b27881c41104fb4d31a59634b2faf3b7dcf83de77fe9dbea

# `routing_rule.py`

## Summary
- INDEX.md を使って必要な本文へ進むためのルーティング規則を構築する関数を定義する。call-scoped context から work-root の定義を取得し、INDEX.md の扱い・読み進め方・判断基準を含む構造化文書とプレースホルダ map を返す。

## Read this when
- INDEX.md の役割、読み進め方、対象本文へ進む判断基準を変更・確認するとき
- routing rule の構造化文書生成や work-root プレースホルダの扱いを変更するとき

## Do not read this when
- INDEX.md の個別エントリー内容や対象ファイルの責務を確認したいとき
- ルーティング規則以外の prompt builder 部品を変更・調査するとき

## hash
- bd6e9b76921aaddbccba9336ae77740768a301b4cc6026b3083008a25e525d14
