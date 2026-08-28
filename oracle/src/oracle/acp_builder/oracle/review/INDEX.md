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
- 対象は oracle review の「新規所見列挙」エージェント呼び出しを組み立てる定義で、レビュー対象と関連所見を含むプロンプトおよび実行パラメータを構成する。
- oracle file の読み取り専用レビューで、対象 oracle file と関連 oracle file の確認を伴う呼び出し設定への入口。

## Read this when
- oracle review の新規所見列挙で、対象 oracle file・関連所見・実行 worktree を渡す呼び出し設定を確認または変更するとき。
- レビュー用プロンプトの補助情報、パス置換、読み取り権限、Structured Output 設定、インデックス事前処理の構成を追うとき。

## Do not read this when
- 新規所見の内容やレビュー判定基準そのものを確認したいときは、レビュー方針や生成された prompt の定義を直接読む。
- oracle review 以外のエージェント呼び出し構築や、Structured Output schema の項目・型だけを確認したいとき。

## hash
- 4754ea9ee8c9110175646e5907e110595f98eedc2fdf45870686777f18ac3fb7

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
- レビュー所見の採否判定を行う oracle review サブコマンド向けに、判定担当エージェントへ渡すプロンプトと起動パラメータを構築する。
- 所見本文と、妥当性を支持・反対する理由を動的プロンプトへ組み込み、oracle の純粋読み取り条件・ルーティング条件・所見ポリシーを適用した呼び出し定義を返す。

## Read this when
- oracle review で個別の所見を人間へ提示すべきか判定する処理を確認・変更するとき。
- 所見、支持理由、反対理由を含む判定用プロンプトの組み立てや、対応するエージェント呼び出し条件を確認するとき。

## Do not read this when
- 所見採否判定そのものではなく、一般的な oracle review や別種のレビュー処理を確認するとき。
- 判定用プロンプトの構築ではなく、Structured Output schema の定義や判定結果の後続処理を直接確認するとき。

## hash
- eaee631c01bebf4c436629cf150aad6d33580e1ec5de62e5eafbff4ef2098c12

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
- oracle review の所見リストを整理する agent call の prompt と起動パラメータを構築する入口。所見同士の内容的な重複・相互矛盾を解消する整理処理へ進むために読む。

## Read this when
- oracle review の所見を統合する agent call の指示文、oracle 専用の読み取り範囲、または起動時パラメータの構築を確認・変更するとき。

## Do not read this when
- 所見の判定基準やレビュー規則そのものを確認したいとき。所見の出力形式だけを確認したいとき。通常の oracle review 実行処理や、別種の agent call パラメータを扱うとき。

## hash
- ab7b7642d6c0519f4aa8c535bd0aa72162dd99bf1f23980f90e1eaef3f47a792

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
- oracle review で、特定の所見が妥当である理由を調査する agent call の prompt と起動パラメータを構築する。
- 所見、既知の擁護理由、既知の反論理由を prompt に組み込み、oracle の読み取り専用レビューとして実行するための設定をまとめる。

## Read this when
- oracle review の所見について、妥当性を擁護する理由を列挙する agent call の構築や変更を行うとき。
- 所見と既知の賛否理由を入力にした oracle review の prompt 生成経路を確認するとき。

## Do not read this when
- 所見の妥当性そのものを評価する実装やレビュー結果の処理を確認したいときは、対応するレビュー評価・結果処理の対象を直接読む。
- 一般的な agent call の共通 prompt 構築規則や oracle の読み取り制約を確認したいだけのとき。

## hash
- 9c12b0a8bf0cd7ddbf3545a228e7853f87fdf6d3386ea7a0dcc7b943b46b9a4d

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
- oracle review の所見について、妥当ではない理由を列挙するエージェント呼び出しのプロンプトと起動パラメータを構築する。
- 対象所見、既知の妥当性支持理由、既知の反証理由をプロンプトへ渡し、oracle 専用の読み取り制約と構造化出力を設定する。

## Read this when
- oracle review の所見に対する反証調査のエージェント呼び出し仕様を確認・変更するとき。
- 反証担当へ渡す入力情報や、oracle review 用のファイルアクセス・ルーティング・起動設定を確認するとき。

## Do not read this when
- 所見の妥当性を支持する理由の列挙や、別の review 判定処理だけを確認したいとき。
- プロンプト構築ではなく、反証結果のスキーマや所見レビューの実行本体を直接確認すべきとき。

## hash
- 3143d7fdb95ba802ecb7118259f40481608b7e23b2732c6a78639f7533db96cb
