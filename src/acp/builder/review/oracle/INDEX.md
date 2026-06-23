# `enumerate_finding.json`

## Summary

- `cmoc review oracle` の新規所見列挙結果を表す Structured Output schema です。
- `findings` 配列 1 項目を要求し、各所見は `severity`、`title`、`oracle_path`、`reason` を持つオブジェクトとして表します。
- `severity` は `fatal` または `minor` を取り、既知の関連所見と重複しない新規所見だけを機械可読に返すための定義です。

## Read this when

- `cmoc review oracle` の新規所見列挙で返す JSON 形式を確認したいとき。
- `findings` 配列の各要素に必要な `severity`、`title`、`oracle_path`、`reason` を把握したいとき。
- 新規所見が無い場合に空配列を返す条件を確認したいとき。

## Do not read this when

- `enumerate_finding.py` の prompt 本文や調査手順を直接確認したいとき。
- `merge_finding.json`、`validate_finding_advocate.json`、`validate_finding_challenger.json`、`judge_finding.json` など、別の review oracle 系 schema を確認したいとき。
- `cmoc review oracle` 以外のサブコマンドや、Structured Output schema ではない仕様を探しているとき.

## hash

- d1bd69c75e8d60791cc304f06e103a7efdcc6566dc16c1254b8a92d6fcb38c5d

# `enumerate_finding.py`

## Summary

- この `enumerate_finding.py` のルーティング文書で、`enumerate_finding.json` への入口です。
- `cmoc review oracle` の新規所見列挙 prompt 正本として、`oracle_path` を起点に必要なら関連する oracle file も読み、既知の関連所見と重複しない新規所見だけを返す流れを案内します。
- 新規所見が無い場合は空配列を返す前提で、`PURE_ORACLE_READ` と `oracle_standard=True` / `review_oracle_standard=True` を伴う read-only な review 系フローを整理する目次です。

## Read this when

- `cmoc review oracle` で新規所見を列挙する prompt と、その出力先 Structured Output schema の対応を確認したいとき。
- `oracle_path` を起点に関連する oracle file を追加で読む前提や、既知の関連所見と重複しない新規所見だけを返す仕様を把握したいとき。
- `PURE_ORACLE_READ` と `oracle_standard=True` / `review_oracle_standard=True` を前提にした呼び出し条件を整理したいとき。

## Do not read this when

- すでに `enumerate_finding.py` か対応する `enumerate_finding.json` を直接確認する目的が決まっていて、この目次を経由する必要がないとき。
- `merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py` など、別の `review/oracle` 系統を確認したいとき。
- `cmoc review oracle` 以外のサブコマンドや、レビュー用 Structured Output schema そのものだけを確認したいとき。

## hash

- ed4cfcfe7079b85b8e68b2bc29c1d10e9bbb9b63e89910f6dd2a30ef229cf036

# `judge_finding.json`

## Summary

- この `judge_finding.json` は、`cmoc review oracle` の所見採否判定結果を表す Structured Output schema です。
- `verdict` と `reason` を要求し、`accept` / `reject` の二択と判定理由だけを返します。
- `judge_finding.py` が出力先として参照する schema で、対象所見を人間へ提示すべきかの最終判定を機械可読に表します。

## Read this when

- 所見の採否判定の JSON 形式を確認したいとき。
- `build_review_oracle_judge_finding_parameter()` が参照する schema の内容を把握したいとき。
- `accept` / `reject` と判定理由の出力要件を確認したいとき。

## Do not read this when

- 所見の列挙、マージ、擁護理由列挙、否定理由列挙の schema を探しているとき。
- `judge_finding.py` の prompt 本文や実装だけを確認したいとき。
- `cmoc review oracle` 以外のサブコマンドや、レビュー用 Structured Output schema 以外を探しているとき。

## hash

- 260ad5636b98dcbb46dc9ebf3181533f5c550384320219dd6c44661e7ec4e53e

# `judge_finding.py`

## Summary

- この `judge_finding.py` のルーティング文書で、`judge_finding.json` への入口です。
- `cmoc review oracle` の所見採否判定を扱い、対象所見と妥当理由・否定理由を入力にして、人間へ提示すべきかを判定する流れを案内します。
- 対応する Structured Output schema は `judge_finding.json` で、`verdict` と `reason` を返す構成です。

