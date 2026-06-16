# `enumerate_finding.py`

## Summary

- `cmoc review oracle` の新規所見列挙 prompt 正本です。
- `enumerate_finding.json` は、新規所見リストの Structured Output schema です。
- 1 回の Codex CLI 呼び出しで 1 つの oracle file を起点にレビューします。

## Read this when

- 新規所見の列挙で Codex CLI に渡す prompt と schema を確認したいとき。
- 既知の関連所見を渡し、重複しない所見だけを返させる仕様を確認したいとき。

## Do not read this when

- 所見リストのマージ、妥当性検証、採否判定を探しているとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `merge_finding.py`

## Summary

- `cmoc review oracle` の所見リストマージ prompt 正本です。
- `merge_finding.json` は、所見リストに対する delete、replace、merge 操作の Structured Output schema です。
- 所見同士の重複や相互矛盾を解消する Codex CLI 呼び出しを案内します。

## Read this when

- 所見リスト整理で Codex CLI に渡す prompt と schema を確認したいとき。
- `finding_id` を使って所見編集操作を返させる仕様を確認したいとき。

## Do not read this when

- 新規所見列挙、所見ごとの理由列挙、採否判定を探しているとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `validate_finding_advocate.py`

## Summary

- `cmoc review oracle` の所見が妥当である理由を列挙する prompt 正本です。
- `validate_finding_advocate.json` は、新規擁護理由リストの Structured Output schema です。
- 対象所見、既知の擁護理由、既知の否定理由を入力として扱います。

## Read this when

- 所見が妥当である理由を Codex CLI に列挙させる仕様を確認したいとき。
- 既知理由との重複を避ける prompt を確認したいとき。

## Do not read this when

- 所見が妥当ではない理由、または採否判定を探しているとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `validate_finding_challenger.py`

## Summary

- `cmoc review oracle` の所見が妥当ではない理由を列挙する prompt 正本です。
- `validate_finding_challenger.json` は、新規否定理由リストの Structured Output schema です。
- 対象所見、既知の擁護理由、既知の否定理由を入力として扱います。

## Read this when

- 所見が妥当ではない理由を Codex CLI に列挙させる仕様を確認したいとき。
- 具体的根拠に基づく反証理由を返させる prompt を確認したいとき。

## Do not read this when

- 所見が妥当である理由、または採否判定を探しているとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `judge_finding.py`

## Summary

- `cmoc review oracle` の所見採否判定 prompt 正本です。
- `judge_finding.json` は、`accept` / `reject` と理由を返す Structured Output schema です。
- 対象所見、擁護理由、否定理由を入力として、人間へ提示すべき所見か判定します。

## Read this when

- 所見の最終採否判定で Codex CLI に渡す prompt と schema を確認したいとき。
- review oracle の最後の品質改善段階を確認したいとき。

## Do not read this when

- 所見の列挙、マージ、理由列挙を探しているとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
