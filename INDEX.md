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
- このリポジトリを VS Code で開くときの作業環境設定をまとめる。Python の既定インタプリタ、フォーマッタ、解析対象の参照先、エディタ表示設定を確認したいときに読む。

## Read this when
- ワークスペースを開いたときの Python 実行環境や補完対象を確認したい。
- 保存時フォーマットや Markdown の編集挙動をこのリポジトリ用に揃えたい。
- エディタがどの領域を Python の解析対象に含めるかを見たい。

## Do not read this when
- アプリの振る舞い、CLI 仕様、oracle の正本仕様を確認したい。
- 個別モジュールの実装やテストの入口を探したい。
- リポジトリ共通の開発手順や役割分担を知りたい。

## hash
- 0aef4837a05e9d291d84fe5e797cb6d07510ae5318130596773c0bd604f435e5

# `oracle`

## Summary
- `oracle/doc` と `oracle/src` への入口をまとめる最上位ルーティング対象。ここでは正本仕様断片と生成入口の所在を見分け、個別本文や実装詳細へ直接進む前に読む先を切り分ける。

## Read this when
- `oracle` 配下で、まず `doc` と `src` のどちらへ進むべきか判断したいとき。
- 正本仕様断片そのものを読む前に、仕様本文と生成入口の責務境界を確認したいとき。
- 共通定義や下位の正本群を探していて、読む対象を先に絞り込みたいとき。

## Do not read this when
- 個別テーマの正本本文を確認したいときは、対応する下位文書を直接読む。
- `oracle` 配下の実装や生成詳細を詰めたいときは、この入口ではなく下位の定義元へ進む。
- `oracle` 全体の案内ではなく、特定の仕様断片やサブ領域だけを知りたいとき。

## hash
- 319117d469b017438d7a35dc1a9c5b3e08261c371ff7b1ba00c646d9c69163d2

# `pyproject.toml`

## Summary
- プロジェクトの配布・実行・検証の基準になる設定本体です。インストール方法、コマンド公開名、依存関係、ビルド方式、pytest・ruff・mypy の前提を確認したいときに読む。ここはアプリ挙動の実装本体ではないので、機能の細部やサブコマンド処理を追う目的ではなく、プロジェクト全体の構成や開発設定を変えるときの起点として使う。

## Read this when
- 依存関係や Python 要件を変えたい、または追加したいとき。
- `cmoc` の公開エントリーポイント、ビルド方式、パッケージング方針を確認したいとき。
- pytest、ruff、mypy の適用範囲や前提条件を確認したいとき。
- プロジェクト全体に効く開発・配布設定を変える前に、基準を一箇所で把握したいとき。

## Do not read this when
- 個別機能の仕様や CLI 挙動を確認したいときは、対応する実装や仕様文書を読む。
- サブコマンドの詳細な実行経路やエラー処理を追いたいときは、この設定ではなく該当モジュールを読む。
- 索引の読み方や対象ファイルの選び方だけを知りたいときは、各階層の `INDEX.md` を読む。

## hash
- 61534104849ba1a0689bfa1d1cba44297dcdc6ea0f4c614f73f351d91c9ddfd4

# `src`

## Summary
- `cmoc` 実行系の最上位ルーティングを担う `src` の入口。CLI 起動点、`oracle.*` への解決 shim、互換公開面、共有 runtime、設定再公開、機能別サブコマンド群を束ねており、まずどの責務の下位モジュールへ進むかを切り分けるために読む。
- ここで確認するのは、`main.py` と `oracle.py` の公開境界、`acp`・`basic`・`config` の互換層、`commons` の共有基盤、`sub_commands` の機能別入口である。個別の実装差や仕様本体は、該当する下位モジュールを直接読む。

## Read this when
- `cmoc` の起動経路やトップレベルのサブコマンド接続を把握したいとき。
- `src` から `oracle.*` を解決する仕組みや、`acp`・`basic`・`config` の互換 import を維持すべきか判断したいとき。
- 共有 runtime helper の入口と、`apply` `review` `session` `tui` `indexing` などの機能別サブコマンドにどこで分かれるかを先に絞りたいとき。

## Do not read this when
- CLI 個別コマンドの詳細な処理や失敗時挙動を知りたいだけなら、対応する `sub_commands` の下位モジュールを直接読む。
- 設定定義、ACP 型、path model、構造化文書、review 対象選択などの正本仕様そのものを確認したいなら、互換層ではなく正本側を読む。
- `src` 配下のどの公開名を残すかではなく、特定 helper の内部実装を追いたいだけなら `commons` や該当サブコマンド側へ進む。

## hash
- c8fa5a02f8496869af14c9f7167958e648957bae4dff3696a75962cf5bdd91a0

# `test`

## Summary
- `test` 配下の回帰テスト群への入口。CLI 外部挙動、runtime 契約、ACP builder の互換性、prompt 生成、review / apply / session / indexing / doctor / Codex 実行まわりの境界を、目的別に読み分けるために使う。
- 個別の実装ではなく、変更対象がどの機能群に属するかを見分けてから下位の専用テストへ進むためのルーティング層。共通 helper の詳細より、各サブコマンドや runtime 契約の外部挙動を確認したいときに読む。

## Read this when
- CLI の外部挙動や runtime 契約が変わる変更で、どのテスト群を読むべきか判断したいとき。
- `apply`、`session`、`review oracle`、`indexing`、`doctor`、`tui`、`codex exec` など、機能別の回帰テストへ進む入口を探したいとき。
- 共通 helper ではなく、機能ごとの統合テストや契約テストの責務境界を知りたいとき。

## Do not read this when
- 個別テストの内部 fixture や helper の実装を直したいときは、該当モジュールの本文へ進む。
- 正本仕様や prompt 本文そのものを確認したいときは、`oracle` 配下の文書や src を直接読む。
- 単一の runtime helper や builder 実装だけを追いたいときは、この上位ルーティングではなく、より直接の対象ファイルを読む。

## hash
- 4424a1b04e6e6cea41c0cdfe035b1b914e2d499b153528cab138de6ede5ca355
