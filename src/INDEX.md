# `acp`

## Summary
- ACP realization implementation の最上位 package。oracle src 側の acp 名前空間と builder 領域への import 互換入口を提供し、実処理本体よりも正本側実装・生成結果・schema 連携へ到達するための薄い接続層として位置づけられる。
- 直下には、package import を成立させる最小入口と、apply、indexing、review、session、TUI など用途別の builder 下位領域へ進む入口がある。

## Read this when
- realization 側の acp 名前空間が oracle src 側とどのように import 互換を保っているかを確認したいとき。
- ACP builder 関連の実装を探し始めるうえで、apply fork、indexing、review finding、session join、TUI 起動パラメータのどの下位領域へ進むべきかを切り分けたいとき。
- acp 配下が独自の処理本体を持つ領域なのか、正本側定義や生成物を再公開・包み直し・実行側契約へ接続する領域なのかを確認したいとき。

## Do not read this when
- ACP の具体的なデータ構造、生成アルゴリズム、prompt 構成、判定基準、入出力仕様を詳しく調べたいとき。その場合は対応する下位領域または正本側実装・仕様断片を読む。
- CLI 全体の制御フロー、git 操作、差分適用、画面描画、イベントループなど、acp の import 互換境界や builder 接続層の外側の処理を調べたいとき。
- repo root 解決、path model、AgentCallParameter、enum、Structured Output schema など、acp 以外の共通基礎定義を確認したいとき。

## hash
- 5a83242ce3f06e1205c92cd19ee1c7201581e8c931116d455f4fb14e53d04914

# `basic`

## Summary
- realization implementation 側の basic 領域で、正本側 basic との import 互換入口、正本側定義の再公開口、ACP 実行時に共有する呼び出しパラメータ型をまとめる場所。
- この領域自体の多くは独自ロジックではなく正本側実装への薄い接続を担い、例外的に ACP 呼び出し条件を実行時に受け渡すための型定義を持つ。

## Read this when
- realization implementation 側から basic 概念を import する経路や、正本側 basic との対応関係を確認したいとき。
- path model や構造化ドキュメント関連の公開名が、realization 側で独自実装されているのか正本側から再公開されているのかを切り分けたいとき。
- ACP のモデル区分、推論努力、ファイルアクセスモード、プロンプト、structured output schema path をまとめて渡す実行時パラメータ型を確認・変更したいとき。
- basic パッケージ全体の入口としての意図を確認し、個別の実装本文へ進むか正本側へ進むかを判断したいとき。

## Do not read this when
- path model の root token の意味、path 変換仕様、構造化ドキュメントの型・関数・検証規則など、再公開元の具体的な仕様や実装を確認したいとき。その場合は正本側の該当本文を読む。
- ACP パラメータ値を組み立てるロジック、モデル選択規則、実際のファイルアクセス制御や権限判定を調べたいだけのとき。その場合はそれらの処理を持つ対象へ進む。
- oracle file と realization file の一般定義、編集責任、正本仕様断片としての扱いを確認したいとき。その場合は基本概念を定義する正本仕様断片を読む。
- CLI 挙動、サブコマンド処理、永続状態、テスト観点など basic の import 入口や共有型と直接関係しない実装を調べたいとき。

## hash
- f1bb0596c35f80d43d7d62b5bccab057c120fc799ccda52f6c1e6b8fb0b8b870

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
- cmoc の実行時共通 helper 群をまとめる実装領域。Codex 呼び出し、CLI サブコマンド共通ライフサイクル、設定、内容 hash、エラー表示、git 操作、ログ、パス、結果型、永続状態、ルーティング文書更新 preflight など、複数の上位機能から共有される runtime 境界を扱う。
- この領域は個別サブコマンドの業務ロジックではなく、上位処理が共通して使う実行基盤と、その公開 import 面・互換入口・責務別 helper への入口として位置づけられる。

