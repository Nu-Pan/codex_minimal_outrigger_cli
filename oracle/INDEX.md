# `doc`

## Summary
- cmoc の正本ドキュメント群への入口。アプリケーション仕様、branch・commit・worktree のモデル、採用しなかった設計案の検討記録、開発ルールを扱い、目的に応じた下位文書へ進むためのルーティングを担う。

## Read this when
- cmoc の正本仕様や開発ルールの所在を確認するとき
- CLI・Codex 呼び出し・ログ・feedback・prompt・run／session・通知などのアプリケーション挙動を調べるとき
- session fork、run の隔離、branch・commit・worktree の関係を調べるとき
- 実装配置、開発環境、テスト要件、テスト実行手順を確認するとき
- 現行仕様ではなく、採用しなかった設計案の背景や採否理由を調べるとき

## Do not read this when
- 実装ファイルやテストの具体的な挙動だけを確認する場合
- 読むべき特定の正本文書が既に判明しており、その本文へ直接進める場合
- 単一の CLI サブコマンドの挙動だけを確認し、関連する仕様の分担や境界を調べる必要がない場合
- 現行仕様や実装の直接の参照先が必要で、採用しなかった設計案の背景を確認する必要がない場合

## hash
- e22ea899003707a6f4c3c086a0c09f6d4a98a7be947fe62bdbb0e81390d1eee6

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
