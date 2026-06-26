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
- Typer による cmoc の最上位 CLI 入口を定義し、`session`、`apply`、`review` などのサブコマンド階層と各 command から実装関数への委譲を束ねる。
- 補完時を除く通常の Click 引数解析エラーを cmoc 共通のエラーレポート形式へ変換する Typer group を含む。
- console script 実行時に cmoc のコマンド名で Typer app を起動する薄いエントリーポイントである。

## Read this when
- cmoc の公開 CLI コマンド構成、サブコマンド名、option 名、または command から呼ばれる実装関数の対応を確認したいとき。
- CLI 引数解析失敗時のエラー表示、終了コード、補完時の例外扱いを調べるとき。
- 新しい top-level command、サブコマンド階層、または Typer command 入口を追加・削除・改名するとき。
- console script から cmoc がどの Typer app を起動するかを確認するとき。

## Do not read this when
- 個別コマンドの実際の処理内容、状態更新、git 操作、worktree 操作、review 実行内容を知りたいだけなら、ここではなく各 command の委譲先実装を読む。
- cmoc の共通エラー型やエラー描画の詳細を変更したいだけなら、ここではなく runtime 側の定義を読む。
- INDEX.md 生成処理そのもの、oracle review の実行ロジック、session/apply の join/fork/abandon の内部仕様を調べたいだけなら、対応する下位実装を直接読む。

## hash
- 1ae81e8854b36901ae139d89729fd33b79be4d1d5836d0a7f352c4e8c307c293

# `sub_commands`

## Summary
- cmoc のサブコマンド実行本体をまとめる領域。初期化、目次保守、TUI 起動、session の作成・取り込み・破棄、apply run の作成・取り込み・破棄、review oracle の対象列挙・実行・INDEX 差分処理・report 生成を扱う。
- 各実装は CLI runtime wrapper から呼ばれる上位制御を担い、clean worktree や active session などの事前条件、branch/worktree/state の更新、Codex 呼び出し、git 操作、利用者向け stdout や report 出力をサブコマンド単位で接続する。
- apply、session、review oracle などは下位モジュールへ責務が分かれているため、どのサブコマンドの lifecycle、helper、report、merge/cleanup 処理へ進むかを選ぶ入口になる。

## Read this when
- cmoc の具体的なサブコマンド実行フローを調べ、初期化、目次保守、TUI、session、apply、review oracle のどの実装へ進むべきか判断したいとき。
- サブコマンド実行時の事前条件検査、clean worktree 要求、cmoc ignore 確認、active session や apply state の条件、CLI runtime wrapper との接続を確認したいとき。
- session branch の作成、home branch への merge、merge せず破棄する処理、session state 更新、branch 削除、conflict 解消依頼などの制御を調べたいとき。
- apply run の fork/join/abandon、apply worktree と apply branch の作成・削除、pid file と実行中 process 停止、想定外差分や merge conflict の扱い、apply report 生成を追いたいとき。
- review oracle の対象 oracle file 列挙、finding enumerate/merge/validate/judge loop、INDEX.md 変更 commit、review branch merge、review report 出力のつながりを確認したいとき。
- INDEX.md の保守対象列挙、既存エントリーの hash 判定、Codex によるエントリー生成、更新 commit、排他 lock、indexing preflight を確認・変更したいとき。
- TUI 起動前の利用者 prompt 編集、parameter 解決、complete prompt 保存、許容 file access mode 検証、Codex TUI 起動までの処理を調べたいとき。

## Do not read this when
- CLI 全体の command 登録、Typer app の構成、共通 runtime wrapper、git command wrapper、repo/work root 解決、state schema、設定モデルなど、複数サブコマンドから使われる共通基盤そのものだけを調べたいとき。
- Codex に渡す prompt や Structured Output schema の本文、parameter builder の詳細を変更したいときは、builder 側の実装を直接読む。
- oracle file の正本仕様、oracle/realization の概念、path keyword の定義、INDEX.md エントリーの書き方など、仕様文書や path model 側の内容を確認したいだけのとき。
- テスト観点から外部挙動を確認したいだけなら、対応する realization test を読む。
- 対象サブコマンドや下位 helper が既に特定できており、fork、join、abandon、report、target 列挙、merge 処理などの個別本文へ直接進めるとき。
- 生成済み report や log の内容を読むだけで、report 生成ロジック、実行 lifecycle、state 更新、branch/worktree cleanup を変更しないとき。

## hash
- b2352131bd516de4a5cb5e325a5d6b362916ec8eac0424042419cb52146dcd9e
