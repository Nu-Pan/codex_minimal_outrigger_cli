# `acp`

## Summary
- oracle 側へ移された ACP builder 実装を、既存の acp import 経路から参照し続けるための互換入口をまとめる領域。
- 正本実装や生成規則を持つ場所ではなく、旧名前空間と oracle 側 builder、realization 側 parameter 表現を接続する薄い互換層として位置づけられる。

## Read this when
- acp import 互換性のために残されている入口の意図や削除条件を確認したいとき。
- acp.builder 系の旧 import 経路が oracle 側の canonical 実装へどう接続されているか確認したいとき。
- builder 互換入口、再エクスポート、oracle src import 準備、repository root 解決、schema path fallback などの接続処理を調べるとき。
- oracle 側 builder の出力を AgentCallParameter や runtime ACP 型へ適合する境界を確認・変更したいとき。
- Codex quota availability probe 用に、既存 AgentCallParameter から最小確認用 parameter を組み立てる処理を探しているとき。

## Do not read this when
- ACP builder の正本仕様、prompt 内容、parameter 内容、生成規則、本体実装を確認したいときは、oracle 側の対応実装や仕様断片を読む。
- apply fork、review、session、TUI など各機能の実行制御、状態管理、画面、イベント処理、git 操作、finding 判定などの実体ロジックを調べたいとき。
- AgentCallParameter、FileAccessMode、path placeholder、oracle file、INDEX.md 記述基準などの一般定義を確認したいときは、より直接の定義や oracle doc を読む。
- 新しい恒久的な builder 機能や公開 API を追加したいだけで、旧 import 経路の互換維持や oracle 側への接続に関心がないとき。

## hash
- d38b1deed05edf564ec221a1e4b72f82e9e3ed2bc807b56918f75a8d6b533d3f

# `basic`

## Summary
- oracle src の basic 互換公開面を集めたディレクトリ。正本側の実体定義を複製せず、既存の `basic.*` 参照を oracle 側実装へつなぐ薄い再公開モジュール群を扱う。
- ACP 型、path model、構造化文書 API など、移行途中の公開参照名を維持するための入口を下位ファイルへ分けている。

## Read this when
- `basic.*` 経由の既存 import 互換性を確認・維持・削除判断したいとき。
- realization 側へ正本型や正本実装を複製せず、oracle 側定義を参照する互換経路を探すとき。
- ACP、path model、構造化文書 API の公開参照名がどの薄い再公開層で支えられているかを確認したいとき。

## Do not read this when
- ACP 型、path model、構造化文書 API そのものの正本定義や具体的な実装ロジックを確認したいとき。その場合は oracle 側の正本実装を読む。
- 新しい仕様や挙動差を検討したいだけで、`basic.*` 互換公開面の要否に関係しないとき。
- `basic.*` 参照の互換維持・移行条件・削除可否に関係しない realization 実装を調べるとき。

## hash
- 54ab8368d48776db5acdef8b70da803a21d33aa7b73e581db4af49727b15dd18

# `cmoc_runtime.py`

## Summary
- 公開済みの実行時 API を既存実装へ委譲する互換 import 経路。実体は別モジュールにあり、この対象は同じ module 名で参照されたときに既存の呼び出し元を壊さないための薄い橋渡しだけを担う。

## Read this when
- 公開済み import path と実体 module の対応を確認したいとき。
- 互換 import path を削除できる条件や、移行中の runtime module 参照を確認したいとき。
- パッケージ公開名と tree 内の直接 import の両方が関係する runtime import 問題を調べるとき。

## Do not read this when
- 実行時機能の本体実装や各 helper の挙動を調べたいときは、委譲先の runtime 実装を読む。
- 新しい runtime 処理を追加・変更したいときは、この互換層ではなく実体 module を読む。
- ビルド成果物全体の生成手順や配布設定を調べたいだけのときは、より直接それを扱う設定・手順の対象を読む。

