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
- cmoc のファイルアクセス規則プロンプトを構築する。アクセスモードに応じた deny rule と、repo-root/work-root のプレースホルダー値を生成する。各モードの規則分岐と、特別な NO_RULE の空出力を確認する入口となる。

## Read this when
- ファイル読み書き規則の生成内容を変更・確認するとき
- FileAccessMode ごとのアクセス制約やプレースホルダー展開を調査するとき

## Do not read this when
- 実際の CLI 処理やプロンプト全体の組み立てを調べるとき
- oracle の設計・テスト規則だけを確認したいとき

## hash
- 8f9a2394a870d7a8de6759fd731a09e870aede864dfeddc1c5f832d5bb1aa84c

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
- oracle file と realization file の定義・役割・下位概念を構築する prompt builder の一部。oracle、realization の責務境界と配置先を説明する StructDoc を返す。

## Read this when
- oracle file と realization file の分類、責務、配置先を確認するとき
- oracle と realization に関する基本説明文の生成処理を変更・調査するとき

## Do not read this when
- 個別の oracle doc・src・test の仕様や実装を確認したいとき
- prompt builder 全体の構成や、基本説明以外の prompt 部品を確認したいとき

## hash
- 52d5324d5a026e9a98b5f944af4b667e19d4b114dd9cf1e66a40c111d3521ea6

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
- oracle file が従うべき標準規範を、構造化文書として構築する実装。人間の認知負荷、仕様断片の正本性、未定義部分、整合性、用語・命名、実装との責務境界、goal/non-goal などの原則を標準項目として定義し、prompt builder が利用できる形式へ変換する。

## Read this when
- oracle file の記述方針や品質基準を変更・確認するとき
- oracle standard を prompt に組み込む処理や構造化文書の生成方法を調査するとき
- oracle file に関する規範項目の追加・削除・整合性を検討するとき

## Do not read this when
- realization code の一般的な実装規約だけを確認するとき
- oracle file の具体的な仕様内容や個別ドキュメントを調査するとき
- prompt builder の他の部品や placeholder の挙動だけを調査するとき

## hash
- 44a731f03bef07e78578477f06d0911569244875809ae1c0d17c7dc9f57b6df2

# `realization_standard.py`

## Summary
- realization file が従うべき規範文章を、複数の Standard として構築する prompt builder 部品。実装の簡潔性・品質・責務分割・oracle src との重複防止・コメント方針・テストや依存関係の肥大化抑制・変更後の整理を扱う。realization standard の prompt 生成処理を確認する入口。

## Read this when
- realization file の実装規範を prompt に組み込む処理を変更・調査するとき
- realization code、test、依存関係、公開面、コメントに関する標準文面の生成元を確認するとき

## Do not read this when
- oracle standard や index entry standard など、別の規範文章の生成処理だけを確認するとき
- prompt builder の共通基盤や StructDoc の実装を直接調査する場合は、まず該当する共通モジュールを読むとき

## hash
- 5dbc1cb4f5d03990e3486c70f90a0bf811d01efbbc2740d4155b8f70d2bc5478

# `routing_rule.py`

## Summary
- INDEX.md を使った文書ルーティング規則の構築処理を定義する。作業対象に応じて読むべき INDEX.md や本文を選ぶための案内文と、work-root のプレースホルダー値を生成する。

## Read this when
- INDEX.md の役割、読み進め方、対象文書の選択基準を確認したいとき。
- プロンプトへ work-root を埋め込むルーティング規則の生成処理を変更・確認するとき。

## Do not read this when
- 特定の INDEX.md の実際のエントリー内容を確認・編集したいとき。
- ルーティング規則以外のプロンプト部品や、文書構造そのものを確認したいとき。

## hash
- 0264980cdd927da5be0d9580428c1d9fb3a129f66b254b0d462d7be9cbd1af5b
