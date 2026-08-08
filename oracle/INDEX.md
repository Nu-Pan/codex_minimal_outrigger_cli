# `doc`

## Summary
- cmoc の正本ドキュメントを集約するディレクトリ。アプリケーション仕様、開発規則、不採用案の検討記録を扱い、それぞれの詳細文書へ進むための入口となる。

## Read this when
- cmoc のアプリケーション挙動や開発規則に関する正本文書の所在を確認するとき
- CLI、実装、テスト、開発環境など複数の仕様領域にまたがる調査・変更対象を特定するとき
- 採用しなかった設計案やリファクタ方針の背景を確認するとき

## Do not read this when
- 確認対象の個別仕様文書がすでに特定できており、その本文だけを読めばよいとき
- 実装コード、テストコード、開発成果物そのものを確認するとき
- INDEX.md のルーティング情報だけを確認するとき

## hash
- 4e0ff981deb0b9327b0f0e4fddc21c26074c20a8d2c00d1f4ee2689ec88392ac

# `src`

## Summary
- 対象領域は、cmoc の oracle 側でエージェント呼び出しを組み立てる実装の入口です。共通の呼び出しパラメータや prompt・Structured Output の構築と、TUI、indexing、feedback、oracle review、realization、session join など用途別の builder へ案内します。

## Read this when
- AI コーディングエージェントのモデル、推論強度、ファイルアクセス、作業ディレクトリ、Structured Output などの呼び出し契約を調べるとき。
- 用途別の agent call parameter や prompt 構築箇所を特定するとき。
- 共通 builder、基盤モデル、用途別 builder のどこから調査を始めるか判断するとき。

## Do not read this when
- 実際のサブコマンド実行フローや agent call の起動処理を調べるとき。
- prompt の共通構造や静的な規範部品だけを確認したいとき。
- 個別の schema、基盤モデル、正本仕様、realization 実装、feedback 保存処理の詳細だけを確認したいとき。

## hash
- a89f29b34b0f33d0f44896bf7f709a868e867b8e0341e43d1d92c987ef12dad8
