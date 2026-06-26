# `acp`

## Summary
- AI エージェント呼び出しに渡すパラメータと標準プロンプト部品を構築する実装領域。用途別の role、goal、補助入力、読み書き制約、モデル設定、reasoning effort、Structured Output schema への接続と、oracle・realization・review・ルーティング文書などの標準文書を agent 向け prompt に組み立てる処理を扱う。
- apply、oracle review、session join、TUI 実行前判定、INDEX.md エントリー生成など、各機能が agent に何を読ませ、何を返させ、どの権限で動かすかを確認する入口である。

## Read this when
- cmoc の機能が AI エージェントを呼び出す際の prompt 構成、補助入力、対象パスや差分の埋め込み、ファイルアクセスモード、モデル種別、reasoning effort、出力 schema の対応を確認・変更したいとき。
- oracle file、realization file、oracle standard、realization standard、review standard、apply review standard、INDEX.md エントリー標準などを、agent prompt としてどの順序・依存関係で注入しているか調べたいとき。
- apply 系で、差分要約、ファイル単位の所見列挙、所見対応作業の agent 呼び出し条件や出力契約を追いたいとき。
- oracle review 系で、新規所見列挙、所見の擁護・反証理由列挙、採否判定、所見リスト整理の prompt と Structured Output schema を確認したいとき。
- session join の merge conflict marker 解消、TUI 実行前の権限・標準参照要否判定、INDEX.md エントリー生成など、特定用途の事前解決 agent 呼び出しを調べたいとき。
- agent に提示されるファイルアクセス規則、INDEX.md を使う読み進め方、oracle file と realization file の基本概念、レビューや実装品質に関する標準文言を変更したいとき。

## Do not read this when
- CLI サブコマンド全体の実行順序、引数解析、永続状態、git 操作、フォーク作成・統合、merge conflict marker の検出、生成結果の保存など、agent 呼び出しパラメータ構築の外側を調べたいとき。
- AgentCallParameter、FileAccessMode、ModelClass、ReasoningEffort、構造化ドキュメント、標準項目、パス解決などの基本データ構造や共通 helper だけを確認したいとき。
- oracle file や realization file の個別本文、または正本仕様断片そのものを読みたいだけで、agent prompt への注入方法を変更しないとき。
- 実際の対象ファイル探索、git diff 生成、変更ファイル抽出、レビュー所見の永続化、所見適用後の作業制御など、prompt に渡す材料を作る側または結果を処理する側の詳細を調べたいとき。
- 生成済み INDEX.md の内容評価や、ルーティング文書の文面作成だけが目的で、標準文書生成処理や agent 呼び出しパラメータの実装を確認する必要がないとき。

## hash
- b449f59beb7b6e0bb094015d8ef2ed93b760fb3b5e08e1b6b462f7328354f46a

# `basic`

## Summary
- cmoc の実装で広く使われる基礎的な型・変換・文書生成部品をまとめる領域。エージェント呼び出しの論理パラメータ、ルートトークン付きパスの解決、規範データの構造化、階層文書の Markdown レンダリングを扱う。
- 個別の CLI コマンドや外部バックエンド呼び出しそのものではなく、上位処理と実現処理が共有する入力仕様、パス表記、構造化文書表現の入口になる。

## Read this when
- エージェント呼び出しに渡すモデル区分、reasoning effort、ファイルアクセス区分、プロンプト、Structured Output schema 参照の保持形式を確認または変更したいとき。
- cmoc 内で `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` などのルートトークン付きパスを扱う処理や、絶対パスとの相互変換、相対パス拒否の挙動を確認したいとき。
- 規範文書を表すデータ構造、必須・禁止・推奨・許容の要求ラベル、背景・要求・判断例への変換や入力検証を確認したいとき。
- 階層化された自然言語文書やコードブロックを Markdown として生成する基本部品、見出し深さ、空行圧縮、本文正規化の挙動を確認したいとき。

## Do not read this when
- 具体的なバックエンド名、実モデル名、CLI 引数、外部コマンド実行形式への変換や呼び出し制御を調べたいだけのとき。
- プロンプト本文のテンプレート、タスク種別ごとの文章生成、Structured Output schema ファイル自体の内容を確認したいとき。
- 個別コマンドの入出力、サブコマンド制御、永続状態、ユーザー向け CLI 挙動を調べたいとき。
- 既存 Markdown の解析、ファイル内容の読み書き、生成済み文書やテスト期待値の具体ケースを確認したいとき。

## hash
- 409b2d79788a2ba3d4db9aca9bbe3794aa6c54b1fee51125127aa7576ab441d9

