# `doc`

## Summary
- cmoc のアプリケーション仕様と開発規約をまとめた oracle 文書群への入口。CLI の利用者向け挙動、状態管理、ログ、プロンプト、run/session lifecycle、branch model、Python 実装、設計、開発環境、テスト方針を扱う。採用しなかった設計案の検討記録にも進める。

## Read this when
- cmoc の共通仕様、CLI 呼び出し、状態管理、ログ、プロンプト、run/session lifecycle を実装・検証するとき
- session fork、run の隔離、branch・commit・worktree の関係や基準 commit を確認するとき
- Python の実装規約、CLI の責務配置、開発環境、pytest によるテスト方針を確認するとき
- realization refactor の作業方式や不採用案の理由を調査するとき

## Do not read this when
- 特定の realization code または realization test の内部実装だけを調査するとき
- 個別機能の具体的な挙動・出力仕様を確認するときは、app_spec 配下の対応する文書を直接読むとき
- 一般的な INDEX.md の読み方やルーティング方針を確認するとき

## hash
- 8ff6bbffa83a828e6c2c92603b5597c6e4a398744360d0175962a12753c56184

# `src`

## Summary
- 参照可能な正本ソースの有無を確認するための入口です。実装仕様や具体的な処理内容は扱いません。

## Read this when
- このディレクトリ内の内容や、参照可能な正本ソースの有無を確認するとき。

## Do not read this when
- 実装仕様や具体的な処理内容を確認したいとき。

## hash
- 2401855b3feb2a70997d095bc32138b71c627bfd7dfeffd9feaa01c27dda4368
