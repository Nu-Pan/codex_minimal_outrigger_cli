# `doc`

## Summary
- cmoc の正本文書群を、アプリケーション仕様、開発ルール、branch model、不採用案などの責務別入口へ案内する文書ツリー。
- 対象の挙動・設計判断・開発規則に応じて、対応する下位文書を選ぶために使用する。

## Read this when
- cmoc の正本仕様や開発規則を探しており、まず文書群の責務別の入口を判断したいとき。
- アプリケーション挙動、git による隔離モデル、開発環境・設計・テスト規則、または不採用となった代替案を調査するとき。

## Do not read this when
- 特定機能の詳細な挙動、CLI 契約、実装配置、テスト要件などが既に明確で、対応する下位文書を直接確認できるとき。
- 具体的な実装コードやテストコードの調査だけを行うとき。

## hash
- 683bf33785d2b73f901add1c2da4c64db4864b82c687c551f4d3f893b3a49271

# `src`

## Summary
- cmoc の oracle 実装群における上位入口。agent call パラメータ、prompt 構築、用途別の起動・検証定義、設定・パス・構造化文書モデルを下位要素へ振り分ける。
- agent call の呼び出し設定や用途別 builder を調べる場合は acp_builder、prompt の組み立て規則や各種ポリシーを調べる場合は prompt_builder、設定・パス解決・Markdown 構造化文書を調べる場合は other から読み始める。

## Read this when
- oracle の実装全体で、agent call 関連の責務がどの下位要素にあるかを判断するとき。
- 呼び出しパラメータ、prompt 構築、用途別起動処理、設定・パスモデルの調査開始点を決めるとき。

## Do not read this when
- 特定の prompt policy、agent call builder、設定クラス、パス解決処理、または構造化文書モデルだけを確認したい場合は、対応する下位要素を直接読むとき。
- agent call の実行結果の保存・集約や、oracle／realization 本文・INDEX.md 自体の編集方法を調べるとき。

## hash
- 4af0b7fbf24db6d6442d583b4b206d10b4771528c060ff8e984534a8ad377dc5