## hash
- a36ad0b5d09cbe7d2be546fdafcd27ff3ddaf803744331274a69fb25f15cd7ee

# `commons`

## Summary
- cmoc の共有 runtime helper 群を集めた領域であり、CLI 共通実行、Codex 呼び出し、設定、git、ログ、path、状態、hash、エラー、INDEX.md 更新などの実行時基盤へ進む入口になる。
- 複数箇所から使われる共通処理の公開入口と個別 helper 実装が並び、横断的な import 経路の確認から、各責務の実装詳細の調査までをこの配下で切り分けて扱う。

## Read this when
- cmoc の実行時共通処理、サブコマンド共通ライフサイクル、Codex exec/TUI 呼び出し、preflight indexing、runtime profile、設定読み書き、git 操作、ログ、path、状態管理、エラー整形、content hash のいずれかを確認または変更したいとき。
- 複数の runtime 共通機能を使う呼び出し側で、公開入口から参照できる helper・型・定数や import 経路を整理したいとき。
- Codex 実行前後の制御、Structured Output 検証、quota/capacity retry、call log、file access rule 違反修復、subcommand event 記録など、実行基盤を横断する挙動を追いたいとき。
- INDEX.md の自動更新、entry 生成、hash 検証、既存 entry 再利用、indexing commit、preflight 登録や排他制御を調べたいとき。

## Do not read this when
- 個別 CLI サブコマンドの業務処理、ユーザー向けコマンド仕様、入力引数、出力 schema だけを確認したいときは、該当するコマンド実装を読む。
- oracle file にある正本仕様、path model の定義、prompt 部品、console/log 仕様そのものを確認したいときは、対応する oracle 側を読む。
- 特定の helper の挙動だけを確認したい場合は、この領域全体ではなく該当する下位モジュールを直接読む。
- テスト、文書、永続化された実行結果、生成物の内容そのものを調べたいときは、それぞれの生成元または利用側を読む。

## hash
- b7c9a4c52f4ba6a463edb2d3a04bd17c48162ac199d8541cc7035772b31465d6

# `config`

## Summary
- oracle 側の設定定義を正本のまま保ち、既存の config 名前空間から参照できるようにする互換再公開層。
- 設定内容そのものは持たず、config.* 参照が残っている間だけ oracle 側の設定定義への橋渡しを担う。

## Read this when
- config.* や config.cmoc_config の参照が、どの oracle 側設定定義へつながるかを確認したいとき。
- oracle 側の設定定義を移動・改名・複製せずに、既存 import 互換性を保つ理由を確認したいとき。
- config 名前空間の互換入口を削除できる条件や、存続理由を判断したいとき。

## Do not read this when
- 設定定義の正本内容や設定値の意味を確認したいときは、oracle 側の設定定義を直接読む。
- 新しい設定仕様や設定処理の実装場所を探しているだけで、config 名前空間の互換維持に関係しないとき。
- realization 側の具体的な config.* 利用箇所を調べたいときは、利用元の実装を直接読む。

## hash
- 9919b273df0aac542a58a032429e4e19f5e883546bbf9ca4b46bbed857841479

# `main.py`

## Summary
- Typer ベースの cmoc CLI 入口を定義し、最上位コマンドと session・apply・review 配下のサブコマンドを各実装関数へ接続する。
- 通常実行時の Click 引数解析エラーを cmoc 形式のエラーレポートへ変換し、補完実行時は Typer/Click の通常処理へ委ねる。

## Read this when
- CLI のコマンド構成、サブコマンド名、option の入口定義を確認または変更したいとき。
- 引数解析失敗時のエラー表示や終了コードの扱いを確認したいとき。
- console script から cmoc の Typer app が起動される経路を追いたいとき。
- 既存の CLI 入口がどのサブコマンド実装関数へ委譲しているかを確認したいとき。

