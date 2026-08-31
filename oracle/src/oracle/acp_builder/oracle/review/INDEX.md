# `enumerate_finding.json`

## Summary
- 対象は oracle review の所見列挙エージェント呼び出しで使う Structured Output スキーマです。レビュー対象・関連 oracle file から、既知の所見と重複しない新規所見を列挙するための出力契約を定義します。
- 出力は findings 配列で、各所見に重大度、短い見出し、主な根拠となる oracle file のパス、新規所見として扱う理由を持たせます。

## Read this when
- oracle review の所見列挙 agent call の出力形式や、レビューで報告する所見オブジェクトの必須情報を確認するとき。
- 新規所見の重複排除を含むレビュー結果の Structured Output 契約を確認するとき。

## Do not read this when
- oracle review の所見列挙以外の agent call の出力形式を確認するとき。
- レビュー所見の具体的な判定基準や oracle file 本文の内容を確認したいときは、対象のレビュー規則や oracle file を直接読むべきです。

## hash
- e6670ec1bd6de1695a325c6ba5caa9e59d0c113e1ec184cd9ce1e472b3cafea8

# `enumerate_finding.py`

## Summary
- `cmoc oracle review` の新規所見列挙用 agent call を構築する。
- レビュー対象 oracle file、関連所見、実行 worktree を基に prompt、ファイルアクセス設定、構造化出力 schema、索引 preflight 付きの起動パラメータを組み立てる。
- prompt には oracle ツリー調査、関連所見との重複回避、oracle review・所見・ルーティングに関する共通ポリシーを適用する。

## Read this when
- `cmoc oracle review` で、既知の関連所見と重複しない新規所見を列挙する agent call の prompt や起動パラメータを確認するとき。
- oracle file のパス、oracle root、agent call の作業ディレクトリを prompt 用の実パスへ解決する処理を確認するとき。
- 新規所見列挙用 call の oracle 専用読み取り権限、構造化出力、indexing preflight の設定を確認するとき。

## Do not read this when
- レビュー対象 oracle file の内容や関連 oracle file の規定そのものを確認したいとき。
- 共通 prompt 生成、パスモデル、構造化文書レンダリング、agent call の基底型の実装を直接調べるとき。
- 所見の保存・表示・判定や、出力 schema の項目定義だけを確認したいとき。

## hash
- e325827f7087e4ffef3a5d2e3b6fa390b783b16714936fc45254c043febd6507

# `judge_finding.json`

## Summary
- 対象は oracle review の所見採否判定 agent call が返す構造化出力を定義する JSON Schema です。所見を人間への確認項目として提示するかどうかを `accept` / `reject` で判定し、その具体的理由を併記します。
- review 配下で、所見の採否判断と理由の出力契約を確認する入口です。

## Read this when
- oracle review の所見を人間へ提示するか採否判定する処理や、その agent call の出力契約を確認・変更するとき。
- 判定結果の値と、採否理由を受け取る側の実装・仕様を追跡するとき。

## Do not read this when
- 所見そのものの生成・レビュー内容・人間への提示処理を直接確認する場合は、それぞれの実装または仕様ファイルを直接読むとき。
- review 以外の agent call の出力契約を確認する場合。

## hash
- 1f7d8a770b624965f162383f1199ef63e5d742ac3f68d4b739b78685857b7bd9

# `judge_finding.py`

## Summary
- oracle review の所見を人間へ提示すべきか判定する agent call の prompt と起動パラメータを構築する。
- 所見本文と、妥当性を支持・反証する理由を判定用 prompt に組み込む oracle review の入口。

## Read this when
- oracle review の所見採否判定に使う agent call の prompt 構成や起動パラメータを確認するとき。
- 判定対象の所見、支持理由、反証理由をどのように agent call へ渡すかを確認するとき。
- PURE_ORACLE_READ、oracle の所見報告方針、ルーティング方針を適用する判定呼び出しの設定を確認するとき。

## Do not read this when
- oracle review の所見そのものの内容や、採否判定の結果を確認したいとき。
- 所見採否判定用 agent call が返す構造化出力の項目やスキーマを確認したいときは、対応する JSON schema を直接読む。
- oracle review 全体のレビュー処理や、所見の生成・検証ロジックを確認したいときは、それぞれの担当対象を直接読む。

## hash
- 53f16da7a6b6bedf88c5d4e7d2f6fec7f1138e3b183f4fc96478a5c8e6a611ab

# `merge_finding.json`

## Summary
- oracle review の所見整理 agent call が返す編集操作の Structured Output schema。入力所見の重複や矛盾を解消するため、削除・単一所見の置換・複数所見の統合を表す。
- 置換・統合後の所見には、重大度、問題の短い見出し、主な根拠となる oracle file のパス、整理理由を指定する。

