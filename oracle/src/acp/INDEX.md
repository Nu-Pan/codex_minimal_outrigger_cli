# `builder`

## Summary
- AI エージェント呼び出しパラメータ構築の正本仕様断片へ進むための領域。適用後レビュー支援、目次エントリー生成、oracle review、セッション合流時の conflict 解消、TUI 実行前パラメータ選定について、prompt に渡す文脈、role・summary・goal、モデル設定、reasoning、ファイルアクセス設定、Structured Output schema との接続を確認する入口になる。
- 各サブコマンドの実処理本体ではなく、担当エージェントへどの前提・制約・入力・出力契約で依頼するかを定義する。

## Read this when
- サブコマンドが AI エージェントを呼び出す際の AgentCallParameter 相当の組み立て方を、用途別に確認したいとき。
- 変更差分要約、ファイル単位レビュー所見列挙、所見修正依頼、INDEX.md エントリー生成、oracle file レビュー、merge conflict marker 解消、TUI 実行前判定のいずれかの prompt 仕様を確認したいとき。
- エージェント prompt に含める対象ファイル、差分、所見、既知理由、標準文書、元プロンプト、対象パスなどの補助文脈の範囲を切り分けたいとき。
- 各 AI 呼び出しで使うモデル種別、reasoning effort、読み取り・書き込み権限、git 操作禁止などの制約、Structured Output schema を確認したいとき。
- AI 呼び出しの応答が、空配列、判定結果、編集操作、要約、所見、実行パラメータなどとしてどの契約で返るかを確認したいとき。

## Do not read this when
- CLI 引数解析、ブランチ作成、fork 適用、merge 実行、conflict 検出、git diff 取得、レポート保存、永続状態更新、画面描画など、各サブコマンドの制御フロー本体を調べたいとき。
- oracle file と realization file の基本定義、path keyword、標準文書本文、Markdown 描画、AgentCallParameter や file access mode の共通部品そのものを確認したいとき。
- 個別の対象ファイル本文を読んで、具体的なレビュー所見、修正内容、conflict 解消判断、または INDEX.md エントリー内容を作りたいとき。
- AI Agent CLI/TUI プロセスの起動処理、端末 UI、エディタ入力、コメント除去、ログや保存先など、エージェント呼び出しパラメータ以外の実装を探しているとき。

## hash
- ab3492b637be835840a696992625f35d6556939fb07da7b9aa6668d0cc9d0f3d

# `prompt_parts`

## Summary
- agent call に渡す各種プロンプト部品を構築する oracle src 群への入口である。
- ファイルアクセス規則、ルーティング規則、oracle / realization の基本概念、oracle / realization / review / INDEX エントリーの標準、完全なプロンプトへの組み立て方を扱う。
- 個別機能仕様そのものではなく、AI に渡す作業規範や標準断片の文面と、それらを完全なプロンプトへ含める条件を確認するための階層である。

## Read this when
- agent に渡す標準プロンプト部品の本文、責務、組み立て順序、依存関係を確認したいとき。
- ファイルアクセス規則、INDEX.md を使ったルーティング規則、oracle file / realization file の基本概念をプロンプトとしてどう提示しているか確認したいとき。
- oracle file、realization file、oracle review、oracle と realization の比較レビュー、INDEX.md エントリー生成の各標準を確認または変更したいとき。
- 新しい標準プロンプト断片を追加する前に、既存の標準断片の範囲、重複、完全プロンプトへの注入条件を把握したいとき。

## Do not read this when
- 特定の CLI サブコマンド、出力 schema、状態ファイル、パスモデルなど、cmoc の個別機能仕様を探しているとき。
- 実際の realization implementation や realization test の現在のコード挙動を調査したいだけのとき。
- StructDoc など、プロンプト部品を表現する下位データ構造そのものの実装を確認したいとき。
- 生成されたプロンプトをどの agent 実行経路へ渡すか、または実際のファイル操作・権限チェック・サンドボックス制御の実装を確認したいとき。

## hash
- f505b8893bffe7a604ba8388cedb63a259644b7e827b79d0884cfc6b0e98c8c9
