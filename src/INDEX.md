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
- cmoc の共有 runtime helper 群を収める領域。Codex exec/TUI 呼び出し、profile/config/content/error/git/logging/path/result/state、apply process、INDEX.md indexing preflight など、複数サブコマンドから参照される実行時支援の実装と公開 import 境界を扱う。
- 個別機能の本体だけでなく、責務別 runtime module を横断して再公開する薄い入口や、互換 import path を維持する境界層も含む。

## Read this when
- CLI サブコマンド共通の実行ライフサイクル、エラー表示、ログ記録、完了サマリー、終了コード化など、runtime 横断の共通挙動を確認または変更したいとき。
- Codex CLI の exec/TUI 起動、profile/CODEX_HOME/schema/call log、Structured Output 検証、quota/capacity retry、resume 継続、preflight 実行の制御を追いたいとき。
- cmoc の config、session/apply state、runtime path、git/worktree/ignore 判定、content hash 保存、外部コマンド結果モデルなど、複数箇所から使われる実行時 helper の責務や公開入口を探すとき。
- apply abandon や linked worktree 復元、process pid file、Codex subprocess tracking、process group 停止など、apply 実行時の補助処理を確認または変更したいとき。
- INDEX.md の自動更新 preflight、entry 再生成、hash による再利用、除外条件、indexing commit、排他 lock の実装を確認または変更したいとき。

## Do not read this when
- 個別サブコマンドの業務処理、CLI 引数、利用者向け出力 schema、report 内容、prompt 構築そのものを確認したいとき。その場合は対象 command や prompt builder の実装を読む。
- path placeholder、config 型、file access rule、session state の仕様意図、INDEX.md entry の文章基準など、正本仕様断片を確認したいとき。その場合は oracle 側の該当文書や定義を読む。
- 生成済みログ、生成済み INDEX.md、特定 directory の routing entry、実行履歴など、runtime 実装ではなく生成物や個別結果を調べたいだけのとき。
- git、path、logging、Codex profile などの低レベル helper のうち目的の責務が既に分かっているときは、この階層全体ではなく該当する責務別本文を直接読む。

## hash
- 76d7833f517c45f653d04efe655d81b438e790735ba147f65a9f5aa91039aae1

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
- cmoc の Typer ベース CLI 入口を定義し、トップレベルコマンドと session・apply・review 配下のサブコマンドを各実装関数へ接続する。
- 通常実行時の Click 引数解析エラーを cmoc 形式のエラーレポートへ変換し、shell 補完時は通常の Typer/Click 挙動を維持する。
- apply fork と review oracle の scope option 値、および apply join の force resolve option を CLI 公開面として定義する。

## Read this when
- cmoc CLI のコマンド階層、サブコマンド名、option 名、デフォルト値、実装関数への接続を確認または変更したいとき。
- CLI 引数解析エラーの表示形式や終了挙動、shell 補完時の例外処理を確認または変更したいとき。
- console script から起動される main 関数や Typer app の構成を確認したいとき。

## Do not read this when
- 個別サブコマンドの実処理、git 操作、worktree 操作、レビュー処理、INDEX 更新処理の詳細を確認したいときは、接続先の実装を直接読む。
- cmoc のエラーレポート構造や描画内容そのものを変更したいときは、runtime 側のエラー定義と描画処理を読む。
- oracle で定義されたサブコマンド仕様そのものを確認したいときは、対応する oracle doc を読む。

## hash
- 090e0a5d4cff8adb41623ebbbd34a7d1b42bac412d81a18a14b3b28da9584fe4

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
- cmoc の利用者向けサブコマンド実装を集約する階層。init、indexing、TUI、session、apply、review などの実行入口から、各コマンド固有の事前条件、状態遷移、git/worktree 操作、出力、失敗時処理へ進むためのルーティング対象。
- 共通 runtime や低レベル helper そのものではなく、CLI サブコマンドとして既存の共通処理をどう接続し、利用者向け挙動としてどうまとめるかを確認する入口になる。

## Read this when
- cmoc のサブコマンド単位で、実行順序、preflight、状態更新、branch/worktree/state 操作、stdout/report 出力、失敗時処理を確認または変更したいとき。
- init、indexing、TUI、session、apply、review のどの実行本体または下位 package へ進むべきか判断したいとき。
- サブコマンドから Codex 実行、INDEX.md maintenance、review loop、apply fork report、設定同期、git 操作などの共通処理へどう接続しているかを追いたいとき。
- 利用者向け CLI 挙動を変更するため、該当サブコマンド固有の orchestration 層を探したいとき。

## Do not read this when
- CLI runtime、git wrapper、path model、state file schema、設定 schema、Codex 呼び出し基盤など、サブコマンド固有でない共通実装だけを確認したいとき。
- oracle file の正本仕様、INDEX.md 生成規則、ルーティング文書規則など、実行本体ではなく仕様文書を確認したいとき。
- 特定サブコマンド内の低レベル helper や report 描画、対象列挙、merge 処理など、読むべき下位 module が既に分かっているとき。
- Typer app への登録やトップレベル CLI entrypoint だけを確認したいとき。

## hash
- de25aa03c87fc923b933fc997f81b8852934fcd21a0cbb4935a2add6bd7032fc
