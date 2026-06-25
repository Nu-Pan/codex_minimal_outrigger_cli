# `builder`

## Summary
- 各種サブコマンドや対話実行の下流で、別の AI エージェントに渡す呼び出しパラメータを構築する実装領域。役割、目的、補助文脈、参照標準、ファイルアクセスモード、モデル種別、reasoning 設定、Structured Output schema の対応づけを扱う。
- 対象となる処理は、変更差分の要約、実装所見の列挙と修正依頼、oracle file レビューの各段階、merge conflict marker 解消依頼、目次エントリー生成、TUI 実行前のパラメータ選定に分かれる。
- 実際の CLI 制御、Git 操作、ファイル走査、レビュー結果の保存、対話 UI の実行ではなく、それらから呼び出される AI タスクの prompt と実行条件を確認するための入口になる。

## Read this when
- AI エージェントに委譲するサブタスクで、どの role、summary、goal、補助プロンプト、標準文書、ファイルアクセス権限を渡すか確認または変更したいとき。
- 変更要約、実装所見、所見修正、oracle file レビュー、conflict 解消、目次エントリー生成、TUI 実行パラメータ選定などの Structured Output schema と呼び出し設定の対応を追いたいとき。
- モデルクラス、reasoning effort、読み取り専用・realization 書き込み・oracle 限定読み取りなどの実行条件が、各 AI 呼び出しでどう選ばれているか調べたいとき。
- 対象ファイル、差分テキスト、既知所見、理由リスト、conflict 対象一覧、ユーザー入力プロンプトなどの入力文脈が、AI 向け完全プロンプトにどう埋め込まれるか確認したいとき。

## Do not read this when
- 各サブコマンドの CLI 引数解析、サブコマンド登録、実行順序、Git 操作、worktree 操作、結果保存など、AI 呼び出しを起動する側の制御フローだけを調べたいとき。
- oracle file、realization file、各種標準、ファイルアクセスモード、パスモデル、構造化 markdown、完全プロンプト生成などの共通概念や共通部品そのものを詳しく確認したいとき。
- 実際に修正・レビュー・conflict 解消される個別の oracle file や realization file の本文を確認すれば足りるとき。
- AI 呼び出し結果を受け取った後の集約、表示、永続化、適用可否判定、または UI 表示や対話処理を調べたいとき。

## hash
- 167fe3cdad1b2b6f00fe1c9de975fc5bace8ef7d9365b74fb627146c4f0ed212

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
