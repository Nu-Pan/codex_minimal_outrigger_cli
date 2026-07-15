# `acp_builder`

## Summary
- ACP builder の oracle src をまとめる領域。AI エージェント呼び出しパラメータの基礎型、各 cmoc サブコマンド向けの prompt・Structured Output 設定、実行時のファイルアクセス方針を扱う。
- 変更要約・ファイルレビュー修正、indexing、oracle review、session join の conflict 解消、TUI 起動・実行パラメータ解決の各仕様を下位要素から確認するための入口。

## Read this when
- ACP builder の agent call パラメータやファイルアクセスモードの仕様を確認するとき。
- `cmoc apply fork`、`cmoc indexing`、`cmoc review oracle`、`cmoc session join`、`cmoc tui` の prompt 構築や Structured Output 設定を調査するとき。
- oracle review の所見列挙・擁護・反証・採否判定・統合のどの処理を読むべきか判断するとき。

## Do not read this when
- ACP builder を呼び出す実行本体や、下流の realization 実装・テストを調査するとき。
- 共通 prompt builder、パス解決、構造化文書処理そのものの実装詳細を調査するとき。
- INDEX.md の生成規則や、oracle と realization の一般的な責務定義だけを確認したいとき。

## hash
- 1f706c9a7496b6a242cc44ea00dd5b2da3430b3d16cf5ae6bf5d2df0ca8b070b

# `other`

## Summary
- `oracle/src/oracle/other` 配下の、cmoc の設定モデル、ルートパス解決、規範文書のデータ化、構造化 markdown 組み立てをまとめて扱う入口。個別ファイルを選ぶ前に、この層でどの共通基盤を読むべきかを判断したいときに使う。

## Read this when
- cmoc の永続設定モデルや、その既定値・保存方針を確認したい。
- ルートパスのプレースホルダ解決や、実パスとの相互変換を確認したい。
- 規範文書を保持するデータ構造や、markdown への落とし込み方を確認したい。
- 階層付き markdown のレンダリング、`cmoc_ref` と `cmoc_block` の検査、文字列やコードブロックの正規化を確認したい。

## Do not read this when
- `cmoc` の各サブコマンドの実行手順や CLI の入出力を追いたい。
- 設定読み書きの具体的な永続化処理や、サブコマンド固有の業務ロジックを見たい。
- 構造化文書やパス解決以外の別系統の共通処理を探したい。

## hash
- 6139c507e1f8a0fcd13dc8bbffa88ee7e994d18d1b93d3403a866d084f29eca8

# `prompt_builder`

## Summary
- oracle と realization、アクセス規則、レビュー基準、ルーティング規則などをプロンプト部品として構造化するソース群。プレースホルダ型、完全な agent 用プロンプトの組み立て、各 standard の注入処理を確認する入口。

## Read this when
- oracle・realization の定義や standard、レビュー基準、ファイルアクセス規則、ルーティング規則を確認または変更するとき
- 完全な agent 用プロンプトの構成、standard の依存関係・注入順序、プレースホルダの扱いを調査するとき

## Do not read this when
- 個別の oracle file・realization file の具体的な仕様や実装を調査するとき
- CLI の実行フロー、ファイル探索、入出力形式、生成済み文書の保存・表示処理を調べるとき

## hash
- 31af1f9fbf5bd64b0d1ff4e5f6dd527ab86afb79a3121e2039b2ab277272b1dc
