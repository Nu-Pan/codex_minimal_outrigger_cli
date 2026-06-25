# `acp`

## Summary
- AI agent 呼び出しの入力契約を作る実装領域。用途別に、role・summary・goal・補助文脈・ファイルアクセス条件・モデル種別・reasoning effort・Structured Output schema を組み合わせた呼び出しパラメータを生成する処理と、そこへ差し込む標準プロンプト部品を生成する処理を扱う。
- サブコマンド本体の制御や低レベル実行基盤ではなく、上位処理が AI に何を依頼し、どの規範・制約・出力形式で応答させるかを確認するための入口になる。

## Read this when
- AI agent 呼び出しに渡すプロンプト内容、補助文脈、ファイルアクセス条件、モデル種別、reasoning effort、Structured Output schema の選定や変更を確認したいとき。
- 変更要約、所見列挙・適用、ルーティングエントリー生成、仕様レビュー、所見の採否判定・統合、conflict marker 解消、実行パラメータ選定など、用途別の AI 依頼内容を追いたいとき。
- 仕様ファイルと編集対象ファイルの扱い、ルーティング規則、ファイルアクセス規則、仕様文書基準、編集対象ファイル保守基準、レビュー基準、ルーティングエントリー基準などが、agent 向けプロンプトへどう組み込まれるか確認したいとき。
- ユーザー入力、対象ファイル内容、差分、レビュー所見、競合箇所、標準文書などの補助情報が、AI 呼び出し時の文脈としてどのように渡されるかを調べたいとき。

## Do not read this when
- CLI 引数解析、サブコマンド登録、作業順序、状態保存、表示、外部コマンド実行など、AI 呼び出し builder を使う側の制御フローだけを調べたいとき。
- AI 呼び出し基盤の型定義、Structured Output 実行器、構造化文書レンダリング、path model、git wrapper などの低レベル共通部品そのものを確認したいとき。
- 仕様本文、テスト本文、個別レビュー基準の正本内容、または生成されたルーティングエントリーの文面そのものを読みたいだけのとき。
- 実ファイル編集、差分分類、merge conflict 解消アルゴリズム、git merge、worktree 操作など、AI への依頼後に行われる具体的な下位処理を調べたいとき。

## hash
- dc6e4d3f587f59405552b72bd38f5f2299ebcd0ca1481c2d2f8652e20babeb07

# `basic`

## Summary
- cmoc の実装全体で共有される基礎的な型・変換ヘルパーをまとめる領域。エージェント呼び出しパラメータ、ルートトークン付きパス解決、規範データ構造、構造化文書から Markdown へのレンダリングを扱う。
- 特定の CLI サブコマンドや業務フローではなく、複数の上位実装から参照される抽象値、パス表現、仕様・文書表現の共通部品を確認する入口になる。

## Read this when
- エージェント呼び出しに渡す論理的なモデル指定、Reasoning effort、ファイルアクセスモード、Structured Output schema パスなどの共通パラメータ構造を確認・変更したいとき。
- cmoc で使う `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` 付きパス表記と実パスの相互変換、ルート探索、相対パス入力の扱いを確認・変更したいとき。
- 規範をコード上で表すデータ構造、要求ラベル、要求本文、判断例、構造化ドキュメントへの変換を確認・変更したいとき。
- 階層化された自然言語文書、仕様断片、レポート、プロンプトなどを Markdown 見出し・本文・コードブロックとしてレンダリングする共通処理を確認・変更したいとき。
- 上位機能で使う前提となる、型定義、入力検証、文書表現、Markdown 出力の境界を先に把握したいとき。

## Do not read this when
- CLI サブコマンドの引数定義、画面出力、終了コード、利用者向けコマンド挙動だけを調べたいとき。
- バックエンドが実際に受理する具体的なモデル名や Reasoning effort、ファイルアクセス指定への変換処理を探しているとき。
- プロンプト本文の生成ロジック、タスク別テンプレート、呼び出し実行の制御フローを調べたいとき。
- 個別機能がどの作業ディレクトリでファイルを作成・更新するか、永続状態や Git 操作をどう扱うかという業務ロジックを確認したいとき。
- 既存 Markdown の解析、INDEX.md のルーティング規則そのもの、正本仕様断片の内容や編集方針を確認したいとき。
- テスト構成、fixture、テストケース追加先を探しているとき。

## hash
- 8d94dca84d270b4fa4b33e15e66d16c39720978cb8732957988df4509bf46751

# `cmoc_runtime.py`

