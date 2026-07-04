# `acp`

## Summary
- oracle src 側の agent call parameter builder を正本に保ちながら、realization 側で旧 `acp.*` import 経路を維持する互換領域。canonical oracle 実装への中継、再公開、公開型変換、runtime path 接続など、既存参照を壊さないための最小適応層を扱う。

## Read this when
- agent call parameter builder 周辺で、旧 `acp.*` import がどの canonical 実装や互換入口へつながるかを確認したいとき。
- oracle 側 builder を複製せず正本として使いながら、realization 側で package path、module alias、公開型変換、runtime path 接続をどう補っているかを調べたいとき。
- apply fork、quota probe、review、session、TUI などの agent call parameter 構築入口や互換層の残存理由・削除条件を確認したいとき。
- 既存 caller や利用者向け公開面に残る `acp.*` import を canonical path へ移行する作業で、影響範囲を絞りたいとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容の正本仕様や人間意図を確認したいとき。対応する oracle 側 builder や oracle file を読む。
- agent call parameter の基本型、enum、構造化出力 schema、汎用 git helper、path model などの共通定義を調べたいとき。それぞれの定義元へ進む。
- apply、review、session、TUI など各機能の実行フロー、UI、branch 操作、結果判定、外部コマンド実行を調べたいとき。機能本体の実装を読む。
- 新しい acp 機能や API 仕様を追加する場所を探しているとき。この対象は互換維持と最小適応層の入口であり、新機能設計の入口ではない。

## hash
- 871c1d3698bf7219f005efd72f17aaff6274f7ddbdb99325bb64f21b9f306cc6

# `basic`

## Summary
- oracle 側の基本型・path model・構造化文書実装を realization 側で複製せず、既存の `basic.*` 公開参照として再公開する互換層をまとめるディレクトリ。
- ACP、path model、struct doc などの既存 import 経路を正本側実装へ委譲し、後方互換性と公開名を維持する入口として位置づけられる。
- 削除可否は、realization 側と利用者向け公開面から該当する `basic.*` 参照がなくなり、正本側または実体 module への移行が済んでいるかで判断する。

## Read this when
- `basic.*` 経由の既存公開参照、互換維持、移行、削除条件を確認したいとき。
- oracle 側の基本型・path model・構造化文書実装を realization 側へ複製せず再公開している import 経路を調べたいとき。
- ACP 型の既定 preflight 付与、path model API、構造化文書 API など、basic 互換層が提供する公開面や `__all__` を調整したいとき。

## Do not read this when
- ACP 型、path placeholder、構造化文書処理などの正本定義や実装詳細そのものを確認したいとき。その場合は再公開先の oracle 側実装を読む。
- preflight 処理、indexing、CLI 挙動、テスト挙動など、`basic.*` 互換参照の維持や削除条件に関係しない処理を調べたいとき。
- 既存の basic 公開参照ではなく、新規 API 設計や利用元固有の挙動だけを確認したいとき。

## hash
- ddd5f3fcf95fe84d0a51ba34e5edc5ce6f7e273f44a044efc2c4d81d41d0394c

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
- cmoc の共通実行時支援を担う runtime helper 群のディレクトリ。Codex 呼び出し、profile、設定、content hash、CLI 実行ライフサイクル、doctor 前処理、error、git、logging、path、result、session state、INDEX 更新 preflight、apply process 管理など、複数サブコマンドから共有される実装を置く。
- 複数の runtime_* 実装を集約する公開入口と、各責務に分かれた runtime 補助実装への入口を提供する。

## Read this when
- CLI サブコマンド横断で使う共通 runtime helper、実行ライフサイクル、Codex exec/TUI 呼び出し、profile、設定、git、path、logging、state、error などの実装箇所を探したいとき。
- INDEX.md 自動更新 preflight、doctor preprocess、apply process 停止、session state 永続化など、個別サブコマンドから呼ばれる共通制御の責務境界を確認したいとき。
- 複数の runtime_* モジュールにまたがる公開 API の集約 import や、既存 import path の互換入口を確認したいとき。

