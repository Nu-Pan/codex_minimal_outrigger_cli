# `fork`

## Summary
- エントリーを生成できません。対象には既存の INDEX.md しかなく、責務を説明する本文は確認できませんでした。

## Read this when
- 対象の責務を示す読み取り可能な本文が用意されたときに、内容を確認してエントリーを生成する。

## Do not read this when
- 現在の情報だけから対象の責務を判断する場合。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `launch_exec.py`

## Summary
- `cmoc oracle edit` の agent 向け完全 prompt と、新しい `codex exec` 初回 call に使う共通パラメータを構築する。
- ユーザー指示を編集目的や判断材料、編集境界とともに prompt へ組み込み、本体実行と handoff 用 skeleton の両方で使う。

## Read this when
- `cmoc oracle edit` の agent に渡す指示や、oracle file の編集範囲・判断材料を変更または確認するとき。
- 本体実行と handoff 用 skeleton で共有する prompt や起動パラメータを調べるとき。

## Do not read this when
- エディタ入力、2 回の call の実行順序、設定の取得、終了 report など、サブコマンド全体の流れを変更または確認するとき。サブコマンドの仕様や該当する呼び出し側を確認する。
- 共通 prompt 構築の仕組みや、別の workload の起動処理を変更するとき。それぞれの共通部品または workload 固有の実装を直接確認する。

## hash
- 65c9a27bb8749f0674f3f6c599c4f97ed09837bdb509f03d4625e458e2e7d68a
