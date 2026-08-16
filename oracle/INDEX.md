# `doc`

## Summary
- oracle/doc 配下の正本仕様群と開発ルール群へ進むための入口。CLI・workflow・branch model・設計上の不採用案、および Python 実装、環境、テスト、品質検査に関する判断を、対象領域の下位文書へ振り分ける。

## Read this when
- cmoc の CLI や workflow の正本仕様、session／run／branch の関係、設計上の代替案、または開発・環境・テスト規則の入口を選ぶとき
- 複数の oracle 文書にまたがる責務や、仕様と開発ルールのどちらを確認すべきかを判断するとき

## Do not read this when
- 対象機能やサブコマンドの詳細仕様が明確で、対応する下位の oracle 文書を直接読めるとき
- 実装配置、テスト実行手順、または個別の仕様・realization file の内容だけを確認する場合

## hash
- d288960342eeda2675dd77edcd54063009eee570ebffaf31d9865493ab2718d3

# `src`

## Summary
- AI コーディングエージェント呼び出しに渡すパラメータ、モデル・推論設定、ファイルアクセスモード、cwd、Structured Output、indexing preflight の共通モデルと構築処理をまとめる領域。
- agent call 用の完全 prompt を、summary・goal、共通 policy、oracle／realization 向け policy、補助文面、placeholder、エディタ入力から構成する処理を扱う。
- call-scoped な repo／work root の解決、root placeholder の実パス化、cmoc 設定モデル、構造化 Markdown の生成・参照検証など、agent call 構築を支える共通基盤を提供する。
- 下位には、agent call パラメータ構築を扱う acp_builder、完全 prompt と policy を扱う prompt_builder、パス・設定・構造化文書を扱う other があり、個別処理の入口として機能する。

## Read this when
- 特定の cmoc 処理が agent call に設定するモデル、推論 effort、ファイルアクセス、cwd、Structured Output、indexing preflight を調査・変更するときは acp_builder を読む。
- 完全 prompt の組み立て順序、summary・goal の注入、policy の選択、placeholder の統合、エディタ入力の初期文面を調査・変更するときは prompt_builder を読む。
- agent call の root path、placeholder、cmoc 設定、構造化 Markdown のデータモデルやレンダリング・参照検証を調査・変更するときは other を読む。
- 下位の個別 agent call、policy、oracle／realization 処理の具体的な Structured Output や prompt 契約を確認するときは、対応する下位要素へ進む。

## Do not read this when
- agent call の実行制御、終了結果の処理、CLI サブコマンド固有の挙動を確認するときは、この共通領域ではなく呼び出し側・実行処理を直接読む。
- collector の保存・集約・重複判定や、feedback の検出・継続判断だけを確認するときは、agent call 構築領域ではなく該当する collector・判定処理を直接読む。
- 個別 policy や個別 prompt 部品の本文だけを確認するときは prompt_builder 全体ではなく、対応する policy または parts 配下を直接読む。
- StructDoc・StructBlock、FileAccessMode、AgentCallPathContext、利用側 CLI 実装の詳細を確認するときは、この入口ではなくそれぞれの定義元・利用側を直接読む。
- INDEX.md 自体や、oracle/src 外の設定ファイル・仕様書の内容を確認するときは、この領域を読む必要はない。

## hash
- 1c9876501c1310fd807e7354ba60786b8f317b064630b1d3eb7267008b3e82ba
