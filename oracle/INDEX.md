# `doc`

## Summary
- `oracle/doc` は、cmoc のアプリケーション仕様、branch・commit・worktree モデル、開発規約、テスト規約・実行手順、採用しなかった設計案を集約する正本文書群への入口です。
- CLI の挙動、session/run lifecycle、Codex 呼び出し、ログ・エラー・feedback、doctor、通知などは `app_spec` 配下へ、実装・環境・テストの規約は `dev_rule` 配下へ、branch 関係は `branch_model.md` へ、代替案の採否背景は `considered_alternative` 配下へ進みます。

## Read this when
- cmoc の正本文書を横断的に探し、対象がアプリケーション仕様、branch モデル、開発規約、テスト規約、または設計上の代替案のどの領域に属するか判断するとき
- 複数の機能領域にまたがる変更・調査で、適切な下位文書群への入口を特定するとき

## Do not read this when
- 確認対象の個別仕様、branch・worktree の用語、開発環境、実装配置、テスト要件、テスト実行手順が明らかな場合は、該当する下位文書を直接読むとき
- 実装コード、既存の INDEX.md、Structured Output schema、外部契約の検証結果だけを確認したいとき
- 現行仕様や具体的な実装手順を確認する目的で、採用されなかった代替案の背景資料だけを扱うとき

## hash
- 68d140042d55e3b29cd69a9023151dfcb8820892b79119b06e2ebcfbcb593cae

# `src`

## Summary
- oracle ソース全体の責務と、共通の agent call 構築から個別領域へ進むための入口を定義するディレクトリです。
- agent call 構築、prompt の合成と policy、feedback 入力契約、設定・パス解決・構造化文書モデルを扱う下位対象へのルーティングを提供します。

## Read this when
- cmoc の agent call 構築全体の責務や、共通パラメータから個別処理へ進む入口を確認するとき
- feedback、indexing、oracle、realization、session、TUI、quota probe の agent call 構築を調査・変更するとき
- prompt の統合順序、policy、placeholder、oracle／realization の共通概念を確認するとき
- feedback reporter の入力項目と検証契約を確認するとき
- 設定値、モデル変換、agent call のパスコンテキスト、構造化文書の Markdown 化を確認するとき

## Do not read this when
- 実際の Codex CLI 呼び出し、sandbox 制約、共通 prompt の実行基盤、またはパス解決の利用側の挙動だけを確認したいとき
- 個別の Structured Output schema の項目・型・形式だけを確認したいとき
- 個別の oracle 文書、realization 実装・テスト、feedback state の保存・集約、または CLI サブコマンドの実装挙動だけを確認したいとき
- 既存の INDEX.md のルーティング内容だけを確認したいとき

## hash
- b495881f82709175d85f4af88454e73c675fd91effc47e6eb46ae06a6b70ad4e
