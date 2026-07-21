# `doc`

## Summary
- cmoc の正本仕様文書群を集約するディレクトリ。アプリケーション仕様、branch・commit・worktree モデル、不採用案の検討記録、Python・CLI・開発環境・テストに関する開発ルールへの入口を提供する。

## Read this when
- cmoc の利用者向け挙動、CLI 共通処理、Codex 連携、ログ、プロンプト、状態管理、run/session lifecycle の仕様を確認するとき
- branch・commit・worktree の関係や run・session のライフサイクルを調査・変更するとき
- Python 実装、CLI 配置、開発環境、realization test のルールを確認するとき
- realization refactor の不採用案や設計判断の背景を調べるとき

## Do not read this when
- 特定機能の実装詳細やテスト内容だけを調査するときは、対応する realization code や個別 oracle 文書へ直接進む
- Python 実行環境、設計ルール、テストルール以外の個別仕様を確認するときは、対象機能の oracle doc へ直接進む
- INDEX.md の読み方やルーティング方針自体を確認するときは、対応する routing 文書を読む

## hash
- 76334f9c23436496e3d197f98d869eeef0e25ce783fbc82d38e208a5edab45a7

# `src`

## Summary
- 参照可能な正本ソースの有無を確認するための入口です。実装仕様や具体的な処理内容は扱いません。

## Read this when
- このディレクトリ内の内容や、参照可能な正本ソースの有無を確認するとき。

## Do not read this when
- 実装仕様や具体的な処理内容を確認したいとき。

## hash
- ede395b8782baefa21af26f3149ccf8021c4806d0acff442d36e09ca18299999
