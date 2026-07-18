# `doc`

## Summary
- cmoc のアプリケーション仕様と開発規則を扱う oracle 文書群。利用者向け挙動、session・run の分離、主要サブコマンド、ログ、状態管理、プロンプト、外部モデルサービス、CLI 設計、Python 開発、テスト方針への入口を提供する。

## Read this when
- cmoc の利用者向け挙動、サブコマンド、実行前処理、状態管理、ログ、プロンプト生成、外部モデルサービスの仕様を調査・実装・検証するとき。
- session・run の branch や worktree 境界、fork/join、branch・commit 名の責務を確認するとき。
- Python 実装、CLI の配置、開発環境、pytest や Real Codex CLI 結合テストの規則を確認するとき。
- 複数のアプリケーション仕様または開発規則にまたがる変更で、個別文書への入口を探すとき。

## Do not read this when
- 個別仕様の詳細が特定できている場合は、このディレクトリ全体ではなく該当する oracle 文書を直接読む。
- 開発手順だけを確認したい場合は、アプリケーション仕様文書ではなく開発規則の文書を直接読む。
- 実装ファイルや Codex CLI の出力品質そのものを調査するとき。
- 採用しなかった設計案の背景だけを確認したい場合は、considered_alternative の文書群を読む。

## hash
- 5874cf4d45f95c7bb999fa96e143650a83dc4fb8c4a9cd601745be647ef2ef53

# `src`

## Summary
- cmoc の oracle src を構成する実装群。ACP agent call の設定、oracle review・apply・indexing などの prompt と Structured Output schema、共通 prompt 規範、設定・パス・構造化文書モデルを扱う。各サブディレクトリは個別機能の prompt 実装や共通モデルへの入口となる。

## Read this when
- oracle src 全体の責務分担や、ACP builder・prompt builder・共通モデルの関係を確認するとき。
- oracle review、apply fork、indexing、session join などの agent call 設定や Structured Output schema の実装を調査するとき。
- cmoc 設定、モデル・推論強度、ファイルアクセス、パス解決、構造化文書変換の実装を確認するとき。

## Do not read this when
- 特定の oracle review 操作、prompt 部品、設定モデル、パスモデルの詳細だけを調べるとき。
- CLI サブコマンドの呼び出し経路や永続化処理など、oracle src 外の上位実装を直接確認すべきとき。
- 既存の Structured Output schema や prompt 本文を変更せず、realization 側の実装だけを調査するとき。

## hash
- 8f7ad14c12fa3be8209bdc255974511dd0ac0d8548d0df716d0e46f050c56fec
