# `doc`

## Summary
- `oracle/doc` は、cmoc の正本仕様と開発規約を横断的に探すための上位ドキュメント領域である。アプリケーション挙動、branch・commit・worktree、採用しなかった代替案、開発ルールの各入口を提供し、目的に応じて下位文書へルーティングする。

## Read this when
- cmoc の仕様・設計背景・開発規約の入口を探すとき
- CLI や session/run、branch・commit・worktree、アクセス制御などの現行仕様または設計判断の所在を横断的に確認するとき
- Python 実装、環境構築、テスト要件、テスト実行手順などの開発ルールへ進む入口を選ぶとき

## Do not read this when
- 確認対象の具体的な下位仕様書、代替案資料、または開発規約文書が明確なときは、その対象を直接読む
- 実装コードや realization file の具体的な挙動だけを調査するとき
- 現行仕様ではなく、特定の不採用案の理由だけを調べる場合は、該当する検討資料へ直接進む

## hash
- beee819dbb0df30587330fbebfc6ca9f7f88055c8f8b8a88a47dfe81d34b9e11

# `src`

## Summary
- `oracle/src` は、cmoc の agent 呼び出し定義と prompt 構築を実装する Python ソースのルートです。
- `acp_builder` は、モデル・推論強度・ファイルアクセス・作業ディレクトリ・Structured Output などの agent call パラメータと、用途別 builder を扱います。agent 起動用途や review・realization・session・TUI・indexing の構成を確認するときの入口です。
- `prompt_builder` は、担当概要・完了条件・共通ポリシー・ファイルアクセス規定・routing・placeholder・editor 入力文面を組み合わせて完全 prompt を構築します。prompt の構成や用途別 policy の注入条件を確認するときに進みます。
- `other` は、cmoc 設定、パス解決、policy の合成、構造化 Markdown のレンダリングを実装します。agent call の環境決定や prompt の共通データ構造を確認するときの入口です。
- `feedback` は、人間対応が必要な問題を報告する reporter input の契約を定義します。feedback 報告項目や入力形式を確認するときに進みます。

## Read this when
- cmoc の agent call 構築、完全 prompt 生成、共通 policy、パス・設定解決、構造化 Markdown、feedback 入力契約の実装を調査するとき
- 下位の用途別 builder や prompt policy の実装へ進む前に、oracle 実装全体の責務分担と入口を把握するとき

## Do not read this when
- CLI サブコマンドの実行制御や agent call の実行処理そのものを確認するとき
- 個別の oracle・realization・session の正本仕様や Git 操作の実装だけを確認するとき
- prompt policy の具体的な要求・禁止事項だけを確認するときは、prompt_builder 配下の該当 policy 実装へ直接進むとき
- 保存済み feedback の収集・集約・重複判定だけを確認するとき
- Codex CLI sandbox など外部規定の正本仕様を確認するとき

## hash
- fcdd97d7927b61f352d2a3e37b21b77cffff9eb7f9b70825a03c9e0b4a8ea9df
