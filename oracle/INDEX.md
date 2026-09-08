# `doc`

## Summary
- cmoc のアプリケーション仕様、開発ルール、session・run の branch model、設計上の検討資料を目的別に案内する正本文書群の入口。現行仕様と開発規則を横断して参照する際の起点となる。

## Read this when
- cmoc のアプリケーション挙動や開発ルールについて、複数領域にまたがる正本仕様の参照先を選ぶとき
- session・run の branch・commit・worktree 関係を確認するとき
- 現行仕様ではなく、不採用案や設計判断の背景を調べるとき

## Do not read this when
- 特定のサブ文書や実装ファイルが直接の参照先として明確なとき
- 具体的な状態遷移、CLI 操作、Python 規約、テスト要件・実行手順などを直接確認したいとき
- 現行仕様ではなく、設計上の代替案や不採用理由を調べる必要がないとき

## hash
- 7471aab60cda425c9f1441fe82cd4ab4cc1e169a9c46bf3d068622af066a133f

# `src`

## Summary
- `oracle` パッケージの実装をまとめる領域。agent call パラメータ、prompt の構築と policy、用途別 ACP builder、設定・パス解決、構造化文書の Markdown 化を扱う。
- agent call や prompt の共通処理から、oracle・realization・feedback・indexing・editor input handoff などの用途別実装へ進む入口になる。

## Read this when
- agent call の共通パラメータ、ファイルアクセスモード、prompt 構築、policy の組み込み規則を確認するとき。
- 用途別 builder、入力スキーマ、設定・パスモデル、構造化文書レンダリングの実装入口を探すとき。

## Do not read this when
- 特定用途の prompt、出力スキーマ、保存処理、または個別 builder の詳細だけを確認したいとき。
- Codex CLI の実行処理そのもの、oracle・realization の具体的な仕様本文、または INDEX.md の構造規則だけを調べるとき。

## hash
- 5fde235f1ae58444b63d0140fc5d45b0504287d048843aed3269e9a184abe113