## Read this when

- `cmoc review oracle` で所見採否判定の prompt と Structured Output schema の対応を確認したいとき。
- 対象所見が人間へ提示すべきかを、妥当理由・否定理由を踏まえて判定する仕様を把握したいとき。
- `judge_finding.py` から `judge_finding.json` へ進む入口を整理したいとき。

## Do not read this when

- すでに `judge_finding.py` か `judge_finding.json` を直接確認する目的が決まっていて、この目次を経由する必要がないとき。
- 所見の新規列挙・マージ・妥当理由列挙・否定理由列挙の仕様を探しているとき。
- `cmoc review oracle` 以外のサブコマンドや、レビュー用 Structured Output schema だけを探しているとき。

## hash

- db0e70e87fafff81bfb61e4ccd0185662810df398bd9b991f8baaf1d1bd32367

# `merge_finding.json`

## Summary

- `cmoc review oracle` の所見リスト整理で使う Structured Output schema です。
- `operations` 配列で `delete`、`replace`、`merge` の編集指示を表し、各要素は `kind`、`target_ids`、`finding` を持ちます。
- `finding` は新しい所見内容を表し、`delete` では `null`、`replace` または `merge` では編集後の内容を返します。

## Read this when

- `cmoc review oracle` の所見リスト整理用 Structured Output schema を確認したいとき。
- 入力された所見群の重複や矛盾を解消する編集操作として `delete` / `replace` / `merge` のどれを返すか整理したいとき。
- `target_ids` に何を入れるか、また `finding` に新しい所見内容を入れるか `null` を返すかを確認したいとき。

## Do not read this when

- 新規所見列挙、妥当理由列挙、否定理由列挙、採否判定など、別の review oracle 系統を確認したいとき。
- `merge_finding.py` の prompt 本文だけを確認したいとき。
- 所見整理ではなく、別の `review/oracle` 配下の schema を探しているとき。

## hash

- ef00100875ad3a93bd012fc2fe2f8dceb892a60020b8f202a80594e2426a60c0

# `merge_finding.py`

## Summary

- この `merge_finding.py` のルーティング文書で、`merge_finding.json` への入口です。
- `cmoc review oracle` の所見リスト整理用 prompt 正本として、入力所見を重複や矛盾が解消されるように編集する流れを案内します。
- `finding_id` を前提に `delete` / `replace` / `merge` の編集操作を返し、十分コンパクトで整合的なら空配列を返す前提を示します。

## Read this when

- `cmoc review oracle` の所見リストマージ prompt と、対応する Structured Output schema の関係を確認したいとき。
- 入力された所見群を整理して、重複や矛盾を解消する編集操作として `delete` / `replace` / `merge` のどれを返すか整理したいとき。
- `finding_id` を前提に、`target_ids` に何を入れるか、また空配列を返してよい条件を確認したいとき。

## Do not read this when

- すでに `merge_finding.py` か対応する `merge_finding.json` を直接確認する目的が決まっていて、この目次を経由する必要がないとき。
- 新規所見列挙、妥当理由列挙、否定理由列挙、採否判定など、別の `review oracle` 系統を確認したいとき。
- `cmoc review oracle` 以外のサブコマンドや、レビュー用 Structured Output schema 以外の仕様を探しているとき。

## hash

- 88af6857e331f529f8017682be3fb75d01a7cd10b480906e49beaca208ad5e4c

# `validate_finding_advocate.json`

## Summary

- `cmoc review oracle` の所見擁護理由列挙用 Structured Output schema です。
- `reasons` という文字列配列のみを返す、読み取り専用の JSON schema です。
- 対象所見に対する新規の妥当理由を列挙する用途で使います。

## Read this when

- `cmoc review oracle` で対象所見の妥当理由を返す JSON 形式を確認したいとき。
- `reasons` という文字列配列だけを返す schema の要件を把握したいとき。
- `validate_finding_advocate.py` に対応する Structured Output schema の正本を見たいとき。

## Do not read this when

- `validate_finding_advocate.py` の prompt 本文や実装の流れを確認したいとき。
- 所見の列挙・マージ・否定理由列挙・採否判定など、別の review oracle schema を探しているとき。
- `cmoc review oracle` 以外のサブコマンドや、レビュー用途以外の Structured Output schema を確認したいとき。

