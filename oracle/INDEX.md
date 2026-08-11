# `doc`

## Summary
- cmoc の正本文書を領域別に案内する入口。アプリケーション仕様、branch・commit・worktree のモデル、不採用案の検討記録、開発ルールを扱い、目的に応じて各文書へ進む。

## Read this when
- cmoc の CLI や利用時挙動に関する正本仕様の所在を特定するとき。
- session、run、branch、commit、worktree の関係やライフサイクルを確認するとき。
- 採用されなかった refactor の作業方式・検査方式・状態管理方式の理由を調べるとき。
- Python 実装、CLI 配置、開発環境、テスト要件、テスト実行手順を確認するとき。

## Do not read this when
- 目的の個別仕様、設計ルール、開発環境文書、テスト要件、テスト実行手順が明確な場合は、その本文を直接読む。
- 実装ファイルやテストの具体的な挙動だけを確認する場合。
- 現行実装や採用済み仕様の詳細を確認する場合に、不採用案の検討記録を読む必要はない。

## hash
- 1c5685f3896323c5aac2e3a9de7623ee0e672534beda4bf48d8c65b020d1232f

# `src`

## Summary
- cmoc の oracle 側ソースコードと構造化出力スキーマの領域。agent call の共通パラメータ、用途別の prompt 構築、oracle・realization・routing・feedback の規則、レビュー判定、パスモデルや文書モデルを扱い、下位ディレクトリの個別定義へ進む入口となる。

## Read this when
- agent call のモデル、推論強度、ファイルアクセス、作業コンテキストを確認・変更するとき。
- 用途別の prompt、Structured Output schema、oracle review、feedback 判定、index entry 生成の定義を調査・変更するとき。
- oracle と realization の扱い、prompt の共通規則、Markdown・構造化文書の生成基盤を確認するとき。

## Do not read this when
- 通常の CLI 実行処理、realization 側の実装・テスト、または oracle の自然言語仕様そのものを確認するとき。
- feedback の保存・集約・重複判定など collector 側の処理だけを調査するとき。
- 特定の agent call や規則が明らかな場合は、この領域全体ではなく該当する下位ディレクトリへ直接進むとき。

## hash
- 2163e860a6467b14ed0e0668fe5abb1da55df3ff2887282e842ab10f88013e04
