# `oracle`

## Summary
- cmoc の agent call に関する prompt 構築・起動パラメータ定義の全体入口。共通の呼び出しパラメータ、パスコンテキスト、構造化文書レンダリング、用途別の prompt／Structured Output 定義へ進むための上位要素を含む。
- agent call の用途別定義を調べる場合は、通常の呼び出しパラメータと quota probe、INDEX エントリー生成、feedback issue の正規化・検証、TUI 起動の各要素へ進む。prompt の構成規則を調べる場合は prompt builder、設定・パス・Markdown 構造化文書を調べる場合は other 配下が入口になる。

## Read this when
- cmoc の agent call 構築定義全体を把握し、個別用途のパラメータ定義や prompt builder への進み先を判断するとき。
- agent call の入力、cwd、ファイルアクセスモード、Structured Output、indexing preflight などの設定責務の所在を確認するとき。

## Do not read this when
- 特定の用途の prompt 文面や Structured Output 契約だけを確認したい場合は、対応する下位要素を直接読むとき。
- agent call の実行処理、feedback の保存・集約、oracle／realization 本文の編集、INDEX.md 更新そのものを調べるとき。
- 設定、パス解決、構造化 Markdown の具体的な実装だけを確認したい場合は、other 配下を直接読むとき。

## hash
- 2d8ab99311ccb61be865c4d7227b8828d358066ec53ee55c577bd2c429f86e95
