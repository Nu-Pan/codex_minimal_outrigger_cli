# `doc`

## Summary
- cmoc の正本ドキュメントを集約するディレクトリ。アプリケーション仕様、branch・commit・worktree のモデル、不採用案の検討記録、Python 開発ルールを扱い、各仕様文書へ進むための入口となる。

## Read this when
- cmoc のアプリケーション挙動、branch・worktree の関係、不採用設計の背景、Python 開発ルールの正本文書を特定するとき
- 複数の正本ドキュメントにまたがる責務境界や参照先を判断するとき

## Do not read this when
- 読むべき個別文書がすでに特定されており、その本文へ直接進めるとき
- 実装配置やテスト実行など、特定の開発ルール文書だけを確認すればよいとき
- INDEX.md のルーティング情報だけを確認するとき

## hash
- fa5811512be861b1792d08fadba76f188af336e1efc708f8132af83de01170fc

# `src`

## Summary
- cmoc の oracle src を収める実装領域です。AI エージェント呼び出しのパラメータ、feedback 入力契約、設定・パス・構造化文書モデル、プロンプト構築部品を扱います。
- agent call builder、feedback、基礎モデル、prompt builder という責務別の下位領域へ進むための入口です。

## Read this when
- cmoc の oracle src 全体から、調査対象の責務を特定して適切な下位領域へ進みたいとき。
- AI エージェント呼び出し、feedback reporter、設定・パスモデル、構造化文書、プロンプト構築のいずれかを横断して確認するとき。

## Do not read this when
- 特定の agent call builder の prompt や Structured Output schema を調査するときは、対応する下位領域へ直接進む。
- feedback の入力契約だけを確認するときは、feedback の schema を直接読む。
- 設定値、パス解決、Standard、StructDoc の個別定義だけを確認するときは、other の対応するモデルを直接読む。
- プロンプト共通部品の実装詳細だけを確認するときは、prompt_builder またはその parts を直接読む。

## hash
- 63540f0412dcba7fc66a19f0e7574cffcdff6f19d1838d48e386e6b0f93174ce