## Read this when
- cmoc の上位コマンドから共有される runtime API、実行結果モデル、例外表示、設定読み書き、git・path・state・logging などの共通基盤を確認または変更したいとき。
- Codex exec/TUI 呼び出しの profile 作成、sandbox/cwd 決定、call log、quota/capacity retry、Structured Output 検証、preflight 実行、subcommand event 記録の流れを追いたいとき。
- CLI サブコマンド実行時の共通フロー、work root 検査、標準サマリー出力、終了コード化、例外時の利用者向け表示、サブコマンド logger の設定を確認したいとき。
- ルーティング文書の自動検査・再生成、対象列挙、既存エントリーの鮮度判定、Markdown 化、排他制御、更新差分 commit の実装を調べたいとき。
- 複数領域をまたぐ変更の前に、共通 runtime の公開面と責務分割を把握し、どの下位 helper へ進むべきか判断したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、業務処理、画面出力、状態遷移の上位制御だけを調べたいとき。その場合は対象コマンドの実装へ進む。
- oracle に書かれた正本仕様、path keyword の概念定義、ルーティング文書の仕様そのもの、session state の仕様意図を確認したいだけのとき。その場合は対応する正本仕様断片を読む。
- 生成済みの個別ルーティング文書の文章内容や、特定ディレクトリ・特定ファイルの要約を直したいだけのとき。その対象本文と生成指示を確認する方が直接的。
- 単一の責務だけを変更することが明らかなときは、この領域全体ではなく、設定、git、path、logging、state、Codex exec/TUI など該当する下位対象へ直接進む。
- 外部コマンドや Codex CLI の出力品質、LLM 応答内容、利用者が読む正本仕様の妥当性を評価したいだけのとき。この領域は実行境界と共通 helper を扱う。

## hash
- f4e88b62d4aba3ecfe842f1c1da9ac7e4b30c1cfeac8be0d08c3fde7175c19f9

# `config`

## Summary
- 実装側の設定パッケージであり、正本側の設定定義へ互換的に到達するための import 入口を提供する。設定値の実体や読み込み・検証などの処理は持たず、正本側定義の再公開境界を扱う。

## Read this when
- 実装側から設定定義へ到達する import 経路を確認したいとき。
- 設定パッケージが正本側の設定定義を実体として委譲し、互換入口として機能しているか確認したいとき。
- 設定モジュールの公開名、再エクスポート範囲、設定パッケージ入口の責務を確認したいとき。

## Do not read this when
- 個々の設定項目の意味、既定値、制約を確認したいとき。ここは設定定義の実体ではなく、正本側定義への入口だけを扱う。
- 設定値の読み込み、解決、検証、変換、永続化などの処理ロジックを調べたいとき。
- 正本仕様として設定内容そのものを確認したいとき。実体を持つ正本側の定義を直接読む方が適切である。

## hash
- 7a2dcace2fd029ab73ce6de095eae0152577f065ea99bdef28edd0f27aa94095

# `main.py`

## Summary
- cmoc の最上位 CLI を構成し、Typer アプリケーション、`session`・`apply`・`review` のサブコマンドグループ、各 CLI コマンドから実装関数への委譲を定義する実装入口。
- 通常の CLI 引数解析エラーを cmoc 形式のエラーレポートへ変換する Typer group を定義し、補完実行時だけ通常の Click/Typer 処理へ逃がす。
- console script から `cmoc` としてアプリケーションを起動するためのトップレベル関数を持つ。

## Read this when
- cmoc の公開 CLI コマンド構成、サブコマンド名、option 名、デフォルト値、各コマンドがどの実装関数へ委譲されるかを確認または変更したいとき。
- CLI 引数解析エラーを cmoc の `CmocError` と `render_error` で表示する挙動、または shell completion 時の例外処理分岐を確認または変更したいとき。
- `cmoc` console script 起動時に Typer app がどの `prog_name` で呼ばれるか、またはトップレベル app とサブ Typer app の接続を確認したいとき。

## Do not read this when
- 個別サブコマンドの本体処理、永続状態操作、git 操作、worktree 操作、レビュー処理、INDEX.md 更新処理の詳細を知りたいだけのときは、各サブコマンド実装を直接読む。
- CLI から呼ばれる実装関数の内部エラー生成、ドメインロジック、入出力ファイルの内容を調べたいだけのときは、この入口ではなく委譲先を読む。
- Typer や Click の一般的な使い方、または cmoc 外のパッケージ設定だけを調べたいときは、この対象を読む優先度は低い。

