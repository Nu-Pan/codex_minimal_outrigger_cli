# `acp`

## Summary
- oracle src 側の ACP builder を正本に保ちながら、realization 側に残る旧 `acp.*` import 経路を維持する互換入口。
- 公開 import 面を壊さない再 export、canonical oracle 実装への中継、必要最小限の realization 側適応、互換維持理由や削除条件を確認するための下位領域への入口になる。

## Read this when
- ACP builder まわりで、旧 import path 互換、oracle 側 canonical builder への委譲、realization 側公開型への適応境界のどこを読むべきか選びたいとき。
- apply、review、session、TUI、indexing、quota probe などの agent call parameter builder 領域について、該当する下位 package または module への入口を探すとき。
- `acp.*` または `acp.builder.*` 参照の移行・削除・互換維持を検討しており、互換入口を残す理由や削除条件を確認したいとき。
- oracle src 由来の acp builder 互換 import が realization 側または公開面でどこに維持されているかを確認したいとき。

## Do not read this when
- oracle 側 builder の正本 prompt、canonical 実装、生成内容そのものを確認したいとき。対応する oracle 側の実装や doc を直接読む。
- ACP parameter の共通型、汎用 git helper、path model、CLI 実行フロー、TUI 描画、apply/review/session の本体挙動など、builder 入口や import 互換と無関係な詳細を調べたいとき。
- 個別 builder の変換処理、wrapper の詳細、quota probe の呼び出し制御など読む対象が既に特定できているとき。該当する下位 module または呼び出し元を直接読む。
- 新しい ACP 機能や API 仕様を追加する場所を探しているとき。この領域は互換維持と中継が主責務であり、機能追加の入口ではない。
- `acp.*` 参照が全公開面と realization 側から消えていることを確認済みで、互換入口の詳細を読む必要がないとき。

## hash
- c1585e905628497eb304f8dd03e1bc86b5dda368d3d830dab9d7efed6dd9994d

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
- cmoc の runtime 共通部品を集めた実装領域。Codex 実行、profile、config、content、CLI 共通処理、error、git、logging、path、result、state、apply process、INDEX 更新 preflight など、複数サブコマンドから参照される横断的な helper と公開 import 境界を扱う。
- 個別機能の実処理を持つ責務別 runtime module と、それらをまとめて再公開する薄い集約層を含むため、サブコマンド固有処理へ入る前に共通実行時支援の入口を探すための階層である。

## Read this when
- Codex exec/TUI 呼び出し、profile 生成、Structured Output 検証、quota/capacity retry、call log、INDEX 更新 preflight など、Codex 実行周辺の共通 runtime 処理を調べたいとき。
- config/state/log/report/schema/worktree/session など、cmoc 管理領域の永続化先、読み書き、検証、実行時 error 変換を扱う共通 helper を探したいとき。
- git branch、worktree、ignore 判定、oracle file 判定、clean worktree 要求、外部 command 結果、CmocError、runtime path、content hash、binary 判定など、複数コマンドで共有される低レベル処理を確認または変更したいとき。
- CLI サブコマンドの共通ライフサイクル、開始・完了表示、終了コード化、サブコマンド logger、console summary、利用者向け error report など、コマンド横断の表示・ログ境界を変更したいとき。
- apply process tracking、pid file、process group 停止、session/apply branch からの worktree 復元など、apply 実行中 process の共通制御を調べたいとき。

## Do not read this when
- 個別サブコマンドの利用者向け挙動、CLI 引数、状態遷移、出力仕様、業務処理だけを確認したいとき。その場合は該当 command 実装やテストへ進む。
- oracle 上の正本仕様、path placeholder の定義、file access rule、INDEX.md の仕様意図、config/state の意図そのものを確認したいとき。その場合は対応する oracle doc または oracle src を読む。
- AgentCallParameter や prompt builder など、LLM 呼び出しに渡す上位入力の組み立て責務だけを調べたいときは、その builder 実装を直接読む。
- 生成済み log や実行履歴の内容を調査したいだけで、logging/runtime 実装を変更しないとき。
- 特定 helper の公開 import 経路ではなく実際の副作用や詳細挙動を追う場合は、集約入口ではなく責務を持つ個別 runtime module を読む。

## hash
- 60d60b49090813d9cb2284516137f8e006fc58934e9397c41b9ecb3aabbaee6d

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
