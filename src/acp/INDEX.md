# `builder`

## Summary
- cmoc の各サブコマンドや TUI 実行前処理で、AI エージェントへ渡す AgentCallParameter を組み立てる領域。role、summary、goal、補助コンテキスト、file access mode、model class、reasoning effort、Structured Output schema の対応を、用途別の prompt 構築実装として扱う。
- 下位領域は、適用レビュー、oracle レビュー、session join の conflict 解消、indexing のルーティング文書エントリー生成、TUI の実行パラメータ解決に分かれる。各 AI 呼び出しが、どの標準文書や対象本文を読み取り専用または書き込み可能コンテキストとして渡すかを確認する入口になる。

## Read this when
- cmoc 内で AI エージェント呼び出しの prompt や AgentCallParameter を構築する実装を探しているとき。
- サブコマンドごとに、AI へ渡す役割、目的、補助プロンプト、参照標準、file access mode、model class、reasoning effort、出力 schema の組み合わせを確認または変更したいとき。
- apply fork の所見列挙、所見対応、変更要約、review oracle の所見列挙・理由検証・採否判定・所見整理、session join の conflict 解消、indexing のエントリー生成、TUI の実行パラメータ解決のいずれかの AI 呼び出し仕様を追いたいとき。
- Structured Output schema を持つ AI 呼び出しについて、後続処理が受け取る機械処理用結果の意味上の責務を確認したいとき。
- oracle file、realization file、git diff、conflict 対象ファイル、ユーザー入力 prompt、既知所見や理由などを、AI 呼び出しの補助文脈としてどのように渡すかを調べたいとき。

## Do not read this when
- 各サブコマンド全体の制御フロー、CLI 引数解析、ブランチ操作、git コマンド実行、対象列挙、保存、表示、並列実行など、AI 呼び出しパラメータ構築の外側を調べたいとき。
- oracle standard、realization standard、review oracle standard、apply review standard、index entry standard そのものの本文や定義を確認したいとき。
- AgentCallParameter、ModelClass、ReasoningEffort、FileAccessMode、StructDoc、complete prompt rendering、path 解決などの共通基盤の型定義や汎用実装を調べたいとき。
- 実際の oracle file や realization file の内容、個別差分、conflict marker の解析、所見の保存形式、または変更カテゴリ分類の具体処理を確認したいとき。
- AI 呼び出しではなく、人間向けのコマンド出力、TUI 表示、エディタ入力処理、テスト実行手順、補助スクリプト、生成物キャッシュを調べたいとき。

## hash
- af100ef39b8d4727bf0cba76688ff7d498dda8a447d312825bf724fb088b7140

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
