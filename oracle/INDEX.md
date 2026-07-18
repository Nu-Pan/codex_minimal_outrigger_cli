# `doc`

## Summary
- cmoc のアプリケーション仕様断片を収録するディレクトリ。利用者向け挙動、CLI サブコマンド、session/run の branch 境界、開発規則、採用しなかった設計案への入口を提供する。

## Read this when
- cmoc の利用者向け挙動やサブコマンド仕様を実装・変更・検証するとき。
- CLI の前処理、補完、ログ、エラー処理、session 状態、実行隔離、prompt 生成などの正本仕様を探すとき。
- session と run の branch/worktree 境界を確認するとき。
- Python 開発環境、CLI 設計・配置、realization test の開発規則を確認するとき。
- 採用されなかった設計案や、その不採用理由を確認するとき。

## Do not read this when
- 具体的な実装コードやテストコードの責務・配置だけを確認したいとき。
- 個別機能の詳細仕様を確認したいときは、対応する仕様文書を直接読む。
- 一般的な利用手順だけを確認したいとき。
- 現行仕様ではなく通常の git 運用やリポジトリ本流の方針だけを確認したいとき。

## hash
- c19411a131c891a1f99a0d17b62ea978801bb43af3ba83c0072b7f903d58d432

# `src`

## Summary
- cmoc の ACP エージェント呼び出しに関する oracle src の領域。サブコマンド別の prompt、Structured Output schema、モデル・推論・アクセス設定を扱う下位領域への入口。
- cmoc の設定・パス解決・規範文書モデル・Markdown 変換を扱う oracle src の領域。
- プレースホルダ展開、完全なプロンプト構築、標準ルール部品とその注入内容を扱う oracle src の領域。

## Read this when
- サブコマンドがエージェントへ渡す AgentCallParameter、prompt、Structured Output schema、モデル・推論強度、ファイルアクセス設定を調査・変更するとき。
- cmoc 固有設定、実行上限、ルートパス解決、規範文書モデル、構造化文書の Markdown 出力を確認するとき。
- プレースホルダ展開、動的プロンプトの構造、標準ルールの依存関係や注入内容を調査・変更するとき。

## Do not read this when
- ACP パラメータの共通型や既定値だけを確認するときは、共通定義を直接読む。
- agent call の実行本体、TUI 画面処理、差分適用、conflict 解消、設定 JSON の永続化や doctor 同期だけを調べるとき。
- 特定サブコマンドの実装・schema、個別標準文書、個別注入パーツ、プロンプト置換ロジックやファイル探索処理だけを確認するとき。

## hash
- 0a53ddf4b79cb93017ab5b869e985003cd44735b67a88c06cbe1752959afec46