# `cmoc_runtime.py`

## Summary
- 公開モジュール名を既存の実体モジュールへ差し替えるだけの互換レイヤー。実装本体は別モジュールに委譲し、この入口から import する利用者にも同じ実体を見せるために、実行時のモジュール登録を置き換える。
- 既存の呼び出し元や配布設定が古い import path を参照している期間だけ残す移行用コードであり、責務別の実行時モジュールまたは実体モジュールへ参照元が移った後は削除対象になる。

## Read this when
- 公開されている古い import path と実体モジュールの対応関係を確認したいとき。
- 互換 import path を残す理由、削除条件、または移行状況を調べるとき。
- この入口を import した場合に、どのモジュール実体が利用されるかを確認したいとき。

## Do not read this when
- 実行時処理そのもののロジック、設定解釈、状態操作、CLI 挙動を調べたいとき。この対象は実装本体ではなく委譲だけを行う。
- 新しい実行時機能を追加・修正したいとき。互換入口ではなく、実体側または責務別の実行時モジュールを読む方が直接的である。
- 互換 import path の削除可否と無関係な一般的なモジュール探索やパス定義を調べたいとき。

## hash
- a36ad0b5d09cbe7d2be546fdafcd27ff3ddaf803744331274a69fb25f15cd7ee

# `commons`

## Summary
- cmoc の実行時共通基盤をまとめる realization implementation 領域。CLI サブコマンド共通ライフサイクル、Codex CLI exec/TUI 呼び出し、profile/config、path、Git、logging、error、content hash、runtime result、session state など、複数の上位機能から共有される低レベル runtime helper と公開 import 境界を扱う。
- 個別の業務サブコマンドではなく、実行前提の検査、外部プロセス実行、永続設定・状態の入出力、ログ記録、利用者向けエラー化、root/path 解決など、cmoc 全体の横断的な実行支援へ進む入口になる。

## Read this when
- CLI サブコマンド全体に共通する開始・完了表示、終了コード化、例外処理、実行ログ、現在 logger の管理を確認または変更したいとき。
- Codex CLI の exec/TUI 呼び出しに関する profile 準備、schema 準備、subprocess 実行、call log、Structured Output 検証、capacity/quota retry、resume 継続、対話起動の失敗時処理を追いたいとき。
- cmoc 設定ファイルの読み書き、既定値補完、不正設定の利用者向けエラー化、Codex profile と permission profile の生成規則を確認したいとき。
- <repo-root>、<work-root>、<cmoc-root> や `.cmoc` 配下の sessions、reports、logs、worktrees、state、config など、実行時 path の解決・配置規則を調べたいとき。
- Git command の共通実行、branch/HEAD/worktree 状態の検査、run worktree 作成・削除、cmoc 内部ディレクトリの ignore 管理を確認または変更したいとき。
- サブコマンド実行イベントや Codex 呼び出し完了サマリーのログ・console 表示、quota 待機時間や elapsed の計測を扱う必要があるとき。
- cmoc 共通の runtime result 型、session state の JSON 入出力、content hash による保存、binary 判定など、複数機能から共有される小さな runtime データ構造や helper を探すとき。
- 共通 runtime API として外部へ露出する公開要素の追加・削除・移動を判断したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、引数定義、dispatch、利用者向け出力の詳細だけを調べたいときは、該当する上位コマンド実装へ直接進む。
- path キーワードそのものの正本定義や oracle/realization の分類など、仕様断片としての概念定義を確認したいときは、正本仕様側の対象を読む。
- INDEX.md の生成ロジック、ルーティング文書の仕様、エントリー生成プロンプトや探索ルールを調べたいときは、indexing を担う実装または正本仕様を読む。
- Codex CLI や Git の外部ツール仕様そのもの、Python 標準例外機構、JSON Lines 形式一般など、cmoc の共通 runtime 実装ではない外部知識を確認したいだけのとき。
- 個別機能が共通 helper をどのタイミングで呼ぶかという上位 workflow を知りたいだけのときは、先に呼び出し側の実装を読む。

## hash
- dd1e284dc5ffb514ae5a50fc919e97a79da7e5dfb9c83d397b3da0cd1515ec6a

# `config`

## Summary
- 開発対象リポジトリごとに変わる cmoc 設定を表す dataclass 群を扱う領域。
- AI エージェント呼び出しの並列数、Codex CLI 向けモデル名と reasoning effort、apply fork と review oracle のループ上限など、永続化される設定値の既定値を確認する入口になる。
- 人間が編集するリポジトリ別設定面に含まれる値の定義を追うための対象であり、設定ファイルの入出力処理そのものは別領域に分かれる。

