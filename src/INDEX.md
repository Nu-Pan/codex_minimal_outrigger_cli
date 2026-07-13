# `acp`

## Summary
- `acp` 層の互換入口をまとめる公開面。`oracle.acp_builder` へ直接つなぐのではなく、既存の `acp.*` 参照を壊さずに正本側へ到達させるための受け口として読む。
- `src/acp/__init__.py` は移行中の互換 import 面を保つための入口に限る。実体や新機能の定義場所ではないので、互換維持の要否や削除条件を確認したいときだけ読む。
- `src/acp/builder` は builder 群の互換公開層。個別の実装や出力規則ではなく、旧来の `acp.builder.*` 参照を残す範囲と正本側への接続を確認したいときに読む。

## Read this when
- `acp.*` の参照を正本側や実体 module に移す作業で、互換入口を残す理由と削除条件を確認したいとき。
- 実装本体ではなく、公開 import 面としてこの階層がどこまで維持されるかを判断したいとき。
- 既存の `acp.builder.*` 呼び出しを壊さずに正本側へ接続する必要があるとき。

## Do not read this when
- 実装処理そのものや生成ロジックを調べたいとき。ここは入口であり、本体は下位 module または `oracle.acp_builder` 側にある。
- 新しい機能や API を追加する場所を探しているとき。ここは互換維持専用で、新規公開面の起点ではない。
- すでに全公開面から `acp.*` 参照を消し終えて、互換入口の維持要否を確認する必要がないとき。

## hash
- 718db3766cb94da5d2e7be8680dcbaae01f2c0a821ac6d66e34bc64fd6bdf833

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
- cmoc の実行時共通基盤をまとめる領域の入口。設定・path・git・ログ・結果・エラー・Codex 実行・Ollama・doctor・preflight・indexing など、複数サブコマンドから共有される runtime helper 群へ進むための起点になる。
- この対象は共通 runtime のまとまりを示すだけで、個別 helper の責務や挙動は下位要素の本文で確認する。共通基盤のどの層へ進むべきかを判断したいときに読む。

## Read this when
- サブコマンド横断で使う共通 helper の配置場所や、まずどの runtime 実装へ進むべきかを確認したいとき。
- Codex 実行前後の共通処理、設定・状態・ログ・path・git・エラー処理・結果型のいずれかをまたいで追いたいとき。
- 共有 helper 群の下位要素へ進む前に、この領域が実行時共通基盤であることを確認したいとき。

## Do not read this when
- 特定 helper の入出力、失敗時挙動、内部分割を確認したいときは、この対象ではなく該当する下位要素の本文を読む。
- CLI コマンド固有の業務処理やテスト固有の処理を調べたいときは、共通基盤ではなくより直接その責務を持つ対象へ進む。
- runtime 全体ではなく単独の設定型、state 型、エラー型などの正本仕様断片だけを確認したいときは、それぞれの対応する正本側を読む。

## hash
- 62c3fc57b848aac4a9fbbe6359b43d2211ebb6560751def3c2e7feeb82dee468

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
- `cmoc` の各サブコマンド実装を束ねる入口で、個別コマンドの制御本体へ進む前に全体の責務分担を見分けるための案内を置く。
- この階層は、コマンドごとの実行制御、状態遷移、レポート生成、共通 runtime への委譲を切り分ける目的で読む。
- ここでは個別処理の詳細よりも、どのサブコマンドがどの下位実装に対応するかを素早く特定できることを重視する。

## Read this when
- `cmoc` のサブコマンド全体を見渡して、目的の実装ファイルを特定したいとき。
- 特定のコマンドの起動経路、状態更新、報告生成、破棄処理などの責務境界を切り分けたいとき。
- 下位の個別実装へ進む前に、まずどの領域を読むべきかを絞り込みたいとき。

## Do not read this when
- 共通 runtime の入出力や基盤処理だけを追いたいときは、より下位の共通実装を読む。
- 個別サブコマンドの引数、エラー処理、出力形式を直接追いたいときは、この階層ではなく該当する実装へ進む。
- サブコマンド以外の package 境界や別領域のルーティングを確認したいとき。

## hash
- d12740d79820c0dfd93cb013d2b9fd6cf192212ae3fdbdee06c552255340cf55
