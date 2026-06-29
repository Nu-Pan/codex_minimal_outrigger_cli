# `acp`

## Summary
- oracle src 側の acp builder 実装を複製せず、既存の `acp.*` import surface を維持するための realization 側互換入口。
- 配下には、移行期間中の公開 import 面だけを保つ入口と、agent call parameter builder 群へ進む package があり、実体や正本仕様は主に別 module または正本側へ委譲される。
- apply・review・session・indexing・TUI・quota availability probe などの builder 領域へ進む前に、互換境界と下位領域の選択を確認するための入口となる。

## Read this when
- `acp.*` import surface が realization 側または利用者向け公開面に残っている理由、削除条件、移行先を確認したいとき。
- agent call parameter builder の実装側 package 構造、正本側 builder への委譲関係、下位 builder 領域への進み先を見分けたいとき。
- oracle src 由来の acp builder を既存参照経路から利用するための互換再公開、placeholder 補正、runtime schema 差し替えの境界を確認したいとき。
- Codex quota availability probe の parameter builder が通常設定から引き継ぐ内容や固定入力を確認・変更したいとき。

## Do not read this when
- acp builder の正本 prompt、schema、出力条件、具体的な値の組み立て仕様を確認したいときは、対応する正本側実装または正本仕様断片を読む。
- apply fork、review、session、indexing、TUI の制御フローや実処理を調べたいときは、この互換入口ではなく各処理本体や下位の実体を持つ実装を読む。
- 新しい acp 機能や API 仕様を追加する場所を探しているときは、この互換維持用の入口ではなく、正本側または実体 module 側の対象を確認する。
- `acp.*` 参照が全公開面と realization 側から消えていることだけを確認済みで、互換入口や削除条件を読む必要がないとき。

## hash
- d567cda67606f83351eafaa565eff81da0c4a980e7583ac6f351be5d170fb6c6

# `basic`

## Summary
- oracle 側 basic 領域の正本実装・型・path model・構造化文書 API を、realization 側の既存公開参照として再公開する互換層を収める。
- ACP 基本型、path placeholder と解決関数、構造化文書 API などを realization 側へ複製せず、既存の `basic.*` import 経路を正本側実体へつなぐ入口として機能する。
- 削除可否は、realization 側と利用者向け公開面から該当する `basic.*` 参照がなくなり、正本側または実体 module への移行が済んでいるかで判断する。

## Read this when
- `basic.*` 経由の既存 import 互換性、公開参照、再公開対象を確認・変更・削除したいとき。
- oracle 側 basic 実装や型を realization 側へ複製せず参照している経路を確認したいとき。
- ACP 関連型、path model API、構造化文書 API の realization 側公開面と正本側実体のつながりを調べたいとき。
- 互換再公開層を残す理由、または削除できる条件を確認したいとき。

## Do not read this when
- ACP 型、path placeholder、path 解決処理、構造化文書処理そのものの正本仕様や実装詳細を確認したいとき。その場合は oracle 側の実体を直接読む。
- agent call parameter の組み立て、CLI 挙動、一般的な path model、テスト挙動など、`basic.*` 再公開互換性に関係しない処理を調べたいとき。
- 新しい正本仕様や型を追加・変更したいとき。その場合は互換再公開層ではなく oracle 側の正本仕様を確認する。

## hash
- 09e7f8600198d28f0638e0443ea9152e2192dcc03ee1e92a8b8efef5cf43c3b9

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
- cmoc の実行時共通 helper 群をまとめる領域。Codex CLI 呼び出し、INDEX 更新 preflight、CLI サブコマンド共通ライフサイクル、設定、content hash、error、git、logging、path、result、session state など、複数の上位機能から使われる runtime 境界を扱う。
- この階層には、個別 helper の実装に加えて、runtime helper 群を横断して import するための集約入口や、旧 import path を維持する互換入口も含まれる。

