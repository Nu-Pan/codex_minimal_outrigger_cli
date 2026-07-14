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
- このリポジトリの最上位の案内ページとして、cmoc の概要、初期セットアップ、`bin` を PATH に通す手順、基本ワークフローへの導線、作業時の注意点をまとめる入口です。
- 新規参加者や、まず何を読めばよいかを確認したいときに読む対象で、詳細な挙動や個別コマンド仕様は下位の正本仕様へ進む前の起点になります。

## Read this when
- cmoc 全体の入口として、概要と最初に必要なセットアップ手順を確認したいとき。
- `cmoc` コマンドを使い始める前に、実行方法や PATH 設定の前提を把握したいとき。
- 基本ワークフローの起点だけを知りたいとき。
- ターミナル操作上の注意点を含め、利用開始時の最低限の案内を探しているとき。

## Do not read this when
- 個別サブコマンドの実行条件や入出力を知りたいときは、対応する正本仕様を読む。
- `oracle` 配下の具体的な作業フローを知りたいときは、基本ワークフローから辿れる専用文書を読む。
- 環境診断、実装詳細、エラー処理、状態管理の仕様を知りたいときは、README ではなく各機能の正本仕様を読む。

## hash
- c6c3f3c5798ecc63f8611a40982f7bc8100116d8a934616bbd2b2a5b5e0a1afc

# `bin`

## Summary
- `cmoc` を起動するための薄いシェルラッパー。リポジトリルート基準で仮想環境 Python を探し、補完プローブも含めて Python 実装への委譲口になる。
- 仮想環境 Python が見つからない、または実行できない場合に、利用者向けの Markdown 形式エラー、セットアップ手順、簡易 call stack を出して失敗する。

## Read this when
- `cmoc` の起動時に、どの Python 実装へ委譲されるかを確認したいとき。
- 仮想環境がない場合の起動失敗挙動や、補完プローブ時に通常起動と異なる分岐を取る理由を確認したいとき。
- 起動前エラーの文面、セットアップ手順、表示用パス、call stack 行番号の組み立てを変更・確認したいとき.

## Do not read this when
- Python 側の CLI サブコマンド、引数解析、業務ロジック、実行後の出力内容を調べたいとき。
- 仮想環境の作成方法そのものや、パッケージ設定を変更したいとき。
- oracle file や path model の正本仕様を確認したいとき。

## hash
- bcc444f615624a979df5ebba33008d88c68e9f32a99b58386f9f0158f7e98b02

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
- `src` 配下の realization 実装の起点。`main.py` の CLI 入口、`commons` の共有 runtime ヘルパー、`sub_commands` の各サブコマンド実装、`acp` 互換レイヤー、`basic` の正本再公開レイヤー、`config` と `oracle` の import shim を束ねる上位ルートとして読む。
- 個別機能の本体ではなく、どの名前空間が互換入口でどれが実装本体かを見分けるための階層。公開 import 面、CLI 委譲先、共有 helper の入口、正本側への橋渡しがこの層の主な関心事であり、詳細な処理仕様を追う入口としては使わない。

## Read this when
- `src` 全体の公開面を俯瞰し、CLI 入口・共有 helper・サブコマンド・互換 shim・正本再公開レイヤーのどこへ進むべきかを決めたいとき。
- `acp.*`、`basic.*`、`config.*`、`oracle.*` の import 経路がこの実装側でどう維持されているかを確認したいとき。
- 新しい実装を追加する前に、既存の上位ルートがどの責務を持ち、どの下位実装へ委譲しているかを見て境界を把握したいとき。

## Do not read this when
- CLI の具体的な引数・エラー表示・サブコマンド挙動を知りたいときは、`main.py` や各 `sub_commands` の対象を直接読む。
- `commons` の個別 helper の入出力や失敗時挙動を知りたいときは、この上位層ではなく該当モジュールを読む。
- `acp` や `basic` の正本仕様そのもの、または `config` や `oracle` の個別実装詳細を確認したいときは、対応する下位対象へ進む。

## hash
- 7e688893627a47bdc9348b9eb6c9edf70ff0c917120c4542958c676c3243ec33

# `test`

## Summary
- `test` 配下の回帰テスト群の入口。`src` と `oracle` の境界をまたいで、CLI 振る舞い、runtime、prompt 生成、indexing、session / apply / doctor の外部挙動を確認したいときにこの階層へ進む。

## Read this when
- 現行の CLI 振る舞いを変えていて、対応する回帰テストを探したい。
- runtime、prompt builder、indexing、session、apply、doctor の外部挙動を確認したい。
- `src` 側の実装変更に対して、どのテストが観測点になるかを絞り込みたい。

## Do not read this when
- 個別機能の実装だけを追いたいときは、対応する `src` 側を先に読む。
- 正本仕様そのものを確認したいときは、対応する `oracle` 側を読む。
- テスト基盤ではなく、実装・仕様・CLI の流れだけを追いたいときは、この階層全体を読む必要はない。

## hash
- 60119930121a210b3270505d6f6b1387dcbd3fbf1e6e3bc0aa61b48b31631c59
