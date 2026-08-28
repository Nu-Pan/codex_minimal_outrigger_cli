# `doc`

## Summary
- cmoc の正本文書群全体への上位入口。アプリケーション仕様、開発ルール、branch 運用、検討資料を領域別に選び、具体的な正本文書へ進むためのディレクトリ。
- CLI の挙動、session・run、feedback、ログ、通知、prompt、Codex 呼び出しなどは app_spec、実装・環境・テストの規則は dev_rule、git による隔離モデルは branch_model、不採用案の背景は considered_alternative から確認する。

## Read this when
- cmoc の正本仕様または開発関連文書の所在を判断するとき。
- 対象機能の個別仕様、開発ルール、branch 運用、または設計上の不採用案へ進む上位入口が必要なとき。

## Do not read this when
- 確認対象の機能やルールが明確で、対応する配下の個別文書を直接読めるとき。
- 実装ファイルやテストの具体的な挙動だけを調べるとき。
- INDEX.md の生成・更新規則そのものを調べるときは、app_spec 内の indexing 仕様を直接読む。

## hash
- 04b8792d848e653c894d15a3fcc08488cdf7ad4c2a37fee7b7ebfd02f5fb490f

# `src`

## Summary
- cmoc の agent call 構築、prompt 生成、設定・パスモデル、構造化文書レンダリング、feedback 処理を担う oracle 実装の入口です。
- agent call の種類別処理は acp_builder、prompt の組み立てと規定文面は prompt_builder、共通の設定・パス・文書構造は other 配下から確認します。

## Read this when
- oracle 実装の責務分担や下位領域の入口を確認したいとき。
- agent call のパラメータ構築、prompt の生成、ファイルアクセス・routing・oracle/realization 関連 policy の実装を調べるとき。
- cmoc の設定、agent call 用パス placeholder、構造化文書の生成・Markdown レンダリングを調べるとき。

## Do not read this when
- oracle の意味仕様や開発規則を確認したいときは、対応する oracle/doc を直接読んでください。
- 特定の agent call、prompt policy、feedback、設定・パスモデルの具体的な挙動だけを調べるときは、対応する下位ディレクトリまたは実装を直接読んでください。
- INDEX.md の生成規則や routing の意味仕様だけを確認したいときは、対応する oracle/doc または専用の下位要素を直接読んでください。

## hash
- 0f9b9bde67c18cf82babfce28d668895c006eae31818b5e27b4b8af7e8c07a01
