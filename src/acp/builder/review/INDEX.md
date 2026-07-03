# `__init__.py`

## Summary
- 既存の review builder 系 import 互換性を保つためだけに残された package 初期化部分。現行実装や公開面から互換 import が消えた時点で削除候補になる境界を示す。

## Read this when
- review builder 周辺の import 互換性を確認する。
- 古い acp.builder.review 系参照を削除できるか判断する。
- 互換 package の残存理由や削除条件を確認する。

## Do not read this when
- review builder の実処理や変換ロジックを調べたい。
- 新しい公開 API や利用者向け機能の仕様を確認したい。
- 互換 import と無関係な builder 実装を変更する。

## hash
- 20e0879d03952a8b860e9d09a0f9c7e08c05699e96390ec504f3e0481a897ebb

# `oracle`

## Summary
- review oracle 用の agent call parameter builder 群を扱う領域。主に finding enumeration、judgment、merge、finding advocate/challenger validation に関する builder 入口と、旧 import 経路を維持する互換層を含む。
- 正本 prompt や canonical 実装そのものではなく、oracle src 由来の builder 結果を realization 側で接続・再公開し、必要な箇所だけ限定的な placeholder 表記補正を行う境界を担う。

## Read this when
- review oracle の finding 関連 agent call parameter 生成経路を確認・変更する。
- known findings、finding、既知理由などを入力にした review oracle prompt 組み立てが、structured output schema や canonical builder へどう接続されるかを追う。
- 旧 import 経路から canonical oracle path への移行状況、互換 shim の再 export 対象、削除可否を判断する。
- oracle src 側に残る oracle root placeholder 表記ゆれを realization 側で最小補正している理由、範囲、削除条件を確認する。

## Do not read this when
- review oracle の正本 prompt 内容そのものを確認したい場合。対応する oracle src や prompt standard を直接読む。
- finding enumeration、judgment、validation の実処理や parameter 構築ロジックの本体だけを確認したい場合。canonical oracle path 側を直接読む。
- review workflow 全体、CLI、永続状態、git 操作など、agent call parameter builder や旧 import 互換と無関係な領域を調べる。
- AgentCallParameter 型そのものや共通 builder 基盤の仕様を確認したい場合。共通定義側を読む。

## hash
- 467b1c9e2a916a59deb15867498c2f5d36f5daa6cc479ed70f2db12ff23bf35f
