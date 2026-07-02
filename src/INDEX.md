# `acp`

## Summary
- ACP builder 関連の旧 import 経路を維持するための realization 側互換入口を置く階層。実体を複製せず、正本側実装や下位 wrapper へ接続する役割を担う。
- apply、review、session、TUI、indexing、quota probe などの builder 領域について、公開参照経路の維持、正本側への委譲、realization 側型への適合、互換コードの削除条件を確認する入口となる。

## Read this when
- ACP builder 関連の `acp.*` import や旧公開 import path が、正本側実装または下位互換 wrapper にどう接続されているか確認したいとき。
- agent call parameter builder の変更で、apply、review、session、TUI、indexing、quota probe などのどの下位領域へ進むべきか判断したいとき。
- oracle src 側へ実体を集約しつつ realization 側に残る互換 package、薄い wrapper、再公開境界の残置理由や削除条件を確認したいとき。
- 正本 builder の出力を realization 側の parameter 型や既存公開面へ適合させる経路を探しているとき。

## Do not read this when
- 個別 builder の正本仕様、prompt、出力条件、具体的な生成ロジックを確認したいときは、対応する oracle 側本文または実装へ進む。
- CLI コマンド全体の制御フロー、fork 作成、branch 操作、diff 生成、画面制御、状態管理など、builder 互換入口以外の処理を調べたいときは、それぞれの実装領域へ進む。
- agent call parameter の共通データ構造、model、reasoning effort、file access mode などの基礎定義だけを調べたいときは、基礎定義側へ進む。
- 新しい acp 機能や API 仕様の追加場所を探しており、旧 import path の維持や正本側 builder への委譲と関係しないとき。
- `acp.*` 参照が全公開面と realization 側から消えていることだけを確認済みで、互換入口の詳細を読む必要がないとき。

## hash
- fc2286cbc273ce54d85c75025fcdc905b01d360d989032802c1f1abaeafec5f6

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
- cmoc の共通実行時支援を集める implementation directory。Codex 呼び出し、CLI 共通ライフサイクル、設定、Git、ログ、パス、状態、INDEX 更新など、複数サブコマンドから共有される runtime helper と集約 import 入口を収める。
- 低レベル helper の実装本文と、互換 import・再 export 用の薄い入口が混在するため、個別挙動を追う場合は対象領域の runtime_* 実装へ進むための入口になる。

## Read this when
- CLI サブコマンド間で共有される runtime helper の所在を探したいとき。
- Codex exec/TUI、preflight、profile、logging など Codex CLI 呼び出し周辺の共通実装を調べたいとき。
- work root 検査、設定 JSON、Git 操作、runtime path、subcommand log、session state、外部コマンド結果、共通エラー表示などの横断的な runtime 処理を確認または変更したいとき。
- INDEX.md 自動更新の preflight、対象走査、hash 判定、エントリー生成、Markdown 描画までの indexing 実行経路を調べたいとき。
- 複数の runtime API をまとめて import する公開入口や、旧 import path を維持する互換入口の責務境界を確認したいとき。

## Do not read this when
- 個別 CLI サブコマンドの引数定義、利用者向け制御フロー、業務処理だけを調べたいとき。その場合は command 実装側を読む。
- oracle 上の正本仕様、path placeholder の概念定義、file access policy、INDEX.md の仕様意図そのものを確認したいとき。その場合は対応する oracle doc または oracle src を読む。
- 特定の helper 関数や型の詳細が既に分かっているとき。その場合は集約入口ではなく、責務を持つ個別 runtime 実装を直接読む。
- 生成済み log や state を利用者視点で読むだけで、runtime の生成・検証・永続化処理を変更しないとき。

## hash
- 32e0e203bab7cab9b7544192274460f194a8a4fc4b6b761f5ace65e585820b02

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
- cmoc のサブコマンド実装を集約するディレクトリ。初期化、indexing、TUI、apply、session、review など、CLI runtime 経由で起動される各コマンドの実行入口と実行制御へ進むための上位ルーティングを担う。
- 各サブコマンドの責務は下位ファイル・ディレクトリに分かれており、ここは目的のコマンド実装、状態遷移、git 操作、report 出力、runtime helper への入口を選ぶために読む。

## Read this when
- cmoc のサブコマンド実装から、対象コマンドに対応するファイルや下位ディレクトリを選びたいとき。
- init、indexing、tui、apply、session、review の実行フロー、preflight、CLI runtime への接続、git 状態操作、成功時出力や report 生成の入口を切り分けたいとき。
- apply run、session lifecycle、review oracle、INDEX.md maintenance、TUI 起動、初期化処理のどの実装へ進むべきか判断したいとき。
- サブコマンド固有の cleanup、branch・worktree・state・process・report の扱いがどの責務に属するかを俯瞰したいとき。

## Do not read this when
- CLI 全体の Typer app 登録、共通 runtime、git command wrapper、path model、設定モデル、state 永続化など、個別サブコマンドではない共通基盤を直接調べたいとき。
- oracle 側の正本仕様断片、INDEX.md エントリー作成基準、またはサブコマンド外部仕様だけを確認したいとき。
- Codex に渡す prompt や Structured Output parameter の詳細、INDEX.md 生成ロジック、report rendering など、下位の専用 builder や共通処理を直接読む方が適切な詳細だけを調べたいとき。
- テスト、fixture、パッケージ外の補助ファイル、またはサブコマンド以外の実装領域を探しているとき。

## hash
- b4ce8066f3e2528489ff8ff90df1a0fd92e0b2d9037aab6b01af9e2cba4ab45e
