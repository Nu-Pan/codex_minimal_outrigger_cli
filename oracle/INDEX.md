# `doc`

## Summary
- cmoc の正本文書群への入口。アプリケーション挙動、session／run の branch 分離モデル、不採用案の背景、開発ルールを案内し、仕様・設計・実装判断の確認先を振り分ける。

## Read this when
- cmoc の機能仕様や状態遷移、branch・worktree 分離モデル、設計上の不採用案、実装・環境・テストの開発ルールを確認するとき。
- 具体的な個別仕様や開発規則へ進む前に、どの正本文書を読むべきか判断するとき。

## Do not read this when
- 実装コードやテストコードの具体的な挙動を確認する場合は、対象の realization file やテストを直接読む。
- 個別仕様、開発環境、テスト要件など対象文書が特定できている場合は、このディレクトリの概要ではなく該当する文書を直接読む。
- INDEX.md の生成・更新規則だけを確認する場合は、indexing の仕様を読む。

## hash
- ec0406de238d8dbe405be191223f06cfa9130d01345cedd0f966687c1b437f13

# `src`

## Summary
- cmoc が Codex CLI などの agent call に渡す prompt と起動パラメータを構築する実装のルートです。
- agent call の共通パラメータ、ファイルアクセスモード、Structured Output schema、およびサブコマンド別の起動定義を扱います。
- prompt_builder は共通 prompt、placeholder、構造化 Markdown、oracle・realization・routing・feedback などの policy を構築します。
- other は cmoc 設定、agent call 用の root path 解決、構造化文書のモデルと Markdown レンダリングを提供します。
- editor_input_handoff はユーザー入力を editor へ渡すための初期入力定義を提供します。

## Read this when
- agent call の prompt、cwd、ファイルアクセスモード、Structured Output schema、または editor input handoff の構築箇所を探すとき。
- cmoc のサブコマンド別に、oracle edit・oracle investigation・oracle review・realization・feedback・indexing・session join・TUI の agent call 定義を確認するとき。
- prompt の共通組み立て、policy の適用、root path placeholder の解決、構造化文書の Markdown 化、または cmoc 設定モデルを調査するとき。

## Do not read this when
- agent call を実際に実行する処理やサブコマンドの業務ロジックを確認したい場合は、対応する実行本体を直接読むとき。
- 個別の oracle file・realization file の意味仕様、レビュー結果、feedback state の保存や集約処理を確認したい場合は、対応する正本仕様または処理本体を直接読むとき。
- 特定の prompt policy、Structured Output schema、サブコマンド別 builder の具体的な契約だけを確認したい場合は、該当する下位対象へ直接進むとき。

## hash
- ddd0e22d3b2ab7507f5aff38e31ec39f570feb4d5a04baafeb145a0a1e6927a0
