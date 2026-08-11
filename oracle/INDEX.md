# `doc`

## Summary
- cmoc の正本仕様ドキュメント群を収める領域。アプリケーション仕様、branch・commit・worktree モデル、開発ルール、採用しなかった設計案の記録を扱い、実装やレビューで人間定義の挙動・責務境界・開発上の規則を確認するための入口となる。

## Read this when
- cmoc のアプリケーション機能、session・run の分岐モデル、branch／commit／worktree の関係を確認するとき
- Python 実装、CLI の配置、開発環境、テスト要件、テスト実行手順を確認するとき
- realization refactor の採用・不採用となった作業方式や設計判断の背景を調べるとき
- 複数の正本仕様領域から対象文書を選び、詳細本文へ進む入口が必要なとき

## Do not read this when
- 特定の実装ファイルやテストファイルの具体的な挙動だけを確認すれば足りるとき
- 特定機能の詳細仕様がアプリケーション仕様の下位領域に直接定義されており、その本文へ直接進めるとき
- 開発環境、テスト要件、テスト実行手順など、対象の専用文書が明確で直接参照できるとき
- 採用済みの現行仕様ではなく、単に実装や実行成果物の形式を確認したいとき

## hash
- c4c7145d95ba5e436215f6b3b24974d5964fc000a2b9537f443f42d57068b3ac

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