## Summary
- 互換用の薄い入口であり、実体のランタイム実装を別モジュールから読み込んで、この import path 自体を実装モジュールへ差し替える。
- 旧来の直接 import 経路や公開設定上の import 経路を残すための橋渡しで、責務固有のランタイム処理はここには置かない。

## Read this when
- トップレベルのランタイム import path がどの実装へ接続されるかを確認したいとき。
- 互換 import 経路の維持・削除条件や、直接 import している呼び出し元への影響を確認したいとき。
- ランタイム実装を移動・分割したあと、この互換入口を残す必要があるか判断したいとき。

## Do not read this when
- ランタイム処理そのものの挙動、引数処理、状態管理、出力生成を調べたいとき。その場合は実体の実装モジュールを読む。
- 新しいランタイム機能や責務固有の処理を実装したいとき。この互換入口ではなく実体側のモジュールを読む。
- パッケージ公開設定やエントリーポイント定義を確認したいだけのとき。その場合は設定ファイルを読む。

## hash
- 223b9df223b1746d08a7487389b45587c37917fa6e9b6d75d8dbb48985527074

# `commons`

## Summary
- cmoc の共有 runtime helper 群を集めた実装領域。CLI サブコマンド共通ラッパー、Codex CLI 呼び出し、Codex profile 準備、設定読み書き、content hash、共通エラー、Git 操作、実行ログ、runtime path、外部コマンド結果型、session state 永続化など、複数の上位処理から使われる横断的な実行時支援を扱う。
- 上位モジュール向けの共通 runtime API 集約入口と、責務別の下位実装が同居しているため、共有 helper の公開面を確認する入口にも、個別 runtime 挙動を追う入口にもなる。

## Read this when
- サブコマンド実行時の共通ライフサイクル、開始・完了表示、終了コード化、例外表示、サブコマンドログ設定など、個別コマンド本体の外側にある CLI 共通処理を確認または変更したいとき。
- Codex CLI の exec/TUI 起動、引数・環境・作業ディレクトリ、Structured Output schema、呼び出しログ、stdout/stderr/output 保存、capacity/quota retry、resume token、validation failure retry などの実行制御を追いたいとき。
- Codex 呼び出し用 profile、sandbox/permission profile、CODEX_HOME、schema/output JSON、Codex JSONL 由来のエラー抽出や capacity/quota 判定を確認または変更したいとき。
- cmoc の設定ファイル読み込み、初期生成、既定値補完、JSON 表現、不正設定の利用者向けエラー化を扱うとき。
- file/text hash、内容 hash 付き生成ファイル、binary 判定など、内容ベースの共通処理を確認または変更したいとき。
- cmoc 共通の実行時エラー構造、Summary・Next actions・Detail・Call stack を含む利用者向けエラー表示を確認または変更したいとき。
- Git コマンド実行の共通化、repository 状態検査、一時 worktree/managed branch の作成・削除、.cmoc の ignore 保証、Git ignore 判定を扱うとき。
- サブコマンド単位の JSON Lines 実行ログ、current logger、実行時間、quota wait の累積を確認または変更したいとき。
- runtime root の解決、.cmoc 配下の sessions/reports/log/worktrees/state/config の配置、timestamp、duration 表示、作業ディレクトリ一時変更を扱うとき。
- 外部コマンドや Codex exec wrapper の共有戻り値データ型を確認または変更したいとき。
- session/apply state の JSON 永続化、branch 名からの session-id 解決、home branch に紐づく active session 探索、状態ファイル不在や非管理 branch のエラーを扱うとき。
- 上位コードから利用する共通 runtime helper、結果型、状態型、Git helper、path helper などの import 経路や公開 symbol を調整したいとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、コマンド構成、ユーザー向けの具体的なコマンド出力を調べたいだけのとき。その場合は command 側の実装へ進む。
- path keyword や root 種別そのものの概念定義を確認したいだけのとき。その場合は path model の定義へ進む。
- 設定値そのもののデータ定義、AgentCallParameter、FileAccessMode、モデル種別、reasoning effort などの基本型だけを確認したいとき。その場合はそれらの定義本文へ進む。
- ログ内容を読む側、集計する側、表示する側の仕様や実装を探しているとき。この領域は主に実行中のログ記録と current logger を扱う。
- Git 以外の高レベルなサブコマンド業務フローや、特定操作がどの順序で状態・レポート・worktree を更新するかを調べたいとき。その場合は該当サブコマンドや状態利用側を読む。
- Codex CLI や Git の実行結果型だけで足りる場合に、実際の subprocess 制御、retry、ログ保存まで読む必要がないとき。
- oracle file の正本仕様、doc、テスト仕様、または実装差を避けたい人間意図を確認したいとき。この領域は realization implementation の共通 runtime 実装であり、正本仕様ではない。

