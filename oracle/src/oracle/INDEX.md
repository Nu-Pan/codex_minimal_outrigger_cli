# `acp_builder`

## Summary
- ACP builder の oracle src 群をまとめるディレクトリ。エージェント呼び出しパラメータ、共通部品、各サブコマンド向けの prompt・Structured Output schema・実行設定を扱い、下位の個別 builder 仕様へ進む入口。

## Read this when
- ACP builder の oracle 正本仕様を調査・変更するとき。
- エージェント呼び出し条件、prompt、Structured Output schema、ファイルアクセス方針、モデル設定のいずれかを確認するとき。
- 下位の個別 builder や共通部品のどれを読むべきかを、ACP builder の責務から絞り込みたいとき。

## Do not read this when
- realization code 側の ACP builder 実装やテストの詳細を確認するとき。
- ACP builder の前後にある実行フロー、CLI 表示、永続化、実際のファイル編集処理だけを調査するとき。
- ACP builder と無関係な oracle 仕様を探しているとき。

## hash
- 41a3209195eb4b46a34acc3be0fd117c39da08e22717d25468dde53b88c8423b

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
