# `oracle`

## Summary
- cmoc の正本実装を構成する Python モジュールと Structured Output 定義をまとめたディレクトリ。
- パス解決・設定モデル・構造化文書、agent call 用 prompt と各種ポリシー、ACP の実行パラメータ、feedback 処理、TUI・editor handoff の入出力を扱う。

## Read this when
- oracle の実装や設定モデルを確認・変更するとき。
- agent call の prompt、ポリシー、Structured Output、実行パラメータの生成経路を追跡するとき。
- feedback 処理や TUI、editor handoff の正本データ形式を確認するとき。

## Do not read this when
- 正本ドキュメントの要求や設計意図だけを確認する場合。
- realization 側の実装やテストの挙動だけを確認する場合。
- 特定の下位責務が明確で、oracle/src/oracle 全体ではなく対応する下位ディレクトリを直接読む方が適切な場合。

## hash
- d82ce4bc223e9cec8356b8545dd722aeb2c82ce5a26e0989db34bf2e42de4935
