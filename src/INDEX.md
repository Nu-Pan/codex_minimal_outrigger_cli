# `acp`

## Summary
- ACP builder 互換領域の入口で、oracle src 側の builder 実装を複製せずに既存の `acp.*` / `acp.builder.*` import 経路から利用できるようにする階層。
- この階層自体は実装本体ではなく、oracle 側への委譲、realization 側公開型への適合、旧 import 経路の維持、互換コードの残存理由と削除条件を確認するための上位ルーティング位置にある。
- apply、common、indexing、quota probe、review、session、TUI などの builder 系互換入口へ進むための切り分け点となる。

## Read this when
- `acp.*` または `acp.builder.*` の旧 import 経路を `oracle.*` や実体 module へ移行する作業で、互換入口を残す理由や削除条件を確認したいとき。
- oracle 側 builder と realization 側の既存公開 import path の対応関係や、戻り値を公開型・AgentCallParameter へ適合させる経路を探したいとき。
- apply、common、indexing、quota probe、review、session、TUI のどの builder 互換領域へ進むべきか切り分けたいとき。
- realization 側または利用者向け公開面に残る ACP builder 互換 import の扱いを判断したいとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容、人間意図などの正本仕様を確認したいときは、対応する oracle 側 builder を読む。
- acp builder の実装内容、生成処理、indexing の探索処理やデータ構造など、互換入口ではなく処理本体を調べたいときは、実体を持つ実装へ進む。
- ACP parameter の基礎構造、公開型、共通 model 設定、file access mode 全体の定義を確認したいときは、それぞれの基本型定義や共通実装を読む。
- 新しい acp 機能や API 仕様を追加する場所を探しているだけで、既存 import path の互換維持や oracle 側委譲に関係しないとき。
- `acp.*` 参照が全公開面と realization 側から消えていることを確認済みで、互換入口の詳細や削除条件を読む必要がないとき。

## hash
- e2017303b02a92dcf66076134d5bd7f43411f6f7244abad681301a14d0f8fe75

# `basic`

## Summary
- oracle 側にある basic 関連の正本実装を realization 側で重複実装せず、既存の `basic.*` import 経路として再公開する互換層を収めるディレクトリ。
- ACP 基本型、path model、構造化文書 API などについて、正本側実装への参照を保ちながら、realization 側および利用者向け公開面の既存参照を維持する入口として位置づけられる。
- この互換層の削除可否は、realization 側と利用者向け公開面から該当する `basic.*` 参照がなくなり、正本側または実体 module への移行が済んでいるかで判断する。

## Read this when
- `basic.*` 経由の既存 import 経路、再公開範囲、互換維持の理由を確認したいとき。
- oracle 側の ACP 基本型、path model、構造化文書 API を realization 側へ複製せず参照する方針を確認したいとき。
- `basic.*` 互換層を残す条件、移行条件、削除できる条件を調べたいとき。

## Do not read this when
- ACP 関連型、path placeholder、path 解決処理、構造化文書処理の定義内容や実処理を確認したいとき。その場合は再公開先の正本側実装を読む。
- CLI 挙動、実行制御、ファイルアクセス制御、テスト挙動など、basic API を利用する処理本体を調べたいとき。
- 既存の `basic.*` 互換参照や公開名に関係しない新仕様・新機能を検討しているとき。

## hash
- 2b1864cfa5bf55fe66730ae8be859de20f405a82e121a9512102f6001b42e250

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
- cmoc の共通実行時支援を集めた領域。Codex 呼び出し、INDEX 更新 preflight、設定、内容 hash、CLI 実行ライフサイクル、エラー表示、git 操作、ログ、path、結果モデル、永続 state、apply 実行管理など、複数サブコマンドから使われる runtime 部品への入口になる。
- 実処理を持つ責務別実装と、既存 import path を保つ薄い集約・互換入口が混在するため、共通 runtime の公開面と個別責務の実装先を切り分けて探すための階層である。

## Read this when
- 複数サブコマンドから共有される runtime helper、結果モデル、例外、path、git、logging、config、state、Codex 実行境界を確認または変更したいとき。
- Codex exec/TUI 呼び出し、Structured Output 検証、quota/capacity retry、call log、profile、CODEX_HOME、file access post-check、indexing preflight の実装経路を追いたいとき。
- INDEX.md 自動更新の対象走査、hash 鮮度判定、既存エントリー再利用、entry 生成依頼、Markdown 描画、排他 lock、更新順序を調べたいとき。
- apply 実行中の worktree 復元、pid file、Codex subprocess 追跡、abandon 時の process 停止を扱う共通 runtime を確認したいとき。
- CLI サブコマンド共通の開始・完了表示、ログ作成、終了コード化、例外表示、完了サマリーなど、個別 command の外側にある実行ライフサイクルを変更したいとき。

## Do not read this when
- 個別サブコマンドの利用者向け仕様、引数、業務処理、出力内容だけを確認したいとき。その場合は command 側の実装や対応するテストへ進む。
- oracle 上の正本仕様、path placeholder の定義、file access rule、INDEX.md の仕様意図、session state の仕様意図を確認したいだけのとき。その場合は対応する oracle doc または oracle src を読む。
- 低レベルな実装ではなく、実行済みログや生成済み成果物の内容を調査したいだけのとき。
- 特定の helper 利用箇所で渡す値や上位 workflow の判断だけを追いたいとき。その場合は、この階層の共通 helper ではなく呼び出し側を読む。

## hash
- 1a8095bc01cf3bb35b28f4e932d4211a9a7e5fbf29c9da3ab7d0ce65128a5186

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
- cmoc のサブコマンド実行本体を集める実装領域。init、indexing、tui、session、apply、review など、CLI entrypoint から呼ばれた後の各操作の orchestration への入口になる。
- 各対象は個別サブコマンドまたはサブコマンド群の責務を持ち、work root、git、state、branch、worktree、Codex 実行、report 出力、INDEX 更新などを伴う制御を調べる際に読み分ける起点になる。

## Read this when
- cmoc の各サブコマンドについて、CLI 登録後の実行フロー、事前条件、状態更新、git 操作、Codex 実行、利用者向け出力を確認または変更したいとき。
- init、indexing、tui の単体サブコマンド実装、または session、apply、review のサブコマンド群のどの下位対象へ進むべきかを判断したいとき。
- session branch や apply run、review oracle など、複数段階のライフサイクルを持つ操作の大きな制御順序と責務境界を追いたいとき。
- INDEX.md maintenance、review report、apply report、TUI prompt、初期化結果など、サブコマンド固有の出力や後処理への入口を探したいとき。

## Do not read this when
- Typer app へのコマンド登録、CLI 引数定義、トップレベル entrypoint だけを確認したいとき。
- git command wrapper、CLI runtime、path model、state model、config、ignore 判定、Codex parameter builder など、共通 helper の低レベル実装だけを調べたいとき。
- oracle doc に書かれた各サブコマンドの正本仕様そのものを確認したいとき。
- INDEX.md の文章生成ロジック、review finding 生成、prompt parameter の具体的文面など、下位の専用モジュールや builder が直接担う詳細だけを調べたいとき。

## hash
- d0139106857328c61dd7a042e2ba83db00d8eb7564a2d1659195804a0700cb64
