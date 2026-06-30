# `oracle`

## Summary
- AI コーディングエージェント呼び出し、共通基礎概念、prompt 構築に関する oracle src をまとめる領域。agent call parameter、標準 prompt 注入、モデル・reasoning effort・ファイルアクセス条件、パスプレースホルダ、規範文書モデル、構造化 Markdown レンダリング helper への入口になる。
- 個別 CLI サブコマンドの実行フローそのものではなく、cmoc 全体で共有される正本仕様断片と、AI へ渡す入力・制約・出力契約を確認するための分岐点として読む。

## Read this when
- cmoc が AI コーディングエージェントを呼び出す際の論理パラメータ、prompt、Structured Output schema、モデルクラス、reasoning effort、ファイルアクセスモードの正本仕様断片を確認したいとき。
- 差分適用後レビュー、ルーティング文書生成、oracle file レビュー、merge conflict 解消、TUI 起動など、用途別の agent call parameter や応答契約を確認・変更したいとき。
- agent call 用 prompt の構築順序、標準文書・規則文書の注入、追加 prompt、プレースホルダ定義、ファイルアクセス規則、ルーティング規則の組み込みを確認したいとき。
- cmoc 全体で共有される設定、ルートパス概念、プレースホルダ付きパスの解決、規範文書モデル、構造化 Markdown レンダリング helper の正本仕様断片を確認したいとき。

## Do not read this when
- 実際の CLI 引数解析、サブコマンド実行制御、git 操作、状態管理、ファイル書き込み、結果集約、表示処理など realization implementation 側の流れだけを調べたいとき。
- 生成済み prompt を受け取った後の agent call 実行処理、バックエンド用の具体的な実行コマンド、サンドボックス設定、結果処理の実装を調べたいとき。
- 個別 CLI サブコマンドの利用者向け入出力、状態ファイル仕様、diff 生成手順、merge conflict marker 検出、TUI 入力取得など、正本仕様断片より外側の処理を確認したいとき。
- oracle file 全般の品質基準、realization standard、review standard、index entry standard など、標準本文そのものを読む必要があり、agent call や共通 helper 側の定義を確認する必要がないとき。

## hash
- dfafb7825f4b8eb74299a5bdbb002b1debc6d7b9849cda7bed17e6999747d9fe
