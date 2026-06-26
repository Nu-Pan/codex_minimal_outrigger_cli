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
- AI agent に渡すプロンプトを構成する標準文書・規則文書・概念説明を、構造化ドキュメントとして組み立てる prompt parts 群を収める領域である。
- ファイルアクセス規則、ルーティング規則、oracle file / realization file の基本概念、oracle・realization・review・INDEX.md エントリーの各標準、完全なプロンプト構成を扱う。
- agent 呼び出し時に組み込む規範本文や標準プロンプトの生成処理を確認するための入口であり、個別機能の CLI 挙動や永続状態そのものではなく、作業者へ提示する文章部品の責務境界を示す。

## Read this when
- agent に渡す標準プロンプトの本文、構成順、組み込み条件、または Codex CLI 向けの表現・パストークン置換を確認・変更したいとき。
- ファイルアクセス制約、INDEX.md を使った読み進め方、oracle file と realization file の責務境界を、プロンプトとしてどう提示しているか確認したいとき。
- oracle file、realization file、oracle review、oracle 適用レビュー、INDEX.md エントリー生成に関する共通規範の文面や判断基準を確認・変更したいとき。
- AI agent の作業前プロンプトに含める規範文書を追加・整理する際、既存の prompt parts がどの標準文書を担っているか把握したいとき。

## Do not read this when
- 特定サブコマンドの引数、入出力 schema、永続状態、path model、実行フローなど、プロンプト本文ではなくプロダクト機能そのものの仕様や実装を探しているとき。
- 構造化ドキュメントの共通型、Standard・Requirement の定義、文字列整形 helper、ルート解決関数など、prompt parts が利用する基礎部品の詳細を確認したいとき。
- 個別の oracle file や realization file の内容をレビュー・実装するために、対象本文そのものを読むべき段階に入っているとき。
- 実際のファイルアクセスを強制するサンドボックス、権限機構、Git 操作、agent 呼び出し処理そのものを調べたいとき。

## hash
- 130ccf2f94c0dd1662a60bd117aa56edb877cd830552ff866391ee1d46236e6f
