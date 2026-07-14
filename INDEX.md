# `LICENSE`

## Summary
- This file is the repository's license grant and warranty disclaimer. Read it when you need to confirm redistribution rights, attribution obligations, or liability terms for using the project in another codebase or release.
- It is the right place to consult for legal permission questions about copying, modifying, sublicensing, or distributing the software.

## Read this when
- You need to know whether the project can be reused, copied, modified, merged, published, sublicensed, or redistributed.
- You need to confirm whether attribution or the license notice must be preserved in derived or distributed copies.
- You need the warranty and liability terms that apply to use of the software.

## Do not read this when
- You are looking for implementation behavior, CLI usage, configuration, or development workflow.
- You need repository structure or routing guidance; a different `INDEX.md` is the better entry point.
- You need project-specific legal exceptions or additional terms, which would have to be stated in another file.

## hash
- a894f2547af0349f234986eb4661f0146f37b7d82f8b22a27a674d5c1236f08f

# `README.md`

## Summary
- この文書はリポジトリ全体の入口で、cmoc の概要、初期セットアップ、最初に押さえるべき使い方を短く案内する。新規導入時や、まず全体像と実行開始手順を確認したいときに読む。
- 詳細な運用手順はここではなく、基本ワークフローを定義する正本へ進むための起点として扱う。

## Read this when
- このリポジトリを初めてセットアップするとき。
- cmoc の役割と、最初に何を行うかを短く把握したいとき。
- 基本的な使い方の入口を探していて、詳細仕様へ進む前段階にいるとき。

## Do not read this when
- 個別コマンドの詳細な振る舞いを知りたいだけのときは、該当する仕様文書を直接読む。
- リポジトリ固有の開発ルールや補助規約だけを確認したいときは、この文書ではなくそれらの正本を読む。
- すでにセットアップ済みで、目的の操作手順も分かっているときは再読しなくてよい。

## hash
- e4571c78602bbcf0bc912efbea8f14f9fd0494760f2a334e3affef69cb32741b

# `bin`

## Summary
- `cmoc` の起動ラッパー。仮想環境の Python を確認し、補完要求か通常起動かを切り替えて `src/main.py` へ渡す。

## Read this when
- `cmoc` の実行前提、特に `.venv` の存在確認と、欠落時に出す案内を確認したいとき。
- シェル補完のときだけ別経路で起動する条件を確認したいとき。
- `cmoc` から実際の CLI 実装へどう入るかを追いたいが、各サブコマンドの処理本体までは不要なとき。

## Do not read this when
- 各サブコマンドの引数解釈や業務ロジックを知りたいときは `src/main.py` や該当サブコマンド実装を読む。
- 仮想環境のセットアップ手順そのものや、利用者向けの運用説明だけが目的なら、このラッパーではなく上位の利用案内を読む。

## hash
- ca144e1b915722cdfe8a460aa67f416f69bc3eac2aea5de84869eaa1f907025e

# `codex_minimal_outrigger_cli.code-workspace`

## Summary
- VS Code のワークスペース設定を確認・変更するときに読む。ここには、このリポジトリを開いたときの既定インタプリタ、Python の解析対象、エディタ既定設定、非表示対象の方針がまとまっている。
- 日常的な実装変更やテスト追加では通常読まない。そうした作業は各実装・テスト・関連 `INDEX.md` を優先し、このファイルはエディタ環境やワークスペース構成に関する判断が必要なときだけ参照する。

## Read this when
- このリポジトリを VS Code のワークスペースとして開くとき
- Python の実行環境や解析対象の既定を確認したいとき
- エディタ側でどのファイルを見せるか・隠すかの方針を変えたいとき

## Do not read this when
- アプリケーションの挙動や CLI の仕様を確認したいとき
- 実装やテストの変更先を探したいとき
- 既存の各領域の `INDEX.md` や本文を読むべき作業をしているとき

## hash
- 1938307f70f255710d75d39c07d860ecb381acbb031ca19b2f2b6e565ac41acb

# `oracle`

## Summary
- cmoc の正本仕様文書群の入口。仕様レベルで全体像をつかみ、個別機能・横断ルール・採用しなかった案のどれを読むべきかを切り分けるために使う。
- この階層は実装手順の入口ではなく、読むべき下位の正本文書へ進むためのルーティングに使う。

