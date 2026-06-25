# `builder`

## Summary
- AI エージェント呼び出し用の builder 群を集めた領域で、apply、indexing、review、session、tui などの上位機能ごとに prompt、Structured Output schema、model class、reasoning effort、ファイルアクセス権限を組み合わせた呼び出しパラメータ構築へ進む入口になる。
- 実行フロー本体ではなく、各処理で AI に何を補助文脈として渡し、どの構造化結果を受け取り、どの実行条件で呼び出すかを確認するためのまとまり。

## Read this when
- cmoc の各機能で、AI Agent CLI/TUI や OpenAI API 相当の呼び出し条件をどの builder が組み立てるかを探したいとき。
- 変更要約、レビュー所見、INDEX.md エントリー生成、merge conflict marker 解消、TUI 実行パラメータ選定などで使う prompt と Structured Output schema の対応を確認したいとき。
- 対象ファイル、差分、所見、ユーザープロンプト、conflict 対象一覧などの補助文脈が AI 向け prompt にどう埋め込まれるかを追いたいとき。
- AI 呼び出しごとのモデル種別、reasoning effort、論理ファイルアクセスモード、読み取り専用・編集許可条件を確認または変更したいとき。

## Do not read this when
- CLI 引数解析、サブコマンド登録、Git 操作、branch/worktree 操作、ファイル走査、結果保存、TUI 表示など、AI 呼び出し builder を利用する側の実行制御を調べたいとき。
- oracle file、realization file、review standard、INDEX.md entry standard、path keyword など、prompt に参照される共通仕様や概念そのものを読みたいとき。
- 汎用的な prompt rendering、AgentCallParameter、path 解決、Markdown 構造化、schema 基盤など、個別 builder より下位の共通部品を調べたいとき。
- 個別の対象ファイルやテスト本文を確認したいだけで、AI 呼び出し契約や構造化出力の設定を変更しないとき。

## hash
- 9896b5c2963598d5c9197b129c4841b8ecee7b6a363b73fe3a1a35f3a75abde0

# `prompt_parts`

## Summary
- AI agent に渡す構造化プロンプトを組み立てるための部品群を扱う。基本の role・summary・goal、ファイルアクセス規則、ルーティング規則、oracle / realization の概念説明、各種標準文書、レビュー規範、INDEX.md エントリー規範を StructDoc として生成する実装への入口になる。
- 個別の標準文書を生成する小さな部品と、それらを有効化フラグと依存関係に従って完全なプロンプト列へまとめる処理を含む。

## Read this when
- agent call に渡すプロンプト全体がどの部品から構成され、どの順序で組み立てられるかを確認したいとき。
- ファイルアクセス規則、INDEX.md を使った読み進め方、oracle / realization の基本概念、oracle 標準、realization 標準、レビュー標準、INDEX.md エントリー標準のいずれかのプロンプト本文を確認・変更したいとき。
- 標準プロンプトを追加・削除・依存関係変更する際に、どの部品を有効化すべきか、また完全なプロンプトへどう注入されるかを追いたいとき。
- AI agent に提示される規範文書の文言や構造化ドキュメント化の入口を探しているとき。

## Do not read this when
- agent call の実行、外部プロセス起動、LLM 応答処理、または生成されたプロンプトの利用側を調べたいとき。
- 構造化文書、標準項目、要求項目、本文整形などの共通基盤型や helper の実装そのものを確認したいとき。
- 個別サブコマンド、path model、状態ファイル、CLI 引数、出力 schema など、プロンプト本文ではなく cmoc の機能仕様や実行ロジックを探しているとき。
- oracle file や realization file の個別本文、またはそれらに対する実際の実装・テスト変更箇所を直接確認したいとき。

## hash
- 25a727f241cbaed861a78599ee7a6bc2bb7b7a218c95be32abdf278f50b3c3cc
