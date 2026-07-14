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
- `commons` 配下の共通 runtime helper 群の入口をまとめる領域。複数のサブコマンドや実行経路から共有される設定、状態、Git、パス、ログ、エラー、Codex 実行、Ollama、doctor、preprocess などの共通処理へ進む前に、どの責務の実装を読むべきかを分けるためのルーティング起点として扱う。
- 個別 helper の実装差ではなく、まず共通基盤全体の責務境界を確認したいときに読む。特定の機能だけを追う場合は、この領域ではなく対応する下位モジュールを直接読む。

## Read this when
- `cmoc` の実行時に複数モジュールで共有する基盤処理の入口を探したいとき。
- 設定、状態、Git、パス、ログ、エラー、Codex 実行、Ollama、doctor、preprocess のどれを読むべきかを切り分けたいとき。
- 共通 helper 群のパッケージ境界を確認してから、個別の責務へ進みたいとき。

## Do not read this when
- 特定の helper の入出力や失敗時挙動を知りたいとき。該当する下位モジュールを直接読む。
- CLI コマンド固有の処理やテスト固有の処理を調べたいとき。共通 runtime helper ではなく、より直接その責務を持つ対象へ進む。
- この領域の下位要素を既に特定しているとき。入口ではなく対象モジュール本文を読む。

## hash
- f9f019fdc740c9d8c36be1b477091f513c16b0783accadac94a1a74f9a3f5d03

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
- `cmoc` のサブコマンド群全体の入口。個別コマンド本体へ進む前に、どの機能がどの実装へ分かれているかを切り分けたいときに読む。
- 共通の起動基盤よりも、`apply` `review` `session` などの責務分担を先に把握したいときのルーティング点になる。
- ここではコマンド群の境界を確認し、細部の引数処理や実行フローは各サブコマンド側へ進む。

## Read this when
- `cmoc` のどのサブコマンド実装を読むべきかを先に判断したいとき。
- サブコマンド群の役割分担だけを確認してから、個別の実行本体へ進みたいとき。
- `apply` `review` `session` などのまとまりごとに、読む対象を絞り込みたいとき。

## Do not read this when
- 特定サブコマンドの引数、制御フロー、エラー処理を調べたいときは、対応する実装ファイルを直接読む。
- 共通の起動処理や CLI 全体の基盤だけを知りたいときは、より上位の入口を読む。
- 結果表示やレポート文面など、個別機能の下位責務を見たいときは、この階層ではなく該当機能の実装へ進む。

## hash
- eb560de04b41bfee108c99b875fc5ac16fa7d609907546bfa9730ace31e39182
