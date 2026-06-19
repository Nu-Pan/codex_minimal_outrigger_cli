# `enumerate_finding.json`

## Summary

- `cmoc review oracle` の新規所見列挙結果を表す Structured Output schema です。
- `findings` という配列を 1 項目として要求し、各所見は `severity`、`title`、`oracle_path`、`reason` を持つオブジェクトとして表します。
- `severity` は `fatal` または `minor` を取り、レビュー対象 oracle file に対する新規所見だけを機械可読に返すための定義です。

## Read this when

- 新規所見列挙の Structured Output schema を確認したいとき。
- `cmoc review oracle` で返す所見リストの JSON 形式を把握したいとき。
- `findings` 配列の各要素に必要な `severity`、`title`、`oracle_path`、`reason` の項目を確認したいとき。

## Do not read this when

- 所見のマージ、擁護理由の列挙、否定理由の列挙、採否判定だけを確認したいとき。
- `enumerate_finding.py` の prompt 本文を直接確認したいとき。
- `cmoc review oracle` 以外の agent call parameter を探しているとき。

## hash

- fb3a61d69e2fd17f7aa95187bbc047f506a87a5b2de70995c4bd66f949401c86

# `enumerate_finding.py`

## Summary

- `cmoc review oracle` の新規所見列挙 prompt 正本で、`enumerate_finding.json` の schema へつながる入口です。
- レビュー対象 oracle file を起点に、既知の関連所見と重複しない新規所見だけを列挙する呼び出し仕様を案内します。

## Read this when

- `cmoc review oracle` で新規所見を列挙する prompt と Structured Output schema を確認したいとき。
- 既知の関連所見と重複しない所見だけを返す仕様や、新規所見がない場合の空配列返却を確認したいとき。
- `enumerate_finding.py` から `enumerate_finding.json` へ進む入口を把握したいとき。

## Do not read this when

- 所見リストの統合、妥当性検証、採否判定の仕様を探しているとき。
- 既知の関連所見を参照せずに、別の review oracle の入口を直接開くとき。

## hash

- 0a1708ae982e20caf152377906c66bd360438aea86e8981862428643a7e21078

# `judge_finding.json`

## Summary

- `cmoc review oracle` の所見採否判定結果を表す Structured Output schema です。
- `verdict` と `reason` を要求し、`accept` / `reject` の二択と理由だけを返します。
- `judge_finding.py` が生成する出力先 schema で、対象所見の最終判定に対応します。

## Read this when

- 所見の採否判定結果の JSON 形式を確認したいとき。
- `build_review_oracle_judge_finding_parameter()` が参照する schema 内容を確認したいとき。
- `accept` / `reject` と判定理由の出力要件を確認したいとき。

## Do not read this when

- 所見の列挙、マージ、擁護理由列挙、否定理由列挙の schema を探しているとき。
- prompt 本文や `judge_finding.py` の実装だけを確認したいとき。
- hash やファイル名など、機械的に付随する情報だけを確認したいとき。

## hash

- 082224582304b30326232c20a0ddc1d173467848fd6990d8cd48d5832b9672db

# `judge_finding.py`

## Summary

- この `judge_finding.py` のルーティング文書で、`judge_finding.json` への入口です。
- `cmoc review oracle` の所見採否判定を担う prompt 正本と、その Structured Output schema を案内します。
- 対象所見、擁護理由、否定理由を入力として、人間へ提示すべき所見かどうかを判定するための目次です。

## Read this when

- 所見の最終採否判定で、Codex CLI に渡す prompt と Structured Output schema を確認したいとき。
- `accept` / `reject` の判定基準と、理由の書き方を整理したいとき。
- `judge_finding.py` と `judge_finding.json` の役割分担をまとめて把握したいとき。

## Do not read this when

- 所見の列挙、マージ、擁護理由列挙、否定理由列挙を確認したいとき。
- `judge_finding.py` ではなく、他の review oracle の prompt 正本や schema を直接開くとき。
- `cmoc review oracle` 以外のサブコマンドや、別系統の agent call parameter を探しているとき。

## hash

- 6910495e355af9736ebbb509135dbad9fad08e8f47bbb5e888975ce05ebd056f

# `merge_finding.json`

## Summary

- `cmoc review oracle` の所見リスト整理で使う Structured Output schema です。
- `operations` 配列で `delete`、`replace`、`merge` の編集指示を表し、各要素は `kind`、`target_ids`、`finding` を持ちます。
- `finding` は新しい所見内容を表し、不要な場合は `null` にできます。

## Read this when

- 所見同士の重複や矛盾を整理するための出力形式を確認したいとき。
- Codex CLI に所見リストの削除・置換・統合を返させる仕様を確認したいとき。
- `merge_finding.py` が参照する Structured Output schema の内容を確認したいとき。

## Do not read this when

- 新規所見の列挙や、擁護理由・否定理由の列挙、採否判定の形式を探しているとき。
- `merge_finding.py` の prompt 本文だけを確認したいとき。
- 所見整理ではなく、別の `review/oracles` 配下の schema を探しているとき。

## hash

