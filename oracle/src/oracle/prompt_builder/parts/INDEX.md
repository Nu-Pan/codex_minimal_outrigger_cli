# `apply_review_standard.py`

## Summary
- oracle file と realization file の不整合、および realization file 単体で明らかな致命的問題を所見として扱うためのレビュー規範を構築する。仕様の隙間だけを理由に所見化しない判断基準や具体例も含む。

## Read this when
- oracle file を realization file に適用した結果のレビュー所見を列挙・評価するとき
- oracle file との不整合、仕様の隙間、実装単体の致命的問題を区別する必要があるとき

## Do not read this when
- レビュー所見の列挙ではなく、oracle file の一般原則や realization file の実装そのものを確認するとき
- 構造化ドキュメントの共通定義やプロンプト生成処理を直接調査するとき

## hash
- 0c69d41cfb94d57df0d3e1e59249241820ca832705e149d3377718c0e781ed84

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
- `cmoc oracle review` が所見を列挙する際の規範文章を構築する。fatal・minor として扱う問題の境界、および oracle file だけでは問題と言い切れない事項を所見にしない原則を、背景・要求・例として StructDoc に変換して返す。

## Read this when
- `cmoc oracle review` のレビュー基準や所見分類を変更・確認するとき
- fatal と minor の判定基準、仕様の隙間の扱いを確認するとき
- oracle file のレビュー用プロンプトを生成・修正するとき

## Do not read this when
- oracle review 以外のプロンプト部品を変更・確認するとき
- 実際の oracle file の内容やレビュー対象を調査するときは、対象の oracle file を直接読む
- StructDoc や Standard の共通実装自体を変更・確認するときは、それらの定義ファイルを直接読む

## hash
- 64ee7071e9eab5d4ea0a841855aef097148772882131514e1f967b84d31a036b

# `oracle_standard.py`

## Summary
- oracle file が従う規範文章を構築する。人間の認知負荷を抑えた疎な正本仕様断片、未定義部分の扱い、仕様間の整合性、実装からの逆流禁止、用語・命名の統一、oracle file 優先、goal/non-goal の境界などを Standard として StructDoc に変換する。
- AgentCallPathContext から root 定義を取得し、`work-root` プレースホルダーを返却する。

## Read this when
- oracle file の規範、仕様断片の書き方、正本仕様と実装の責務境界を確認するとき
- oracle standard の構造化文書生成や Standard 定義を変更するとき

## Do not read this when
- realization code の具体的な動作や CLI 機能を調査するとき
- oracle file の規範ではなく、他の prompt builder 部品や個別仕様を確認するとき

## hash
- a4591683096c830a9d8f57525436de044e2788180a22c06caf4f4a53aae4d57b

# `realization_standard.py`

## Summary
- realization file が従うべき規範文章を構築する。実装・テスト・コメント・ファイル分割・抽象化・公開面・依存関係・不要な旧実装の整理に関する標準を、背景・要求・例を含む構造化文書として提供する。
- realization standard の生成時に call-scoped context から work-root 定義を取得し、各規範文書へプレースホルダーを渡す。

## Read this when
- realization file、realization code、realization test の品質基準や削除・統合方針を確認するとき
- oracle src と realization src の責務境界、コメントや docstring の根拠記載、ファイル分割・抽象化の判断基準を確認するとき
- 公開面・設定・状態・依存関係・生成物を追加する可否や、変更後の整理方針を確認するとき
- realization standard を構築する処理や、その出力に含まれる標準項目を変更するとき

## Do not read this when
- INDEX.md のルーティング規則やエントリー形式だけを確認したいときは、INDEX.md 関連の対象を直接読む
- oracle の正本仕様そのものや Python 実行環境・テスト実行方法を確認したいときは、対応する oracle 文書を直接読む
- 特定の realization 実装・テストの挙動を調査するだけで、realization file 全般の規範を確認する必要がないとき

## hash
- 667977a7edea2e30fa8684ad26e1d89dd9beb3b51f82bb4cd987a93871281d71

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
