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
- cmoc の実行時共通機能を集めた領域。Codex 呼び出し、INDEX 更新、apply process 制御、CLI 共通ライフサイクル、config、content hash、error 表示、git 操作、logging、path、実行結果、session state などの runtime helper と、それらをまとめる import 境界を扱う。
- 個別サブコマンドの業務処理本体ではなく、複数の処理から共有される実行時境界、永続状態、外部コマンド境界、利用者向け共通エラー・ログ・表示を確認する入口になる。

## Read this when
- Codex exec/TUI 呼び出し、profile、Structured Output、quota/capacity retry、call log、file access post-check などの共通 runtime 制御を調べたいとき。
- INDEX.md の自動更新 preflight、エントリー生成、hash 鮮度判定、対象除外、並列更新、差分 commit の実装経路を確認・変更したいとき。
- apply process の追跡・停止、pid file、session/apply branch と worktree の対応、process group 終了制御を扱うとき。
- CLI サブコマンド共通の実行前後処理、ログ作成、完了サマリー、終了コード化、共通エラー表示、stdout 契約を変更したいとき。
- config 永続化、content hash 保存、git 状態操作、runtime path、subcommand logging、実行結果モデル、session state file など、複数機能から使われる runtime helper を探すとき。

## Do not read this when
- 個別サブコマンドの利用者向け挙動、引数、出力仕様、業務フローだけを調べたいとき。その場合は command 実装または対応するテストへ進む。
- oracle 上の正本仕様、path placeholder、file access rule、config 型、session state の仕様意図だけを確認したいとき。その場合は対応する oracle doc または oracle src を読む。
- 特定の低レベル helper の利用箇所ではなく、正本仕様や上位 workflow の意図を確認したいとき。
- 生成済みログ、実行履歴、キャッシュ的な成果物の内容を確認したいだけで、runtime 実装自体を変更しないとき。

## hash
- 9eab34992267268966132292ce9e1c723620f1c74a8c3d0628116b11163e2c44

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