## hash
- d62438efb3f1d4e4ca4db8b72cba84a32e2d5e1a7c90ce280d27e37a7c87a49b

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
- Typer による cmoc CLI の最上位エントリーポイントを定義し、session・apply・review などのサブコマンド群を各実装関数へ接続する。
- Codex 実行・TUI 実行の直前に indexing preflight を挟む wrapper と、再入防止・用途別 skip 判定を持つ。
- 通常の CLI 引数解析エラーを cmoc のエラー表示形式へ変換する Typer group を提供する。

## Read this when
- CLI の公開コマンド構成、サブコマンド名、option、各コマンドが呼び出す実装関数を確認・変更したいとき。
- Codex exec または Codex TUI 呼び出し前に indexing が実行される条件、skip 条件、対象 root の決定方法を調べたいとき。
- Typer や click の引数解析エラーが、cmoc のエラーレポートへ変換される入口を確認したいとき。
- アプリケーション起動時に呼ばれる CLI root と、各 subcommand group の登録関係を追いたいとき。

## Do not read this when
- 個別サブコマンドの業務ロジックや状態更新の詳細だけを調べたいときは、ここではなく対応する sub_commands 配下の実装を読む。
- runtime の外部コマンド実行、git 実行、repo/work root 解決、エラー描画の詳細を調べたいときは、ここではなく runtime 側の実装を読む。
- indexing preflight の具体的な走査・生成ロジックを調べたいときは、ここではなく indexing command 側を読む。
- 設定値の構造や AgentCallParameter の内容を調べたいだけのときは、それぞれの定義元を読む。

## hash
- 2042f0df636939b33c38361126b44e08a0d2c3c0f1df794096e3f0ba5b9baf58

# `sub_commands`

## Summary
- サブコマンド実装を集約する領域。初期化、対話型実行、INDEX.md 保守、oracle review、session lifecycle、apply lifecycle など、利用者向け CLI 操作ごとの実行本体と周辺 helper への入口になる。
- 各サブコマンドは、実行前提の検証、worktree/branch/state/report/process などの操作、Codex CLI 呼び出し、利用者向け出力、失敗時 cleanup や rollback といった制御をそれぞれの責務範囲で扱う。
- 下位には、apply 系と session 系のまとまったディレクトリに加え、review の統括・対象列挙・finding loop・INDEX 取り込み・report 描画、indexing、init、tui の個別実装が並ぶ。

## Read this when
- 特定の cmoc サブコマンドが、CLI 入力を受けた後にどの順序で検証、Git 操作、状態更新、Codex 呼び出し、出力生成を行うか確認・変更したいとき。
- apply、session、review、indexing、init、tui のいずれかの実行フロー、失敗条件、cleanup、rollback、report、process 管理、worktree/branch lifecycle を追いたいとき。
- サブコマンド固有の制御から、より細かい helper 実装へ進む前に、どの下位モジュールまたは下位ディレクトリが担当しているかを選びたいとき。
- oracle review の対象列挙、finding 処理、INDEX.md 差分取り込み、report 出力のように、review 系機能内の責務分担を見極めたいとき。
- INDEX.md の保守実行、初期化処理、対話型プロンプト処理など、単独サブコマンドに閉じた利用者向け挙動を確認・変更したいとき。

## Do not read this when
- Typer app へのサブコマンド登録、共通 CLI wiring、共通エラー表示、引数定義の外枠だけを調べたいときは、CLI 全体を組み立てる上位実装へ進む。
- repo root、work root、path keyword、git wrapper、worktree helper、branch helper、config、session state schema などの共通 runtime 機能そのものを調べたいときは、runtime や共通 utility 側を読む。
- Codex CLI に渡す AgentCallParameter や prompt parameter の具体的な文面・Structured Output schema だけを変更したいときは、builder 側の該当実装を読む。
- oracle file の正本仕様内容、INDEX.md エントリー生成規則、AGENTS 設定、memo の扱いなど、サブコマンド実装ではなく仕様断片やルール本文を確認したいとき。
- 生成済み report、過去実行結果、pid 状態ファイルなどの個別生成物の内容を確認したいだけのときは、出力先の生成物を直接読む。

## hash
- 73be0dcf777d466ec3008594523e7271fe3fdb2f4b9da85a5b0c37be70a853dd
