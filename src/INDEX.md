# `acp`

## Summary
- `acp` 名前空間の互換公開面を維持するための薄い入口。実体実装は別 module に置かれ、この対象は既存 import 経路を壊さずに正本側へつなぐ役割に限られる。
- `acp.builder` 配下の互換入口と薄い実装層を束ねる上位ディレクトリ。公開面維持と各 builder 領域への振り分けの起点であり、個別仕様は下位対象で確認する。

## Read this when
- `acp.*` の参照を別実体へ移す途中で、互換入口を残す必要性や削除条件を確認したいとき。
- 利用者向け公開面に残る `acp.*` import の扱いを判断したいとき。
- `acp.builder.*` の既存参照互換を維持したいとき。
- 互換入口から正本実装へ到達する振る舞いを確認したいとき。
- この名前空間に残す薄い公開面と削る対象を判断したいとき。
- 配下の builder 領域を横断して、互換層と正本側実装の境界を確認したいとき。

## Do not read this when
- 実装本体や生成処理そのものを調べたいとき。この対象は薄い互換入口なので、実体のある module へ進む。
- 新しい機能や API 仕様を追加する場所を探しているとき。この対象は互換維持専用で、機能追加の入口ではない。
- `acp.*` 参照がすでに公開面から消えており、互換入口の詳細が不要なとき。
- 個別の builder の具体仕様や生成ロジックを確認したいとき。対応する下位対象を読む。
- 正本側の builder 実装そのものを変更したいとき。
- `acp.builder` 以外の公開面や別名互換の方針を確認したいとき。

## hash
- e2d563ef36ccb3f8b5e940da4bbea68388ac913d9c84434709541a667e22c3d2

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
- cmoc の共通 runtime helper 群をまとめる領域の入口。個別 helper の実装ではなく、複数モジュールから共有される基盤処理の配置先と境界を確認したいときに読む。
- この領域は、共通 runtime の公開入口と、その下位にある実装群へ進む前のルーティングに使う。個別の入出力や失敗時挙動は下位要素で確認する。

## Read this when
- 複数モジュールから使う共通 helper の入口や配置先を確認したいとき。
- 共有 runtime の下位要素へ進む前に、この領域が共通基盤のまとまりであることを確認したいとき。
- 共通 helper 群のどの層を読むべきかを、上位のサブコマンド実装に進む前に判断したいとき。

## Do not read this when
- 特定 helper の内部アルゴリズム、入出力、失敗時挙動を確認したいとき。
- CLI コマンド固有の処理やテスト固有の処理を調べたいとき。
- 共有基盤そのものではなく、より直接その責務を持つ下位要素を読むべきとき。

## hash
- 49db763ddeb7039c57a0d13a1b3a415a75750990b785a80495d1433b27c348ba

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
- `src/sub_commands` は `cmoc` のサブコマンド実行入口を束ねる階層で、ここでは個別コマンド本体へ進む前に役割の境界を切り分ける。共通の CLI 入口と、apply・session・review・tui・補助コマンドの分岐先を選ぶための案内として読む。
- `apply` は apply 系サブコマンド群の実行入口をまとめる。破棄・適用・統合・レポートのどれを追うべきかを切り分けたいときに読む。
- `doctor.py` は doctor サブコマンドから CLI runtime の preprocess 実行へ委譲する薄い入口を扱う。doctor 固有の処理ではなく、どの preprocess 経路に接続されるかを確認したいときに読む。
- `eval_oracle.py` は want を書き出した oracle の評価を review oracle 実装へ委譲する入口を扱う。評価本体そのものではなく、評価経路の接続関係を確認したいときに読む。
- `indexing.py` は indexing サブコマンドの起動入口を扱う。事前検査を通したうえで work root の INDEX.md 更新と commit をつなぐ外形的な流れを確認したいときに読む。
- `review` は review 系サブコマンド群の package 境界と review oracle 実行入口をまとめる。review oracle の実行フローや、review 系の個別実装へ進む前の切り分けに使う。
- `review_index.py` は review worktree/branch の差分を INDEX.md のみに制限して commit し、必要なら session branch へ merge する処理を扱う。INDEX.md 以外の差分検査や merge 競合の自動解消を追いたいときに読む。
- `review_loop.py` は review oracle の所見処理ループ本体を扱う。所見の追加・統合・再検証・採用判定の順序や、merge finding の編集検証を確認したいときに読む。
- `review_paths.py` は finding に入った oracle_path を実体 path と比較用 key に正規化する補助を扱う。レビュー対象の oracle file 参照先解決や、root プレースホルダの解釈を確認したいときに読む。
- `review_report.py` は review oracle レポートの Markdown 生成を扱う。レポート本文、frontmatter、集計、表示順、保存先の見せ方を変えたいときに読む。
- `review_targets.py` は review oracle の対象となる oracle file を scope と session 状態に基づいて列挙する。full scope と session scope の対象範囲の違いを確認したいときに読む。
- `session` は session 系サブコマンド群の package 境界と個別入口をまとめる。session の開始・統合・終了のどれを追うべきかを切り分けたいときに読む。
- `tui.py` は `cmoc tui` の実行本体を扱う。編集プロンプトの作成、エディタ起動、実行パラメータ解決、TUI 起動までの流れを確認したいときに読む。

## Read this when
- `cmoc` のサブコマンド群の中で、どの入口がどの責務を持つかを先に切り分けたいとき。
- apply・session・review のどれを読むべきかを、目的から判断したいとき。
- 特定のサブコマンド実装へ進む前に、この階層の案内だけで十分か確認したいとき。

## Do not read this when
- 個別サブコマンドの引数、エラー処理、内部ロジックの詳細を追いたいときは、該当ファイルへ直接進む。
- review 対象の選定、レポート生成、所見ループなどの個別機能の内部仕様を知りたいときは、対応する下位モジュールを読む。
- 共通 runtime や git 操作など、より下位の共通実装だけを見たいときは、この階層ではなく共通モジュールを読む。

## hash
- 603b52d4a0ec6f94c75da3423e1070256fc1b6a7fc4ee02ebf4a8c9224fe885b
