# `builder`

## Summary
- AI エージェント呼び出しに渡す AgentCallParameter を、用途別の complete prompt、補助入力、file access mode、model/reasoning、Structured Output schema 参照として組み立てる builder 群をまとめる領域。
- 対象は、apply fork の変更要約・所見列挙・所見対応、indexing の目次エントリー生成、review oracle の所見列挙・検証・採否・整理、session join の conflict marker 解消、TUI の実行パラメータ解決など、AI に何を依頼し、どの制約と出力契約で呼び出すかを定義する処理である。
- 実際の CLI 制御、git 操作、ファイル更新、レビュー結果の保存、目次ファイルの描画や永続化ではなく、各機能が AI 呼び出しへ渡すプロンプトと呼び出し条件を確認するための入口になる。

## Read this when
- cmoc の各機能が AI エージェントを呼び出す際の prompt、補助文脈、アクセス権限、モデル区分、推論量、Structured Output schema の対応関係を調べたいとき。
- apply fork、indexing、review oracle、session join、TUI parameter resolve のいずれかで、AI に渡す作業目的・禁止事項・標準文脈・入力データがどう complete prompt に組み込まれるか確認したいとき。
- 特定フェーズの出力 schema と、その schema を参照する AgentCallParameter 構築処理を対応づけて確認したいとき。
- AI 呼び出しの file access mode が readonly、pure oracle read、realization write などのどれに設定されるか、またその権限が prompt 上の作業範囲とどう対応するかを追いたいとき。
- 新しい AI 呼び出し builder を追加または既存 builder を変更する前に、同種の呼び出し定義の責務分割や schema 参照の置き方を確認したいとき。

## Do not read this when
- CLI サブコマンドの引数解析、実行順序、状態管理、git branch 操作、merge 実行、ファイル列挙、保存、表示など、AI 呼び出し前後の制御フローだけを調べたいとき。
- AI が返した構造化結果を実際に適用する処理、レビュー結果や目次情報を永続化する処理、または markdown として描画する処理を調べたいとき。
- complete prompt の共通構築規則、StructDoc や render 処理、path model、AgentCallParameter、FileAccessMode などの基礎型そのものを調べたいとき。
- oracle file、realization file、review standard、apply review standard、index entry standard など、builder が参照する標準文脈の本文や一般規約を読みたいだけのとき。
- 個別の AI 呼び出しではなく、対象コマンドの利用者向け仕様、実際の実装修正箇所、またはテストだけを直接確認したいとき。

## hash
- 2fa7d3217c15a26c90e074c17bfdf5257f83b909cb8438de8523b0f8a4d778ee

# `prompt_parts`

## Summary
- AI agent に渡す prompt part 群を構築する realization implementation のまとまり。ファイルアクセス規則、ルーティング規則、oracle / realization / review / apply / index entry 各標準、oracle と realization の基本概念、完全プロンプトへの統合を扱う。
- 個別の規範本文を StructDoc や Standard 群として組み立てる部品と、それらを agent call 用の完全なプロンプトへ条件付きで合成する入口を含む。
- cmoc が AI に作業前提、読み書き制限、仕様断片と実装の責務境界、レビュー所見の判断基準、INDEX.md エントリー品質基準を提示するための prompt 構築層として読む対象になる。

## Read this when
- AI agent に渡すプロンプト本文の部品を確認・変更したいとき。
- ファイルアクセス規則、INDEX.md ルーティング規則、oracle file / realization file の基本説明、oracle standard、realization standard、review standard、apply review standard、index entry standard のいずれかを prompt としてどう構築しているか調べたいとき。
- 複数の標準 prompt part が完全プロンプトへどの条件・順序・依存関係で組み込まれるか確認したいとき。
- AI に渡す文面で、内部呼称や root token を作業対象向け表現へ置換する処理を確認・変更したいとき。
- 新しい標準プロンプト部品を追加する場所や、既存の標準プロンプト部品の責務境界を見極めたいとき。

## Do not read this when
- 個別 CLI コマンドの実行制御、サブプロセス起動、状態ファイル操作、入出力 schema など、生成されたプロンプトを使う側の実装を調べたいとき。
- StructDoc、StructCodeBlock、Standard、Requirement などの構造化文書データ型や変換 helper の低レベル実装だけを確認したいとき。
- path token、work root、run root などのパスモデル定義や解決規則そのものを調べたいとき。
- 特定の oracle file や realization file の仕様本文・実装本文をレビューしたいだけで、AI 向け標準文書の構築処理を確認する必要がないとき。
- OS 権限やサンドボックスなど、実際のファイルアクセス制御 enforcement を調べたいとき。

## hash
- 3dc7eddb00b95bd55c4a14f6240d0875654efbd91c6d58002807cb691bbf70cd
