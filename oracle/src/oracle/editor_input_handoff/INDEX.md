# `body.py`

## Summary
- 項目別の依頼内容と oracle 参照、および送信元識別情報から、エディター入力へ書き込む Markdown 本文を構築する実装。入力項目の空値拒否、送信元情報の必須性・絶対パス検証、各セクションの配置とレンダリングを確認したい場合の入口。

## Read this when
- エディター入力本文のセクション構成、参照ファイルの掲載、送信元情報の埋め込みを確認したいとき。
- 本文生成時の入力値検証や、送信元ログパスなどの保持条件を調べたいとき。

## Do not read this when
- JSON 入力スキーマや MCP 呼び出し側の検証・書き込み処理を確認したいときは、overwrite_input.json または呼び出し側を直接読む。
- 受信側へ渡す作業案内の生成規則を確認したいときは、guide.py を読む。

## hash
- 0bc5f3a764b654dfdbd2635092ce5f0d4bba016594a6ba343501b84f047d8769

# `get_handoff_guide_input.json`

## Summary
- 人間が指定した target ID を受け取り、対応するエディター入力ハンドオフ・ガイド取得処理へ渡すための入力スキーマです。入力は空白でない単一の target ID に限定されます。

## Read this when
- target ID を指定してハンドオフ・ガイド取得を呼び出す入力契約を確認・変更するとき。

## Do not read this when
- ハンドオフ・ガイド本文の生成規則や取得結果の形式を確認するときは、対応する実装または result スキーマを直接読むべきです。

## hash
- ba99ecf430882cf3dcd443d0fa70e892ac1b45f060980faf7f53381f4104bc72

# `get_handoff_guide_result.json`

## Summary
- `editor_input_handoff` の get_handoff_guide 操作が返す結果の JSON Schema。成功時は対象に対応する handoff ガイド本文、失敗時は取得できなかった理由を表す。

## Read this when
- get_handoff_guide の結果契約を確認・変更するとき。
- 成功・失敗それぞれの返却形式を実装やテストから確認するとき。

## Do not read this when
- get_handoff_guide 以外の操作の結果形式を確認するとき。
- handoff ガイド本文の生成ロジックや対象選択の実装を直接調べるとき。

## hash
- cd2702db609493b0f02ee5273bea04cb843f841a35261e6ed36d43c8d28a35ef

# `guide.py`

## Summary
- 完全 prompt skeleton を受け取り、受信先への依頼作成方法・記入項目・参照上の注意を含む Markdown の handoff ガイド文面を構築する関数。生成物には受信先の prompt template をタグ付きで埋め込む。

## Read this when
- 受信先の editor input handoff ガイドの文面構築や、そのガイドに含める prompt template の扱いを確認したいとき
- handoff ガイドの使い方・記入の目安・完全 prompt skeleton の配置を調べるとき

## Do not read this when
- handoff 本文の項目、空欄検証、参照ファイル、送信元情報の注入を確認したいとき
- handoff target の lifecycle や MCP の入力・上書き処理を確認したいとき

## hash
- a27040792ca678e214a6c0c0b6cf9adc30029ce6da5b9ffa7df74f6a22beb3ba

# `overwrite_input.json`

## Summary
- エディター入力上書きツールが受け取る入力オブジェクトの正本スキーマです。引き渡し先、目標、作業依頼、背景、決定事項、未確定事項、および oracle 参照を定義します。

## Read this when
- エディター入力上書きツールの入力形式を確認・変更するとき。
- 引き渡し内容の必須項目、自由記述項目、oracle 参照の形式を確認するとき。

## Do not read this when
- エディター入力の上書きツール自体の実装を調べるとき。
- 上書き以外の入力形式や、別の JSON スキーマを確認するとき。

## hash
- b0b7150f35d21f50cd8d5b5686cff5a73d5073d87f88fce2d1aff8a997348f04
