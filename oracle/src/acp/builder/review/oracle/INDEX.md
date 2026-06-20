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

- この `enumerate_finding.py` のルーティング文書で、`enumerate_finding.json` への入口です。
- `cmoc review oracle` の新規所見列挙 prompt 正本として、`oracle_path` を起点に必要なら関連する oracle file も読み、`related_findings` と重複しない新規所見だけを返す流れを案内します。
- 新規所見が無い場合は空配列を返す前提で、レビュー対象 file 周辺の prompt と Structured Output schema の分岐を整理する目次です。

## Read this when

- `cmoc review oracle` で新規所見を列挙する prompt と、その出力先 Structured Output schema の対応を確認したいとき。
- 既知の関連所見と重複しない新規所見だけを返す仕様や、新規所見が無い場合の空配列条件を確認したいとき。
- `PURE_ORACLE_READ` 前提で、レビュー対象 oracle file と関連所見を入力に取る呼び出し条件を整理したいとき。

## Do not read this when

- すでに `enumerate_finding.py` か `enumerate_finding.json` を直接確認する目的が決まっていて、この目次を経由する必要がないとき。
- `merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py` など、別の review oracle 系統を確認したいとき。
- `cmoc review oracle` 以外のサブコマンドや、Structured Output schema そのものだけを確認したいとき。

## hash

- d144aeb7ad4a8f42a6ff89a023223288915d4c5e355378fba38c76e7396613b9

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

- この `review/oracle` ディレクトリのルーティング文書で、`judge_finding.py` と対応する `judge_finding.json` への入口です。
- `cmoc review oracle` の所見採否判定を扱い、対象所見と擁護理由・否定理由を入力にして、人間へ提示すべきかを判定する流れを案内します。
- 対応する Structured Output schema は `judge_finding.json` で、`verdict` と `reason` を返す構成です。

## Read this when

- `cmoc review oracle` で、所見採否判定の prompt と Structured Output schema の対応を確認したいとき。
- 対象所見が人間へ提示すべきかを、擁護理由・否定理由を踏まえて判定する仕様を把握したいとき。
- `judge_finding.py` から `judge_finding.json` へ進む入口を整理したいとき。
- `oracle` ツリー内の仕様断片を根拠に、accept / reject の判定条件を確認したいとき。

## Do not read this when

- すでに `judge_finding.py` か `judge_finding.json` を直接確認する目的が決まっていて、この目次を経由する必要がないとき。
- 所見の新規列挙・マージ・擁護理由列挙・否定理由列挙の仕様を探しているとき。
- `cmoc review oracle` 以外のサブコマンドや、レビュー用 Structured Output schema だけを探しているとき。

## hash

- 11d8c2f798a970c0a9a3cb42f72f0e926a52a4898e334d8bdffd17e968a4243e

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

- この `merge_finding.py` のルーティング文書で、`merge_finding.json` への入口です。
- `cmoc review oracle` の所見リスト整理用 prompt 正本として、入力された所見群を整え、重複や矛盾を解消する編集操作を返す流れを案内します。
- `finding_id` を前提に、`delete` / `replace` / `merge` のいずれを返すかと、十分コンパクトで整合的なら空配列を返す条件を整理する目次です。

## Read this when

- `cmoc review oracle` の所見リストマージ prompt と、その出力先 Structured Output schema の対応を確認したいとき。
- 入力された所見群を整理して、重複や矛盾を解消する編集操作として `delete` / `replace` / `merge` のどれを返すか整理したいとき。
- `finding_id` を前提に、十分コンパクトで整合的なら空配列を返す仕様や、`target_ids` に何を入れるかを確認したいとき。

## Do not read this when

- すでに `merge_finding.py` か対応する `merge_finding.json` を直接確認する目的が決まっていて、この目次を経由する必要がないとき。
- 新規所見列挙、妥当理由列挙、否定理由列挙、採否判定など、別の `review oracle` 系統を確認したいとき。
- `cmoc review oracle` 以外のサブコマンドや、レビュー用 Structured Output schema 以外の仕様を探しているとき。

## hash

- 7ef8828ee7ee8def4b8a3365e6530f942766d68e662dbee09b60ed541a609376

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

- `validate_finding_advocate.py` のルーティング文書で、対応する `validate_finding_advocate.json` への入口です。
- `finding`、`known_advocate_reasons`、`known_challenger_reasons` を受け取り、`oracle` 配下の file を根拠に対象所見が妥当である新規理由だけを列挙する prompt 正本です。
- `PURE_ORACLE_READ`、`oracle_standard=True`、`structured_output=True` を伴う read-only な review 系フローを案内します。

## Read this when

- `cmoc review oracle` で、対象所見の擁護理由を新規に列挙する prompt と Structured Output schema の対応を確認したいとき。
- 対象所見、既知の妥当である理由、既知の妥当ではない理由を入力にして、重複しない妥当理由だけを返す仕様を把握したいとき。
- `PURE_ORACLE_READ` と `oracle_standard=True` を前提に、レビュー対象の oracle file だけを根拠に調査する条件を確認したいとき。

## Do not read this when

- すでに `validate_finding_advocate.py` か `validate_finding_advocate.json` を直接開く対象として決めているとき。
- 所見が妥当ではない理由を列挙する `validate_finding_challenger.py` / `validate_finding_challenger.json`、または採否判定の `judge_finding.py` / `judge_finding.json` を確認したいとき。
- `cmoc review oracle` 以外のサブコマンドや、別系統の review oracle を探しているとき。

## hash

- 1000ce90679faa7ad0c38444851b3c6bcff2026bccbce6fed8bff2269103bb80

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

- この `validate_finding_challenger.py` のルーティング文書で、`validate_finding_challenger.json` への入口です。
- `cmoc review oracle` の所見が妥当ではない理由を列挙する prompt 正本と、対応する Structured Output schema を案内します。
- 対象所見と既知の理由を入力に、反証候補を整理するための目次です。

## Read this when

- `cmoc review oracle` で、所見が妥当ではない理由を列挙する prompt と Structured Output schema の対応を確認したいとき。
- 対象所見、既知の擁護理由、既知の否定理由を入力にして、新規の否定理由だけを返す仕様を把握したいとき。
- `oracle` ツリー内の仕様断片を根拠に調査する前提や、`pure_oracle_read`・`oracle_standard=True`・`structured_output=True` を伴う呼び出し条件を確認したいとき。

## Do not read this when

- すでに `validate_finding_challenger.py` か `validate_finding_challenger.json` を直接確認する目的が決まっていて、この目次を経由する必要がないとき。
- 所見が妥当である理由を列挙する `validate_finding_advocate.py` / `validate_finding_advocate.json` を確認したいとき。
- 所見の採否判定を行う `judge_finding.py` / `judge_finding.json` や、別系統の `cmoc review oracle` 入口を探しているとき。

## hash

- b59aa298967bb41210dce009511fb154f2b5ece25afc42bde8e433d80ae1a784
