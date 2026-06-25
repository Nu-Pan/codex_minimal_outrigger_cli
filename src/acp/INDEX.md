# `builder`

## Summary
- AI エージェント呼び出し用のパラメータ構築を扱う領域。`apply`、`indexing`、`review`、`session`、`tui` などの各処理について、prompt、role、goal、補助文脈、ファイルアクセス条件、モデル設定、推論量、Structured Output schema の対応を定義する。
- cmoc の各サブコマンドや TUI 実行前処理で、AI に何を読ませ、何を出力させ、どの権限で作業させるかを確認する入口になる。

## Read this when
- AI エージェントへ渡す呼び出しパラメータの組み立てを、処理ごとに確認または変更したいとき。
- prompt に含める role、summary、goal、補助文脈、対象本文、標準指示、既知所見、差分などの渡し方を追いたいとき。
- Structured Output schema が、レビュー所見、理由、採否、差分要約、INDEX.md エントリー、TUI パラメータ判定などでどの責務を持つか確認したいとき。
- AI 呼び出しにおける model class、reasoning effort、file access mode、realization 書き込み可否、git 操作禁止条件などの組み合わせを調べたいとき。
- `cmoc apply fork`、`cmoc indexing`、`cmoc review oracle`、`cmoc session join`、TUI 実行前パラメータ解決のいずれかで、AI 呼び出し前の入力契約や出力契約を実装・テストしたいとき。

## Do not read this when
- 各サブコマンド全体の CLI 引数解析、実行順序、状態更新、git コマンド実行、保存処理など、AI 呼び出しパラメータ構築より外側の制御フローを調べたいとき。
- oracle file、realization file、review standard、apply review standard、INDEX.md 運用規則などの標準本文そのものを確認したいとき。
- Markdown レンダリング、構造化文書表現、パス解決、AgentCallParameter 型、モデル種別やファイルアクセスモードの共通定義など、呼び出し構築を支える共通基盤を調べたいとき。
- 個別の変更対象ファイル、実際の差分検出、分類アルゴリズム、conflict marker 検出、TUI 表示や入力取得など、AI に渡すパラメータ以外の具体処理を確認したいとき。

## hash
- d2a1ff13e7c9eb45eaef45de557128432770d36ed0e1a612ae6904d022892c93

# `prompt_parts`

## Summary
- AI エージェントへ渡すプロンプト部品を構築する実装群。oracle / realization の基本概念、oracle・realization・レビュー・ルーティング・ファイルアクセス・INDEX.md エントリーの各標準文書を、構造化文書として組み立てる責務を持つ。
- 個別標準の本文生成だけでなく、役割・概要・ゴール・アクセス規則・ルーティング規則・補助プロンプトを組み合わせ、標準間の依存関係や Codex CLI 向けの語句・ルート置換を含む最終プロンプト構成への入口になる。
- レビューで所見として扱うべき差分、仕様断片の隙間として許容すべき実装差、実装・テストの肥大化抑制、INDEX.md を使った読み進め方など、AI に提示する作業規範の生成箇所を探すための起点となる。

## Read this when
- AI エージェントへ提示する標準プロンプトや規範文書の生成内容、組み込み順序、依存関係を確認・変更したいとき。
- oracle file と realization file の責務境界、oracle 標準、realization 標準、レビュー標準、ルーティング規則、ファイルアクセス規則、INDEX.md エントリー標準のいずれかの文面生成を探したいとき。
- Codex CLI 向けに cmoc 固有語やルートトークンがどのように置換され、作業ルート解決失敗がどう扱われるかを確認したいとき。
- レビュー用プロンプトで、oracle file 単体の問題分類や oracle file と realization file の不整合判定をどの基準で説明しているか確認したいとき。
- ファイル読み書きモードごとの禁止範囲、INDEX.md による探索手順、または INDEX.md エントリー品質基準を AI へどう説明しているか確認したいとき。

## Do not read this when
- 個別サブコマンド、path model、永続状態、出力 schema など、プロダクト機能そのものの仕様や実装詳細を探しているとき。
- 構造化文書、標準、要求、本文整形 helper などの共通データ型や変換基盤そのものを調べたいとき。
- 読み書きモードの列挙値、パス語彙、ルート解決規則そのものを確認したいだけのとき。
- 生成された規範文書を使う側ではなく、実際の OS レベル・実行環境レベルのアクセス制御や enforcement を探しているとき。
- 既に読む対象が個別の標準生成モジュールに絞れており、プロンプト部品群全体の入口や関連標準の所在を確認する必要がないとき。

## hash
- 71d4b1e646d4a6240474c06b0580734d8c752f8fc6c40d644f9a0b9912d88cbe
