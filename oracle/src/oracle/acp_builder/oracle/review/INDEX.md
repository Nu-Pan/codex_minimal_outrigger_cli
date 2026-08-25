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
- oracle review で新規所見を列挙する agent call の prompt と起動パラメータを構築する。レビュー対象 oracle file、関連所見、実行 worktree を受け取り、oracle 読み取り専用・所見列挙・ルーティング等の方針を組み込んだ呼び出し定義を生成する。

## Read this when
- `cmoc oracle review` の新規所見列挙処理における prompt 内容や agent call パラメータの構築を確認・変更するとき。
- レビュー対象 oracle file と既知の関連所見を prompt に渡す仕組み、または oracle review 用の実行コンテキストを確認するとき。

## Do not read this when
- oracle review の所見スキーマ自体を確認したい場合は、対応する JSON schema を直接読む。
- レビュー実行そのものや、oracle file の内容・レビュー規則を確認したい場合は、この builder ではなく prompt により参照される oracle 関連定義を読む。

## hash
- 2e54f2f96e2c4ca691a0f8ac41fd6d41d2d23c7805330530b759878190f0aaeb

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
- oracle review の所見採否判定エージェント呼び出しを構築する関数。所見本文と賛成・反対理由をプロンプトへ組み込み、純粋な oracle 読み取り権限、効率重視モデル、最大推論、構造化出力スキーマ、起動前インデックス処理などの実行パラメータを設定する。

## Read this when
- `cmoc oracle review` の所見採否判定プロンプトやエージェント起動パラメータを変更・確認するとき
- 所見、賛成理由、反対理由が判定エージェントへどのように渡されるかを確認するとき

## Do not read this when
- 所見採否判定の出力形式そのものを確認する場合は、同じディレクトリの構造化出力スキーマを直接読むとき
- 一般的なプロンプト組み立て規則や共通のパス・アクセス制御を確認する場合は、それぞれの共通ビルダーやポリシー定義を直接読むとき

## hash
- a4560c43ba1ba148c24543369a07fc5f8d32622180cbd494eca4e4f85803f7b1

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
- oracle review の所見リストを整理する agent call の prompt と起動パラメータを構築する。所見の重複・相互矛盾を解消する編集操作を列挙させ、Structured Output の事後条件として対象 ID の妥当性も指定する。
- `build_oracle_review_merge_finding_parameter` が、所見リスト、oracle-only のファイルアクセス、パスコンテキスト、モデル・推論設定、Structured Output schema、インデックス事前処理をまとめて `AgentCallParameter` として返す。

## Read this when
- oracle review の所見リストを統合する agent call の prompt 内容、アクセス制約、モデル設定、Structured Output schema の指定を確認・変更するとき。
- 所見リストを動的 prompt に埋め込む処理や、各編集操作の対象 ID に関する決定論的事後条件を確認するとき。

## Do not read this when
- oracle review の所見の内容やレビュー規則そのものを確認する場合は、所見統合の起動定義ではなく、対象の oracle policy・findings policy 文書を直接読む。
- 一般的な agent call の基礎型やモデル・アクセスモードの定義を確認するだけの場合は、`oracle.acp_builder.basic` を直接読む。
- Structured Output の具体的な出力項目・型・形式を確認する場合は、併設された JSON schema を直接読む。

## hash
- 48bca7f28b0818fdd76279a2fa6ee16922f71be21afe037fca616ff2bf70b98f

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
- oracle review で、指定された所見が妥当である理由を調査するためのエージェント呼び出しパラメータを構築する。所見、既知の擁護理由、既知の反論理由をプロンプトへ埋め込み、oracle のみを読むレビュー方針と Structured Output schema を設定した `AgentCallParameter` を返す。
- このファイルは、対象所見の妥当性を擁護するレビュー用 prompt の内容と、効率重視モデル・最大推論 effort・事前インデックス実行などの起動条件を定義する。レビュー処理そのものや所見の判定ロジックは担当しない。

## Read this when
- `cmoc oracle review` における所見擁護エージェントの prompt または起動パラメータを変更・確認するとき
- 所見、既知の擁護理由・反論理由がレビュー用 prompt にどう渡されるかを確認するとき
- oracle 専用読み取り、モデル設定、Structured Output schema、インデックス事前実行の設定入口を探すとき

## Do not read this when
- 所見の妥当性を実際に判定するレビュー処理や、擁護理由の内容そのものを調査するとき
- Structured Output の項目や形式だけを確認したいときは、対応する JSON schema を直接読むとよい
- 一般的な prompt 構築や `AgentCallParameter` の共通仕様を確認するときは、それぞれの共通実装を直接読むとよい

## hash
- 37562023ac286d7d9ae5b01f761c20a70df1f7da475959ef27cc1513531c9cc8

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
- oracle review で、指定された所見が妥当ではない理由を列挙するエージェント呼び出しパラメータを構築する。所見、既知の賛成理由、既知の反証理由をプロンプトへ渡し、PURE_ORACLE_READ とレビュー関連ポリシーを適用する。モデル・推論設定、構造化出力スキーマ、作業ディレクトリ、インデックス事前処理も含めた起動設定を返す。

## Read this when
- oracle review の所見に対する反証理由列挙用 agent call のプロンプトや起動パラメータを確認・変更するとき。
- finding、既知の advocate/challenger 理由、agent_call_cwd のプロンプトへの組み込み方を確認するとき。

## Do not read this when
- oracle review の別の判定処理や、反証理由の出力スキーマそのものを確認したいときは、対応する実装または JSON スキーマを直接読む。
- 一般的な agent call パラメータや共通プロンプト生成の仕様だけを確認する場合。

## hash
- 7d2036c682f981a23f920daaf04398568a8f46829139dc946df01c9512400643
