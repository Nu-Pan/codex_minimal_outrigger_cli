# `acp`

## Summary
- `acp` 互換公開入口と、その配下にある builder 関連の互換入口・実装群を案内するディレクトリ。既存の `acp.*` 参照を維持しながら、`oracle.*` または実体モジュールへ委譲・移行するための入口となる。

## Read this when
- `acp` 公開名や既存 import の互換性を維持・削除する判断をするとき。
- `acp.builder.*` の委譲経路、または apply・quota probe・indexing・review・session・TUI など builder 領域の読む先を判断するとき。

## Do not read this when
- `acp` 配下の特定モジュールの内部実装や正本仕様だけを確認したいとき。該当する実体モジュールまたは `oracle.acp_builder` を直接読む。
- `acp` 互換入口と無関係な機能を調査・変更するとき。

## hash
- 260636d04ac749be845fb420b312882055a92b169c34b907a7bd2c72b0206212

# `basic`

## Summary
- `basic` パッケージの公開互換層。`basic.*` という既存 import 経路を維持するための再公開口がまとまっており、個別の実体仕様ではなく「どの公開名を残すか」「どこから辿るか」を判断するときに読む。

## Read this when
- `basic.*` の互換 import を残すか削除するかを判断したいとき。
- `basic.acp`、`basic.path_model`、`basic.struct_doc` の公開名が何を供給しているかを確認したいとき。
- 既存利用者が `basic` 側の公開面を参照している前提で、移行先や正本側への辿り方を確認したいとき。

## Do not read this when
- ACP 型や path model、構造化文書の本体仕様を知りたいときは、ここではなく正本側を直接読む。
- `basic` という互換入口ではなく、個別の実体定義や変換規則そのものを確認したいとき。
- `basic` 配下の個別モジュールの公開内容だけを知りたいときは、対象モジュールを直接読む。

## hash
- b5f40e564f1a3f6d5658b4601d5f614e8a63d57f7eb0e7e2a673bf62618594a6

# `cmoc_runtime.py`

## Summary
- runtime 実装を別モジュールへ委譲し、既存の import 経路を一時的に維持する互換 shim。公開名と実体の移行期間にだけ意味を持つ。

## Read this when
- runtime module の import 経路、公開 module 名、または互換 alias の残存理由を確認したいとき。
- 呼び出し元を移行した後に、この互換 shim を削除できるか判断するとき。

## Do not read this when
- runtime の具体的な処理内容や責務分割を調べたいとき。この対象は実装本体ではなく委譲だけを扱う。
- 新しい runtime 挙動を追加・変更したいとき。実体側の runtime 実装を読む方が直接的。

## hash
- a36ad0b5d09cbe7d2be546fdafcd27ff3ddaf803744331274a69fb25f15cd7ee

# `commons`

## Summary
- 対象ディレクトリの実装は、cmoc の複数箇所から共有される runtime helper 群をまとめる領域で、Codex 実行、CLI 共通処理、設定・状態・Git・パス・ログ・エラー・Ollama などの横断的な基盤を扱う。個別の責務や実装詳細を確認するための下位モジュールへの入口として機能する。

## Read this when
- cmoc の複数モジュールにまたがる runtime 共通処理の配置や責務の全体像を確認したいとき。
- 特定の helper を読む前に、設定・状態・Git・パス・ログ・Codex 実行などのどの共有基盤へ進むべきか判断したいとき。

## Do not read this when
- 特定の helper の入出力、失敗時挙動、保存形式、実行制御を確認したいときは、該当する下位モジュールを直接読む。
- 個別 CLI サブコマンドの業務フローやテスト固有の処理を調べたいときは、それぞれの直接の実装を読む。

## hash
- 11fb86014feb31590bac877237d2670f393a4972666f3fb1c1571f1b4d7b6968

# `config`

## Summary
- `config.*` 参照を既存利用者向けに維持するための互換入口群。ここでは設定の実体を持たず、正本の oracle src を再公開する経路だけを確認する。
- `config.cmoc_config` から Cmoc 設定型を再公開する入口。設定定義そのものではなく、既存の公開参照を壊さないための接続点として読む。

## Read this when
- `config` からの import 経路を維持・確認したいとき。
- `config.cmoc_config` 経由で Cmoc 系の設定型を参照したいとき。
- 設定の正本を変更せず、互換入口の有無だけを確認したいとき。

