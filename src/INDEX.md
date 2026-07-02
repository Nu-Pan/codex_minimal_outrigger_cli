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
- cmoc の共通ランタイム支援を集めた実装領域。Codex 呼び出し、INDEX 更新 preflight、CLI 共通ライフサイクル、設定、内容 hash、エラー表示、Git、ログ、path、結果モデル、session/apply 状態、apply process 停止など、複数サブコマンドから使われる runtime_* 系 API を扱う。
- 単一 API の実装だけでなく、共通 runtime API の再エクスポート入口や互換 import 入口も含み、個別 command 層から共有される低レベル制御の入口になる。

## Read this when
- 複数サブコマンドにまたがる runtime helper、Codex CLI 実行、INDEX.md 自動更新、Git/worktree 操作、ログ、設定、状態管理、path 解決、共通エラー表示の実装箇所を探したいとき。
- CLI command 層から呼ばれる共通実行ライフサイクル、外部 command/Codex 実行結果の受け渡し、quota/capacity/retry、file access rule 違反検出などの共通制御を確認または変更したいとき。
- 個別 runtime_* モジュールへ進む前に、commons runtime 領域の責務分担や、集約 import 入口と責務別実装のどちらを読むべきかを判断したいとき。

## Do not read this when
- 特定の CLI サブコマンド固有の引数、利用者向け制御フロー、prompt 生成、report 内容だけを調べたいとき。その場合は command 側や対象サブコマンドの実装へ進む。
- oracle file 上の正本仕様、path placeholder の定義、file access policy の仕様意図、INDEX.md エントリー標準そのものを確認したいとき。その場合は oracle 側の該当文書を読む。
- 生成済みログ、実行履歴、memo、または個別の状態ファイル内容を調査したいだけで、runtime 実装自体を変更しないとき。

## hash
- 78dcdaebd36c11e4d5a5f0697c114735732269d72588b2806ec7ac04e132734e

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
- CLI の各サブコマンド実行本体を集める実装領域。session、apply、review、init、indexing、tui など、利用者向けコマンドを共通 runtime や下位 helper へ接続する orchestration 層への入口になる。
- 各領域は、コマンドごとの事前条件、root/config 解決、git・worktree・state 操作、Codex 呼び出し、report や stdout 出力までの大きな制御順序を扱い、詳細な共通処理は runtime や専用 helper へ委譲する。
- サブコマンド単位で読む先を選ぶ分岐点であり、特定コマンドの外部挙動や実行フローを確認するときは該当する下位要素へ進む。

## Read this when
- どのサブコマンド実装が特定の CLI 挙動、状態遷移、git 操作、Codex 呼び出し、report 出力を担当しているかを切り分けたいとき。
- session の作成・合流・破棄、apply run の開始・統合・破棄、review oracle の実行、初期化、INDEX maintenance、TUI 起動などの実行入口を探したいとき。
- サブコマンドが共通 runtime、preflight、root/config 解決、worktree/state/helper 群へどのようにつながるかを追いたいとき。
- CLI から起動された後の command name、argv、事前検査、成功・失敗時出力、cleanup の大枠を確認・変更したいとき。

## Do not read this when
- CLI parser、トップレベルのサブコマンド登録、Typer app 配線だけを確認したいときは、CLI entrypoint や routing 側を読む。
- git 実行 wrapper、path model、state model、config、runtime、lock、ignore 判定などの低レベル共通 helper 自体を変更したいときは、該当する共通実装を直接読む。
- oracle file と realization file の定義、path token、managed branch、各コマンドの正本仕様などを確認したいときは、実装ではなく oracle 側の該当文書を読む。
- INDEX.md 本文生成、review finding 生成、prompt builder、report rendering、merge conflict 解決など、サブコマンド配下のさらに専用化された詳細だけを調べたいときは、その責務を持つ下位要素へ直接進む。

## hash
- aa475b5b45bf3169cc3cf2a86894f27614f758f7f9c74b57cd3734be150f15f3
