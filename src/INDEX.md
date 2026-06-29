# `acp`

## Summary
- realization implementation 側の ACP 名前空間入口であり、oracle src 側の acp 実装へ到達するための互換 import 経路を提供する領域。
- パッケージ入口そのものは最小の import 成立用で、下位の builder 領域では apply fork、review oracle、session join、TUI、indexing などの builder 関連互換入口や薄い adapter へ進むための境界を扱う。
- ACP の正本仕様や実処理本体ではなく、正本側実装を実行側 package 構造から参照するための realization 側の入口として位置づけられる。

## Read this when
- realization implementation 側から acp 名前空間または ACP builder 関連機能をどの import 経路で参照できるか確認したいとき。
- oracle src 側の acp 実装と realization 側 package 構造の対応関係、互換入口、薄い adapter の有無を切り分けたいとき。
- apply fork、review oracle、session join、TUI、indexing など、ACP builder 配下のどの領域へ進むべきか判断したいとき。
- repository root 解決、oracle src import 準備、runtime 側 AgentCallParameter への橋渡し、実行時契約に合わせた小さな補正が ACP builder 境界で扱われるか探しているとき。

## Do not read this when
- ACP の正本仕様断片、builder prompt 本文、Structured Output schema、model 設定、reasoning effort、file access mode などを確認したいとき。その場合は対応する oracle 側の仕様文書または実装を読む。
- ACP や builder の具体的な処理内容、生成処理、変換ロジック、判定基準、データ構造、公開関数・クラスの詳細を理解したいとき。その場合は該当する下位の実装本体または委譲先を読む。
- apply fork 全体、review workflow、TUI 起動後の画面処理、session join の制御など、ACP builder 境界より外側の orchestration や UI 本体を調べたいとき。
- path model、AgentCallParameter、基本 enum、repository root 解決そのものなど、ACP builder から参照される基礎定義の意味を確認したいとき。

## hash
- 56927e3e786f0d74a811d77c19fc18cce0355bfe5a2e6a928be857f383432498

# `basic`

## Summary
- realization implementation 側で、正本側の basic 領域にある基礎概念や共有型へ到達するための薄い互換入口をまとめるパッケージ。
- ACP 呼び出しパラメータ、path model、構造化ドキュメントなどの実体は正本側に置き、この領域は独自仕様や主要ロジックを持たず、通常の実装側 import 経路から同じ公開要素を参照できるようにする位置づけを持つ。

## Read this when
- realization implementation 側の基礎パッケージが、正本側の basic 領域と import 構造上どのように対応しているかを確認したいとき。
- ACP 型、path model、構造化ドキュメント関連の公開要素について、実装側から正本側へ接続する入口を探したいとき。
- basic 領域に独自実装があるのか、正本側の再公開だけなのかを切り分けたいとき。

## Do not read this when
- ACP 型のフィールド、enum 値、path token の意味、構造化ドキュメントの変換規則など、正本定義や詳細仕様そのものを確認したいとき。その場合は正本側の対応本文を読む。
- ACP パラメータ値の組み立て、ファイルアクセス制御、権限判定、structured output schema 検証など、再公開入口ではなく実際の処理ロジックを調べたいとき。
- oracle file と realization file の一般定義、編集責任、標準方針、ルーティング文書の生成規則を確認したいとき。その場合はそれらを定義する正本仕様断片を読む。

## hash
- c4d76a0cbbb4df80f82c4d01d5bdb0499d90084134f17dd15ffafde1f759d161

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
- cmoc の realization implementation のうち、CLI 実行時に複数サブコマンドや上位処理から共有される runtime helper 群を収める領域。
- Codex CLI 呼び出し、preflight indexing、設定、内容 hash、エラー表示、git 操作、ログ、パス、結果型、session state など、横断的な実行時支援の実装と、それらをまとめて公開する import 入口を扱う。
- 個別サブコマンドの業務ロジックではなく、サブコマンドや workflow が共通して利用する実行境界、永続状態、外部プロセス、標準配置、失敗時表示の責務へ進むための入口である。

