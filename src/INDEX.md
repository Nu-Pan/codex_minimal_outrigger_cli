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
- cmoc の実行時処理で共通利用される helper 群を集めた実装ディレクトリ。Codex 呼び出し、preflight indexing、CLI 実行ライフサイクル、設定、content hash、error、git、logging、path、result、session state など、複数の上位コマンドから参照される runtime 境界を扱う。
- 個別 module は責務別に分割されており、集約 import 用の入口、互換 import 用の入口、実処理を持つ runtime module、索引更新処理の中心実装が同階層に並ぶ。

## Read this when
- 上位コマンドや他ディレクトリの実装から、cmoc 共通 runtime helper の入口や責務別 module を探したいとき。
- Codex exec/TUI 呼び出し、Codex profile、quota/capacity retry、Structured Output、preflight indexing、call log など Codex 実行周辺の共通制御を確認・変更したいとき。
- CLI サブコマンド共通の開始・終了処理、終了コード化、利用者向けエラー表示、サブコマンドログ記録の挙動を確認・変更したいとき。
- 設定ファイル、内容 hash 保存、binary 判定、git subprocess/worktree 操作、runtime path、ログ、結果型、session state 永続化など、複数機能にまたがる共有 runtime 処理を調べたいとき。
- INDEX.md 生成 preflight、索引 entry の鮮度判定、Codex への entry 生成依頼、Markdown entry 描画など、索引更新の実装側フローを追いたいとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、画面出力、状態遷移全体を確認したいだけのときは、呼び出し側の command 実装へ進む。
- oracle file に書かれた正本仕様、path keyword の概念定義、INDEX.md の意味仕様、session state の仕様意図などを確認したいときは、oracle 側の本文へ進む。
- 実行時 helper を呼び出すだけで、共通処理の挙動や契約を変更しないときは、利用箇所の実装から必要な公開名だけ確認する。
- 生成済みログ、実行レポート、永続状態ファイルの実データを調査したいときは、この runtime 実装ではなく対象の保存先や読み取り側へ進む。
- テスト期待値や fixture の調整が主目的で、runtime helper の契約変更を伴わないときは、対応する test 側を先に読む。

## hash
- 4084d537449bdfd10eb7ff1e6e950c7dd160084ef77daca29266eb4c74a44832

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
- cmoc のサブコマンド実装を集約する領域で、初期化、INDEX maintenance、TUI 起動、session 操作、apply 操作、review oracle 実行などの CLI 入口と実行フローを扱う。
- 各対象は CLI runtime への接続、実行前条件の検査、branch/worktree や git 操作、状態更新、Codex 呼び出し、利用者向け出力や report 生成への入口として位置づく。
- 共通 runtime や低レベル helper そのものではなく、サブコマンド単位で既存処理をどう組み合わせて利用者操作へ結びつけるかをたどるための階層である。

## Read this when
- cmoc の個別サブコマンドの実行順序、preflight、CLI runtime への渡し方、成功時出力や失敗時処理を確認・変更したいとき。
- session branch、apply branch/worktree、review 用 worktree、home branch への merge など、サブコマンド起点の branch/worktree ライフサイクルを追いたいとき。
- 初期化、INDEX maintenance、TUI 起動、apply fork/join/abandon、review oracle、session fork/join/abandon のうち、どの実装入口へ進むべきかを選びたいとき。
- サブコマンドから Codex 実行、report 保存、INDEX.md 変更の commit/merge、状態ファイル更新、clean worktree や ignore 条件の検査へどこから入るかを確認したいとき。

## Do not read this when
- CLI runtime の共通規約、path 解決、git wrapper、設定読み込み、state file 入出力、ignore 判定などの共通部品だけを調べたいとき。
- サブコマンドの外部仕様や正本仕様断片そのものを確認したいときは、実装ではなく oracle 側を読む方が適切なとき。
- INDEX.md の文章生成、対象探索、lock、commit など indexing 共通処理の詳細だけを調べたいとき。
- Codex 用 prompt builder、Structured Output parameter、設定モデル、path token 解決など、サブコマンドから呼ばれる下位処理の詳細だけを調べたいとき。
- テストケース、fixture、トップレベル CLI 登録、package metadata、またはサブコマンド以外の realization implementation を探しているとき。

## hash
- a56f2c95d40481c849f3d70d04541341c552ddf853a88c5ca240901a3372dd88
