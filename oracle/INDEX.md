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
- AI コーディングエージェント呼び出しに渡すパラメータ、アクセスモード、cwd、prompt、Structured Output schema をまとめる構成への入口。
- agent call の prompt を組み立てる共通部品、ポリシー、oracle・realization の基本説明、routing、feedback 報告、editor input handoff を扱う。
- indexing、feedback、oracle 編集・調査、realization の適用・リファクタ、session join、TUI、quota probe など用途別の起動パラメータ構築へ進む起点。
- パス解決、cmoc 設定、構造化ドキュメントのレンダリングなど、agent call と prompt 構築を支える共通モデルも含む。

## Read this when
- agent call の共通パラメータ、FileAccessMode、Structured Output schema、cwd、indexing preflight の扱いを確認または変更するとき。
- 複数の agent call に共通する prompt、file access、oracle・realization、routing、feedback reporting の規定を確認するとき。
- 特定の cmoc 操作に対応する agent call の prompt 構築や起動パラメータの入口を探すとき。
- prompt のプレースホルダ、パスコンテキスト、設定モデル、構造化ドキュメントの生成・レンダリングを調べるとき.

## Do not read this when
- 特定の agent call の詳細な作業手順や出力契約だけを確認したいときは、該当する用途別 builder または schema を直接読む。
- oracle doc、realization file、feedback state などの正本データや保存内容そのものを確認したいとき。
- Codex CLI の実際の起動処理や、agent call 後の状態管理・実行結果処理だけを調査したいとき。

## hash
- 06f5bcfd3a9c90663c02273f8af3360520ad35052c21128991733f46d58ec77c
