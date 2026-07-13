# `acp`

## Summary
- `acp` 系の公開入口をまとめる上位領域。`oracle.acp_builder` 側の正本実装へつなぐ互換導線と、配下の機能別入口を読むための分岐点として使う。
- この階層は実装本体ではなく、旧 `acp.*` 参照をどこへ維持するか、どこから実体実装へ進むかを判断するための案内に限定される。

## Read this when
- `acp.*` の旧 import 互換を残す必要があるか、削除できるかを判断したいとき。
- 正本側の実装を保ちながら、この領域がどの機能入口を公開しているかを確認したいとき。
- 互換入口の削除条件や、配下の機能別入口へ進むべきかを選びたいとき。

## Do not read this when
- 正本の実装内容そのものを確認したいときは、ここではなく実体側の領域を読む。
- 個別機能の挙動や内部処理を調べたいときは、上位の互換案内ではなく該当する下位領域を読む。
- `acp.*` 参照がすでに不要かどうかだけを確認済みで、互換導線の詳細が不要なとき。

## hash
- 3681d21e3acf193cc38bf135dd703e4f4882dcd64a572df3d32f6219be206ab9

# `basic`

## Summary
- oracle src 側の基本 API を realization 側の既存公開面から再公開する互換層。ACP 型、path model、構造化文書 API などを複製せず、正本側定義への参照として維持する入口をまとめる。
- 既存の `basic.*` import 経路を残すための領域であり、削除可否は realization 側と利用者向け公開面から対応する互換参照がなくなり、正本側または実体 module への移行が済んでいるかで判断する。

## Read this when
- realization 側で `basic.*` 経由の公開 import 経路や互換維持を確認したいとき。
- oracle src 側の正本定義を複製せず、既存参照へ再公開している箇所を探したいとき。
- ACP 型、path model、構造化文書 API の互換再公開を残す理由、公開名、削除条件を確認したいとき。

## Do not read this when
- ACP 型、path placeholder、構造化文書処理そのものの仕様や実装詳細を確認したいとき。その場合は再公開先の正本側実装を読む。
- `basic.*` 互換参照や公開 import 経路ではなく、一般的な CLI 挙動、テスト挙動、path 変換仕様の検討をしているとき。
- 新しい基本 API や公開面を追加する実装場所を探しているとき。

## hash
- ad0cfb03fb2c682437a55ec2ac464197bd2fc5eb3bb3da22e79f7473d62523e7

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
- cmoc の複数領域から再利用される共通補助処理を束ねるパッケージ境界。個別の実装詳細ではなく、共有 helper 群の入口としてどこから進むべきかを判断するために読む。

## Read this when
- 複数モジュールから使う共通 helper の置き場所や、この領域が共有補助の入口かどうかを確認したいとき。
- 共有 helper 群へ進む前に、このまとまりが実行時の共通基盤に属することを確認したいとき。

## Do not read this when
- 特定 helper の入出力、失敗時挙動、内部アルゴリズムを確認したいとき。該当する下位要素を直接読む。
- CLI コマンド固有の処理やテスト固有の処理を調べたいとき。共有 helper ではなく、より直接その責務を持つ対象を読む。

## hash
- a3e9b270c4255ef03b2d425f740765a9b39cd67edf04c1c8ed9d38512cc8af80

# `config`

## Summary
- oracle src 側の設定実装を正本に保ちながら、realization 側に残る旧来の `config.*` import を受け止める互換入口をまとめるディレクトリ。
- 設定定義や設定ロジック本体は持たず、正本側の定義を複製せず再公開する境界を確認する入口になる。

## Read this when
- 旧来の `config.*` import が realization 側でどこに受け止められているか確認したいとき。
- 正本側の設定実装を複製せず参照・再公開する互換方針に関わる変更を行うとき。
- 既存の公開参照や互換 import を削除・置換できる条件を判断したいとき。

## Do not read this when
- 設定値の定義、意味、読み込み、検証などの本体挙動を確認したいとき。
- oracle src 側の正本となる設定実装そのものを確認したいとき。
- 互換 import の維持や再公開経路に関係しない設定項目追加・実装変更を行うとき。

## hash
- 97eb1bfd8f73945ab835c22962809b5a59009f2d7e1581a56e7058b6c8c786a4

# `main.py`

## Summary
- Typer ベースの cmoc CLI 入口を定義し、root command と session/apply/review 配下の subcommand を各実装関数へ接続する。
- CLI 引数解析エラーを cmoc のエラーレポート形式に変換する group、補完時の例外処理回避、console script からの起動責務を持つ。
- scope option の公開値や alias command など、利用者が直接触れる command 面の薄い配線を扱う。

## Read this when
- CLI command、subcommand、option、alias、console script 起動の追加・変更・削除を確認したいとき。
- Typer/Click の引数解析エラーが cmoc 形式で表示される経路、または shell completion 時の挙動を確認したいとき。
- CLI 入口からどの sub command 実装へ委譲されるか、scope option が実装へどう渡るかを確認したいとき。

## Do not read this when
- 各 command の実処理、git 操作、worktree 操作、review/apply/session の制御内容を知りたいだけなら、対応する sub command 実装を直接読む。
- cmoc 共通 error 型や error 表示本文の構造を変更したいだけなら、runtime 側の定義を読む。
- oracle や INDEX 更新の仕様本文を確認したいだけなら、仕様文書または該当実装へ進む。

