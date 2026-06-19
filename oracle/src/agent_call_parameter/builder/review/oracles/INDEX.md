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

- `cmoc review oracle` の新規所見列挙 prompt 正本で、`enumerate_finding.json` への入口です。
- レビュー対象 oracle file と既知の関連所見を入力に、新規所見だけを列挙する呼び出し仕様を案内します。

## Read this when

- `cmoc review oracle` で新規所見を列挙する prompt と Structured Output schema を確認したいとき。
- 既知の関連所見と重複しない所見だけを返す仕様や、新規所見がない場合の空配列返却を確認したいとき。
- `enumerate_finding.py` から対応する `enumerate_finding.json` へ進む入口を把握したいとき。

## Do not read this when

- `cmoc review oracle` の所見マージ、擁護理由列挙、否定理由列挙、採否判定の仕様を確認したいとき。
- `enumerate_finding.py` ではなく、別の review oracle 用 agent call parameter や JSON schema を直接開くとき。
- 既知の関連所見を参照せずに、別系統のレビュー入口を探しているとき。

## hash

- 606191b0601ebc7a7c2aa049aed41df3ddb77397d9b9df04716ffdb58255c660

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
- 対象所見と、その妥当性を支持する理由・否定する理由を入力に、人間へ提示すべき所見かどうかを判定するための目次です。

## Read this when

- 所見の最終採否判定で、`judge_finding.py` の prompt 正本を確認したいとき。
- `accept` / `reject` の判定基準と、`reason` の書き方を整理したいとき。
- `judge_finding.py` と `judge_finding.json` の役割分担を把握したいとき。

## Do not read this when

- 所見の新規列挙、マージ、擁護理由列挙、否定理由列挙の仕様を確認したいとき。
- `judge_finding.json` の JSON schema だけを直接確認したいとき。
- `cmoc review oracle` 以外のサブコマンドや別系統の agent call parameter を探しているとき。

## hash

- 6432165b519b778781fbd7e662652308ad7218ac9c10c53c30ab2f9fdb34e38f

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

- `cmoc review oracle` の所見リストマージ用 prompt 正本への入口です。
- 対応する `merge_finding.json` は、所見群に対する delete・replace・merge 操作を返す Structured Output schema です。
- 入力された所見群を整理し、重複や矛盾を解消するための呼び出し仕様をまとめます。

## Read this when

- `cmoc review oracle` の所見リストマージ用 prompt 正本と、その出力先 schema の対応を確認したいとき。
- 所見同士の重複や相互矛盾を解消する編集操作として、delete・replace・merge のどれを返すか整理したいとき。
- 入力所見の `finding_id` を使った整理フローや、十分コンパクトなら空配列を返す仕様を把握したいとき。

## Do not read this when

- 新規所見の列挙仕様や、擁護理由・否定理由の列挙仕様を探しているとき。
- `merge_finding.json` を含む所見マージ用 Structured Output schema ではなく、別の review oracle の入口を確認したいとき。
- `cmoc review oracle` 以外のサブコマンドや、レビュー以外の agent call parameter を探しているとき。

## hash

- f4ce50f5ef7843113c66cc83dd78161d74ac45c561e25e9f31f140b935e6ea99

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

- この `validate_finding_advocate.py` は、`cmoc review oracle` の所見擁護理由列挙 prompt 正本で、`validate_finding_advocate.json` への入口です。
- 対象所見と既知の理由を受け取り、`oracle` 配下のファイルを根拠に、新規の妥当理由だけを機械可読に列挙する呼び出し仕様を案内します。
- レビュー用の入力生成と出力 schema の対応関係をまとめる、所見擁護フローのルーティング文書です。

## Read this when

- `cmoc review oracle` で、所見が妥当である新規理由だけを列挙する prompt と Structured Output schema の対応を確認したいとき。
- 対象所見、既知の妥当である理由、既知の妥当ではない理由を入力にして、重複しない擁護理由を返す仕様を把握したいとき。
- `oracle` ツリー内の仕様断片を根拠に調査する前提や、`pure_oracle_read`・`oracle_standard=True`・`structured_output=True` を伴う呼び出し条件を確認したいとき。

## Do not read this when

- すでに `validate_finding_advocate.py` か `validate_finding_advocate.json` を確認する目的が決まっていて、この目次を経由する必要がないとき。
- 所見が妥当ではない理由を列挙する `validate_finding_challenger.py` / `validate_finding_challenger.json` を探しているとき。
- 所見の採否判定を行う `judge_finding.py` / `judge_finding.json` や、別系統の review oracle の入口を確認したいとき。

## hash

- 5db4466eeedae444efe1b72ca3cf8af724077057bef2111549fadd26611ff464

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
- `validate_finding_challenger.json` という Structured Output schema に接続し、新規の否定理由だけを返す呼び出し仕様を案内します。
- 対象所見、既知の擁護理由、既知の否定理由を入力として扱い、反証候補を整理するための目次です。

## Read this when

- 所見が妥当ではない理由を Codex CLI に列挙させる仕様を確認したいとき。
- 具体的な根拠に基づく反証理由を返させる prompt と Structured Output schema の対応を確認したいとき。
- 既知の擁護理由・否定理由を踏まえたレビュー用の入力仕様をたどりたいとき。

## Do not read this when

- 所見が妥当である理由を列挙したいとき。
- 所見の採否判定を確認したいとき。
- すでに `validate_finding_challenger.py` または対応する JSON schema を直接開く予定があるとき。

## hash

- 8768240de4f3d5afc71c0cb666fcddc34e1f679ce093f6fc784aa793ba691aca
