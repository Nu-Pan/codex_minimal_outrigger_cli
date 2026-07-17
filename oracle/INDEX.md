# `doc`

## Summary
- cmoc の正本文書群を分野別に収録するディレクトリ。アプリケーション仕様、branch・worktree モデル、採用しなかった代替案、開発規則を確認する際の入口となる。

## Read this when
- cmoc の仕様・設計判断・開発手順に関する oracle doc を探すとき。
- 対象文書の分野が、アプリケーション仕様、branch モデル、設計上の不採用案、Python・CLI・テストなどの開発規則に該当するとき。

## Do not read this when
- 対象の仕様文書や開発規則が既に特定できており、下位の個別文書へ直接進めるとき。
- realization code の具体的な実装詳細や INDEX.md のルーティング規則を調査するとき。

## hash
- 93a29b2dd58656d436d1f2348cf47df3f7a0ad36270f7f5256ebcdb693c3dedb

# `src`

## Summary
- ACP builder の oracle src をまとめる領域。AI エージェント呼び出しパラメータ、cmoc の各サブコマンド向け prompt・Structured Output 設定、実行時のファイルアクセス方針を扱う。
- cmoc の設定モデル、既定値、ルートパス解決、規範文書のデータ化、構造化 markdown の処理など、複数機能から利用される共通基盤を確認する入口。
- 完全な agent 用 prompt の組み立て、静的・動的 prompt の統合、oracle／realization の規範や各 standard の注入、プレースホルダ展開を扱う。

## Read this when
- ACP builder の agent call パラメータやファイルアクセスモードを確認・変更するとき。
- cmoc apply fork、indexing、review oracle、session join、tui の prompt 構築や Structured Output 設定を調査するとき。
- 設定モデル、既定値、保存方針、ルートパスのプレースホルダ解決を確認するとき。
- 規範文書のデータ構造、markdown 変換、構造化 markdown のレンダリング・検査・正規化を調査するとき。
- agent 用 prompt の構成、prompt 統合、standard の注入、oracle／realization 定義の組み込みを調査するとき。

## Do not read this when
- ACP builder の実行本体、下流の realization 実装・テスト、CLI の実行手順や入出力を調査するとき。
- 共通 prompt builder、パス解決、構造化文書処理の実装詳細を直接確認するときは、該当する下位要素へ進む。
- 個別の oracle file や realization file の仕様・実装そのものを確認するとき。
- レビュー結果の保存・表示形式、JSON schema、prompt builder 全体の呼び出し側を確認するとき。
- oracle と realization の一般的な責務定義や INDEX.md の生成規則だけを確認したいとき。

## hash
- 01b799a6dbf45ad4c2b87ade2bfd772c87c8969fcf29151bc65d93b438bf8a30
