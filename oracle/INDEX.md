# `doc`

## Summary
- cmoc の自然言語 Markdown で書かれた正本仕様断片を集めた領域。利用者向け CLI workflow、サブコマンドの外部挙動、session/apply 状態、run 隔離、Codex CLI 呼び出し、ログ、エラー、補完、インデクシング、プロンプト規範、branch/worktree モデル、開発・テスト規則、不採用設計案を確認する入口になる。
- 個別サブコマンドの引数、事前条件、状態遷移、merge・cleanup・report・終了コードなど、実装差を避けたい利用者可視の仕様へ進むための自然言語仕様群である。
- 実装者が realization code を追加・修正するときに守る Python コーディング規則、CLI 実装配置、開発環境、pytest の対象範囲など、コード作業前の共通判断基準も扱う。
- 採用済み仕様だけでなく、AI-generated kaizen の自動注入、作業計画レビュー、apply 前の独立計画立案などを採用しない理由を確認するための設計判断の入口にもなる。

## Read this when
- cmoc の CLI 挙動、標準 workflow、サブコマンドの呼び出し順、引数、事前条件、正常系・失敗系、stdout・report・終了コードを実装・修正・テストするとき。
- session の fork/join/abandon、apply の fork/join/abandon、oracle review、初期化、明示インデクシング、AI Agent CLI/TUI 起動など、利用者が呼ぶサブコマンド単位の正本仕様を探すとき。
- session state、apply state、run branch、linked worktree、cmoc-managed branch、fork/join commit、session home branch など、git branch・commit・worktree による制御モデルを確認するとき。
- cmoc から Codex CLI を呼び出す方法、profile、環境変数、stdin、stdout/stderr、Structured Output、retry/resume、quota 待機、並列実行、編集禁止領域の扱いを確認するとき。
- サブコマンド実行中のコンソール出力、JSON Lines ログ、タイムスタンプ、パス表示、共通エラー処理、自動補完プローブ時の副作用抑制、INDEX.md の生成・更新タイミングを扱うとき。
- agent に渡すプロンプトや人間向けレポートの文面で、cmoc 固有概念を具体値へ解決して渡すべきか、日本語文面と英語識別子をどう使い分けるかを判断するとき。
- realization code や realization test を追加・変更する前に、Python の書き方、型ヒント、import、docstring、コメント、ログ、非公開識別子、CLI 構成、共通処理配置、開発環境、pytest 対象範囲を確認したいとき。
- cmoc の設計で、AI memory、kaizen 自動注入、人間による作業計画レビュー、apply 前の独立計画立案などを追加すべきか検討し、不採用理由や責務分担の背景を確認したいとき。

## Do not read this when
- oracle file と realization file の基本定義、正本性、編集主体、責務分担だけを確認したいときは、基礎概念を扱う文書を読む。
- パスキーワード、root 種別、パス解決の実装詳細だけを確認したいときは、パスモデルの仕様または実装へ直接進む。
- プログラミング言語や設定ファイルで記述された oracle 側の builder、schema、型定義、テスト仕様そのものを確認したいときは、自然言語文書ではなく該当する oracle の実装・テスト領域へ進む。
- 特定の realization implementation、realization test、helper、既存関数、現在のコード構造、テスト期待値を調べたいだけなら、対象の実装またはテストへ直接進む。
- 個別の Codex CLI 呼び出しごとの具体的な AgentCallParameter、builder の引数構築、Structured Output schema 定義そのものを確認したいだけなら、対応する builder や schema 実装を読む。
- 通常の git 操作一般、任意 branch の汎用 merge、join 済み結果の rollback、旧サブコマンド互換など、現行 cmoc の自然言語仕様が対象外としている機能を探しているとき。
- pytest の一般的な使い方、fixture 設計、PEP 8 などの一般論だけを調べたいときは、cmoc 固有の正本仕様として確認する必要がある場合を除き、外部資料や既存テストを参照する。

## hash
- 09c369265022cf151758c71f88021cb19dd54bdc5a4e17d1f66d62dbc1ed2feb

# `src`

## Summary
- cmoc の正本仕様断片のうち、プログラミング言語・設定形式で表された仕様実装をまとめる領域。AI agent 呼び出しパラメータ構築、共通注入プロンプト、Structured Output 契約、root token 付きパス解決、規範文書モデル、構造化文書の Markdown 描画、リポジトリ単位の永続設定を扱う。
- 下位領域へ進むための入口として、用途別 agent 呼び出し仕様を確認する領域、複数領域から参照される基礎モデル・helper を確認する領域、設定 dataclass と Codex CLI 向け値対応を確認する領域へ分岐する。
- 自然言語で書かれた仕様判断そのものではなく、cmoc が正本仕様として参照する実装形式の断片を読むための階層である。

## Read this when
- cmoc の oracle source として、AI agent に渡す role、summary、goal、補助プロンプト、ファイルアクセス制約、モデル種別、reasoning effort、Structured Output schema の正本値を確認したいとき。
- AgentCallParameter、モデル分類、reasoning effort、ファイルアクセスモード、root token 付きパス表記、実パス解決、規範モデル、構造化文書描画など、複数の正本仕様実装から参照される基礎概念を確認したいとき。
- リポジトリごとに永続化される cmoc 設定、既定値、Codex CLI が受理するモデル名・reasoning effort 名への対応、apply fork や review oracle のループ上限を確認したいとき。
- 新しい正本仕様実装を追加・変更する前に、既存の用途別パラメータ構築、共通プロンプト部品、基礎 helper、設定面の責務分担を把握したいとき。

## Do not read this when
- 自然言語の oracle doc 本文、oracle test、または realization 側の実装・テストを直接確認したいとき。
- CLI 引数解析、サブコマンドの実行フロー、git 操作、ファイル入出力、端末 UI、永続状態の実際の読み書きなど、正本仕様断片ではなく realization の処理を調べたいとき。
- 個別の仕様判断、レビュー所見、変更方針、conflict 解消内容、INDEX.md エントリー文面そのものを考えるために、より直接の oracle doc や対象ファイル本文を読むべきとき。
- 既存のルーティング文書、生成キャッシュ、実行時生成物、または機械的なファイル一覧だけを確認したいとき。

## hash
- 31115c606b0f2eb78bae3825d5eb02b2e36dfcba6fddba0e7610c4bfdc402712