## hash
- 8e9205551785f5e63cb72c666b12049b600ee51d0e204d4198c7d568ba55a7a3

# `oracle.py`

## Summary
- 通常起動時に `src` だけが import path にある場合でも、正本側 `oracle/src/oracle` package を `oracle.*` として解決するための互換 shim。
- realization 側に残る `oracle.*` 再公開入口を個別に複製せず、正本側 package への submodule search path だけを提供する。

## Read this when
- `PYTHONPATH=src` や `bin/cmoc` からの起動直後に、`oracle.other` や `oracle.acp_builder` の import がどう成立するか確認したいとき。
- `src/config`、`src/basic`、`src/acp/builder` の薄い再公開 module が正本側実装へ到達する import 境界を確認・変更するとき。
- oracle src を realization 側へ複製せずに、既存互換 import path を成立させる理由を確認したいとき。

## Do not read this when
- 個別の正本仕様断片、prompt builder、設定定義、path model、ACP builder の本文を確認したいとき。その場合は `oracle/src/oracle` 配下の該当本文を読む。
- CLI サブコマンドや runtime helper の実処理を調べたいとき。この対象は import 境界だけを扱う。
- apply fork の個別 prompt 構築や AgentCallParameter の値を確認したいときは、該当 builder を直接読む。

## hash
- b6f4097cc1550a057bef77dda6b9e5434b394da2d2831fb96ccbf3d319c4222d

# `sub_commands`

## Summary
- cmoc の利用者向けサブコマンド実装をまとめる階層で、初期化、indexing、TUI、session、apply、review などの CLI 操作入口を扱う。
- 各対象は CLI runtime への接続、実行前条件、状態・branch・worktree 操作、Codex 呼び出し、利用者向け出力や report 生成など、サブコマンドごとの orchestration へ進むための入口になる。
- 共通 runtime や git wrapper、path model、state 永続化、INDEX.md 生成本体などは別階層へ委譲され、この階層では利用者操作単位の制御境界から読む先を選ぶ。

## Read this when
- 特定の cmoc サブコマンドが CLI から起動された後、どの runtime helper や下位処理へ渡されるかを確認・変更したいとき。
- 初期化、indexing、TUI、session、apply、review の実行条件、preflight、clean worktree 要求、branch/worktree 操作、state 更新、cleanup、利用者向け出力をサブコマンド単位で追いたいとき。
- session branch の作成・破棄・join、apply run の fork・abandon・join、review oracle の対象列挙から report 生成までなど、利用者操作に対応する制御フローの入口を探したいとき。
- サブコマンド実装から、Codex subprocess 実行、INDEX.md maintenance、review loop、report writer、merge conflict 処理などの詳細実装へどこで分岐するかを確認したいとき。
- CLI 全体の登録層ではなく、各サブコマンドが受け持つ実行時副作用や失敗時処理の責務境界を把握したいとき。

## Do not read this when
- Typer app へのサブコマンド登録、トップレベル CLI entrypoint、共通の CLI runtime 規約だけを確認したいとき。
- git 実行 wrapper、path model、config load、state file schema、timestamp、reports directory、cmoc ignore 判定などの共通部品そのものを調べたいとき。
- oracle doc 上のサブコマンド正本仕様や利用者向け要求そのものを確認したいときは、実装階層ではなく oracle 側を読む。
- INDEX.md の文章生成、差分検出、更新対象探索、ルーティング文書規約、Codex prompt builder の詳細だけを調べたいとき。
- 個別サブコマンドのさらに低レベルな処理だけを調べたい場合は、この階層全体ではなく apply、session、review、review_loop、review_index、review_report、review_targets など目的に直結する下位対象へ進む。

## hash
- f98a874160b4b4d24fa9e2d4fef9a44d28f4413fd76047124324c76f095d78cd
