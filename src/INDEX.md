# `acp`

## Summary
- realization 側に残る ACP builder 互換入口を束ねる領域。実体を oracle 側の builder 実装へ委譲・再公開し、既存の `acp.*` import 経路を移行期間中も維持するための package 境界として機能する。
- この領域は ACP builder の正本仕様や主要ロジックの置き場ではなく、互換 import 面と builder 関連下位領域への入口を扱う。

## Read this when
- ACP builder に関する既存の `acp.*` import が、realization 側でどの互換入口を通って oracle 側実装へ接続されているか確認したいとき。
- `acp.*` 参照を oracle 側または実体 module へ移行する作業で、互換入口を残す理由、残されている範囲、削除条件を判断したいとき。
- apply fork、review oracle、session join、TUI 起動パラメータ、indexing など、ACP builder 関連の下位領域へ進む入口を探しているとき。
- realization 側が ACP builder の主要ロジックを独自に持つのか、oracle 側実装への委譲・再公開・薄い adapter に留まるのかを切り分けたいとき。

## Do not read this when
- ACP builder の正本仕様、prompt 本文、Structured Output schema、モデル設定、file access mode、具体的な生成・判定ロジックを確認したいとき。その場合は oracle 側の対応箇所へ進む。
- apply fork 全体の制御フロー、fork 作成、git 操作、実行 orchestration、CLI 入出力、TUI 画面やイベント処理など、builder 互換境界ではない実行本体を調べたいとき。
- repository root 解決、path model、AgentCallParameter、列挙値などの基本定義そのものを調べたいとき。
- ACP builder 以外の ACP 関連モジュール、または互換入口ではない新規機能の実装場所やテスト対象を探しているとき。

## hash
- f7207b0bad7b979db2f1f9b34a848febceb53a3b368d0082039040f8f0775144

# `basic`

## Summary
- realization implementation の basic 領域で、既存の basic 系 import 経路を保つための互換・再公開層をまとめる場所。ACP 関連型、path model、構造化ドキュメント関連の公開名を正本側の実体へ接続し、この層自体には独自の定義・変換・検証ロジックをほぼ持たない。
- 正本側の基本概念を複製せず、realization 側や利用者向け公開面に残る既存参照を維持する入口として位置づけられる。互換層を残す理由や削除条件は、既存参照が残っているか、正本側または実体 module への移行が済んでいるかで判断する。

## Read this when
- realization implementation から正本側の basic 系公開要素へどの import 経路で接続しているかを確認したいとき。
- ACP 関連型、path model、構造化ドキュメント関連の公開名について、独自実装ではなく正本側の再公開になっている互換境界を確認したいとき。
- 既存の basic 系参照を維持する必要があるか、または互換入口を削除できるかを判断したいとき。
- 正本側の基本型や基本概念を realization 側で複製せずに公開している理由を確認したいとき。

## Do not read this when
- ACP 関連型、path model、構造化ドキュメントの具体的な定義、列挙値、変換規則、検証ロジック、挙動を調べたいとき。その場合は再公開元の正本側実装を読む。
- CLI 挙動、生成処理、テスト観点、または basic 領域以外の realization implementation の責務を調べたいとき。
- 正本仕様断片そのもの、oracle file と realization file の基本概念、またはルーティング文書の生成規則を確認したいとき。
- 新しい基本型や新しい挙動を追加する場所を探しているとき。この対象は互換用の公開入口であり、正本側の定義追加場所ではない。

## hash
- ef20b14eaabf3dde66ce344012d9e8b0114678a8dded41acd4e70edb4a06622d

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
- cmoc の realization implementation のうち、CLI 実行時に複数サブコマンドや上位処理から共有される runtime helper 群を収める領域。
- Codex CLI 呼び出し、preflight indexing、設定、内容 hash、エラー表示、git 操作、ログ、パス、結果型、session state など、横断的な実行時支援の実装と、それらをまとめて公開する import 入口を扱う。
- 個別サブコマンドの業務ロジックではなく、サブコマンドや workflow が共通して利用する実行境界、永続状態、外部プロセス、標準配置、失敗時表示の責務へ進むための入口である。

## Read this when
- CLI サブコマンド共通の実行ライフサイクル、終了コード化、標準サマリー、例外表示、subcommand log の設定を確認・変更したいとき。
- Codex exec/TUI 呼び出し、profile・sandbox・CODEX_HOME・call log・quota/capacity retry・Structured Output 検証・preflight indexing との接続を調べたいとき。
- INDEX.md 更新 preflight、索引 entry の鮮度判定、対象内容抽出、Codex への entry 生成依頼、Markdown entry 描画など、索引更新の実装を追いたいとき。
- cmoc 設定ファイル、内容 hash 保存、git worktree/branch 操作、runtime path、ログ、結果モデル、session state file など、複数機能から共有される runtime 基盤を探しているとき。
- 上位実装の import 面を整理する前に、共通 runtime API がどの module に分かれ、どの集約入口から公開されているかを把握したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、業務処理、利用者向けレポート、状態遷移の上位 workflow を調べたいだけのとき。その場合は該当する command や workflow 実装へ進む。
- oracle の正本仕様、INDEX.md entry に書くべき意味情報、path keyword の定義、session state の仕様意図などを確認したいとき。その場合は対応する oracle doc/source を読む。
- テストケース、fixture、期待値だけを確認・変更したいとき。その場合は test 側の対象へ進む。
- 生成済みの log、report、schema store、call log の内容を読みたいだけで、生成・保存・表示の runtime 実装を変更しないとき。
- 単一の下位責務がすでに分かっており、その具体挙動だけを調べたいとき。その場合は設定、git、path、logging、Codex exec/TUI、state などの該当 runtime 本文へ直接進む。

## hash
- 0b097804faf6ca4f419c75c19e0f00f112e3a385fd6ffd4e3895a419ec8290ea

# `config`

## Summary
- oracle 側の設定実装・設定定義を正本に保ったまま、realization 側や公開面に残る旧来の設定参照を受けるための互換入口をまとめる領域。
- 設定ロジック本体や正本仕様を持つ場所ではなく、既存 import 経路を維持するための再公開・橋渡しだけを担う。

## Read this when
- realization 側で旧来の設定参照がどこで受け止められているかを確認したいとき。
- 設定定義を複製せずに oracle 側の正本へ寄せたまま、既存参照名を維持している境界を調べたいとき。
- 旧来の設定 import や再公開を削除・置換する作業で、互換入口を残す理由や削除できる条件を確認したいとき。

## Do not read this when
- 設定項目の内容、型、読み込み、検証など、設定挙動の本体を確認したいとき。
- oracle 側の正本仕様断片または正本となる設定実装そのものを確認・変更したいとき。
- 新しい設定項目や公開面を追加する設計判断をしたいだけで、旧来参照との互換維持が論点ではないとき。

## hash
- 17a599971aa7a7a73a6a5499580e2f5660f4a85618ca80119352eb9cd8185b91

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
