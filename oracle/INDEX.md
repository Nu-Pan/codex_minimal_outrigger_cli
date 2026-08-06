# `doc`

## Summary
- cmoc のアプリケーション仕様、branch・commit・worktree のモデル、不採用案、Python 開発規則を分野別に収める正本文書群。アプリケーション挙動や開発・テスト方針を確認する際の入口となる。

## Read this when
- cmoc のアプリケーション仕様を調査し、対象となる個別仕様文書を選ぶとき
- branch・session・run・worktree の関係やライフサイクルを確認するとき
- Python の実装、CLI 設計、開発環境、テスト規則・実行手順を確認するとき
- 採用されなかった refactor の作業方式や検査方式の設計理由を調べるとき

## Do not read this when
- 対象の個別仕様文書がすでに特定でき、その本文を直接読むべきとき
- 実装配置、テスト実行手順、開発環境など、対象文書が明確なアプリケーション仕様以外の事項を直接確認するとき
- 現行実装の詳細や具体的なテスト内容だけを確認したいとき

## hash
- 8363ba78bb8990c78d226077232e8a198b51602418f0eeb1f455085169542272

# `src`

## Summary
- cmoc の正本ソースを集約する領域です。agent call の論理パラメータ、用途別 prompt、Structured Output schema、パス・設定・構造化文書・規範のモデルと生成処理を扱います。
- agent call 用の共通モデルと用途別 builder、prompt を組み立てる共通部品、補助的なパス解決・設定・構造化 Markdown 処理が主な構成要素です。

## Read this when
- agent call のモデルクラス、推論負荷、ファイルアクセス、cwd、prompt、Structured Output の契約を調査・変更するとき。
- 用途別の oracle、realization、feedback、review、indexing、TUI、session join 用 prompt の正本を確認するとき。
- prompt 共通規範、パス placeholder、設定、構造化文書のレンダリングを確認するとき。
- 特定の責務が明らかな場合は、agent call builder、prompt builder、または補助モデルの下位領域から確認を始めるとき。

## Do not read this when
- 実際の CLI・TUI 実行フローや agent call の上位制御を調査するとき。
- oracle の自然言語仕様、通常の realization 実装・テスト、feedback の保存・集約処理だけを確認したいとき。
- 対象が特定の用途別 prompt、共通 prompt 部品、または補助モデルに限定されている場合は、この領域全体ではなく該当する下位要素へ直接進むとき。

## hash
- ab37af7a33dbad5010a76c115a1adc4cc80a4fe7a82ac0874da7fcb17b970690
