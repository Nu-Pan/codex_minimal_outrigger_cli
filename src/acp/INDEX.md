# `builder`

## Summary
- サブコマンドや TUI 実行前処理から AI エージェントを呼び出すためのパラメータ構築をまとめる領域。工程ごとの role・goal・補助コンテキスト・file access mode・model class・reasoning effort・Structured Output schema の組み合わせを定義する。
- レビュー所見列挙、所見修正依頼、差分要約、oracle レビュー、merge conflict 解消、ルーティング文書エントリー生成、TUI パラメータ解決など、用途別の prompt builder と出力契約への入口になる。

## Read this when
- 特定の cmoc サブコマンドが AI エージェントへ渡す complete prompt、補助文脈、標準文書参照、アクセス権限、モデル設定、出力 schema を確認または変更したいとき。
- AI 呼び出しの入力として、対象パス、git diff、所見リスト、既知理由、conflict 対象一覧、元プロンプトなどがどのように埋め込まれるかを追いたいとき。
- Structured Output schema が、レビュー所見、所見理由、採否判定、所見整理操作、変更要約、INDEX.md エントリー、TUI パラメータ選択結果としてどの機械処理契約を持つか確認したいとき。
- file access mode、model class、reasoning effort、schema ファイル有無の組み合わせを、用途別のエージェント呼び出しパラメータとして調べたいとき。
- 共通 prompt 部品を使う側の実装として、サブコマンド固有の role・summary・goal・aux prompt がどう組み立てられるか確認したいとき。

## Do not read this when
- サブコマンド全体の制御フロー、CLI 引数解析、ファイル探索、git コマンド実行、保存、表示、ブランチ操作など、AI 呼び出しパラメータ構築の外側を調べたいとき。
- complete prompt の共通構造、Markdown レンダリング、構造化ドキュメント部品、AgentCallParameter 型、file access rule、パス解決の汎用実装そのものを調べたいとき。
- oracle standard、realization standard、review standard、apply review standard、index entry standard の本文や判断基準そのものを確認したいとき。
- 実際の oracle file や realization file の仕様・実装内容、個別差分の検出処理、変更カテゴリ分類、conflict marker 検出などの具体的な処理ロジックを調べたいとき。
- 生成済み INDEX.md の内容や、ルーティング文書として各エントリーが妥当かどうかを確認したいだけのとき。

## hash
- d2a1ff13e7c9eb45eaef45de557128432770d36ed0e1a612ae6904d022892c93

# `prompt_parts`

## Summary
- AI agent に渡すプロンプトを構成する標準部品群を集めた領域。oracle / realization の基本概念、各種標準、レビュー基準、ファイルアクセス規則、ルーティング規則、INDEX.md エントリー規範などを、構造化文書として生成する実装を扱う。
- 完全な agent prompt の組み立てに使われる個別プロンプト部品の責務と、標準プロンプト同士の関係を確認する入口になる。

## Read this when
- agent に渡すプロンプトへ、どの標準文書や規則文書が含まれるかを確認・変更したいとき。
- oracle file、realization file、レビュー、INDEX.md、ファイルアクセス、ルーティングに関する共通規範のプロンプト本文を確認・調整したいとき。
- 標準プロンプトの有効化フラグ、依存関係、注入順序、または基本プロンプトとの組み合わせを追いたいとき。
- AI agent に提示される作業規則の文面が、構造化文書としてどのように生成されるかを調べたいとき。

## Do not read this when
- 個別サブコマンドの CLI 挙動、状態ファイル、path model、入出力 schema など、プロンプト部品ではない機能仕様や実装を探しているとき。
- oracle file や realization file の本文そのものを編集・確認したいだけで、それを説明する標準プロンプトの生成処理を調べる必要がないとき。
- 構造化文書の基盤型、文字列整形 helper、agent 呼び出し処理など、プロンプト部品を利用する下位または上位の仕組みを調べたいとき。
- 特定の標準文書の内容だけが必要で、読むべき個別部品がすでに分かっているとき。

## hash
- 7f9fda2fe4128e8d183a1375518232cccaa31de36b6d084d39a849528b23664f
