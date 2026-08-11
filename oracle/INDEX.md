# `doc`

## Summary
- cmoc の正本文書を集約する領域。CLI の挙動仕様、branch・commit・worktree のモデル、開発ルール、および採用しなかった設計案の検討記録への入口を提供する。実装・テスト・環境構築・状態管理などの判断では、目的に対応する下位文書へ進む。

## Read this when
- CLI 自動補完の境界条件や通常実行との処理差を確認するとき
- session fork、run の隔離、branch・commit・worktree の関係を確認するとき
- cmoc の Python 実装、CLI 設計、開発環境、テスト要件、テスト実行手順を確認するとき
- realization refactor で採用しなかった方式の理由や設計背景を調査するとき

## Do not read this when
- Windows toast 通知固有の自動補完境界を確認するときは、該当する Windows toast 通知仕様へ直接進む
- 特定の CLI 挙動や出力内容だけを確認するときは、対応するアプリケーション仕様へ直接進む
- テストの意味上の要件だけを確認するときは、テスト要件文書へ直接進む
- テストや品質検査の実行手順だけを確認するときは、テスト実行手順文書へ直接進む
- 現行の realization refactor 状態、具体的な realization 実装、ログや実行成果物の形式だけを確認するときは、対応する直接の対象へ進む
- 採用済みの現行仕様や実装の根拠を確認するときは、不採用案の検討記録を入口にしない

## hash
- b6377c37db9079c98721fa5b6a15605384c5ad016415cb2b2aa8c2b4e74d0360

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
