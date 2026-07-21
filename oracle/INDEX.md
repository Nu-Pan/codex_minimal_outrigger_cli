# `doc`

## Summary
- cmoc のアプリケーション仕様、branch・commit・worktree モデル、不採用案、Python 開発規則を扱う oracle 文書群。利用者向け挙動や状態管理などの機能仕様、開発・設計・テスト規約を確認するための入口。

## Read this when
- cmoc の共通挙動、CLI、状態管理、ログ、プロンプト、run/session lifecycle の仕様を確認するとき
- session fork、run 隔離、branch・commit・worktree の責務やライフサイクルを調査するとき
- Python 実装、CLI 配置、開発環境、pytest テストの規約を確認するとき
- realization refactor で採用しなかった作業方式や設計案の理由を確認するとき

## Do not read this when
- 特定の realization code や realization test の内部実装だけを調査するとき
- 個別機能の詳細仕様を確認する場合は、対象機能の oracle 文書を直接読むとき
- 一般的な INDEX.md の読み方やルーティング方針を確認するとき
- README だけで足りる一般的な利用方法を知りたいとき

## hash
- 318f7a77359b92470dccdc8b5bf57cf1c5e87e7860cff72da0d26c07c7865045

# `src`

## Summary
- 参照可能な正本ソースの有無を確認するための入口です。実装仕様や具体的な処理内容は扱いません。

## Read this when
- このディレクトリ内の内容や、参照可能な正本ソースの有無を確認するとき。

## Do not read this when
- 実装仕様や具体的な処理内容を確認したいとき。

## hash
- 2401855b3feb2a70997d095bc32138b71c627bfd7dfeffd9feaa01c27dda4368