## Read this when
- cmoc の挙動や設計を仕様レベルで確認したいとき。
- どの正本文書を先に読むべきか判断したいとき。
- 機能仕様、共通ルール、採用しなかった案のどれを読むべきか切り分けたいとき。
- CLI の横断仕様、実装規約、テスト規約、環境条件を確認したいとき。

## Do not read this when
- 利用手順だけを知りたいとき。
- 読むべき個別文書がすでに分かっているとき。
- 実装やテストの詳細だけを追いたいとき。
- 特定の不採用案の背景だけが必要なとき。

## hash
- 9813fb19ca96c4e14207f1ffbf3374663050a6d579d04a651f384b8e6565dcf6

# `pyproject.toml`

## Summary
- プロジェクトの配布・インストール・テスト実行に関わる設定の正本。依存関係、`cmoc` のエントリポイント、`src` と `oracle/src` のパッケージ配置、pytest の import パスを確認・変更したいときに読む。

## Read this when
- 新しい依存を追加・更新したい。
- `cmoc` の起動方法や公開エントリポイントを変えたい。
- `src` / `oracle/src` のパッケージ配置や配布対象を確認したい。
- pytest から `src` と `oracle/src` を import できる前提を変えたい。

## Do not read this when
- 個別の CLI 挙動やサブコマンド仕様を確認したい場合は、各サブコマンド側の文書や実装を先に読む。
- 実装ロジックやテストケースの詳細を追いたい場合は、`src` や `test` の該当ファイルを直接読む。
- 配布メタデータではなく利用手順を知りたい場合は、README を読む。

## hash
- d01948ab1730e2747d529d49d8c8ca10b84bd6a86e19d7b2810ee87c95ccb904

# `src`

## Summary
- `src` は公開 import の受け口と正本実装の接続点をまとめる階層で、`acp` や `basic` の互換公開名、`config`・`oracle` の参照切替、`main.py` の CLI 入口、`commons` の共通基盤、`sub_commands` の機能分岐を見分けるために読む。実装詳細を追う前に、どの責務の本体へ進むべきかを切り分けるためのルーティング層として扱う。
- ここで読むべきなのは、公開名を残すか、どの実体へ辿るか、どの上位入口から下位責務へ進むかを判断するときであって、個別機能の仕様本文そのものではない。

## Read this when
- 公開 import 名や互換入口を残すべきか、削除や置き換えが可能かを判断したいとき。
- `acp`、`basic`、`config`、`oracle` のような正本実装への接続点を確認したいとき。
- CLI の全体入口から、`doctor` や `tui`、`session`、`apply`、`review` などのどの実装へ進むべきか整理したいとき。
- 共通基盤の責務境界と、個別サブコマンド実装の境界を先に切り分けたいとき。

## Do not read this when
- 個別モジュールの具体的な処理内容や挙動を知りたいだけなら、直接その対象モジュールを読む。
- 互換入口の存廃ではなく、内部の実装差や処理順を調べたいだけならここではない。
- 正本仕様そのものや機能の詳細を確認したいときは、この階層ではなく対応する実体側を読む。

## hash
- 4cfb03eeef80793bd0f4e3ad7fcfc90b69a1b52f7238726fea39c886bfaf878f

# `test`

## Summary
- Test 領域全体のルーティング入口です。共通 test support と個別の回帰テストを、対象の挙動ごとに選び分けるために使います。

## Read this when
- まず test 配下で読むべき補助モジュールや回帰テストを絞り込みたいとき。
- CLI、runtime、indexing、review oracle、apply、session、Codex 呼び出しのどれに属する test かを見分けたいとき。
- 共通 helper を読むべきか、個別テストを読むべきかの境界を確認したいとき。

## Do not read this when
- すでに読むべき個別 test ファイルが特定できているとき。
- 対象の正本仕様そのものを確認したいときは、対応する oracle 側を先に読むべきです。
- test 配下の一覧だけを見たいときは、この directory entry ではなく個別ファイルへ進んでください。

## hash
- 801de085db4e988507d618225071758cb9e0962af508d46f99dd423f52006c77
