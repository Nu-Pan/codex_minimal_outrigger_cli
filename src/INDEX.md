# `acp`

## Summary
- ACP builder 関連の realization 側入口。正本側実装を複製せず既存の acp 系 import 参照を保つための互換層と、quota availability probe 用 parameter builder への入口を扱う。
- この対象自体は実装本体ではなく、旧来 import 経路の維持理由、削除条件、下位 builder 領域への振り分けを確認するための場所である。

## Read this when
- acp 系 import surface と正本側 builder 実装の対応関係を確認したいとき。
- 既存の acp または acp.builder 系参照を残す理由、互換入口の削除条件、移行判断を確認したいとき。
- apply、review、session、TUI、indexing、common など ACP builder 関連の下位領域へ進む前に入口を選びたいとき。
- Codex quota availability probe に渡す最小限の AgentCallParameter 生成内容を確認または変更したいとき。

## Do not read this when
- ACP builder の正本仕様断片、prompt 正本文面、出力条件、判定仕様そのものを確認したいときは、対応する oracle 側の本文を読む。
- apply fork、review oracle、session join、TUI 起動 parameter、indexing 生成処理などの具体的な実装本体を調べたいときは、該当する下位領域または正本側実装を読む。
- AgentCallParameter 型、model、reasoning effort、file access mode などの基礎定義を確認したいときは、基礎定義側を読む。
- Codex CLI の実行規則、quota probe parameter 生成後の runtime 処理、CLI コマンド全体の制御フローを調べたいときは、実行側またはコマンド実装側を読む。
- 互換 import 経路の維持や削除判断と関係しない新規機能、画面制御、状態管理、ユーザー向け挙動を探しているときは、より直接その責務を持つ対象へ進む。

## hash
- 79093e544721f088a1f881c40244ac903a6259bce6431129e8174e574d58cc60

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
- cmoc の共通 runtime 支援を担う実装群。Codex 呼び出し、INDEX 更新 preflight、CLI 共通ライフサイクル、設定、内容 hash、エラー表示、Git 操作、ログ、パス解決、実行結果モデル、session state 永続化など、複数サブコマンドから共有される基盤処理への入口になる。
- 個別の runtime helper は責務別に分かれており、公開 import の互換入口や複数 runtime API の集約入口もこの階層に含まれる。

## Read this when
- 複数サブコマンドから共有される実行時処理、Codex 実行制御、INDEX 自動更新、Git・path・config・state・logging・error などの共通基盤を確認または変更したいとき。
- Codex exec/TUI の起動環境、retry、quota/capacity、Structured Output 検証、call log、file access rule 違反検出など、Codex subprocess 境界の実装を追いたいとき。
- CLI サブコマンド共通の開始・完了表示、終了コード化、例外表示、サブコマンド log、current logger の扱いを確認したいとき。
- INDEX.md の生成・更新 preflight、対象探索、hash 鮮度判定、既存エントリー再利用、並列生成、排他制御を調べたいとき。
- 設定 JSON、内容 hash 保存、binary 判定、Git worktree・branch・ignore 判定、runtime path、結果データ構造、session state 永続化などの共通 helper を探すとき。

## Do not read this when
- 個別 CLI サブコマンドの利用者向け仕様、引数定義、コマンド固有の状態遷移や業務処理だけを調べたいとき。その場合はサブコマンド側の実装を読む。
- oracle file にある正本仕様断片、path model、file access rule、INDEX.md 仕様意図、prompt 文面そのものを確認したいとき。その場合は対応する oracle 側を読む。
- 特定の共通 helper の低レベル実装だけを変更したいことが明確なときは、この階層全体ではなく責務に対応する個別 runtime 実装へ直接進む。
- 生成済み log の解析、利用者向け通常出力の高レベル仕様、JSON schema の正本、または外部から見えるコマンド単位の挙動だけを確認したいとき。

## hash
- 0ccb25f474d928415cea020075957e077077be0e88ee5427811eb575a58814e1

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
- CLI サブコマンド実装を集約する領域で、初期化、index maintenance、TUI 起動、session lifecycle、apply run、review oracle の各実行入口へ進むためのルーティング対象。
- 各サブコマンドは共通 runtime に接続し、事前条件検証、git/worktree/state 操作、Codex 実行連携、成功時出力や report 生成など、利用者向け CLI 挙動の具体化を担う。

## Read this when
- どのサブコマンド実装へ進むべきかを、初期化、index 更新、TUI、session 操作、apply 操作、review oracle の観点で切り分けたいとき。
- CLI サブコマンドの実行フロー、preflight、runtime への渡し方、git branch/worktree/state 操作、出力や report 生成に関係する変更を行うとき。
- apply run、session lifecycle、review oracle、INDEX.md maintenance、初期化時 ignore 保証、TUI 起動 parameter 解決の入口を探すとき。

## Do not read this when
- CLI 全体の登録、共通 runtime、git wrapper、path model、設定読み込み、state file の低レベル読み書きだけを調べたいときは、それぞれの共通基盤を直接読む。
- oracle file の正本仕様、INDEX.md 文章生成ロジック、Codex prompt builder、LLM 呼び出し自体の詳細を確認したいときは、対応する oracle または builder/runtime 側を読む。
- 対象サブコマンドや補助責務がすでに特定できている場合は、この階層ではなく該当する下位対象へ直接進む。

## hash
- 821d5c9c432b6b29d7c13ed2e092cd299ac2aa54c1fc0a15615667ba8a9f66da