## hash

- f265bb48178831b146ee5d071395ff0dd9dfb6bb509f2d062fa54e3243f4cb4e

# `validate_finding_advocate.py`

## Summary

- `validate_finding_advocate.py` と対応する `validate_finding_advocate.json` への入口をまとめる `review/oracle` 配下のルーティング文書です。
- `cmoc review oracle` の「所見が妥当である理由」を列挙する prompt 正本と、その Structured Output schema を案内します。
- 対象所見に対して新規の妥当理由だけを返す read-only フローの起点です。

## Read this when

- `cmoc review oracle` で所見の妥当理由列挙の入口を探したいとき。
- `validate_finding_advocate.py` と `validate_finding_advocate.json` の対応関係を確認したいとき。
- 既知理由と重複しない新規の妥当理由を、`oracle` 配下の file を根拠に返す仕様を整理したいとき。

## Do not read this when

- すでに `validate_finding_advocate.py` か `validate_finding_advocate.json` を直接確認する目的が決まっていて、この目次を経由する必要がないとき。
- 所見が妥当ではない理由を列挙する `validate_finding_challenger.py` 側を確認したいとき。
- 所見の採否判定や新規所見列挙など、別の `review oracle` 系統を探しているとき。

## hash

- fd4941548fcf86db04531ac224b4262d0926c233e9470dbd8aa67b8996803222

# `validate_finding_challenger.json`

## Summary

- `cmoc review oracle` の所見が妥当ではない理由を返す Structured Output schema です。
- `reasons` という文字列配列だけを要求し、対象所見に対する新規の否定理由を機械可読に返すための定義です。
- レビュー用の所見否定理由列挙フローで使う、読み取り専用の JSON schema です。

## Read this when

- `cmoc review oracle` で、所見が妥当ではない理由を JSON 形式で返す出力仕様を確認したいとき。
- 否定理由を 1 つ以上の文字列配列として返す Structured Output schema を把握したいとき。
- `validate_finding_challenger.py` に対応する schema の正本を見たいとき。

## Do not read this when

- すでに `validate_finding_challenger.py` かこの `validate_finding_challenger.json` を直接開いて内容を確認する目的が決まっているとき。
- 所見が妥当である理由を返す `validate_finding_advocate.json` を確認したいとき。
- 所見の採否判定を返す `judge_finding.json` や、別系統の review oracle 仕様を探しているとき。

## hash

- a90232c11fe6071e9aaf6200efe525e546aef4775f06fb11cc71018c28f1d214

# `validate_finding_challenger.py`

## Summary

- この `<cmoc-root>/oracle/src/acp/builder/review/oracle` ディレクトリのルーティング文書で、`validate_finding_challenger.py` と対応する `validate_finding_challenger.json` への入口です。
- `cmoc review oracle` の所見否定理由列挙 prompt 正本として、対象所見に対する新規の否定理由だけを返す流れを案内します。
- 対応する Structured Output schema は `validate_finding_challenger.json` で、否定理由の文字列配列を返す構成です。

## Read this when

- `cmoc review oracle` で、対象所見が妥当ではない理由を新規に列挙する prompt と Structured Output schema の対応を確認したいとき。
- `finding`、`known_advocate_reasons`、`known_challenger_reasons` を入力にして、既知の理由と重複しない否定理由だけを返す仕様を把握したいとき。
- `PURE_ORACLE_READ` と `oracle_standard=True`、`review_oracle_standard=True` を前提に、`oracle` 配下の file だけを根拠に調査する read-only な review フローを確認したいとき。

## Do not read this when

- すでに `validate_finding_challenger.py` か `validate_finding_challenger.json` を直接確認する目的が決まっていて、この目次を経由する必要がないとき。
- 対象が所見の否定理由列挙ではなく、擁護理由列挙・採否判定・新規所見列挙・所見整理のどれかにあるとき。
- `cmoc review oracle` 以外のサブコマンドや、別の Structured Output schema を探しているとき。

## hash

- 0e940691ef68bfa6c135c4db3a5df544eb898e6b5945882fa2e8ee7749789e21
