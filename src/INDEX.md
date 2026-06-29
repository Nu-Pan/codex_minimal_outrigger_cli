# `acp`

## Summary
- realization 側に残る ACP builder 互換入口をまとめる領域。旧来の `acp.*` import 経路を保ちつつ、実体は oracle 側または下位 builder 実装へ委譲するための公開境界として機能する。
- この階層は ACP builder の正本仕様や具体的な組み立て処理そのものではなく、互換 package、再公開層、最小 wrapper の所在と、下位の builder 領域へ進む入口を示す。

## Read this when
- realization 側で残っている ACP 関連の公開 import path や互換入口を確認したいとき。
- 旧来の `acp.*` 参照を oracle 側や実体 module へ移行する際に、どの互換境界が残っているか判断したいとき。
- apply、indexing、review、session、TUI、quota probe などの agent call parameter builder 領域へ進む前に、上位の入口と領域分担を把握したいとき。
- ACP builder 周辺で、正本実装への委譲、再公開、prompt 表記補正、realization 側 parameter 型への適合といった互換層の所在を探したいとき。

## Do not read this when
- ACP builder の具体的な prompt、parameter 組み立て、repo root 解決、型変換、検証ロジックを確認したいときは、該当する下位 builder 領域または oracle 側の正本実装へ進む。
- apply fork、review、session、TUI などのコマンド全体の制御フロー、UI 処理、状態管理、branch 操作、diff 生成、CLI 引数処理を調べたいときは、それぞれの実処理を担う領域へ進む。
- AgentCallParameter、FileAccessMode、model、reasoning、file access、structured output schema などの共通型や基礎定義を確認したいときは、基本モジュールへ進む。
- 互換 import 経路がすでに不要かどうかではなく、新しい ACP 機能や API 仕様の追加場所を探しているときは、この互換入口ではなく正本仕様、実装本体、またはテスト対象を読む。

## hash
- 44f3cc01dbe60bbdc0dbe978dbaae33bb0fd1efc48bc610b46dd9359452dbca2

# `basic`

## Summary
- 正本側にある ACP 型、path model、構造化文書 API を realization 側の既存公開面へ再公開する互換領域。
- 正本実装や型を複製せず、既存の `basic.*` 参照を保つための薄い入口として位置づけられる。
- 削除条件は、realization 側と利用者向け公開面から対応する `basic.*` 参照がなくなり、正本側または実体 module への移行が済んでいること。

## Read this when
- realization 側で維持されている `basic.*` import 経路や再公開対象を確認したいとき。
- ACP 型、path model、構造化文書 API を正本側から再公開している互換境界を確認したいとき。
- `basic.*` 互換参照を残す理由、移行方針、または削除条件を判断したいとき。

## Do not read this when
- ACP 型、path placeholder、path 解決、構造化文書、Markdown 描画などの実体定義や処理内容を確認したいとき。その場合は再公開先の正本側実装を読む。
- 新しい基本型、path 変換仕様、構造化文書の挙動を追加・変更する場所を探しているとき。この領域は互換再公開を担い、正本側の仕様追加場所ではない。
- CLI 挙動、生成ロジック、変換処理、テスト観点など、`basic.*` 互換 import の維持と無関係な実装責務を調べたいとき。

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
- cmoc の共有 runtime helper 群を集める実装領域。Codex CLI 呼び出し、preflight indexing、CLI サブコマンド共通実行、設定、content hash、git、logging、path、外部コマンド結果、session state、共通エラー表示など、複数の上位機能から横断利用される基盤処理を扱う。
- この階層は、個別サブコマンドの業務フローではなく、サブコマンドや Codex 実行経路が依存する共通の実行時境界を探す入口になる。公開 import 集約だけを担う小さな入口と、実際の挙動を担う責務別 helper が混在しているため、目的に応じて集約入口か個別実装へ進む。
- INDEX.md 自動更新については、preflight からエントリー生成、対象走査、hash 鮮度判定、既存エントリー再利用、Codex への生成依頼、Structured Output 検証、Markdown 描画までの実装がここに含まれる。