## hash
- e8d8163fd3e7c5f366a20e21707b54b8ee05450bce0e135bf7b3b5493681c4e6

# `oracle.py`

## Summary
- `src` だけを import 対象にした起動時にも、正本側の `oracle` package を解決できるようにする package shim。packaged realization tree の外にある oracle source directory を `__path__` に設定し、見つからない場合は import 失敗として明示する。

## Read this when
- `src` 起点の実行環境で `oracle.*` import を成立させる仕組みを確認したいとき。
- realization code から正本側 oracle module を参照する import 経路や package shim の挙動を調べるとき。
- `oracle package source was not found` という import error の原因を確認するとき。

## Do not read this when
- oracle source の個別 module の仕様や実装内容を確認したいときは、正本側の該当 module を直接読む。
- CLI command、状態管理、入出力処理など cmoc 本体の realization implementation を調べたいときは、それぞれの担当 module を読む。
- oracle file と realization file の定義やパス概念そのものを確認したいときは、対応する正本仕様文書を読む。

## hash
- b6f4097cc1550a057bef77dda6b9e5434b394da2d2831fb96ccbf3d319c4222d

# `sub_commands`

## Summary
- `cmoc` の各サブコマンド実行入口をまとめる階層。ここでは個別コマンドの責務境界を見分け、必要なら対応する実行本体や共通 runtime 側へ進む。
- `apply` は apply 系の実行制御を扱い、fork・join・abandon・fork report の役割分担と実行順序を追いたいときの入口になる。
- `session` は session 系の開始・統合・終了を扱い、fork・join・abandon の状態遷移や branch 操作を確認したいときの入口になる。
- `review` は review 系サブコマンド群の package 境界と review oracle 実行フローを扱い、対象選択・所見収集・レポート出力を追いたいときの入口になる。
- `indexing` は INDEX.md 更新と commit をつなぐ実行入口で、前提条件と更新の外形的な流れを確認したいときに読む。
- `tui.py` は `cmoc tui` の起動入口で、元プロンプト編集、エディタ起動、実行パラメータ解決、TUI 起動の流れを確認したいときに読む。
- `doctor.py` は doctor サブコマンドから runtime preprocess への薄い委譲入口で、doctor 固有処理ではなく委譲先を確認したいときに読む。
- `eval_oracle.py` は want を書き出した oracle 評価を review oracle 実装へ委譲する薄い入口で、評価本体そのものではなく接続先を確認したいときに読む。
- `review_index.py` は review worktree や branch の差分を INDEX.md に絞って検査・確定・取り込みする処理を扱い、INDEX.md 以外の差分混入や merge 解決条件を確認したいときに読む。
- `review_loop.py` は review oracle の所見処理ループ本体を扱い、所見の列挙・統合・再検証・採否判定の順序を追いたいときに読む。
- `review_paths.py` は review 結果に含まれる oracle_path の解決と正規化を扱い、finding の参照先を worktree 間で同一 key として扱いたいときに読む。
- `review_report.py` は review oracle レポートの Markdown 生成を扱い、frontmatter、集計、finding の見せ方、保存先を確認したいときに読む。
- `review_targets.py` は review oracle の対象 oracle file を scope と session 状態に基づいて列挙する処理を扱い、どの file が対象になるかを確認したいときに読む。

## Read this when
- `cmoc` サブコマンド階層の中で、どの責務がどのファイルにあるかを切り分けたいとき。
- apply 系サブコマンドの実行順序、終了時の state や report の流れを把握したいとき。
- session 系サブコマンドの開始・統合・終了の責務分担を確認したいとき。
- review oracle の対象選択、処理ループ、レポート生成、パス正規化のどこを読むべきか迷っているとき。
- INDEX.md 更新の起動条件と外形的な実行順序を確認したいとき。
- `cmoc tui` の入力プロンプト、エディタ起動、起動前後のパラメータ解決を確認したいとき。
- doctor の実行入口がどの runtime preprocess に接続されるかを確認したいとき。
- want を書き出した oracle の評価経路が review oracle と同一であることを確認したいとき。
- review worktree や branch の差分が INDEX.md のみに制限される条件を確認したいとき。

## Do not read this when
- 個別サブコマンドの引数定義や内部制御を詳しく追いたいときは、対応する実装ファイルへ直接進む。
- branch や worktree の一般的な操作だけを確認したいときは、共通 runtime 側を読む。
- review 以外のサブコマンドや正本仕様そのものを探したいときは、この階層ではなくより直接の対象や oracle 側を読む。
- INDEX.md の更新内容そのものや更新アルゴリズムの詳細を知りたいときは、`commons.indexing` 側を読む。
- doctor preprocess の中身や診断項目を調べたいときは、その preprocess 本体を読む。
- review oracle の評価処理本体、出力、検査内容を確認したいときは、委譲先の review oracle 実装を読む。
- review レポート本文の構成や採点基準を変えたいときは、`review_report.py` を読む。
- finding の `oracle_path` 以外の項目解釈や列挙ロジックを変更したいときは、`review_paths.py` ではない別の対象を読む。
- review 対象 oracle の探索・判定・実行制御を確認したいだけなら、レポート生成側や対象選定側の対象を優先する。

## hash
- 515ed47c00f5247dcec86f8f1f33d8156fbec1b92730bf00a41c6df99e7b0676
