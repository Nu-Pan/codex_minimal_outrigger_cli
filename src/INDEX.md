# `acp`

## Summary
- ACP 名前空間の realization implementation を束ねる領域。oracle src 側の acp 実装と互換の import 経路を提供するパッケージ入口と、ACP builder 関連の下位領域へ進む入口を持つ。
- 実処理の多くは下位の builder 領域または oracle 側実装にあり、この階層自体は acp パッケージを import 可能にする境界と builder 名前空間へのルーティング起点として位置づけられる。

## Read this when
- src 側で acp 名前空間がどの入口から成立しているか、または oracle src 側 acp 実装との import 互換境界を確認したいとき。
- ACP builder まわりの apply、indexing、review、session、TUI など用途別領域へ進む前に、src/acp 配下の全体構成を切り分けたいとき。
- acp パッケージ直下で実処理を探すべきか、下位の builder 領域や oracle 側実装へ進むべきかを判断したいとき。

## Do not read this when
- acp の具体的な処理内容、データ構造、関数、クラス、prompt 構成、入出力仕様を直接調べたいとき。その場合は下位の該当領域または oracle 側実装を読む。
- ACP builder 以外の CLI ルーティング、公開 API、テスト、生成済み成果物、または oracle 側の正本仕様断片そのものを探しているとき。
- apply fork の実行制御、git 操作、作業ディレクトリ管理、レポート保存など、builder 用 agent call parameter 構築や import 互換境界を超えた処理を調べたいとき。

## hash
- 0850077e0e96de01434ec6c4c9afad9aae06ebd66ff9be1daa8dbc0dc41cb163

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
- cmoc の realization implementation のうち、複数のサブコマンドや上位処理から共有される実行時 helper 群をまとめる領域。
- Codex CLI 呼び出し、preflight indexing、設定読み書き、内容 hash、CLI 共通ライフサイクル、共通エラー表示、git 操作、ログ、パス、実行結果モデル、session state 永続化など、cmoc 実行基盤の横断的な処理への入口になる。
- この階層には、実処理を持つ runtime module と、既存 import path を維持するための集約・互換 import 入口が混在しているため、具体挙動を読む場合は責務別の下位本文へ進む。

## Read this when
- cmoc の複数機能で共有される runtime helper、共通型、共通エラー、共通ログ、共通 path、git 操作、Codex 呼び出し境界、設定や状態の永続化に関する実装場所を探すとき。
- Codex exec/TUI の起動前後処理、Structured Output 検証、quota/capacity retry、call log、preflight indexing など、Codex subprocess 境界の共通制御を確認または変更したいとき。
- CLI サブコマンドの共通実行フロー、終了コード化、標準サマリー、例外表示、サブコマンド log との接続を調べたいとき。
- INDEX.md 自動更新の preflight、対象列挙、既存エントリー鮮度判定、欠落エントリー生成、Markdown 描画、専用 commit 作成の流れを追いたいとき。
- cmoc の標準保存先、work/root/repo path、memo 判定、session state file、config file、logs、schema store など、複数領域から参照される runtime 配置規則の実装へ進みたいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、CLI 引数定義、利用者向けレポート生成だけを調べたいとき。その場合はコマンド層の対象へ進む。
- oracle file の正本仕様、path keyword の概念定義、session state や CLI 出力の仕様意図を確認したいとき。その場合は対応する oracle doc または basic 層の正本仕様を読む。
- テストの期待値や fixture、外部挙動の検証内容を確認したいとき。その場合は realization test 側へ進む。
- 特定の共通 helper の具体的な入出力、副作用、例外条件だけを調べたい場合は、この階層全体ではなく、設定、git、path、logging、state、Codex exec/TUI など該当責務の本文へ直接進む。
- 既存 import 面の確認だけでなく新しい runtime 処理を追加する場所を探しているときは、集約・互換 import 入口ではなく、責務が一致する実処理 module を読む。

## hash
- 546ccc8be91d8ec63fedc0188bed189db4fa8004cfba12bd782008d9872a7864

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
- cmoc の利用者向け CLI サブコマンド実装を集める領域で、初期化、INDEX maintenance、TUI 起動、session lifecycle、apply lifecycle、review oracle 実行をそれぞれの操作単位へ振り分ける入口になる。
- 各サブコマンドは CLI runtime への接続、実行前条件の確認、work root・branch・worktree・state・report などへの副作用制御、成功時または失敗時の利用者向け出力を扱う。
- 詳細な生成ロジックや共通 helper そのものよりも、サブコマンドとしてどの処理をどの順序で起動し、どの下位実装へ委譲するかを把握するための階層である。

## Read this when
- cmoc の特定サブコマンドについて、CLI からの実行入口、実行前条件、状態遷移、branch/worktree 操作、cleanup、report 出力、標準出力の流れを確認・変更したいとき。
- 初期化、INDEX maintenance、TUI 起動、session 作成・破棄・join、apply fork・abandon・join、review oracle のいずれかの実装入口を探したいとき。
- サブコマンドが CLI runtime、Codex 実行 callback、git 操作、ignore 保証、work root runtime、state 更新、report writer などの共通部品へどこから接続するかを追いたいとき。
- review oracle や apply のように複数段階の処理を持つサブコマンドで、対象列挙、反復処理、INDEX 反映、merge conflict 対応、fork report、cleanup などの下位処理へ進む入口を選びたいとき。
- 利用者操作単位で、実行中 process の扱い、pid file、temporary branch/worktree、session branch への取り込み、home branch への merge などのライフサイクルを調べたいとき。

## Do not read this when
- CLI 全体のトップレベル登録、Typer app 構成、共通 runtime wrapper、path model、config load、git wrapper、state file 永続化など、サブコマンド横断の基盤だけを調べたいとき。
- 各サブコマンドの正本仕様や公開仕様そのものを確認したいときは、実装入口ではなく対応する oracle doc を読むべきである。
- INDEX.md の本文生成、差分検出、lock、commit、ルーティング文書規約、Structured Output parameter など、サブコマンドから呼ばれる共通処理の詳細だけを調べたいとき。
- Codex exec に渡す prompt や builder parameter の具体的な文面・schema だけを確認したいときは、prompt builder や parameter builder 側を直接読む方が適切である。
- reports directory、timestamp、process start time、cmoc ignore 判定、clean worktree 判定、path token 解決などの共通仕様または共通 helper の詳細だけを調べたいとき。
- テスト、fixture、または oracle と realization の概念定義を探しているときは、このサブコマンド実装階層ではなく対応する test、oracle、basic module を読む。

## hash
- 788a183350c2b5db694f70a2f9d8d82bd1ff74817dbb5377fe08e2fd9b6cf6da
