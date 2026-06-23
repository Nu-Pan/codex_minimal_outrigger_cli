# `oracle`

## Summary
- oracle file レビューにおける AI 呼び出しパラメータ構築と、その各段階で使う Structured Output schema をまとめる領域。
- 新規所見の列挙、所見の妥当性を支持する理由の列挙、妥当ではない理由の列挙、採否判定、所見リストの整理・マージという review oracle 固有の処理への入口になる。
- 各処理は、対象所見や既知理由、既知所見、標準プロンプト断片を補助文脈として渡し、読み取り専用アクセス、モデル種別、推論量、対応 schema を組み合わせた AgentCallParameter を構築する。

## Read this when
- `cmoc review oracle` で oracle file を対象にしたレビュー所見の生成、検証、採否判定、整理のどの AI 呼び出し設定を使うか確認したいとき。
- oracle file レビューの各段階で、対象 oracle、対象所見、既知所見、既知の肯定理由・反証理由がプロンプトへどう渡されるかを追いたいとき。
- review oracle 系の出力契約として、新規所見、肯定理由、反証理由、採否判定、重複・矛盾解消操作のどれを返すべきか判断したいとき。
- oracle 標準や review oracle 標準を有効にしたプロンプト構築、ファイルアクセスモード、モデル種別、reasoning effort、structured output schema の対応関係を確認・変更したいとき。

## Do not read this when
- oracle file や realization file の基本概念、正本仕様断片としての一般原則、レビュー基準そのものを確認したいだけのとき。
- `cmoc review oracle` 全体の CLI 引数解析、サブコマンド登録、実行制御、結果の保存・集約・表示処理を調べたいとき。
- 汎用的な AgentCallParameter、プロンプト組み立て、構造化 markdown レンダリング、パス解決の共通実装を調べたいとき。
- oracle file 本文の具体的な仕様内容や、個別の正本仕様断片そのものを読みたいとき。
- review 以外のサブコマンド、または oracle file ではない realization file のレビュー処理を調べたいとき。

## hash
- 7bddd7a92d53c8b7121fc04854a4e5d08f075023b11e1cf629d9db89a800df91