## Read this when
- CLI サブコマンド共通の実行ライフサイクル、終了コード化、標準サマリー、例外表示、subcommand log の設定を確認・変更したいとき。
- Codex exec/TUI 呼び出し、profile・sandbox・CODEX_HOME・call log・quota/capacity retry・Structured Output 検証・preflight indexing との接続を調べたいとき。
- INDEX.md 更新 preflight、索引 entry の鮮度判定、対象内容抽出、Codex への entry 生成依頼、Markdown entry 描画など、索引更新の実装を追いたいとき。
- cmoc 設定ファイル、内容 hash 保存、git worktree/branch 操作、runtime path、ログ、結果モデル、session state file など、複数機能から共有される runtime 基盤を探しているとき。
- 上位実装の import 面を整理する前に、共通 runtime API がどの module に分かれ、どの集約入口から公開されているかを把握したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、業務処理、利用者向けレポート、状態遷移の上位 workflow を調べたいだけのとき。その場合は該当する command や workflow 実装へ進む。
- oracle の正本仕様、INDEX.md entry に書くべき意味情報、path keyword の定義、session state の仕様意図などを確認したいとき。その場合は対応する oracle doc/source を読む。
- テストケース、fixture、期待値だけを確認・変更したいとき。その場合は test 側の対象へ進む。
- 生成済みの log、report、schema store、call log の内容を読みたいだけで、生成・保存・表示の runtime 実装を変更しないとき。
- 単一の下位責務がすでに分かっており、その具体挙動だけを調べたいとき。その場合は設定、git、path、logging、Codex exec/TUI、state などの該当 runtime 本文へ直接進む。

## hash
- 0b097804faf6ca4f419c75c19e0f00f112e3a385fd6ffd4e3895a419ec8290ea

# `config`

## Summary
- 実装側の設定パッケージであり、正本側の設定定義へ互換的に到達するための import 入口を提供する。設定値の実体や読み込み・検証などの処理は持たず、正本側定義の再公開境界を扱う。

## Read this when
- 実装側から設定定義へ到達する import 経路を確認したいとき。
- 設定パッケージが正本側の設定定義を実体として委譲し、互換入口として機能しているか確認したいとき。
- 設定モジュールの公開名、再エクスポート範囲、設定パッケージ入口の責務を確認したいとき。

## Do not read this when
- 個々の設定項目の意味、既定値、制約を確認したいとき。ここは設定定義の実体ではなく、正本側定義への入口だけを扱う。
- 設定値の読み込み、解決、検証、変換、永続化などの処理ロジックを調べたいとき。
- 正本仕様として設定内容そのものを確認したいとき。実体を持つ正本側の定義を直接読む方が適切である。

## hash
- 7a2dcace2fd029ab73ce6de095eae0152577f065ea99bdef28edd0f27aa94095

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
- cmoc の利用者向けサブコマンド実装をまとめる階層で、初期化、indexing、TUI、session、apply、review などの CLI 操作入口を扱う。
- 各対象は CLI runtime への接続、実行前条件、状態・branch・worktree 操作、Codex 呼び出し、利用者向け出力や report 生成など、サブコマンドごとの orchestration へ進むための入口になる。
- 共通 runtime や git wrapper、path model、state 永続化、INDEX.md 生成本体などは別階層へ委譲され、この階層では利用者操作単位の制御境界から読む先を選ぶ。

## Read this when
- 特定の cmoc サブコマンドが CLI から起動された後、どの runtime helper や下位処理へ渡されるかを確認・変更したいとき。
- 初期化、indexing、TUI、session、apply、review の実行条件、preflight、clean worktree 要求、branch/worktree 操作、state 更新、cleanup、利用者向け出力をサブコマンド単位で追いたいとき。
- session branch の作成・破棄・join、apply run の fork・abandon・join、review oracle の対象列挙から report 生成までなど、利用者操作に対応する制御フローの入口を探したいとき。
- サブコマンド実装から、Codex subprocess 実行、INDEX.md maintenance、review loop、report writer、merge conflict 処理などの詳細実装へどこで分岐するかを確認したいとき。
- CLI 全体の登録層ではなく、各サブコマンドが受け持つ実行時副作用や失敗時処理の責務境界を把握したいとき。

## Do not read this when
- Typer app へのサブコマンド登録、トップレベル CLI entrypoint、共通の CLI runtime 規約だけを確認したいとき。
- git 実行 wrapper、path model、config load、state file schema、timestamp、reports directory、cmoc ignore 判定などの共通部品そのものを調べたいとき。
- oracle doc 上のサブコマンド正本仕様や利用者向け要求そのものを確認したいときは、実装階層ではなく oracle 側を読む。
- INDEX.md の文章生成、差分検出、更新対象探索、ルーティング文書規約、Codex prompt builder の詳細だけを調べたいとき。
- 個別サブコマンドのさらに低レベルな処理だけを調べたい場合は、この階層全体ではなく apply、session、review、review_loop、review_index、review_report、review_targets など目的に直結する下位対象へ進む。

## hash
- f98a874160b4b4d24fa9e2d4fef9a44d28f4413fd76047124324c76f095d78cd