## Read this when
- oracle review の所見リストを重複・矛盾なく整理する agent call の出力形式を確認するとき
- delete、replace、merge の編集操作や、置換・統合後の finding の必須内容を確認するとき

## Do not read this when
- oracle review の個別所見の内容や判定根拠を確認したいとき
- review agent の実装処理や agent call のプロンプトを確認したいときは、対応する実装・プロンプト定義を直接読む

## hash
- 5923a92dd19bdf2d335a7a650455c2b48c4c68f0662aff06d27f02a0cf7e5be2

# `merge_finding.py`

## Summary
- oracle review の所見リストを統合する agent call の prompt と起動パラメータを構築する定義。
- 所見の重複や相互矛盾を解消する編集操作を決定するための oracle review 用エントリー。

## Read this when
- `cmoc oracle review` で、既存の所見リストを finding_id 単位で整理・統合する処理を確認または変更するとき。
- 所見マージ用 agent call の作業条件、oracle 限定のアクセス権、動的に渡す所見リストを確認するとき。

## Do not read this when
- oracle review の個別所見の内容や判定基準を直接確認したいとき。
- Structured Output の項目定義だけを確認したいとき。
- 所見統合ではなく、通常の oracle review 実行や別の prompt builder の責務を確認するとき。

## hash
- 03a038525b28fc6811c40b0ff169fe30d31d2335225c90aa52098bcef2545e57

# `validate_finding_advocate.json`

## Summary
- 対象所見の妥当性を補強する追加理由を返す、oracle review の擁護理由追加調査 agent call 用 Structured Output schema。既知理由との重複を避け、該当理由がない場合は空配列とする。

## Read this when
- oracle review で、既知理由とは別に対象所見を支持する根拠を追加調査・整理するとき。

## Do not read this when
- 対象所見の擁護理由を追加する必要がなく、別の review 出力や一般的な Structured Output の定義だけを確認するとき。

## hash
- 6ea3f1f1deec3852b1311bc1a06b6ebfdb9542806c46be39c35bee233d3ff870

# `validate_finding_advocate.py`

## Summary
- Oracle review で指定された所見が妥当である理由を調査・列挙する agent call の prompt と起動パラメータを構築する定義。所見、既知の支持理由、既知の反対理由を入力として、oracle のみを読み取り対象にした呼び出し条件を組み立てる。

## Read this when
- `cmoc oracle review` で、特定の所見を支持する根拠の調査用 agent call の構築方法を確認したいとき。
- 所見と既知の賛否理由を prompt に埋め込み、oracle review 用の実行パラメータを生成する処理を変更・調査するとき。

## Do not read this when
- 所見の妥当性そのものをレビューしたいとき。
- oracle review の反証理由の列挙や、別種の agent call パラメータ構築を直接確認したいとき。

## hash
- 96542e56c3f668aaa3010718bfacbd6e0deeb35cf424adc6913758b4e35edd12

# `validate_finding_challenger.json`

## Summary
- oracle review の反証理由追加調査 agent call が返す出力を定義する。
- 既知理由と重複しない、対象所見が妥当ではない理由を収集するための入力形式である。
- 該当する追加理由がない場合も扱えるため、反証理由の調査結果を確認・受け渡しするときの入口になる。

## Read this when
- oracle review で、既知理由とは別の反証理由を追加調査する agent call の出力形式を確認するとき。
- 対象所見が妥当ではない理由の調査結果を処理するとき。

## Do not read this when
- 既知理由や対象所見の具体的な内容を確認するとき。
- oracle review の別の入出力形式や、反証理由の調査ロジック自体を確認するとき。

## hash
- 1da4ac7411e16adb0312f2cc52e660766d29f93a4a9d8e55becdd071b8cf45f6

# `validate_finding_challenger.py`

## Summary
- oracle review の所見が妥当ではない理由を調査する agent call の prompt と起動パラメータを構築する定義。
- 所見、既知の妥当理由、既知の反証理由を入力として、PURE_ORACLE_READ のレビュー検証経路へ進む入口。

## Read this when
- oracle review の所見について、妥当ではない理由を追加調査する agent call の構築方法を確認したいとき。
- 所見と既知の賛成・反対理由を prompt に渡すレビュー検証経路を追うとき。

## Do not read this when
- 所見の妥当性を支持する理由の調査や、通常のレビュー実装を確認したいとき。
- agent call の共通 prompt 構築規則や出力スキーマ自体を直接確認すべきとき。

## hash
- 757d5d3e3c51b55fe92ce8ac2535e8a0e45fbf4f7388918898b6d2d2d4d2431e
