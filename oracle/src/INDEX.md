# `oracle`

## Summary
- AI コーディングエージェント呼び出しの共通パラメータ、feedback 入力、基盤モデル、プロンプト構築部品をまとめる oracle src の入口。
- 呼び出し設定の共通定義を確認するときは acp_builder、feedback 正規化入力を確認するときは feedback、リポジトリ設定やパス・規範・構造化文書のモデルを確認するときは other、プロンプトの組み立てや共通規範を確認するときは prompt_builder 配下へ進む。

## Read this when
- AI コーディングエージェント呼び出しのモデル、推論強度、ファイルアクセスモード、cwd、Structured Output、indexing preflight の共通契約を確認するとき。
- feedback の入力構造や issue 正規化に使う Structured Output を確認するとき。
- リポジトリ設定、パス解決、規範モデル、構造化文書モデルの定義を確認するとき。
- プロンプトの共通構成、プレースホルダ、エディタ入力、oracle・realization・routing 関連の規範を確認するとき。

## Do not read this when
- 特定の agent call、サブコマンド、または TUI の起動設定を調査するときは、acp_builder 配下の対応する下位要素へ直接進む。
- feedback の保存、集約、重複判定や、問題検出後の継続判断だけを調査するときは、対応する実装や collector 側へ直接進む。
- 個別のプロンプト本文や共通規範の詳細だけを確認するときは、prompt_builder 配下の対応する部品へ直接進む。
- 具体的な oracle file、realization file、レビュー所見の内容を確認するときは、対象ファイルを直接読む。

## hash
- 9fbad843f8e44477af90f1da7e4595d99dd64c88cbed895e64f0f1fb183c0307
