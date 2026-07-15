# `acp`

## Summary
- `acp` 互換の公開入口をまとめる階層で、既存の `acp.*` 参照を壊さずに正本実装へ進むための導線を扱う。
- 配下の互換入口は、名前解決・委譲・移行経路の確認が主目的で、実体仕様を読む場所ではない。
- `common` は現時点で実体を持たない目印として扱い、共通処理の本体を探す入口にはしない。

## Read this when
- `acp` という公開名を残すべきか、削除できるかを判断したいとき。
- 既存の利用者向け参照を壊さずに、`oracle` 側の実体へ切り替える導線を確認したいとき。
- 既存の `acp.builder.*` import を維持したまま、どの実体へ進むべきか整理したいとき。
- 互換層を残す必要があるか、削除や置き換えが可能かを見極めたいとき。

## Do not read this when
- `acp` 配下の具体的な実装内容や移行先の詳細を知りたいだけなら、直接その実体モジュールを読む。
- 互換入口の存廃ではなく、`acp.*` の内部挙動そのものを変えたいだけならここではない。
- 実装本体や機能仕様を知りたいときは、この階層ではなく対応する正本側のモジュールを読む。
- `common` に実装がある前提で読むべきではない。

## hash
- fc9f0af91ccee72360f126f08015e64058d869a21efbd45fd17da3b90bc0bf60

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
- `src/sub_commands` 配下の CLI サブコマンド実装をまとめた入口。apply、review、session、tui、doctor、indexing などの起動処理と、各ライフサイクル・評価・レポート・パス解決の実装へ進むためのルーティングを提供する。

## Read this when
- サブコマンド全体から、目的に応じて読むべき実装ファイルを切り分けたいとき。
- apply、review、session、tui などの開始・実行・終了フローの入口を確認したいとき。
- レビュー対象選定、oracle 評価、レポート生成、INDEX 更新など、サブコマンド単位の責務分担を把握したいとき。

## Do not read this when
- 特定サブコマンドの詳細な引数、制御フロー、エラー処理を調べるときは、対応する実装ファイルを直接読む。
- 共通 helper、状態管理、Git の低レベル操作、個別の prompt・report・path 処理だけを調べるときは、それぞれの定義元を直接読む。
- CLI 全体の共通起動処理や、サブコマンド以外の実装を調べるとき。

## hash
- 6814f39c454242d9f8981bf5682fc5ca03314b8e04e21f9c35f99dc4f4ec4bb4
