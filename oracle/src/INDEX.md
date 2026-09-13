# `oracle`

## Summary
- cmoc が agent 呼び出しに渡す設定、prompt、policy、構造化出力契約を用途別に組み立てる実装群への入口。
- agent call の共通パラメータ、用途別 builder、prompt の統合、ファイルアクセス・oracle・realization・routing・feedback などの規定を扱う。
- oracle、feedback、indexing、quota probe、realization、session join、TUI、およびエディタ入力上書きに関する下位実装や入力契約へ進むための階層。

## Read this when
- cmoc の agent 呼び出しを用途別に構築する条件、prompt の構成、出力契約、作業ディレクトリ、ファイルアクセス、indexing preflight を確認するとき。
- oracle・realization・feedback・routing・conflict 解消などの policy を agent prompt に組み込む経路を横断して追跡するとき。
- 特定用途の agent call builder、Structured Output 入力契約、または共通の設定・パス・構造化文書処理への入口を判断するとき。

## Do not read this when
- 特定用途の prompt、起動条件、出力契約だけを調べる場合は、該当する下位 builder や schema を直接読む。
- agent call の共通パラメータ型、設定値、パス解決、構造化文書処理の一般定義だけを確認する場合は、対応する共通実装を直接読む。
- agent call の実行そのもの、各用途の意味仕様、oracle・realization の正本仕様、feedback の収集処理、または INDEX エントリー生成規則を確認する場合は、それぞれの実行処理・正本仕様・収集処理を直接読む。

## hash
- 3f1f377679ddaf5e34f77103b155e66e5cd2798164272a8d66316be691967387
