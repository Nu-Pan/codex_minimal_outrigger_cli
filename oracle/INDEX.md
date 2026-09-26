# `doc`

## Summary
- cmoc の正本仕様をまとめた文書群です。アプリケーションの共通動作や各コマンドの契約、利用 workflow を示します。
- 共有する branch・session・run のモデル、開発規則・環境・テスト要件、および過去に不採用とした方式の理由も扱います。不採用案の記録は現行仕様の代わりにはなりません。

## Read this when
- cmoc の共通動作、複数の workload にまたがる責務や優先関係を確認・変更するとき。
- session・run の branch、commit、worktree の関係や利用 workflow を把握するとき。
- 開発規則、環境構築、テスト要件を確認するとき、または設計案を不採用とした理由が判断に関係するとき。

## Do not read this when
- 特定コマンドの目的、引数、成果物、失敗時の扱いだけを確認する場合は、そのコマンドの仕様へ直接進んでください。
- 特定の仕組みの細部だけが必要な場合は、その仕組みを定める個別仕様へ進んでください。
- 正確な algorithm、schema、prompt 文面などが oracle doc から委譲されている場合は、その詳細を所有する oracle src を参照してください。

## hash
- 72bbbdb4cf5e8d9d1048f327c00320f8f5ab404e818a9a5f73ccbbbb12030ca9

# `src`

## Summary
- CMOC の oracle 実装を集め、共有モデルや文章構築部品から agent 向け prompt を組み立てる。
- 操作別の agent call 定義、editor input handoff の生成、フィードバックの処理など、実装上の動作を確認する入口。

## Read this when
- 共通 prompt の構成や、操作ごとの agent call が受け取る指示・パラメータの実装を調査または変更するとき。
- パス、設定、文書検索、文書参照、構造化文書のモデルや、handoff・フィードバック処理の実装を追うとき。

## Do not read this when
- CMOC が満たすべき人間の意図や規範を確認するときは、oracle の文書仕様を直接読む。
- 製品コードを変更するときは realization の実装を、期待動作や検証条件を確認するときは oracle のテストを直接読む。

## hash
- 6f5890ba0dcf0d311e0437cacd7347250de3ff1d619d5af6fea8a95945bebbae