## Do not read this when
- 各サブコマンドの実処理、git 操作、worktree 操作、review 実行内容を知りたいときは、委譲先のサブコマンド実装を読む。
- cmoc の正本仕様や CLI 挙動の人間意図を確認したいときは、対応する oracle doc を読む。
- INDEX.md 更新処理そのものの詳細を確認したいときは、indexing の実装を読む。
- Typer や Click の一般的な使い方だけを調べたいときは、この対象を読む必要はない。

## hash
- 8e9205551785f5e63cb72c666b12049b600ee51d0e204d4198c7d568ba55a7a3

# `oracle`

## Summary
- AI エージェント呼び出しパラメータ、プロンプト構築、設定・パス・規範文書・構造化 Markdown レンダリングに関する正本由来の実装領域への入口。
- 用途別 agent call の role、goal、制約、Structured Output schema、file access mode、標準プロンプト片、プレースホルダ、基礎モデルの読む先を選ぶためのルーティング対象。
- apply fork、目次生成、oracle file レビュー、session join conflict 解消、TUI 起動、アクセス規則違反復旧など、AI 呼び出しに関わる仕様断片由来の構成を確認する起点となる。

## Read this when
- AI エージェント呼び出しパラメータ、論理モデルクラス、reasoning effort、ファイルアクセスモード、目的別 prompt や Structured Output schema の正本由来定義を確認したいとき。
- 完全な agent call prompt の組み立て順、静的・動的 prompt 部品、標準プロンプト片、プレースホルダ定義の合成を確認または変更したいとき。
- cmoc の設定モデル、ルートパスプレースホルダ、実パス解決、規範フォーマット、構造化 Markdown 出力変換などの基礎モデルへ進みたいとき。

## Do not read this when
- agent call の実行手順、プロセス起動、結果処理、永続状態管理、git 操作、fork 作成、branch 操作など、実行制御そのものを調べたいとき。
- 個別サブコマンドの処理手順、CLI 入出力、状態管理、TUI 画面制御、設定の読み書き処理、JSON 変換処理を確認したいとき。
- oracle file 本体の仕様内容、レビュー基準本文、INDEX.md エントリー品質基準、既存 Markdown parser、または特定 realization file の実装内容そのものを確認したいとき。

## hash
- 97a65d3f4eb034acdc3695fe498f5bb14fc3ae7b1e9ea9500feb7a754a14ea64

# `sub_commands`

## Summary
- CLI サブコマンド実装のうち、apply、indexing、init、review、session、tui に関する生成済み実装をまとめる階層。各サブコマンドの実行入口、runtime 接続、git/worktree/state 操作、レポート生成、cleanup などの上位 orchestration へ進むための入口になる。
- apply run、INDEX.md maintenance、初期化、review oracle、session 操作、TUI 起動のどの実装を読むべきかを切り分けるルーティング対象であり、共通 runtime や低レベル helper そのものではなくサブコマンド側の制御を扱う。

## Read this when
- 生成済み実装側で CLI サブコマンドの入口や実行フローを探しているとき。
- apply、indexing、init、review、session、tui のどの領域へ進むべきかを切り分けたいとき。
- サブコマンド実行時の preflight、runtime 設定、git branch/worktree 操作、session state 更新、cleanup、レポート出力、Codex 呼び出しへの接続箇所を確認したいとき。
- review oracle の対象列挙、反復処理、INDEX.md 差分 merge、レポート描画など、review 系処理の責務別入口を探したいとき。

## Do not read this when
- 生成済み build 配下ではなく正本の実装ソースを編集したいとき。
- oracle file の正本仕様、サブコマンド仕様、INDEX.md エントリー仕様そのものを確認したいとき。
- session state、git wrapper、report directory、timestamp、CLI runtime、Codex exec、prompt builder、Structured Output schema などの共通処理や下位処理だけを確認したいとき。
- apply、indexing、init、review、session、tui 以外のサブコマンド実装を探しているとき。

## hash
- 8185a5842ddddfd9dad4ad964e359bb8c42d5ade422c7e9b6ac24f577a230b6e