## Read this when
- Codex exec や TUI 起動に関する profile 準備、CODEX_HOME、sandbox/file access mode、call log、stdout/stderr/output 保存、retry、quota/capacity 制御、resume、Structured Output schema の扱いを調査または変更したいとき。
- CLI サブコマンド共通の実行ライフサイクル、work root 検査、ログ作成、開始・完了表示、終了コード化、例外表示、現在のサブコマンド logger の設定を確認したいとき。
- INDEX.md を Codex 実行前に自動更新する処理、対象ファイル選別、除外条件、entry 再生成条件、hash 計算、並列更新、排他 lock、Codex への entry 生成依頼を追いたいとき。
- cmoc の設定 JSON、runtime path、content hash 保存、binary 判定、git repository/worktree 操作、`.cmoc` ignore 処理、session state 永続化、共通エラーレポート、外部コマンド結果モデルなどの共有 helper を探したいとき。
- 複数の runtime helper がどの import 入口から公開されているか、または互換 import 入口が実体実装へどう接続されているかだけを確認したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、CLI アプリへの command 登録、利用者向け業務フロー、固有の状態更新や出力 schema を調べたいとき。その場合は command 実装側へ進む。
- oracle file にある正本仕様、path model の抽象定義、INDEX.md の仕様意図、session state などの仕様意図そのものを確認したいとき。その場合は対応する oracle 側を読む。
- 実装やテスト全体の入口、パッケージ構成、上位ディレクトリからのルーティングだけを確認したいとき。その場合はより上位の案内を読む。
- Codex が返した自然言語回答の品質評価、LLM 出力内容の妥当性判断、または利用者プロンプトそのものの設計だけをしたいとき。ここで扱うのは runtime 境界と機械的な実行結果の処理である。
- 生成済みログや状態ファイルを解析する読み取り側、または特定の保存先をどの上位機能がいつ利用するかだけを調べたいとき。その場合は利用側の実装へ進む。

## hash
- 942811c84f9fae764e89fe0b8aad3800be2d4e3ba0b2b64fae2adb82db634a32

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
- cmoc の CLI サブコマンド実装を集める領域で、初期化、indexing、TUI、apply、review、session などの利用者向け操作を runtime・git 操作・状態管理・出力生成へ接続する入口になる。
- 各対象はサブコマンドごとに分かれ、単体ファイルは薄い orchestration、下位 package は lifecycle や loop、report、対象列挙、merge などの段階別実装を担う。
- CLI 登録後に実際のコマンド挙動、事前条件、worktree/branch 操作、Codex 呼び出し、利用者向け結果出力のどこを読むべきかを選ぶための分岐点として使う。

## Read this when
- cmoc のサブコマンド実行本体がどこにあり、対象操作に応じて init、indexing、tui、apply、review、session のどれへ進むべきかを切り分けたいとき。
- サブコマンドが CLI runtime を通じて preflight、work root runtime、git 操作、Codex 実行関数、状態更新、標準出力や report 生成へどう接続しているかを追いたいとき。
- apply run、review oracle、session lifecycle など、branch/worktree を伴うサブコマンドの大きな制御順序や下位 helper への入口を探したいとき。
- 初期化、INDEX.md maintenance、TUI 起動など、個別サブコマンドの実行条件、副作用、利用者向け出力を実装側から確認・変更したいとき。

## Do not read this when
- Typer app へのトップレベル登録、CLI 全体の共通 runtime、設定読み込み、path model、git wrapper、state schema など、サブコマンド本体ではなく共有基盤だけを調べたいとき。
- oracle doc にある外部仕様や正本仕様断片を確認したいとき。実装挙動ではなく仕様根拠が必要なら oracle 側を読む。
- INDEX.md の生成アルゴリズム、review finding の prompt、apply report の本文構造、process tracking など、より直接の下位モジュールや builder が既に特定できているとき。
- テスト、fixture、実行ログ、生成済み report の内容を確認したいだけで、サブコマンド実装の制御フローを読む必要がないとき。

## hash
- 7e67ca84b4947b391ea69bfced2ff17706b9946a9ae24d8de03e377043a1aff1
