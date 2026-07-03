# `acp`

## Summary
- oracle 側の canonical ACP builder を正本に保ちつつ、realization 側に残る既存の公開 import 経路を壊さず接続する互換層。
- agent call parameter builder の旧参照、再公開、module alias、package path 接続、realization 側公開型への必要最小限の適合を扱う。
- 実装本体や正本仕様ではなく、旧 import 面を維持する理由、canonical 実装への到達経路、移行期間中の削除条件を確認する入口になる。

## Read this when
- ACP builder 周辺の旧 import 経路、再 export、module alias、package path 接続が canonical 実装へどうつながるかを確認したいとき。
- 既存参照を保つための互換 package や shim を残す理由、公開面維持、削除条件、移行可否を判断したいとき。
- agent call parameter builder 入口を探し、oracle 側の生成結果を realization 側公開型や既存利用者向け公開面へ適合させる境界を追いたいとき。
- realization 側または利用者向け公開面に残る旧 import 参照の扱いを判断したいとき。

## Do not read this when
- agent prompt、structured output、parameter 生成内容、canonical builder 実装などの正本仕様断片を確認したいだけのとき。
- 各機能の実行フロー、CLI 引数処理、永続状態、git 操作、画面描画、イベント処理を調べたいとき。
- AgentCallParameter 型、共通 enum、汎用 git helper、path model、file access rule 検出、ログ収集など builder 互換層以外の共通基盤を調べたいとき。
- 旧 import 互換ではなく個別 builder の変換処理、wrapper の詳細挙動、新規公開 API の設計をしたいとき。

## hash
- c0af36a827c20f72bc478007859048ba68c9e41da8674608a553c068ba14daa1

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
- cmoc の実行時共通部品を集めた領域。Codex 呼び出し、INDEX 更新、CLI 共通ライフサイクル、設定、内容 hash、エラー表示、git 操作、ログ、path、実行結果、session state、apply process 管理など、複数サブコマンドから使われる runtime 支援を扱う。
- 実処理を持つ責務別実装と、それらをまとめて参照する薄い公開入口が同階層にあり、個別サブコマンド固有の業務処理ではなく横断的な実行基盤を確認する入口になる。

## Read this when
- 複数のサブコマンドや runtime 処理で共有される helper、型、例外、ログ、path、git、config、state、Codex 実行制御を探したいとき。
- Codex exec/TUI 呼び出し、profile 作成、Structured Output 検証、quota/capacity retry、call log、file access rule post-check など、agent call の共通実行境界を調べたいとき。
- INDEX.md 自動更新の preflight、対象走査、hash 鮮度判定、既存エントリー再利用、エントリー生成、排他制御、更新 commit 条件を確認または変更したいとき。
- CLI サブコマンド共通の開始・完了表示、終了コード化、例外表示、サブコマンドログ、完了サマリー、work root 検査を扱うとき。
- session state、apply process tracking、cmoc 管理 worktree/branch、git ignore 判定、memo 判定、内容 hash 保存など、上位 workflow から呼ばれる共通 runtime 境界を確認したいとき。

## Do not read this when
- 個別サブコマンドの利用者向け挙動、引数、状態遷移、出力仕様を確認したいだけの場合は、該当する command 実装やテストへ進む。
- oracle file にある正本仕様、path placeholder の定義、file access rule の意図、config や state の仕様根拠を確認したい場合は、対応する oracle 側の文書や定義を読む。
- 特定 helper の呼び出し元だけを調べたい場合や、上位 workflow の制御判断を追いたい場合は、その workflow 側を先に読む。
- 生成済みログや実行履歴の内容確認が目的で、runtime logging や Codex 呼び出し実装そのものを変更しない場合は、この領域を読む必要はない。

## hash
- 9a85a862656a1292071d364dd5c1e9aab3675358ef53361c26cd549fab0fbd12

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
- cmoc の各サブコマンド実装を収める領域。init、indexing、tui、session、review、apply などの CLI 実行入口と、各 workflow の orchestration 層への入口になる。
- サブコマンドごとの事前条件、runtime 接続、git/worktree/state 操作、Codex 呼び出し、report 出力、merge/abandon などの利用者向け制御フローを調べるための分岐点である。
- 詳細な生成ロジック、prompt builder、共通 runtime、git wrapper、path/state model そのものではなく、サブコマンド単位でそれらをどう接続しているかを読む起点になる。

## Read this when
- cmoc のサブコマンド実装のうち、どの領域へ進むべきかを判断したいとき。
- init、indexing、tui、session、review、apply の実行順序、事前条件、状態遷移、出力、失敗時処理を確認または変更したいとき。
- session branch、run worktree、state file、report、process id、git merge/commit/delete などが各サブコマンドでどう扱われるかを追いたいとき。
- review や apply の対象列挙、finding 処理、INDEX 変更反映、session branch への反映または破棄など、workflow 全体の入口から下位処理への接続を確認したいとき。
- CLI runtime、Codex Exec/TUI、設定、root 解決、ignore/preflight、共通 helper がサブコマンド実行本体からどう呼ばれているかを確認したいとき。

## Do not read this when
- サブコマンドに依存しない CLI 登録、runtime 共通規約、git wrapper、config、path model、state model の詳細だけを調べたいとき。
- Codex に渡す prompt、Structured Output parameter、builder の具体的な内容だけを確認したいとき。
- INDEX.md の本文生成、差分検出、lock、commit、ルーティング文書作成規則そのものを調べたいとき。
- oracle file、realization file、path placeholder、scope などの正本仕様断片を確認したいとき。
- 個別 workflow の下位 helper が担う対象列挙、report 描画、path 解決、merge operation 検証などに読む対象をすでに絞れているとき。

## hash
- 52f30255596f02c59497dc4f3311b5de2c0da2ad1500b87198876dba75f55fac
