# `acp`

## Summary
- `acp` 名前空間の互換入口をまとめる親パッケージ。`acp.*` を既存利用者向けに残す必要があるかを判断するときや、実体を `oracle.*` 側へ切り替える導線を確認するときに読む。ここには正本実装は置かず、下位の互換入口へ進むための案内だけを持つ。

## Read this when
- `acp` という公開名を残すべきか、削除できるかを判断したいとき。
- 既存の `acp.*` 参照を壊さずに、正本の `oracle.*` 実装へ寄せる経路を確認したいとき。
- 配下の互換入口がどの正本領域を束ねているかだけを先に把握したいとき。

## Do not read this when
- `acp` 配下の具体的な委譲先や実装差分を知りたいだけなら、該当する下位入口を直接読む。
- 互換入口の存廃ではなく、`acp.*` の内部挙動そのものを変えたいだけならここではない。
- 正本の仕様や実装を確認したいなら、`oracle.*` 側を読む。

## hash
- 82a8a0e896b0a52f6e2e625574a9eadacdab826f06480b40a4ebe788ad53d4c5

# `basic`

## Summary
- `basic` 配下の公開面をまとめて案内する入口。ここでは正本実装を置かず、互換 import を維持する層と再公開先への導線だけを読む。
- `basic.acp`、`basic.path_model`、`basic.struct_doc` を残すか切り替えるかを判断するときの起点になる。

## Read this when
- `basic.*` の公開名を残す必要があるか、削除してよいかを判断したいとき。
- `basic` 経由で公開される ACP 型、path model、構造化文書 API の参照先を確認したいとき。
- 互換 import の境界と、どの再公開先を直接読むべきかを見分けたいとき。

## Do not read this when
- ACP 型そのもの、path 解決の本体、構造化文書の型やレンダリング規則など、正本仕様の中身を確認したいときは各再公開先を直接読む。
- `basic` 以外の新規実装配置先を探しているだけなら、ここではなく該当する実装モジュールを読む。

## hash
- 6427f271674f13de9f39976c4fe0d10226ad4c7573c6fa05a58ee5db32f274b7

# `cmoc_runtime.py`

## Summary
- `commons.cmoc_runtime` を現行の公開窓口として import している呼び出し元、または公開 API の互換性を確認したいときに読む。責務は、責務別 runtime module から集約した公開名を 1 つの互換境界として再公開すること。
- この層で確認すべきなのは、`cmoc_runtime` という import path を残すか、どの公開名を外へ出すか、そして `commons.cmoc_runtime` への移行条件である。個別の CLI 挙動や各 helper の内部実装は、再公開先の各 runtime module を直接読む。

## Read this when
- `cmoc_runtime` からの import 互換性、再公開される名前、または静的解析向けの公開契約を確認したいとき。
- 既存の呼び出し元が `cmoc_runtime` を直接 import している前提で、移行先の公開面を崩さずに整理したいとき。
- 公開名の追加・削除・移行条件だけを見たいとき。

## Do not read this when
- CLI の実行ライフサイクルやサブコマンド処理の詳細を知りたいときは、`commons.runtime_cli` を読む。
- Codex 実行、TUI、設定、状態、git、ファイル内容など個別責務の実装や仕様を確認したいときは、それぞれの責務別 runtime module を直接読む。
- この互換境界を変えずに、内部 helper の実装だけを追いたいとき。

## hash
- c0bdd8ba4af0c43cdf13063ff1295c6589df92a67855d06c1c28cf290027ec4d

# `commons`

## Summary
- cmoc の複数実行経路で共有される runtime helper 群の集約点。個別機能の本体ではなく、`commons` 配下の共有基盤をたどる入口として使う。

## Read this when
- 複数モジュールから再利用される共通 helper の所在や公開入口を確認したいとき。
- 共有 helper 群の下位要素へ進む前に、この領域が runtime 共通基盤であることを把握したいとき。

## Do not read this when
- 個別 helper の入出力や失敗時挙動を知りたいとき。この対象ではなく、該当する下位要素を読む。
- CLI 固有の業務ロジックやテスト固有の処理を追いたいとき。共有 helper ではなく、より直接その責務を持つ対象へ進む。

## hash
- 724070cf61c382b210e00610faf029ba4c9e7bb2aa93d98cdfa5793c3a11ad06

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
- `cmoc` の最上位 CLI 入口とサブコマンド接続を案内する対象です。トップレベルのコマンド構成、共通の引数エラー変換、`main()` からの起動経路を確認したいときに読む。
- 個別サブコマンドの実処理ではなく、`doctor` `tui` `session` `apply` `review` `eval-oracle` `indexing` へどの公開名で振り分けるか、また `apply` と `review` の option 値の選択肢を確認したいときに読む。

## Read this when
- `cmoc` のコマンド構成や公開されるサブコマンド名を確認したいとき。
- CLI 引数解析エラーを `cmoc` 形式のエラーレポートへ変換する挙動を変えたい、または確認したいとき。
- `doctor` `tui` `session` `apply` `review` `eval-oracle` `indexing` の入口がどの実装へつながるかを見たいとき。
- `apply` と `review` の option 値の候補や既定値を確認したいとき。
- console script から `cmoc` を起動する最短経路を確認したいとき。

## Do not read this when
- 各サブコマンドの処理内容、状態遷移、レポート生成の詳細を知りたいときは、対応する下位モジュールを読む。
- `cmoc apply fork` や `cmoc review oracle` の手順や仕様本文を確認したいときは、該当する oracle doc を読む。
- `INDEX.md` 更新規則や索引生成の詳細を知りたいときは、`indexing` 側の実装とその仕様を読む。
- git 操作や worktree 操作の詳細を知りたいときは、接続先の実装を読む。

## hash
- 69fb1bf5b1b12340db48a63f99de040ba4942cc13103ba131f4d2123f8f1cdb0

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
- `cmoc` のサブコマンド群をまとめて案内する入口。個別サブコマンドへ進む前に、どの実装層を読むべきかを切り分けるために使う。
- 共通の CLI 基盤や低レベルの branch/worktree 操作ではなく、`apply`、`review`、`session`、`tui` などの機能別入口へ振り分ける役割を持つ。

## Read this when
- `cmoc` のどのサブコマンド実装へ進むべきかを判断したいとき。
- 機能別の入口だけを先に把握してから、個別の実行本体や補助処理に進みたいとき。

## Do not read this when
- 個別サブコマンドの引数、実行順、エラー処理を見たいときは、該当するサブコマンド実装を直接読む。
- session state、review 対象選択、report 生成のような個別責務を追いたいときは、対応する下位モジュールを読む。
- branch や worktree の一般操作、共通ランタイムだけを見たいときは、この階層ではなくより基礎の対象へ進む。

## hash
- 5a99f164641e0f5dcb7d4475571817db9dde16b4a405b3747ec910033330297f
