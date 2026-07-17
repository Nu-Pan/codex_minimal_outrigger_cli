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
- agent call 用の完全なプロンプトを組み立てる実装と、プレースホルダ対応型、oracle／realization やルーティング規範などをプロンプトへ変換する部品群を収録する。プロンプト構成全体や個別 standard の注入処理、プレースホルダ表現を調査・変更するときの入口となる。

## Read this when
- 完全な agent 用プロンプトの構成や、静的・動的プロンプトの統合方法を確認したいとき。
- oracle／realization の定義・standard、アクセス規則、INDEX.md ルーティング規則を prompt に組み込む処理を調査・変更するとき。
- プレースホルダ展開に使う型や、各 standard の個別 build 処理を確認したいとき。

## Do not read this when
- CLI コマンドの処理、ファイル探索、実際の読み書き、agent の業務ロジックを調査するとき。
- 個別の oracle file や realization file の仕様・実装そのものを確認するとき。
- レビュー結果の保存・表示形式や JSON schema、prompt builder 全体の呼び出し側を確認したいとき。

## hash
- f9d742947ac0f7005fc9eaf397ee3bdc7ced921e1551f6c05017d48b8b87b07b