## Do not read this when
- 設定仕様そのものを確認したいときは、正本側の oracle src を読む。
- `config.*` 以外の公開面や新規設定追加を扱いたいとき。
- 設定定義の項目意味や保存仕様を調べたいとき。

## hash
- c121a67917bdcc7850097d1a5fc153afb19f375da55ada79794c9c5739b22514

# `main.py`

## Summary
- `cmoc` の CLI 入口をまとめる。トップレベル app と各サブコマンドの接続、共通の引数エラー変換、`main()` からの起動を扱う。
- 個別サブコマンドの実処理そのものではなく、CLI からどの実装へ振り分けるかと、`doctor`・`tui`・`session`・`apply`・`review`・`eval-oracle`・`indexing` の公開面を確認するための入口。
- `cmoc` の全体的な起動条件や option 値の列挙を確認したいときに読む。

## Read this when
- `cmoc` のコマンド構成やサブコマンドの公開名を確認したいとき。
- CLI 引数解析エラーを `cmoc` 形式のエラーレポートに変換する挙動を確認したいとき。
- `doctor`、`tui`、`session`、`apply`、`review`、`eval-oracle`、`indexing` の各 CLI 入口がどの実装へつながるかを確認したいとき。
- `ApplyForkScope` や `ReviewOracleScope` のような CLI option 値の選択肢と既定値を確認したいとき。
- console script から `cmoc` を起動する最小経路を確認したいとき。

## Do not read this when
- 各サブコマンドの処理内容や状態遷移の詳細を知りたいときは、それぞれの sub command 実装へ進む。
- `cmoc apply fork` や `cmoc review oracle` の詳細な手順・レポート形式を知りたいときは、このファイルではなく該当する oracle doc を読む。
- `INDEX.md` の更新規則や索引生成の詳細を知りたいときは、`indexing` の実装とその対象資料を読む。
- CLI の見た目ではなく、実際の git 操作や worktree 操作の詳細を知りたいときは、接続先の実装を読む。

## hash
- f903f580144c8a4ca2d67d9a8e0558542f9fbaaf2acfa2cbbb697979c6750788

# `oracle.py`

## Summary
- `src` から `oracle.*` を import したときに、正本側の実装群へ解決させるための境界を見る入口。`oracle` 名前空間の参照先を切り替える仕組みだけを扱い、個別の oracle 実装内容を追う前段として読む。

## Read this when
- `src` 経由の import で正本側 `oracle.*` が見つからない、または参照先の切り替え方法を確認したいとき。
- `oracle` 名前空間を packaged realization ではなく正本ソースへ向ける必要があるかを判断したいとき。

## Do not read this when
- `oracle.*` 配下の個別機能や実装内容を知りたいときは、ここではなく正本側の該当モジュールを読む。
- 通常のアプリ機能や CLI の挙動を追いたいだけなら、この import 解決の仕組みは読まなくてよい。

## hash
- 7ef36bb425d49e4907bce740821b18302da678a21b33bf887d9fd94c111929a5

# `sub_commands`

## Summary
- CLI のサブコマンド実装を集約する領域。apply・session・review のライフサイクル処理と、oracle 評価、INDEX 更新、doctor、TUI の実行入口を扱う。
- 各サブコマンドの入口から、state・branch・worktree・Codex 実行・report 生成などの専用実装へ進むための起点となる。

## Read this when
- サブコマンドの実行入口や、apply・session・review・TUI などの処理群から読むべき実装を選びたいとき。
- apply または session の fork・join・abandon、branch/worktree と state のライフサイクルを調べたいとき。
- review oracle の対象選定、実行ループ、finding の検証・判定、INDEX 差分の merge、report 出力を追いたいとき。
- oracle 評価、INDEX 更新、doctor preprocess、TUI 起動の CLI 接続を確認したいとき.

## Do not read this when
- サブコマンド共通の CLI ルーティング、state 操作、worktree 操作、Git 操作だけを調べたいときは、対応する共通 runtime 実装へ直接進む。
- 特定の prompt builder、report 描画、path 解決、対象列挙など単一の補助責務だけを調べたいときは、この領域全体ではなく該当する専用実装へ直接進む。
- apply・session・review と無関係なサブコマンドの実装を調べたいとき。

## hash
- 23fec24fe7617e706f2a6a890c038fcff7cd8d9d455df61eddd3e0b1cf15423d
