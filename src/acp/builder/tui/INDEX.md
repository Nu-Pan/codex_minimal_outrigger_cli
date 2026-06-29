# `__init__.py`

## Summary
- 正本側の ACP builder TUI パッケージとの互換性を示すだけの package 初期化地点。具体的な処理や公開オブジェクトは持たず、この階層が互換 package として存在する理由を示す。

## Read this when
- ACP builder の TUI 関連 package が、正本側の対応 package と互換の入口として用意されているかを確認したいとき。
- この package 初期化地点自体に、追加の初期化処理、公開 import、互換性説明があるかを確認したいとき。

## Do not read this when
- TUI の構築処理、画面制御、入出力処理などの実装内容を調べたいとき。
- 正本仕様断片そのもの、または互換先の詳細な挙動を確認したいとき。
- 関数、クラス、定数、CLI 動作などの具体的な公開面を探しているとき。

## hash
- 0a593accdb428d084c035fe120f2a06b5788abb28e112e72252680ca369fb14d

# `launch_tui.py`

## Summary
- TUI 起動用の AgentCallParameter 生成を oracle 側の正本実装へ委譲しつつ、既存の公開 import path を維持する互換入口。
- oracle 側で組み立てたパラメータから Structured Output schema 指定だけを外し、対話的な TUI 起動では schema を渡さないという実装上の差分を担う。
- 削除条件は、realization 側と利用者向け公開面の両方から、この互換 import path への参照がなくなること。

## Read this when
- TUI 起動時に渡す AgentCallParameter の生成経路や、Structured Output schema を無効化している理由を確認したいとき。
- oracle 側の TUI 起動パラメータ生成と、realization 側の既存公開 import path との接続を調べるとき。
- 互換 import path の維持・削除条件、または TUI 起動パラメータの公開面への影響を変更・確認するとき。

## Do not read this when
- TUI 起動パラメータそのものの正本仕様や引数全体の組み立てを確認したいだけなら、委譲先の oracle 側実装を読む。
- Structured Output schema を要求する非 TUI 起動や index entry 生成など、schema 付き AgentCallParameter の挙動を調べたい場合は、その起動種別の builder を読む。
- TUI 表示、キー操作、画面描画などの対話 UI 本体の挙動を調べたい場合は、起動パラメータ生成ではなく TUI 実行側の実装を読む。

## hash
- 4b32161e90fc11b826340f1f17158acbeae5f46b75ec0a538f1d381aac45f932

# `resolve_parameter.py`

## Summary
- TUI の resolve parameter 構築で使う公開入口をまとめる薄い実装モジュール。正本側のパラメータ構築関数をそのまま公開し、TUI で選べるファイルアクセスモード集合を正本 enum から導出して公開する。
- 独自の変換ロジックや状態管理は持たず、TUI ビルダー層から正本実装由来の resolve parameter 構築機能とファイルアクセスモード候補へ到達するための中継点として位置づく。

## Read this when
- TUI ビルダー層で resolve parameter の構築入口や公開 API を確認したいとき。
- TUI で扱うファイルアクセスモード候補がどこから導出されるかを確認したいとき。
- この階層から正本側の resolve parameter 構築関数を利用する import 境界を確認したいとき。

## Do not read this when
- resolve parameter 構築の具体的な引数組み立てや検証処理を確認したいとき。この対象ではなく、正本側の構築関数本体を読む。
- ファイルアクセスモード enum 自体の定義や各モードの意味を確認したいとき。この対象ではなく、正本側の基本定義を読む。
- TUI 全体の画面制御、入力処理、描画、対話フローを調べたいとき。この対象は公開入口の中継だけを扱う。

## hash
- 397d9d6c29f5c7ee1e126d51d959f814e9032cb2eb2c71b58e3907f9bd17a2ad
