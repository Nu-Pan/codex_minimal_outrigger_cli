# `acp`

## Summary
- ACP builder 領域への実装側入口。既存の `acp.*` import 参照を維持する互換入口と、quota probe など実装側で持つ agent call parameter builder への下位入口をまとめる。
- 正本側 builder を複製せず参照するための互換層と、実際に parameter を組み立てる下位領域を切り分けるためのルーティング対象。

## Read this when
- ACP builder 全体から、目的の agent call parameter 生成処理または互換入口がどの下位領域にあるかを選びたいとき。
- 既存の `acp.*` import 参照、正本側 builder への委譲、公開参照経路、互換入口の削除条件を確認したいとき。
- apply fork、review oracle、session join、TUI 起動、file access recovery、indexing、quota probe などの builder 関連処理の入口を探しているとき。
- builder 領域にある対象が、正本側への薄い再公開なのか、実装側で parameter を生成する処理なのかを見分けたいとき。

## Do not read this when
- 個別 builder の関数、型変換、prompt 補正、import 経路補正、schema fallback などの具体処理を直接確認したいときは、該当する下位領域へ進む。
- agent call parameter の基礎型、model、reasoning effort、file access mode の定義を調べたいときは、基礎定義側へ進む。
- CLI コマンドの制御フロー、branch 操作、diff 生成、Codex CLI 実行、TUI 描画など、parameter builder 以外の実処理を調べたいときは、それぞれの実行側へ進む。
- 正本仕様断片、prompt の正本文面、oracle 側 builder 本体、indexing や review の仕様そのものを確認したいときは、対応する oracle 側の本文へ進む。

## hash
- 79f02f6a83cdd11df298cb43e21c3b55bf875861f43fb9485447172ee7f7b976

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
- cmoc の共通ランタイム支援を集める実装ディレクトリ。Codex 実行、CLI 共通ライフサイクル、設定、Git、ログ、パス、状態、INDEX.md 自動更新など、複数領域から使われる runtime helper とその再エクスポート入口を持つ。
- 個別の runtime_* モジュールへ進むための入口であり、共通処理の実装場所、互換 import、責務別 helper の所在を判断するために使う。

## Read this when
- CLI サブコマンド、Codex exec/TUI、Git、設定、ログ、状態、パス、INDEX.md 更新などにまたがる共通 runtime 実装の所在を探したいとき。
- 複数の runtime helper をまとめて import する集約入口や、旧 import path を保つ互換 module の責務を確認したいとき。
- Codex 実行前 preflight、INDEX.md 自動更新、Structured Output 検証、quota/capacity retry、file access rule 検査など、共通実行基盤の制御を追いたいとき。
- サブコマンド共通の開始・完了表示、例外表示、ログ記録、実行結果型、永続 state、設定 JSON、runtime 保存先 path などの共通部品を変更したいとき。

## Do not read this when
- 個別 CLI コマンドの引数定義、利用者向け制御フロー、業務処理だけを調べたいときは、そのサブコマンド実装へ直接進む。
- oracle 上の正本仕様や path placeholder の概念定義、INDEX.md の仕様意図だけを確認したいときは、対応する oracle doc または仕様側を読む。
- 特定の低レベル処理だけを調べたい場合は、この階層全体ではなく、Git、設定、path、content、error、logging、state、Codex profile など責務に対応する module を直接読む。
- 公開 import 面ではなく新しい業務ロジックを追加したいだけのときは、共有 runtime に置く必要があるかを確認し、該当する上位実装を先に読む。

## hash
- 52acc5047b83b6eae6c3bd0d70dae0e32758cee0ae223765f1d163d29c3e0d4f

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
- CLI サブコマンドごとの実行入口と制御実装を集める領域で、初期化、索引更新、TUI、session lifecycle、apply lifecycle、review oracle などの利用者操作を runtime・git・状態管理・Codex 実行へ接続する。
- 各サブコマンドは、実行前条件の確認、対象 worktree や branch の準備、状態更新、commit・merge・cleanup、利用者向け出力や report 生成までの大きな制御順序を担う。
- 詳細な共通処理や仕様断片そのものではなく、利用者が起動する操作から下位 helper・共通処理へ入るためのサブコマンド別オーケストレーションを探す入口になる。

## Read this when
- cmoc の特定サブコマンドが、CLI runtime からどのように起動され、どの preflight、状態確認、git 操作、出力処理へ進むかを確認または変更したいとき。
- 初期化、索引更新、TUI、session の開始・統合・破棄、apply の開始・破棄・取り込み、review oracle の実行など、利用者操作単位の実装箇所を選びたいとき。
- サブコマンド実行時の branch/worktree 作成、対象列挙、Codex 実行、pid や state の扱い、commit・merge・conflict 処理、cleanup、report 出力の入口を追いたいとき。
- サブコマンド固有の補助処理と、共通 runtime helper、git helper、状態管理、prompt builder、report builder など下位領域との接続位置を切り分けたいとき。

## Do not read this when
- CLI 全体のアプリ登録、Typer 構成、runtime 共通規約、path 解決、git 実行 wrapper、state schema、設定モデルなど、サブコマンド横断の低レベル共通処理だけを調べたいとき。
- INDEX.md の本文生成、oracle file の正本仕様、prompt や Structured Output schema、LLM 出力品質、設定値定義など、サブコマンド制御ではない詳細を確認したいとき。
- 特定のサブコマンド内でも、対象列挙、review loop、report rendering、merge conflict 解決、Codex subprocess 起動などの下位詳細だけを調べる場合で、より直接の実装領域が分かっているとき。
- テスト、fixture、oracle 側ドキュメント、または利用者向け仕様だけを探しており、realization implementation のサブコマンド実行フローを読む必要がないとき。

## hash
- 2b844e55f7f67ead55a46e11118fbfe054f57b1691b87dee013942e78bdbae6c
