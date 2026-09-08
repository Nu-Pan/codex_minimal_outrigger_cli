# `doc`

## Summary
- cmoc の正本文書・開発規則・branch model・設計上の不採用案を、アプリケーション仕様、開発ルール、branch 関係、検討資料の責務別に振り分ける文書群への入口。現行仕様と実装に追従する規則、または過去の設計判断の背景を参照する際の起点となる。

## Read this when
- cmoc の仕様・開発規則・branch model・設計判断の背景のうち、どの文書群を読むべきか切り分けるとき。
- 複数の領域にまたがる調査や変更で、現行の正本仕様、開発上の規則、Git の概念、採用しなかった案の境界を確認するとき。

## Do not read this when
- 参照対象の仕様文書、開発規則、branch model、または検討資料がすでに特定できており、その本文だけを確認したいとき。
- 実装コード、個別の oracle／realization file、または特定 agent call の厳密な builder・schema を直接調べるとき。

## hash
- b3d44843265139beb73a7d08bfd6c1ff3a64b164c740395084b0a596820926ba

# `src`

## Summary
- AI コーディングエージェント呼び出しの共通パラメータ型、ファイルアクセスモード、パスコンテキストを提供する。
- quota probe、indexing、feedback、oracle、realization、session、TUI など用途別の agent call パラメータ構築への入口を提供する。
- prompt_builder で task・scope・completion criteria・non-goals、各種 policy、placeholder、構造化 Markdown prompt を組み立てる。
- editor input handoff の初期文面、feedback issue の正規化・remediation、oracle と realization の編集・調査・追従・conflict 解消に関する call 設定を扱う。
- other では root path の解決・placeholder 変換、構造化文書のレンダリング、cmoc と Codex の call 設定を扱う。

## Read this when
- agent call の共通設定、アクセスモード、cwd、Structured Output schema、indexing preflight の設定を確認するとき。
- 用途別 builder がどの prompt policy と対象パスを組み合わせるかを確認するとき。
- oracle・realization の編集、レビュー、調査、追従、feedback remediation、session join conflict 解消の call 構築責務を調べるとき。
- 構造化 prompt の生成・Markdown レンダリング、root path または placeholder の解決方法を確認するとき。

## Do not read this when
- Codex CLI の共通実行処理や外部ツール側の実際の挙動だけを調査するとき。
- 特定用途の prompt、出力契約、編集対象の詳細が必要な場合は、該当する下位ディレクトリの対象を直接読む。
- oracle・realization file の正本仕様や具体的な編集手順を確認するとき。

## hash
- f6be3456a3ade6b98b42c74347001d21d3dc7d4625e3294082f534772d889d55
