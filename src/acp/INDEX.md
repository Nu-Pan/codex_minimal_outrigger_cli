# `builder`

## Summary
- AI エージェント呼び出しパラメータを組み立てる builder 群を集約する領域。apply fork、INDEX.md エントリー生成、oracle review、session join の conflict 解消、TUI 実行前パラメータ解決について、prompt 内容、補助文脈、ファイルアクセス制約、model class、reasoning effort、Structured Output schema との接続を扱う。
- サブコマンドや TUI の上位制御そのものではなく、各処理が AI に何を依頼し、どの権限・出力契約で呼び出すかを確認するための入口になる。

## Read this when
- cmoc の各機能が AI エージェントへ渡す prompt、補助文脈、ファイルアクセス権限、model class、reasoning effort、Structured Output schema を確認または変更したいとき。
- apply fork の差分要約・レビュー所見・所見修正依頼、INDEX.md エントリー生成、oracle review の所見フロー、session join の conflict marker 解消、TUI 実行前のパラメータ解決のいずれかについて、エージェント呼び出し内容を追いたいとき。
- 生成側の prompt 構築と、差分要約・レビュー所見・INDEX.md エントリー・TUI パラメータ判定などの構造化出力契約の対応を確認したいとき。
- AI 呼び出し時にどの標準文書や対象ファイル情報が prompt に埋め込まれ、どの読み取り・編集制約がエージェントへ渡されるかを調べたいとき。

## Do not read this when
- CLI 引数解析、サブコマンドの実行順序、保存、表示、集計、git 操作、merge 実行、conflict marker 検出など、AI 呼び出しパラメータ構築の外側にある上位制御や低レベル処理を調べたいとき。
- oracle standard、realization standard、review standard、apply review standard、path model など、prompt に含められる標準文書や共通概念の本文そのものを確認したいとき。
- 汎用的な prompt 部品、Markdown rendering、構造化文書表現、AgentCallParameter 型、パス解決など、個別 builder に閉じない共通基盤を調べたいとき。
- 生成済み INDEX.md の内容や特定ディレクトリのルーティング判断そのもの、具体的な oracle file の仕様内容、TUI 表示や対話 UI の挙動を確認したいとき。

## hash
- df5167760f825c45794b2df8bc4a55c628309d6c6056b6db902bee67d77e4c84

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