## Read this when
- Codex 実行、INDEX 自動更新、CLI 共通実行、git 操作、設定読み書き、path 解決、ログ、結果モデル、session state など、cmoc の複数機能から共有される runtime 処理を探すとき。
- 個別サブコマンドではなく、サブコマンド横断の進捗表示、終了コード化、例外表示、ログ作成、現在 logger 管理などの共通実行ライフサイクルを確認または変更したいとき。
- Codex CLI の exec/TUI 起動、profile や CODEX_HOME、Structured Output schema、quota/capacity retry、call log、preflight との接続など、Codex subprocess 境界の実装を追うとき。
- INDEX.md の自動最新化、対象走査、hash 鮮度判定、既存エントリー再利用、Structured Output 検証、更新順序や排他制御を扱うとき。
- runtime helper の移動・分割・統合により、共有 import 入口や互換 import 入口の公開面を調整する必要があるとき。

## Do not read this when
- 個別 CLI サブコマンドの引数定義、利用者向け操作フロー、出力 schema、固有の業務処理だけを調べたいとき。その場合は command 側の実装へ進む。
- path placeholder の抽象仕様、oracle 上の正本要求、INDEX.md エントリー標準、session state の仕様意図など、正本仕様断片そのものを確認したいとき。その場合は対応する oracle 側を読む。
- 設定モデル、AgentCallParameter、CmocConfig などのデータモデル定義そのものだけを確認したいときは、モデル定義側へ直接進む。
- 生成済みログの解析、レポート表示、状態値の利用先など、runtime helper が取得・保存した値を上位機能がどう使うかを調べたいときは、その上位機能の実装を読む。
- 特定の低レベル処理だけを調べる場合は、この階層全体ではなく、git、path、config、content、logging、Codex profile など責務に対応する個別 runtime 実装へ進む。

## hash
- 1630161fc6d1ddeaefbd396ba1338ed1a51c5a9ac30ee759b0c30d74b330cf6e

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
- CLI のサブコマンド実装を領域別に収める入口。apply、indexing、init、review、session、tui などの実行本体へ進むための責務境界を示す。
- 各サブコマンド領域は、CLI runtime への接続、preflight、git/worktree/state 操作、Codex 実行連携、report や利用者向け出力など、サブコマンド固有の orchestration を扱う。
- サブコマンド単位で読む先を選ぶための階層であり、共通 runtime、低レベル git helper、設定・状態モデル、oracle 側の正本仕様そのものではなく、realization implementation の入口として読む。

## Read this when
- cmoc のサブコマンド実装のうち、apply、indexing、init、review、session、tui のどの領域へ進むべきかを選びたいとき。
- CLI runtime 経由の起動、preflight、安全条件確認、git branch/worktree 操作、state 更新、Codex subprocess 連携、report 出力など、サブコマンド固有の制御境界を切り分けたいとき。
- apply run、review oracle、session lifecycle、初期化、INDEX.md maintenance、TUI 起動など、利用者が呼び出す操作の実装入口を探したいとき。
- 複数のサブコマンドにまたがる変更で、どの実装領域が直接関係するかを比較して読む先を絞りたいとき。

## Do not read this when
- CLI 共通 runtime、git wrapper、config load、state 永続化、path 解決、Codex exec/TUI 起動基盤など、サブコマンド固有ではない低レベル共通処理だけを調べたいとき。
- サブコマンドの正本仕様や公開仕様そのものを確認したいとき。この対象は realization implementation の入口であり、仕様根拠としては oracle 側を読む。
- INDEX.md 生成内容、review finding 品質、report 本文、prompt parameter schema など、下位の専用実装や builder が直接担う詳細だけを確認したいとき。
- Typer app へのトップレベル登録や CLI 全体の entrypoint だけを確認したいとき。
- テスト、fixture、生成済みレポート、または oracle file の列挙条件など、サブコマンド実行本体ではない対象を探しているとき。

## hash
- b14629844a1ca0d90a0ed02abdb0ead77518474a090a6a6708efd047801cc185