## Do not read this when
- 個別サブコマンドの利用者向け仕様、引数定義、出力文言、業務処理の高レベル制御だけを調べたいときは、対象サブコマンドの実装へ進む。
- oracle file に書かれた正本仕様、prompt 部品、path placeholder の定義、config 型の正本、INDEX.md entry の文章基準そのものを確認したいときは、oracle 側の該当文書や定義へ進む。
- 生成済み INDEX.md の個別 entry 内容、実行済みログ、特定 directory のルーティング判断など、runtime helper の実装変更を伴わない確認だけが目的のとき。

## hash
- f1b0d60e48382337499f22984e8bf5e1f223560ab9a5624902190a4f79637b07

# `config`

## Summary
- oracle src 側の設定実装を正本に保ったまま、realization 側と利用者向け公開面に残る旧来の設定参照経路を受ける互換入口群。
- 設定定義や設定ロジック本体を担わず、正本定義の複製を避けながら既存 import を成立させる境界を扱う。

## Read this when
- 旧来の設定参照経路が realization 側でどこに受け止められているか確認したいとき。
- oracle src 側の設定実装を正本に保ちつつ、互換 import を維持している理由や境界を確認したいとき。
- 設定定義の複製を避けるための再公開経路や、その削除可否を判断したいとき。

## Do not read this when
- 設定項目そのものの正本定義を確認したいとき。
- 設定値の読み込み、検証、適用などの本体挙動を調べたいとき。
- 旧来の設定参照経路や互換 import の残存理由が論点ではない作業をするとき。

## hash
- 97eb1bfd8f73945ab835c22962809b5a59009f2d7e1581a56e7058b6c8c786a4

# `main.py`

## Summary
- cmoc の Typer ベース CLI 入口を定義し、root command と session/apply/review 配下の subcommand を各実装関数へ接続する。
- CLI 引数解析エラーを cmoc 形式のエラーレポートへ変換する group、scope option 用 enum、console script からの起動口を含む。

## Read this when
- CLI command/subcommand の登録、command 名、option、scope 値、起動関数への接続を確認・変更したいとき。
- Typer/Click の引数解析エラーを cmoc のエラー表示へ変換する挙動を確認・変更したいとき。
- console script 実行時に cmoc app がどの prog_name で起動されるかを確認したいとき。

## Do not read this when
- 各 subcommand の具体的な処理内容、branch 操作、INDEX 更新、review/apply/session の実装詳細を調べたいときは、接続先の sub_commands 配下を読む。
- cmoc のエラー型や表示形式そのものを調べたいときは、runtime 側の定義を読む。
- CLI の公開面ではなく oracle 上の正本仕様を確認したいときは、対応する oracle doc を読む。

## hash
- 87c32ef9bd4fe1d9be5ff0b9d3d99ff8966e0284bf8e9b52c562b351fddf8c6e

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
- cmoc のサブコマンド実装をまとめる領域。init、doctor、indexing、tui、apply、session、review などの利用者向けコマンド入口と、その上位制御を扱う。
- 各対象はサブコマンド単位または review/apply の補助実装単位に分かれ、CLI runtime や共通 helper そのものではなく、コマンドの事前条件、状態遷移、出力、失敗時処理へ進むための入口になる。

## Read this when
- cmoc の利用者向けサブコマンド実装を調べ、どのコマンド本体または補助実装へ進むべきか判断したいとき。
- init、doctor、indexing、tui、apply、session、review の実行順序、事前条件、状態操作、利用者向け出力、失敗時処理を確認または変更したいとき。
- apply や review のように複数 module に分かれたサブコマンドで、対象列挙、loop、report、branch/worktree/state 操作などのどの実装を読むべきか選びたいとき。
- CLI runtime から呼ばれる各サブコマンドの接続点、command 名、argv、外部実行関数や共通処理への依存関係を追いたいとき。

## Do not read this when
- CLI runtime、git wrapper、path model、state file schema、設定 schema、ignore 判定、lock、Codex 呼び出しなど、サブコマンド固有でない共通基盤の詳細だけを調べたいとき。
- 各サブコマンドの正本仕様を確認したいだけのときは、実装ではなく対応する oracle doc を読む。
- Typer app へのトップレベル登録、CLI 全体の entrypoint、共通エラー表示だけを確認したいとき。
- 具体的に読むべきサブコマンドまたは補助実装が既に分かっており、その対象へ直接進めるとき。

## hash
- d519b9bf88f7f8305e109d35d6dc38031a5f75790d4c62ceb3c6c8a752f0588f
