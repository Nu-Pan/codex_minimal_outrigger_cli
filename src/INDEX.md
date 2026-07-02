# `acp`

## Summary
- ACP builder 関連の既存 import 経路を維持するための互換入口を置く領域。oracle src 側の正本実装を複製せず、`acp.*` や `acp.builder.*` 参照から委譲先へ接続する役割を持つ。
- builder 配下の apply、common、indexing、review、session、tui、quota probe などへ進むための上位入口であり、互換 wrapper の残置理由、公開 import 面、委譲先、削除条件を見分けるために読む。

## Read this when
- `acp.*` または `acp.builder.*` 参照が oracle 側 builder 実装へどの互換入口を経由して接続されているか確認したいとき。
- realization 側や利用者向け公開面に残る ACP builder 互換 import、旧 import 経路、公開名、委譲先、削除条件を判断したいとき。
- apply、common、indexing、review、session、tui、quota probe など、ACP builder 関連の下位領域へ進む入口を選びたいとき。
- oracle src 側の正本 builder 実装を利用しつつ、既存利用者や残存参照を壊さないための公開面を調べたいとき。

## Do not read this when
- ACP builder の具体的な生成ロジック、repo root 解決、parameter 型変換、prompt 補正などを直接確認したいときは、該当する下位領域または実装本体へ進む。
- builder の正本仕様、prompt 文面、出力条件、判定仕様、file access rule などを確認したいときは、対応する oracle file または正本側実装を読む。
- AgentCallParameter、FileAccessMode、model、reasoning effort などの基礎定義を調べたいときは、基礎定義側を読む。
- CLI コマンド全体の制御フロー、fork 作成、branch 操作、TUI 描画、runtime 実行処理など、ACP builder 互換入口ではない責務を調べたいときは、より直接の実装領域へ進む。
- 新しい ACP 機能や API 仕様を追加する場所を探しているとき。この領域は互換維持用の入口であり、機能追加の正本ではない。

## hash
- a6158e66e2fbebb54c3bbcd32c755744a03ec22b354c2bce3b62cbdc6f87da63

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
- cmoc の共通 runtime helper 群を収める実装ディレクトリ。Codex 実行、CLI ライフサイクル、設定、Git、ログ、パス、状態、INDEX.md 自動更新など、複数サブコマンドから使われる共有処理への入口になる。
- 個別責務の runtime_* 実装に加えて、既存 import path を保つ互換入口や、共通 API をまとめて再エクスポートする集約モジュールを含む。

## Read this when
- 複数サブコマンドにまたがる共通 runtime 処理の読む先を探したいとき。
- Codex CLI/TUI 呼び出し、profile、preflight、Structured Output、quota/capacity retry、call log、file access rule 違反検出に関わる実装を確認または変更したいとき。
- CLI サブコマンド共通の実行順序、console 出力、サブコマンドログ、エラー表示、終了コード化を調べたいとき。
- 設定ファイル、Git 操作、runtime path、content hash、binary 判定、実行結果モデル、session state file などの共有 helper を探したいとき。
- INDEX.md 自動更新の preflight、対象探索、entry 生成、hash 鮮度判定、Markdown 描画、並列生成、排他 lock を確認または変更したいとき。

## Do not read this when
- 個別サブコマンド固有の引数定義、利用者向け制御フロー、業務処理だけを調べたいとき。その場合は該当する command 実装へ進む。
- oracle 上の正本仕様、path model、file access rule、INDEX.md entry standard などの仕様意図を確認したいとき。その場合は対応する oracle file を読む。
- AgentCallParameter、FileAccessMode、設定データクラス、enum などの型定義そのものを変更したいとき。その場合は定義側を直接読む。
- 生成済み log や state の利用者向け解析、または特定の保存物を読む側の処理だけを探しているとき。

## hash
- aaa13161bb01bde58287b814caf0aedfa6bce19c8129d0485023ae36a5a452c0

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
- CLI サブコマンド実装を集約する領域で、init、indexing、tui、apply、session、review 系の実行入口とサブコマンド別 orchestration へ進むための入口になる。
- 各対象は CLI runtime 経由の起動、preflight、git 操作、state 更新、Codex subprocess 連携、レポート生成など、利用者向けコマンドの具体的な実行制御を扱う。
- 共通 runtime や低レベル helper そのものではなく、個別サブコマンドがそれらをどう組み合わせて外部挙動を作るかを確認するために読む。

## Read this when
- 特定の CLI サブコマンドの実行順序、preflight、引数受け渡し、利用者向け出力、失敗時処理を確認・変更したいとき。
- init、indexing、tui、apply、session、review のどの実装領域へ進むべきかを選びたいとき。
- apply run、session lifecycle、review oracle、INDEX.md maintenance、初期化、TUI 起動など、サブコマンド単位の制御フローを追いたいとき。
- サブコマンドが git 操作、worktree/branch 管理、state file、Codex Exec/TUI、report 出力、indexing 共通処理へどこから依存しているかを確認したいとき。

## Do not read this when
- CLI 共通 runtime、git wrapper、path model、state file schema、設定読み込み、ignore 判定などの低レベル共通処理だけを調べたいときは、それぞれの共通実装を読む。
- oracle file の正本仕様断片、サブコマンドの外部仕様、prompt builder、LLM 呼び出し詳細だけを確認したいときは、対応する oracle または builder/runtime 側を読む。
- 読むべきサブコマンドや補助モジュールがすでに決まっている場合は、この階層ではなく該当する下位対象へ直接進む。

## hash
- 8ea1d673dd2276b559bbaf9325a03a85ab7e7b0830606e348dc404f6fd1a62e2
