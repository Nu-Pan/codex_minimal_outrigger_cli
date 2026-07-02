# `acp`

## Summary
- ACP 関連の realization 側公開入口。正本側実装を複製せずに既存の `acp.*` import 経路を維持する互換層と、builder 関連の委譲境界・probe parameter 生成領域への入口を担う。
- ACP builder 作業で、正本側へ進むべきか、互換 import 維持を確認すべきか、quota availability probe 用 parameter 生成を確認すべきかを切り分ける階層。

## Read this when
- `acp.*` import 参照を維持する互換入口の残置理由、削除条件、公開面での扱いを確認したいとき。
- ACP builder の realization 側入口、正本側 builder への委譲、旧 import 経路との対応を確認したいとき。
- apply、review、session、TUI、indexing、file access recovery などの builder 関連作業で、下位領域のどこへ進むべきかを選びたいとき。
- Codex quota availability probe 用に既存 parameter から動作確認用 parameter を組み立てる処理を確認または変更したいとき。

## Do not read this when
- ACP builder の正本仕様、prompt 正本文面、出力条件、判定仕様そのものを確認したいときは、対応する oracle file または正本側実装を読む。
- apply fork の制御フロー、branch 操作、diff 生成、CLI 引数処理、TUI の描画やイベント処理など、builder 入口ではない実行処理を調べたいとき。
- AgentCallParameter、FileAccessMode、model、reasoning effort などの基礎データ構造を調べたいときは、基礎定義側を読む。
- 互換 import 経路や quota probe parameter 生成に関係しない新規機能の実装場所やテスト対象を探しているとき。

## hash
- 248a388b2bb432024fda8f641ba769be61d6b5a7ebfdc16b34ec63f0a8a01d2e

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
- cmoc の共通 runtime helper 群を集める実装領域。Codex 実行、CLI 共通処理、設定、Git、ログ、パス、状態、INDEX.md 更新など、複数サブコマンドから使われる横断的な処理への入口になる。
- 集約 import 入口と責務別 runtime 実装が同階層に並び、個別挙動を調べる場合は該当する runtime_* 実装へ進むための階層である。

## Read this when
- 複数の CLI サブコマンドや agent call 実行経路から共有される runtime 処理の所在を探したいとき。
- Codex exec/TUI 起動、profile、preflight、call log、Structured Output、quota/capacity retry、file access rule 違反検出など Codex 呼び出し周辺の共通実装を確認したいとき。
- CLI 共通ライフサイクル、利用者向けエラー表示、Git 操作、設定ファイル、runtime path、ログ、結果モデル、session state などの共通処理を変更する対象を選びたいとき。
- INDEX.md 自動更新の preflight、対象走査、既存エントリー再利用、hash 鮮度判定、Codex へのエントリー生成依頼を扱う実装へ進みたいとき。

## Do not read this when
- 個別サブコマンドの引数定義、利用者向け制御フロー、サブコマンド固有の状態更新だけを調べたいとき。その場合はサブコマンド実装側へ進む。
- oracle file にある正本仕様、path model、file access rule、INDEX.md エントリー標準などの仕様意図を確認したいとき。その場合は対応する oracle doc または oracle src を読む。
- 共通 runtime helper を使う側の業務ロジックだけを変更したいとき。呼び出し元の実装を先に読み、共通挙動を変える必要がある場合だけこの階層へ進む。
- 生成済みログ、状態ファイル、設定ファイルなどの実データを調査したいだけのとき。この階層はそれらを読み書きする実装を扱う。

## hash
- 75c4be2394933baceda860ab1abe2e509d4027c1552cedf502b3c2c5775c34be

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
- CLI サブコマンド実装を集約する領域で、init、indexing、tui、apply、session、review 系の実行入口とサブコマンド別 orchestration へ進むための入口になる。
- 各対象は CLI runtime 経由の起動、preflight、git 操作、state 更新、Codex subprocess 連携、レポート生成など、利用者向けコマンドの具体的な実行制御を扱う。
- 共通 runtime や低レベル helper そのものではなく、個別サブコマンドがそれらをどう組み合わせて外部挙動を作るかを確認するために読む。

## Read this when
- 特定の CLI サブコマンドの実行順序、preflight、引数受け渡し、利用者向け出力、失敗時処理を確認・変更したいとき。
- init、indexing、tui、apply、session、review のどの実装領域へ進むべきかを選びたいとき。
- apply run、session lifecycle、review oracle、INDEX.md maintenance、初期化、TUI 起動など、サブコマンド単位の制御フローを追いたいとき。
- サブコマンドが git 操作、worktree/branch 管理、state file、Codex Exec/TUI、report 出力、indexing 共通処理へどこから依存しているかを確認したいとき。

## Do not read this when
- CLI 共通 runtime、git wrapper、path model、state file schema、設定読み込み、ignore 判定などの低レベル共通処理だけを調べたいときは、それぞれの共通実装を読む。
- oracle file の正本仕様断片、サブコマンドの外部仕様、prompt builder、LLM 呼び出し詳細だけを確認したいときは、対応する oracle または builder/runtime 側を読む。
- 読むべきサブコマンドや補助モジュールがすでに決まっている場合は、この階層ではなく該当する下位対象へ直接進む。

## hash
- 8ea1d673dd2276b559bbaf9325a03a85ab7e7b0830606e348dc404f6fd1a62e2