- f868a37cdad381d03923be50d6124465def9d8bf9a30c5e2b422bc15d6462dd0

# `merge_finding.py`

## Summary

- この `merge_finding.py` は、`cmoc review oracle` の所見リストマージ用 prompt の正本です。
- 対応する `merge_finding.json` は、所見リストに対する delete・replace・merge 操作を返す Structured Output schema です。
- 入力された所見群を整理し、重複や矛盾を解消するための Codex CLI 呼び出しの入口です。

## Read this when

- `cmoc review oracle` の所見リスト統合用 prompt と Structured Output schema を確認したいとき。
- 所見同士の重複や相互矛盾を解消する編集操作の仕様を把握したいとき。
- 既存の所見一覧を整理して、delete・replace・merge のどの操作を返すべきか判断したいとき。

## Do not read this when

- 新規所見の列挙や、所見ごとの擁護理由・否定理由の列挙を確認したいとき。
- `finding_id` を使った所見編集操作ではなく、別の review oracle の prompt や schema を探しているとき。
- `cmoc review oracle` 以外のサブコマンドや、レビュー以外の agent call parameter を探しているとき。

## hash

- 84a11388e0f57c714c7e9b9dc30dc6bf523f4ba73712e002c24628eb9b35b00d

# `validate_finding_advocate.json`

## Summary

- `cmoc review oracle` の所見擁護理由列挙用 Structured Output schema です。
- `reasons` という文字列配列のみを返す、読み取り専用の JSON schema です。
- 対象所見に対する新規の妥当理由を列挙する用途で使います。

## Read this when

- `cmoc review oracle` で対象所見が妥当である理由を列挙させる schema を確認したいとき。
- 既知の擁護理由と重複しない新規理由だけを返す出力形式を把握したいとき。
- `validate_finding_advocate.py` に対応する Structured Output schema の正本を見たいとき。

## Do not read this when

- `validate_finding_advocate.json` ではなく、所見の列挙・マージ・否定理由列挙・採否判定の schema を探しているとき。
- 所見が妥当ではない理由や、別の review oracle の Structured Output schema を確認したいとき。
- `cmoc review oracle` 以外のサブコマンドの agent call parameter を確認したいとき。

## hash

- 13b65613e2180ae59ac57ee18ec599068795bfea9ce54363fbccf4484de3159c

# `validate_finding_advocate.py`

## Summary

- 仕様断片を根拠に、対象所見が妥当である新規理由だけを列挙するための入口です。
- 入力として対象所見、既知の妥当である理由、既知の妥当ではない理由を受け取り、重複を避けた理由一覧を返す想定です。
- 根拠の具体性を重視し、推測ではなく明確な裏付けに基づく説明をまとめます。

## Read this when

- 所見を擁護する追加理由を洗い出したいとき。
- 既知の理由と重複しない新規の根拠だけを抽出したいとき。
- 対象の妥当性を支持する説明を、証拠に基づいて整理したいとき。

## Do not read this when

- 所見が妥当ではない理由を探したいとき。
- 所見の採否そのものを判定したいとき。

## hash

- 04ae4a22dab3ba5cd4a88916d6ed8fa230ebdf0b9b536d5800fede7a888c9b9f

# `validate_finding_challenger.json`

## Summary

- 所見が妥当ではない理由を返す Structured Output schema です。
- 文字列配列 1 項目を要求し、否定理由だけを格納する出力形式です。
- レビュー用の所見否定理由列挙フローで使う出力仕様です。

## Read this when

- 所見が妥当ではない理由を JSON 形式で返す出力形式を確認したいとき。
- 否定理由を 1 つ以上の文字列配列として返す Structured Output を把握したいとき。
- レビュー用の所見否定理由列挙フローで使う出力仕様を確認したいとき。

## Do not read this when

- 所見が妥当である理由の出力形式を確認したいとき。
- 所見の採否判定を返す出力形式を確認したいとき。
- prompt 本体やレビュー手順だけを確認したいとき。

## hash

- 13b65613e2180ae59ac57ee18ec599068795bfea9ce54363fbccf4484de3159c

# `validate_finding_challenger.py`

## Summary

- `cmoc review oracle` の所見が妥当ではない理由を列挙する prompt 正本です。
- `validate_finding_challenger.json` は、新規否定理由リストの Structured Output schema です。
- 対象所見、既知の擁護理由、既知の否定理由を入力として扱い、反証用の所見候補を整理する目次です。

## Read this when

- 所見が妥当ではない理由を Codex CLI に列挙させる仕様を確認したいとき。
- 具体的な根拠に基づく反証理由を返させる prompt と schema の対応を確認したいとき。
- 既知の擁護理由・否定理由を踏まえたレビュー用入口をたどりたいとき。

## Do not read this when

- 所見が妥当である理由を列挙したいとき。
- 所見の採否判定を確認したいとき。
- すでに `validate_finding_challenger.py` または `validate_finding_challenger.json` を直接開く予定があるとき。

## hash

- 9cc08affa54281b9a7b8f5d26fbfc04ae5e617c34b8b915074ea604f993733c2
