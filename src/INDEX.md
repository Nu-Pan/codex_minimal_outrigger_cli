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
- Codex 実行、CLI サブコマンド共通ラッパー、設定、content hash、エラー表示、Git 操作、ログ、path 解決、結果型、session state など、cmoc の複数上位機能から共有される実行時 helper 群をまとめる領域。
- 個別サブコマンドの業務処理ではなく、上位コードが共通 runtime 機能を使うための公開入口と、外部プロセス・永続状態・作業ディレクトリ・利用者向けエラーを横断的に扱う下位実装への入口になる。

## Read this when
- 共通 runtime API の公開面や、上位モジュールから import できる helper・結果型・状態型の入口を確認したいとき。
- CLI サブコマンド実行の共通ライフサイクル、ログ設定、終了コード化、例外表示、完了サマリーの処理を調べたいとき。
- Codex CLI 呼び出し、profile/schema/output JSON、quota/capacity/retry/resume、Codex 呼び出しログの共有実装を確認または変更したいとき。
- cmoc 設定ファイル、content hash、Git repository/worktree 操作、root path と `.cmoc` 配下の保存先、subcommand log、session state の共通 helper を探すとき。
- 複数のサブコマンドや上位モジュールで同じ runtime 処理を共有する場所を判断したいとき。

## Do not read this when
- 特定サブコマンドの引数定義、処理順、業務ロジック、利用者向けコマンド構成だけを調べたいとき。その場合は command 実装側へ進む。
- AgentCallParameter、FileAccessMode、CmocConfig、path keyword などの基本データ定義や概念説明そのものを確認したいとき。その場合はそれらを定義する basic/config 側へ進む。
- oracle の正本仕様断片、仕様文書、仕様上の要求を確認したいとき。この領域は realization implementation の共通 runtime 実装であり、仕様本文ではない。
- テスト期待値や fixture から外部挙動を確認する方が直接的なとき。その場合は対応する test 側へ進む。

## hash
- 79e4e4c0c104007f8c54077d2022f5331eb04328b998c9d8e36499965d7751ee

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
- サブコマンド実装をまとめる領域で、初期化、対話実行、indexing、oracle review、session lifecycle、apply lifecycle など、cmoc の利用者向け操作ごとの統括フローと下位処理への入口を担う。
- 各サブコマンドは、実行前提の検証、worktree・branch・session state・report・Codex 呼び出し・INDEX.md 更新などを、それぞれの操作単位で分担している。
- review と apply は統括フローから対象列挙、loop、INDEX.md 差分処理、report、低レベル補助処理へ分かれており、session は開始・join・破棄の lifecycle 操作を下位ディレクトリにまとめている。

## Read this when
- cmoc の特定サブコマンドについて、実行条件、状態遷移、Git 操作、worktree 操作、出力、report 生成、Codex 呼び出しの接続点を探したいとき。
- 初期化、対話実行、indexing、oracle review、session、apply のどの実装へ進むべきか、サブコマンド単位で切り分けたいとき。
- oracle review の対象列挙、finding loop、INDEX.md 差分の commit/merge、review report 生成など、review 系処理の責務境界を確認したいとき。
- apply の開始、破棄、join、finding 適用、禁止領域差分 rollback、merge、cleanup、report 生成など、apply lifecycle の入口や下位実装を探したいとき。
- session branch の作成・取り込み・破棄、active session 制約、merge conflict 解消、session state 更新など、session lifecycle の実装を調べたいとき。
- INDEX.md 更新対象の選別、既存 entry の検証、Codex CLI による entry 生成、INDEX.md 書き戻しと commit の流れを確認したいとき。

## Do not read this when
- Typer app 全体の登録や最上位 CLI 配線だけを確認したいときは、上位の CLI 実装を読む。
- work root、path keyword、git wrapper、config、cmoc ignore、session state schema、report directory、Codex 実行 wrapper など、複数サブコマンドで使う共通 runtime helper 自体を調べたいとき。
- Codex CLI に渡す prompt parameter、AgentCallParameter builder、Structured Output schema の具体的な文面や型定義だけを変更したいときは、builder や schema 側を読む。
- oracle file の正本仕様内容、INDEX.md entry の生成規則、oracle と realization の基本定義を確認したいときは、oracle 側の本文を読む。
- 個別のテスト期待値や過去の生成済み report の内容を確認したいだけのときは、test または report 出力先を直接読む。

## hash
- f5d57c5dadb72377d019f0ba7cf4aa726c402679e754add9d0b85144b3b9e600
