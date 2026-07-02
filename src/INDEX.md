# `acp`

## Summary
- ACP builder 互換入口の上位領域。正本側にある実体を既存の公開参照経路から使えるようにし、旧来の参照名、委譲、公開型への適合、互換 wrapper の削除条件を切り分ける入口になる。
- この領域自体は builder の正本仕様や実処理本体を持つ場所ではなく、正本側実装を複製せずに移行期間中の公開 import 面を保つための薄い境界である。

## Read this when
- ACP builder 系の既存公開参照が、正本側実装や正本側 package 構造へどのように接続されているかを確認したいとき。
- agent call parameter 構築経路で、正本側 builder への委譲、realization 側公開型への変換、互換 wrapper、旧 import 経路の扱いを追いたいとき。
- apply fork、review、quota availability probe、session、TUI、indexing、common などの builder 種別ごとに、どの互換入口へ進むべきか判断したいとき。
- 公開面または realization 側に残る ACP builder 参照を、正本側参照へ移行できるか、互換入口を残す必要があるか判断したいとき。

## Do not read this when
- builder の prompt、parameter 生成内容、判定仕様、出力条件、人間意図などの正本仕様断片を確認したいときは、対応する oracle 側の本文を読む。
- apply fork コマンド全体、TUI の画面制御、review 機能全般、indexing の生成処理や探索処理など、builder 互換入口ではない実処理を調べたいときは、その責務を持つ実装へ直接進む。
- ACP parameter の基礎データ構造、model、reasoning effort、file access mode、path model、汎用 helper などの共通定義を確認したいときは、該当する基礎定義を読む。
- 新しい ACP 機能や API 仕様を追加する場所を探しているだけで、既存公開参照の互換維持や正本側実装への委譲判断に関係しないとき。

## hash
- 90d83fde69a289bed54e459713d6563eecd7e7ba7db46c94fc5c0fd10705d6fa

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
- cmoc の共有 runtime helper 群を置く実装ディレクトリ。Codex 呼び出し、INDEX 更新 preflight、CLI 共通ライフサイクル、設定、Git、ログ、path、エラー、結果、状態管理など、複数サブコマンドから使われる共通処理への入口になる。
- 単一の集約 import 入口と、責務別の runtime_* 実装に分かれており、個別挙動を調べる場合は対象領域の実装へ進むための分岐点になる。

## Read this when
- 複数の CLI サブコマンドや上位機能から共有される runtime 処理の所在を探したいとき。
- Codex exec/TUI 呼び出し、INDEX.md 自動更新、config 読み書き、Git 操作、logging、path 解決、state 永続化など、共通 runtime 境界に関わる変更対象を選びたいとき。
- 集約 import 入口を使うべきか、責務別 runtime 実装を直接読むべきか判断したいとき。

## Do not read this when
- 個別サブコマンドの利用者向け挙動、引数、業務処理だけを調べたいとき。その場合は command 側の実装へ進む。
- oracle 上の正本仕様、path model、INDEX.md 仕様意図、file access rule の根拠を確認したいとき。その場合は対応する oracle doc または oracle src を読む。
- 生成済みログ、実行履歴、状態ファイルの内容確認が目的で、runtime 実装自体を変更しないとき。

## hash
- 46c7cefb5df49ca98d035a9c75958fdfcc83907fdad44b62fb0d695bef69d98b

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
- CLI サブコマンドの実行本体を集める実装領域。session、apply、review、init、indexing、tui など、利用者向けコマンドを runtime・git 操作・状態管理・report 出力へ接続する入口になる。
- 各サブコマンドの詳細は責務ごとに下位へ分かれており、この階層はコマンド種別ごとの読む先を選び、実行前条件、状態遷移、後始末、共通処理への委譲位置を切り分けるための起点である。

## Read this when
- 利用者向けサブコマンドの実行フロー、事前条件、git 操作、状態更新、cleanup、report 出力の入口を探したいとき。
- session や apply の branch・worktree・state の扱い、review の対象列挙から report までの制御、init/indexing/tui の orchestration をどこで読むべきか判断したいとき。
- サブコマンド固有の処理と、runtime helper、git wrapper、設定、path model、parameter builder などの共通処理との境界を確認したいとき。
- INDEX.md maintenance、review 用 INDEX 変更、apply/report、TUI 起動 parameter など、利用者コマンドから下位処理へ入る接続点を追いたいとき。

## Do not read this when
- Typer への登録やトップレベル CLI 配線だけを確認したいときは、CLI entrypoint 側を直接読む。
- git コマンド wrapper、state 永続化、root 解決、設定読み込み、clean worktree 判定、cmoc ignore 判定など、サブコマンドに限らない共通 helper の詳細だけを調べたいとき。
- Codex に渡す prompt や Structured Output parameter の具体的な組み立てだけを確認したいときは、対応する parameter builder 側を読む。
- oracle 上の正本仕様そのもの、または INDEX.md エントリー作成基準そのものを確認したいときは、実装ではなく対応する oracle file を読む。

## hash
- f2292c7b233a95637741eaeda01d5b6966abbe41de2cbbd8d33c3564f75456cf
