# `launch_tui.py`

## Summary
- `cmoc tui` のユーザー入力を完全 prompt に組み込み、Codex TUI の起動パラメータを構築する。
- 通常の `cmoc tui` 呼び出しの prompt と起動設定を調べる入口となる。

## Read this when
- 通常の `cmoc tui` が agent に渡す prompt の構成や、作業ルート・ファイルアクセス・handoff・indexing preflight の起動設定を調べる、または変更するとき。
- ユーザー入力が完全 prompt の作業内容や完了条件にどう反映されるか追うとき。

## Do not read this when
- `cmoc oracle investigation` の調査用 prompt や oracle 読取制限を調べる場合は、その呼び出し専用の builder へ進む。
- 完全 prompt の共通構造や個別 policy の定義だけを調べる場合は、共通 prompt builder や policy builder へ進む。
- `AgentCallParameter` や `FileAccessMode` の型定義だけを調べる場合は、共通の型定義へ進む。

## hash
- 2b300becbdd5415cea02a02f128eed378ccc4d514305a1477dbbf585a9dc685a
