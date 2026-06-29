# `__init__.py`

## Summary
- oracle.acp_builder.review と互換の package であることだけを示す、review builder 領域の package 初期化用ファイル。実装ロジックや詳細な仕様ではなく、互換名前空間としての位置づけを確認する入口になる。

## Read this when
- review builder 領域で、oracle 側の同名 package と対応する realization package が存在するかを確認したいとき。
- package としての互換性や import 経路の成立だけを確認したいとき。

## Do not read this when
- review builder の具体的な処理、関数、クラス、出力、制御フローを調べたいとき。
- 正本仕様断片としての review builder の要求を調べたいとき。
- package 初期化以外の実装変更先を探しているとき。

## hash
- adf6124f1c3a49a136159186b6a58b39f4321e0113527b60e85d8b1e3205484e

# `oracle`

## Summary
- レビュー用 oracle finding 処理に関する realization 側の互換・補正層をまとめる領域。finding の列挙、統合、検証、判定へ到達するための agent call parameter 生成や再公開入口を扱う。
- 主な責務は、正本側 builder の生成結果を利用しつつ、review oracle 用 prompt へ対象 oracle file 本文やレビュー指示を追加すること、または正本側実装へ委譲する import 経路を保つことにある。
- 一部の実装は正本側 prompt に残る oracle root 表記の不整合だけを最小補正し、型・モデル・推論設定・アクセス設定・structured output schema などの共通設定は維持する薄い互換層として位置づく。

## Read this when
- review oracle の finding 列挙・統合・検証・判定に関する realization 側の公開経路や委譲先を確認したいとき。
- oracle file レビュー用の agent call parameter がどのように作られ、レビュー基準、対象 oracle file 本文、既知 finding、検証対象 finding が prompt に渡るかを確認・変更したいとき。
- 正本側 builder の出力に対して realization 側がどの範囲だけを補正しているか、特に oracle root 表記の補正や dynamic input を改変しない制約を確認したいとき。
- 対象 oracle path の解決、対象ファイルが存在しない場合の本文扱い、markdown code fence のエスケープなど、oracle file 本文をレビュー prompt に埋め込む周辺処理を調べたいとき。
- review oracle 関連の realization module が独自ロジックを持つのか、正本側実装を再公開するだけなのかを切り分けたいとき。

## Do not read this when
- review finding の判定基準、重複判定、意味解釈、統合方針そのものを理解したいとき。この領域ではなく、委譲先またはレビュー基準を構築する側を読む。
- oracle file の正本仕様本文や oracle/realization の基本概念を確認したいとき。この領域は正本仕様の入口ではなく、仕様を prompt や import 経路へ接続する realization 実装である。
- AgentCallParameter の型定義、モデル選択、reasoning effort、file access mode、structured output schema の一般仕様を調べたいとき。共通パラメータ定義側を読む。
- review oracle 以外の builder、検証以外の処理、または CLI 出力仕様やテスト観点を探しているとき。より上位の routing または該当責務の本文へ進む。
- 正本側 prompt 標準や oracle src の文言そのものを変更したいとき。この領域は正本仕様を置き換えず、realization 側の最小補正や互換 import 境界だけを扱う。

## hash
- 99a5f39538b7b577b05adcf4fd7fa0c83020ca18d3c3531e4fbf004aa47a5731
