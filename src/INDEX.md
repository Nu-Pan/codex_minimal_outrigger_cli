# `acp`

## Summary
- realization 側の ACP 公開入口をまとめる階層。旧来の `acp.*` import 互換を維持する薄い入口と、ACP builder 領域へ進むための下位入口を扱う。
- 実装本体や正本仕様をこの階層に複製せず、oracle 側または下位 builder 領域へ委譲する境界を示すための場所。

## Read this when
- realization 側に残る ACP 関連の公開 import path や互換入口の所在を確認したいとき。
- 既存の `acp.*` 参照を維持する理由、移行時の扱い、削除条件を判断したいとき。
- ACP builder に関する realization 側入口から、apply・review・session・TUI・indexing などの下位領域へ進むべきか切り分けたいとき。

## Do not read this when
- ACP builder の prompt 本文、出力 schema、モデル選択、file access mode などの正本仕様を確認したいとき。対応する oracle 側の仕様や実装へ直接進む。
- apply・review・session・TUI・indexing の具体的な処理ロジックや入出力仕様をすでに特定しているとき。該当する下位領域または正本側実装を読む。
- CLI 全体の制御フロー、git 操作、画面描画、状態管理、共通型など ACP 公開互換入口以外の挙動を調べたいとき。

## hash
- dcd7d5111374b4a2d587b83c9cc3a8e21db76e440dfb93db28c472f9064726f8

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
- cmoc の realization implementation のうち、複数の CLI サブコマンドや上位処理から共有される runtime helper 群をまとめる領域。Codex 呼び出し、設定、内容 hash、CLI 実行ライフサイクル、エラー表示、git 操作、ログ、path、結果型、session state、索引更新 preflight など、横断的な実行時基盤への入口になる。
- 個別実装は責務ごとに分割されており、公開 import 面を集約する薄い facade、Codex exec/TUI 起動境界、profile/sandbox 境界、永続状態やログの読み書き、外部コマンド結果の共通モデルなどを必要に応じて選んで読むための階層である。

## Read this when
- CLI サブコマンド実装から共通 runtime 機能を使うための依存先や、複数領域にまたがる公開 helper の所在を確認したいとき。
- Codex CLI 呼び出しの実行制御、profile・sandbox・CODEX_HOME・Structured Output・quota/capacity retry・call log・TUI 起動などの runtime 境界を調査または変更したいとき。
- 設定ファイル、内容 hash、binary 判定、path 解決、timestamp、ログ、結果型、共通エラー表示、git repository 操作、session state 永続化など、サブコマンド横断の補助処理を探しているとき。
- Codex 実行前の索引更新 preflight、INDEX.md entry の鮮度判定、生成依頼、保存、関連 commit 作成といった indexing 実装の流れを追いたいとき。
- 新しい共有 helper を追加する前に、既存の共通 runtime 層に同じ責務または近い責務の実装があるか確認したいとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、利用者向け出力、状態遷移 workflow そのものを調べたいとき。その場合は該当するサブコマンド側の実装へ進む。
- path model、oracle file、realization file、INDEX.md 形式、CLI 仕様などの正本仕様断片を確認したいだけのとき。その場合は oracle 側の本文を読む。
- テスト期待値や fixture の具体内容を確認したいとき。その場合は realization test 側へ進む。
- 特定の runtime helper の詳細挙動がすでに分かっているときは、この階層全体ではなく対応する責務の本文を直接読む。
- 生成済みログ、状態ファイル、schema store、作業 tree 内の成果物そのものを調べたいだけのとき。ここはそれらの配置や読み書きに関わる実装入口であり、実データの閲覧先ではない。

## hash
- 21977af6089144637d2ffbcf2dfa10bfa80fc9aa5e697d39771c95ea7464fc25

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
- cmoc の各 CLI sub command の realization implementation を集約する領域で、操作別の実行入口と orchestration を扱う。
- session lifecycle、apply lifecycle、review oracle、INDEX maintenance 起動、初期化処理、TUI 起動など、CLI runtime から呼ばれる処理を個別実装へ振り分ける入口になる。
- サブコマンド横断の共通基盤そのものではなく、各操作固有の preflight、branch/worktree 操作、state 更新、Codex 実行、report/CLI 出力、cleanup へ進むためのルーティング起点として読む。

## Read this when
- cmoc のサブコマンド実行フローを調べ始め、どの操作別実装へ進むべきかを選びたいとき。
- CLI runtime から各サブコマンド固有処理へ渡す command 名、argv、preflight、runtime root、Codex 実行 callback、利用者向け出力の入口を探したいとき。
- branch/worktree 操作、state file 更新、clean worktree 要求、cmoc ignore 保証、report 生成、cleanup などが、どのサブコマンド実装に属するかを切り分けたいとき。
- 個別操作の詳細に入る前に、session lifecycle、apply lifecycle、review oracle orchestration、INDEX maintenance 起動、初期化処理、TUI 起動の実装上の境界を確認したいとき。

## Do not read this when
- CLI アプリ全体の登録、top-level entrypoint、共通 runtime、git wrapper、path model、設定 load、state model の詳細だけを調べたいときは、それぞれの共通実装を読む。
- サブコマンドの正本仕様や利用者向け要求そのものを確認したいときは、実装ではなく対応する oracle doc を読む。
- 対象のサブコマンドや操作が既に特定できており、実行入口ではなく fork、join、abandon、review loop、report、target 列挙、INDEX merge などの詳細だけを調べたいときは、該当する下位実装を直接読む。
- INDEX.md の文章生成、差分検出、lock、commit など indexing 共通処理の内部ロジックや、Codex prompt builder の具体的な文面・schema だけを調べたいときは、この階層ではなく各専用実装を読む。

## hash
- bbc200198445b2051ddadbc421a873bcb24ba37991fb50e3c208657f56946d86
