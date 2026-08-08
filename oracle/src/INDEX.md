# `oracle`

## Summary
- cmoc の oracle src を収める実装領域です。AI エージェント呼び出しのパラメータ、feedback 入力契約、設定・パス・構造化文書モデル、プロンプト構築部品を扱います。
- agent call builder、feedback、基礎モデル、prompt builder という責務別の下位領域へ進むための入口です。

## Read this when
- cmoc の oracle src 全体から、調査対象の責務を特定して適切な下位領域へ進みたいとき。
- AI エージェント呼び出し、feedback reporter、設定・パスモデル、構造化文書、プロンプト構築のいずれかを横断して確認するとき。

## Do not read this when
- 特定の agent call builder の prompt や Structured Output schema を調査するときは、対応する下位領域へ直接進む。
- feedback の入力契約だけを確認するときは、feedback の schema を直接読む。
- 設定値、パス解決、Standard、StructDoc の個別定義だけを確認するときは、other の対応するモデルを直接読む。
- プロンプト共通部品の実装詳細だけを確認するときは、prompt_builder またはその parts を直接読む。

## hash
- 2f9029f5db933ceb399c082bdfe3a9d7f89e909295ad7ddeef7c29b86aacd89d
