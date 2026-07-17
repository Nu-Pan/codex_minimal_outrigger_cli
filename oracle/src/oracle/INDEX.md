# `acp_builder`

## Summary
- ACP builder の oracle src 群をまとめるディレクトリ。agent 呼び出しパラメータ、Structured Output schema、prompt、モデル・アクセス設定など、各種 cmoc 操作の呼び出し条件に関する正本仕様断片への入口。
- 共通部品と、apply fork・indexing・oracle review・session join・tui など個別処理向けの builder 定義に分かれる。特定の呼び出し条件や出力契約を調査する際は、該当する下位要素へ進む。

## Read this when
- ACP builder の呼び出し条件、prompt、Structured Output schema、モデル設定、ファイルアクセス方針を確認・変更するとき。
- 対象の cmoc 操作に対応する oracle src や、builder 間で共有される状態・結果表現の仕様を探すとき。

## Do not read this when
- 差分取得、fork の作成・適用、session の通常同期、レビュー探索手順、TUI 本体など、agent 呼び出しパラメータ構築より前後の実行フローを調査するとき。
- realization code の実装・テスト詳細、共通 prompt builder やパス解決など別領域の実装詳細だけを確認したいとき。

## hash
- db2d089c09f353354398c8b7f604923bf5b3e0522140ea83bb23cabc5580cc73

# `other`

## Summary
- cmoc の設定モデル、パス解決、規範データ構造、構造化 Markdown 文書生成を担う実装群。設定値やルート表記、規範の変換、文書レンダリングの挙動を確認するための入口。

## Read this when
- cmoc の設定項目・既定値・モデル設定・処理上限を確認するとき
- ルートパスのプレースホルダ解決や実パス変換の仕様を確認するとき
- 規範データの構造や StructDoc への変換を確認するとき
- Markdown の構造化・参照検証・正規化・レンダリング挙動を確認するとき

## Do not read this when
- 設定 JSON の生成・同期処理だけを確認したいとき
- 個別サブコマンドの入出力や業務ロジックを確認したいとき
- 各 Enum や StructDoc、個別標準文書の定義そのものだけを確認したいとき
- oracle file の配置・命名など上位方針を確認したいとき

## hash
- f276f1e2313374f8ecfca66e0cd40596db4c89891ffe03aaa47ece4001c8a0a4

# `prompt_builder`

## Summary
- oracle と realization の定義、各種 standard、レビュー基準、ファイルアクセス規則、ルーティング規則をプロンプト builder 部品として管理するディレクトリ。個別の規範文面や、それらを構造化プロンプトへ変換する処理を調査・変更する際の入口となる。

## Read this when
- oracle / realization の基本定義や責務境界を確認・変更するとき。
- oracle standard、realization standard、レビュー基準、ファイルアクセス規則、INDEX.md の routing 規範を確認・変更するとき。
- 複数の標準・規則を agent 用プロンプトへ注入する部品の構成を調査するとき。

## Do not read this when
- 個別の oracle file、realization file、CLI 実行処理、実際のファイル操作を調査するとき。
- StructDoc や Requirement など共通データ構造の定義だけを確認したいとき。
- 対象本文の具体的な INDEX.md 要約だけを作成するときは、対象本文を直接読む。

## hash
- aadaf4690ecb57aa6f380b264e7722bbe6be24f0c56c455754313ceb1df535f4
