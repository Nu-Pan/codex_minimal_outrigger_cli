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
- AI agent 呼び出しに渡す構造化プロンプトを、基本プロンプト、ファイルアクセス規則、ルーティング規則、任意追加文書、各種標準文書から組み立てる実装群を扱う。
- oracle file と realization file の基本概念、oracle file の記述標準、realization file の保守標準、oracle レビュー基準、oracle と realization の照合レビュー基準、INDEX.md エントリー基準、INDEX.md を使った読み進め方を、それぞれ StructDoc として生成する入口になっている。
- Codex CLI 向けに root token や用語を実パス・作業者向け表現へ置換し、要求された基準プロンプトに必要な前提基準を自動的に含める層でもある。

## Read this when
- AI agent に渡す完全なプロンプトが、どの規則・基準文書をどの順序で含めるか確認または変更したいとき。
- ファイルアクセス規則、INDEX.md ルーティング規則、oracle/realization の基本説明、oracle/realization の品質基準、レビュー所見基準、INDEX.md エントリー基準の本文生成を調整したいとき。
- 基準プロンプトの有効化フラグ、依存関係、注入順序、または Codex CLI 向けの用語・root token 置換を変更したいとき。
- agent に提示される規範文書の内容が、構造化文書としてどこで作られているかを探したいとき。

## Do not read this when
- 実際の CLI サブコマンド実行、永続状態操作、入出力 schema、作業ディレクトリ管理など、プロンプト生成ではない実行時挙動を調べたいとき。
- 構造化文書、標準項目、要求項目、パスモデル、ファイルアクセスモードの型定義や共通データ構造そのものを確認したいとき。
- 個別の oracle file が定めるプロダクト仕様や、特定機能の実装・テスト詳細を探しているとき。
- INDEX.md エントリー作成のために対象本文がすでに個別ファイルへ絞れており、プロンプト部品全体の構成を確認する必要がないとき。

## hash
- 40fcbd0059bc3f3d6b77da462b3ea48a0406fb0caac37ebd87aaa4e7154b201a
