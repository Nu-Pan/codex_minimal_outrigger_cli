# `builder`

## Summary
- cmoc の各機能が AI エージェントへ処理を依頼する際の呼び出しパラメータ構築領域への入口。complete prompt に渡す role、summary、goal、補助文脈、標準文書参照、ファイルアクセス権限、モデル区分、推論量、Structured Output 契約の接続を、用途別の下位領域に分けて扱う。
- 対象となる処理は、フォーク適用時の変更要約・所見列挙・所見対応、目次エントリー生成、oracle review の所見処理、session join の conflict marker 解消、TUI 実行パラメータ解決である。実際の業務ロジックやファイル更新そのものではなく、下流 AI に渡す作業指示と出力契約を構成するための builder 群を収める。

## Read this when
- AI エージェント呼び出しで使う prompt 本文、補助文脈、参照標準、ファイルアクセスモード、モデル選択、推論量、Structured Output schema の対応を確認または変更したいとき。
- フォーク適用、目次生成、oracle review、session join、TUI パラメータ解決のうち、どの処理向けの AI 呼び出し設定へ進むべきかを判断したいとき。
- 差分、対象ファイル、所見リスト、レビュー理由、conflict 対象ファイル、ユーザープロンプトなどの入力が、下流 AI への補助プロンプトとしてどう埋め込まれるかを追いたいとき。
- AI 呼び出し結果に Structured Output schema が必要な処理で、呼び出しパラメータと返却形の接続を確認したいとき。

## Do not read this when
- CLI サブコマンドの引数解析、実行順序、状態管理、git 操作、ファイル走査、保存、表示など、AI 呼び出し前後の制御フローを調べたいとき。
- complete prompt の共通構築規則、構造化 Markdown レンダリング、パス解決、ファイルアクセスモード定義、AgentCallParameter 型そのものを調べたいとき。
- 差分解析、所見の統合・重複排除、conflict marker の実際の解消、TUI 入力の前処理、修正結果の検証など、AI に依頼される作業の中身や呼び出し後の処理を調べたいとき。
- 個別の Structured Output 項目の意味だけを確認したい場合は、該当する schema 本文へ直接進めばよい。

## hash
- db3debc81c0ddff3d09773cf623d66c945face4a1e7eafc5954e8b9fea4f9953

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
