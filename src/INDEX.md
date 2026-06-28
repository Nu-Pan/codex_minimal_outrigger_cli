# `acp`

## Summary
- oracle src 側の ACP 実装を、realization implementation 側の import 経路から参照できるようにする互換パッケージ領域。
- この領域自体は ACP の処理本体や正本仕様断片ではなく、acp 名前空間の成立と builder 配下の互換入口へ進むための上位入口として位置づけられる。
- 下位には builder 領域があり、適用、indexing、review、session、TUI などの正本側 builder 実装へ src 側から到達するための接続点を束ねる。

## Read this when
- src 側の acp パッケージが oracle src 側の ACP 実装とどのような import 互換経路を持つか確認したいとき。
- ACP 関連の実処理を読む前に、realization implementation 側ではどの階層が単なる互換入口で、どこから下位領域へ進むべきか切り分けたいとき。
- ACP builder 配下の適用、indexing、review、session、TUI などの領域へ進む前に、acp 名前空間全体の入口と下位接続を確認したいとき。

## Do not read this when
- ACP の具体的な処理内容、データ構造、関数、クラス、入出力仕様、アルゴリズムを調べたいとき。その場合は正本側の対応実装、または builder 配下のより直接の対象を読む。
- oracle file としての正本仕様断片を確認したいとき。この領域は realization implementation 側の互換入口であり、正本仕様本文ではない。
- ACP 以外の import 互換入口や、cmoc 全体の path model、oracle file、realization file の定義を調べたいとき。

## hash
- c41aed1061b3fbcd4d835d9ce74914d79dddca143b31ee93117b75b1396c1c88

# `basic`

## Summary
- realization implementation 側の basic パッケージ領域であり、正本側 basic 実装への互換 import 入口をまとめる。
- この領域自体は独自の機能実装を持つより、ACP、path model、構造化ドキュメントなどの公開名を正本側から再公開する薄い接続層として位置づけられる。

## Read this when
- realization implementation 側で basic 関連 API がどこから公開されるかを確認したいとき。
- 正本側 basic 実装と realization implementation 側 basic パッケージの import 構造上の対応を確認したいとき。
- ACP、path model、構造化ドキュメント関連の公開入口が、独自実装ではなく正本側の再公開であるかを切り分けたいとき。
- basic 配下の個別領域へ進む前に、この階層が担う役割が互換 import 入口と再公開層であることを把握したいとき。

## Do not read this when
- ACP、path model、構造化ドキュメントの具体的な型、関数、変換規則、検証ロジック、生成ロジックを調べたいとき。その場合は再公開元の正本側実装を読む。
- path model の概念定義や root token の意味など、正本仕様断片としての説明を確認したいとき。その場合は正本側の該当本文を読む。
- realization implementation 側で独自に実装された basic 処理を探しているとき。この領域の本文は主に正本側への中継を示す。
- cmoc 全体の oracle file と realization file の責務分担、INDEX.md エントリー生成規則、ルーティング文書の書き方を調べたいとき。その場合はそれらを定義する正本仕様断片を読む。

## hash
- 4b2b1d9eae2fa6fa3d4011887739b3a417de79c6b3d1066763f21b5d6bc39d9d

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