## Read this when
- リポジトリ別に保持される cmoc 設定項目や既定値を確認・変更したいとき。
- 初期化時に生成・同期される設定ファイルへ含める値や、Enum 系の値を JSON 保存向けに扱う前提を確認したいとき。
- Codex CLI に渡すモデル名、reasoning effort 名、AI 呼び出し並列数、apply fork や review oracle の処理回数上限を調整したいとき。

## Do not read this when
- CLI 引数、サブコマンド構文、実行時の入出力フローを調べたいだけのとき。
- 設定ファイルの実際の読み書き、JSON 変換処理、または `.cmoc` 配下のパス解決処理を調べたいとき。
- oracle file、realization file、パスキーワード定義、INDEX.md 生成ルールそのものを確認したいとき。

## hash
- 324dfe3034cabedbb119cb79c0c59fcdd422ac0747dbbc5e095eba5140bb0d71

# `main.py`

## Summary
- Typer で cmoc の最上位 CLI アプリケーションと `session`、`apply`、`review` のサブアプリケーションを組み立て、各 CLI コマンドを対応する実装関数へ委譲する入口。
- 補完時を除く Click の引数解析例外を cmoc 共通のエラーレポート形式へ変換する TyperGroup を定義し、console script から `cmoc` として起動する処理を持つ。

## Read this when
- cmoc の利用者向け CLI コマンド名、サブコマンド構成、CLI option の定義、または各コマンドがどの実装関数へ委譲されるかを確認したいとき。
- 通常の引数解析エラーが cmoc のエラー表示に変換される入口処理や、shell completion 時だけ通常の Typer/Click 処理に任せる分岐を確認したいとき。
- console script から Typer アプリケーションがどの `prog_name` で起動されるかを確認したいとき。

## Do not read this when
- 各サブコマンドの具体的な業務処理、git 操作、worktree 操作、状態更新、Codex 起動内容を調べたいときは、ここではなく委譲先のサブコマンド実装を読む。
- cmoc 共通エラー型やエラー表示の詳細仕様を調べたいときは、ここではなく共通 runtime 側の定義を読む。
- INDEX.md 更新処理そのものの実装やルーティング文書生成の詳細を調べたいときは、CLI 入口ではなく indexing コマンドの実装を読む。

## hash
- d006d1da926e4a93665361add1951df6f42340ee39221dbf66c068cb9e5b620e

# `sub_commands`

## Summary
- CLI サブコマンドごとの実行ロジックを集約する領域。初期化、対話起動、ルーティング文書更新、oracle レビュー、apply 実行、session 操作など、利用者が起動する主要操作の入口と orchestration を扱う。
- 各サブコマンドは共通 runtime、git 操作、state 管理、worktree・branch 操作、Codex 呼び出し、レポート生成などの下位機能を組み合わせ、コマンド単位の事前条件、状態遷移、出力、失敗時処理を定義する。
- 下位要素は、apply 系、session 系、review 系、indexing、init、TUI 起動に分かれており、どのサブコマンド実装へ進むかを選ぶための入口になる。

## Read this when
- 利用者向けサブコマンドの実行フロー、事前条件、終了時の状態更新、CLI 出力、失敗時の扱いを調べたいとき。
- サブコマンドが session branch、apply/review 用 branch・worktree、session state、report、INDEX 変更、git 操作とどう接続されるかを追いたいとき。
- apply fork/join/abandon、session fork/join/abandon、oracle review、indexing、init、TUI 起動のうち、どの実装へ進むべきかを判断したいとき。
- Codex 呼び出しを含むサブコマンドの orchestration、対象列挙、実行 loop への委譲、結果の commit・merge・report 化を確認または変更したいとき。

## Do not read this when
- CLI 全体の command 登録、共通 runtime wrapper、設定モデル、path model、git wrapper、state file schema など、サブコマンド横断の基盤そのものを調べたいとき。
- Codex に渡す prompt や Structured Output parameter の本文だけを確認したいときは、各 parameter builder 側を直接読む。
- oracle file と realization file の概念、ルーティング文書仕様、INDEX.md エントリー生成規則など、正本仕様や文書方針を確認したいとき。
- 特定サブコマンド内の対象列挙、実行 loop、report 描画、merge conflict 解決など、詳細担当モジュールが既に分かっているときは、その下位要素へ直接進む。

## hash
- ea3bac407fc3621d62bdcdfd467c679e8a3613a9e713d62b3bf547540daf55b4
