# `acp`

## Summary
- oracle src 側の ACP builder 実装を複製せず、既存の `acp.*` import 経路を正本側実装または薄い wrapper へ接続する互換入口領域。
- agent call parameter builder 周辺の公開参照維持、正本側 builder への委譲、realization 側 parameter 型への適合、互換コードの残置理由と削除条件を確認するための上位入口。
- apply、review、session、TUI、indexing、quota probe などの builder 領域へ進む前に、実処理の所在が正本側か realization 側の互換入口かを切り分けるために使う。

## Read this when
- ACP builder 周辺で、既存の `acp.*` import 参照が正本側実装へどのように接続されているか確認したいとき。
- realization 側または利用者向け公開面に残る `acp.*` import、再公開 module、薄い wrapper、暫定補正について、残す理由や削除条件を判断したいとき。
- apply、review、session、TUI、indexing、quota probe などの agent call parameter 生成周辺で、どの下位領域または正本側実装へ進むべきか見分けたいとき。
- 正本側 builder の出力を realization 側で利用する際の委譲関係、型適合、公開 import 経路維持の境界を調べたいとき。
- 同名機能が realization 側にあるように見える場合に、実処理の所在が正本側実装か互換入口かを切り分けたいとき。

## Do not read this when
- 個別 builder の具体的な生成ロジック、repo root 解決、prompt 文面、出力条件、判定仕様を直接確認したいときは、下位の個別領域または正本側実装を読む。
- CLI コマンド全体の制御フロー、branch 操作、diff 生成、TUI 描画、イベント処理、Codex CLI 実行など、parameter builder 以外の処理を調べたいときは、その責務を持つ実装へ進む。
- agent call parameter の共通データ構造、model、reasoning effort、file access mode などの基礎定義を確認したいときは、基礎定義側を読む。
- 正本仕様断片そのものや oracle 側の実装内容を確認したいときは、互換入口ではなく対応する正本側本文を読む。
- 新しい ACP 機能や API 仕様を追加する場所を探しているとき。この領域は既存 import 経路の互換維持と正本側 builder への委譲関係の確認に限られる。

## hash
- 019351fc7abed6d4fdfa427d4b9b4e7ba2b2fe31646193a530fa79a164393daf

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
- cmoc の実行時共通基盤を扱う実装群。Codex CLI 実行、INDEX 更新 preflight、設定読み書き、content hash、git 操作、logging、path 解決、実行結果、session state、CLI サブコマンド共通ライフサイクルなど、複数の上位機能から使われる runtime helper を集める。
- 個別 helper の実装本文へ進むための入口であり、runtime 系 API の集約 import、互換 import、責務別 runtime module の所在を判断するための階層。

## Read this when
- Codex 実行、INDEX.md 自動更新、設定、git、path、logging、state、外部コマンド結果など、cmoc 全体で共有される runtime helper の実装場所を探したいとき。
- CLI サブコマンド共通の実行順序、エラー表示、ログ作成、work root 検査、完了サマリーなど、個別コマンドをまたぐ実行基盤を確認または変更したいとき。
- Codex exec/TUI の profile 作成、subprocess 起動、quota/capacity retry、Structured Output 検証、call log、preflight のいずれかに関わる挙動を追いたいとき。
- INDEX.md 更新処理の対象判定、hash 鮮度判定、既存エントリー再利用、エントリー生成依頼、並列更新、排他 lock を確認または変更したいとき。
- runtime helper を移動・分割・統合し、共有 import 入口や互換 import 入口の調整が必要なとき。

## Do not read this when
- 個別 CLI コマンドの引数定義、command 登録、利用者向け業務フローだけを調べたいときは、該当 command 実装へ進む。
- oracle file にある正本仕様断片、path model の概念定義、INDEX.md の仕様意図そのものを確認したいときは、対応する oracle 側の文書または実装を読む。
- 上位機能が runtime helper から得た値をどう使うか、session/report/apply などの業務状態をどう進めるかだけを知りたいときは、その上位処理の実装を読む。
- 生成済みログや保存済み state の利用者向け解析、または特定の出力 schema の利用者向け仕様だけを調べたいときは、その読み取り側や仕様側へ進む。

## hash
- a3c1ff07ee7ca18708e14e206db9c3fc65f61f27ad32de8416b92f4a06cf09f9

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
- CLI サブコマンド実装の上位入口。初期化、indexing、TUI、apply、review、session など、利用者が起動する操作を runtime や下位制御処理へ接続する実装群を扱う。
- 各サブコマンド領域は、実行前条件の確認、work root や session/apply state の扱い、git 操作、Codex 実行、report 出力などの大枠を担い、詳細な共通処理は runtime・git・config・state・builder など別領域へ委譲する。
- どのサブコマンド実装または下位 package へ進むべきかを、操作種別と責務境界から選ぶための判断起点として読む。

## Read this when
- CLI サブコマンドの実装を探しており、初期化、indexing、TUI、apply、review、session のどの領域へ進むべきかを選びたいとき。
- 利用者向けコマンドが CLI runtime、work root runtime、Codex exec/TUI、git 操作、state 更新、report 生成へどのようにつながるかを大枠で確認したいとき。
- apply run、review oracle、session lifecycle のように複数モジュールへ分かれたサブコマンド制御の入口を特定したいとき。
- サブコマンド実行前の preflight、clean worktree 要求、cmoc ignore 保証、branch/worktree 準備、後始末などがどのコマンド領域に属するかを切り分けたいとき。
- 特定サブコマンドの正本仕様ではなく、その仕様を具体化する realization implementation の配置と読む順序を判断したいとき。

## Do not read this when
- CLI 全体の Typer app 登録、トップレベル entrypoint、共通 runtime 規約だけを調べたいときは、それらを担う上位または runtime 側を読む。
- git command wrapper、config load、state 永続化、path 解決、ignore 判定、timestamp、report directory 解決など、サブコマンド固有ではない低レベル共通処理だけを確認したいとき。
- Codex exec/TUI の汎用起動機構、prompt builder、Structured Output parameter、LLM 呼び出し基盤だけを調べたいとき。
- サブコマンドの正本仕様や公開仕様そのものを確認したいときは、realization implementation ではなく対応する oracle file を読む。
- 実装ではなくテスト、fixture、生成済み report、または INDEX.md 文章品質だけを確認したいとき。

## hash
- c8e2c382df6ff1efe9104b0511fb735d284131d55505b1658d0e39aac35ba371
