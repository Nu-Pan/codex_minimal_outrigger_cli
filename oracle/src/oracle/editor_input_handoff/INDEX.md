# `body.py`

## Summary
- 項目別の自由記述、文書参照、送信元情報を Markdown handoff 本文に配置し、送信元値の条件を検査する builder。本文の構成と送信元情報の受理条件を確認する入口です。

## Read this when
- 項目別の内容や文書参照が本文にどう配置されるか、送信元情報がどう検査されるかを確認するとき。
- 本文 builder の呼び出し元と責務の境界を追うとき。

## Do not read this when
- MCP の入力項目・意味・受理条件を確認するときは、agent 向け入力 schema と MCP 入力処理から確認してください。
- 送信元情報の取得、active target の検証、submission の転送や書き込みを追うときは、runtime MCP と起動側の処理から確認してください。
- handoff ガイドの文面や prompt 雛形、文書参照の検査・表記を確認するときは、それぞれのガイド生成処理または文書参照モデルを確認してください。
- target のライフサイクル、agent の手順・権限、editor input の確定手順を確認するときは、handoff の意味仕様を確認してください。

## hash
- 0bc5f3a764b654dfdbd2635092ce5f0d4bba016594a6ba343501b84f047d8769

# `get_handoff_guide_input.json`

## Summary
- cmoc_editor_input.get_handoff_guide に渡す入力オブジェクトの受理条件を定め、取得対象の handoff target を指定する契約の入口です。

## Read this when
- get_handoff_guide の呼び出し入力に関する制約を確認・変更するとき。

## Do not read this when
- ガイド取得の成功・失敗時に返る結果の形式を確認するときは、結果スキーマへ進んでください。
- overwrite に渡す依頼内容や参照の入力条件を確認するときは、overwrite の入力スキーマへ進んでください。
- target の有効期間や検証、ガイドの保持・取得動作などの意味仕様を確認するときは、editor input handoff の仕様文書へ進んでください。

## hash
- ba99ecf430882cf3dcd443d0fa70e892ac1b45f060980faf7f53381f4104bc72

# `get_handoff_guide_result.json`

## Summary
- 人間が指定した受信先の handoff ガイド取得について、MCP の結果を受け渡す契約を定める。呼び出し入力やガイド生成ではなく、取得結果の境界を調べる対象。

## Read this when
- get_handoff_guide の結果検証や、結果を受けた成功・失敗処理を変更または調査するとき

## Do not read this when
- 呼び出し内容や入力の受理条件を調べるときは、入力スキーマへ進む
- ガイドの文面や構築方法を調べるときは、ガイド構築定義へ進む
- handoff のライフサイクルや agent の手順全体を調べるときは、意味仕様へ進む

## hash
- cd2702db609493b0f02ee5273bea04cb843f841a35261e6ed36d43c8d28a35ef

# `guide.py`

## Summary
- 受信先の完全 prompt skeleton を取り込み、使い方と記入の目安を含む handoff ガイドの Markdown を構成する。
- ガイドの実際の文面と構成を確認する入口。項目別入力から上書き本文を作る処理とは責務が異なる。

## Read this when
- handoff ガイドの文面や節構成を確認・変更するとき。
- 受信先の完全 prompt skeleton をガイドへ組み込む方法を確認するとき。

## Do not read this when
- handoff の利用条件や機能の意味を確認するときは、意味仕様を参照する。
- 項目別入力から生成する上書き本文や送信元情報を調べるときは、本文構築の実装を参照する。
- ツール入力の受理条件や結果の形式を調べるときは、対応するスキーマを参照する。

## hash
- a27040792ca678e214a6c0c0b6cf9adc30029ce6da5b9ffa7df74f6a22beb3ba

# `overwrite_input.json`

## Summary
- cmoc_editor_input.overwrite に渡す入力契約を定め、項目の意味や記入条件、参照指定、未該当・未確認時の扱いを示す正本の JSON Schema。
- handoff の依頼内容を overwrite 用入力として作成するときの参照先。

## Read this when
- overwrite の入力項目や受理条件、oracle 参照の指定方法を確認・変更するとき。
- handoff の依頼を項目別に準備する際、未該当・未確認の内容をどう扱うか確認するとき。

## Do not read this when
- handoff 全体の手順、target 管理、失敗時の動作、agent の利用条件を確認するときは、editor input handoff の仕様を参照する。
- 生成される本文の見出しや配置を確認するときは、本文 builder を直接参照する。
- editor input file の生成・確定方法や書き込み境界を確認するときは、それぞれの共通仕様を参照する。

## hash
- b0b7150f35d21f50cd8d5b5686cff5a73d5073d87f88fce2d1aff8a997348f04
