# `acp`

## Summary
- ACP 互換の realization package。`acp.*` の公開 import 経路を維持しつつ、下位の builder adapter などを通じて canonical な oracle 側実装へ接続する。
- `acp` 公開入口の存廃判断と、builder 用途別の下位要素へ進むための起点となる。

## Read this when
- `acp.*` の互換 import 経路や公開入口全体を確認したいとき。
- ACP builder の用途別 adapter へ進む入口を選びたいとき。

## Do not read this when
- `acp` 公開入口の存廃だけを判断したいなら、入口モジュールを直接読む。
- 特定の builder の実装・canonical 仕様・利用箇所を調べたいなら、該当する下位要素または参照元を直接読む。

## hash
- 19748d31bd6289625fef47d1a672db39bd72ee4039df05de799d7d7caeb3ec5a

# `basic`

## Summary
- `basic` 配下の互換 import 入口をまとめるディレクトリ。ACP 型、path model、構造化文書 API などを正本や oracle 側から再公開し、既存の `basic.*` 公開面を維持する。個別実装や正本定義を確認する場合は各再公開元へ進む。

## Read this when
- `basic.*` の互換 import を維持・廃止する判断をするとき。
- `basic.acp`、`basic.path_model`、`basic.struct_doc` の公開経路や再公開元を確認するとき。
- 利用者向け公開面の移行先や互換層の維持条件を調べるとき。

## Do not read this when
- ACP 型、path model、構造化文書 API の正本仕様や実装詳細を確認したいときは、各 oracle 側の定義を直接読む。
- 個別モジュールと無関係な処理を調査・変更するとき。

## hash
- 292bc262556c427d8a4a7636a2c7e14127adfdea1c7d57f167e9bfa04d4ce5ea

# `cmoc_runtime.py`

## Summary
- `commons.cmoc_runtime` の公開名を互換的に再公開する薄い import shim。pyproject が `cmoc_runtime` を公開し、ツリー内の呼び出し元がこのパスを直接 import している間の移行入口。

## Read this when
- `cmoc_runtime` の互換 import path、公開名、または runtime module への移行状況を確認するとき。

## Do not read this when
- runtime の実装や責務別 module の詳細を確認するときは、`commons.cmoc_runtime` または該当する runtime module を直接読む。
- 互換 path の移行完了後は、この shim を読む必要はない。

## hash
- ce0901465f229760c4bd1f4c5ce3f4a035bb53bf6aee04de082b5843cff3ff17

# `commons`

## Summary
- cmoc の共通 runtime helper を集約する commons パッケージ。CLI 実行、Codex 呼び出し、設定・状態・Git・パス・ログ・feedback・結果処理など、複数の上位機能から利用される横断的な実装への入口。
- INDEX.md の検査・生成 lifecycle、Codex exec/TUI 境界、runtime 設定・状態・worktree 管理、feedback の収集・保存・移行、実行時エラーやログ処理を扱う。個別機能の詳細は対応する runtime_* モジュールへ進む。

## Read this when
- commons 配下の共通 runtime API や、複数の CLI・セッション・Codex 機能にまたがる処理の入口を確認するとき
- Codex 実行、INDEX 更新、設定・状態・Git・worktree、feedback、ログ、エラー、パス管理の実装対象を選ぶとき

## Do not read this when
- 特定の runtime 機能の実装詳細だけを調査・変更するときは、対応する runtime_* モジュールを直接読む
- 利用者向けの正本仕様や個別 CLI サブコマンドの業務ロジックだけを確認するときは、対応する oracle 文書またはサブコマンド実装へ直接進む

## hash
- 4af51ce0da00e27871309684aedc092d083bf77c40d290af84287b2b5c96dd4a

# `config`

## Summary
- 設定モジュールの互換入口を提供するディレクトリ。`__init__.py` は `config.*` 参照を成立させ、`cmoc_config.py` は oracle 側の設定型を定義せず realization 側から再公開する。設定仕様の確認先ではない。

## Read this when
- 既存利用者の `config` または `config.cmoc_config` 参照を維持・確認するとき。
- 設定型の import 経路や互換入口の有無を調べるとき。

## Do not read this when
- 設定定義の内容や仕様そのものを確認するときは、oracle 側の設定定義を直接読む。
- 設定参照を新規に追加する実装判断では、利用側の参照経路を直接確認する。

## hash
- fbc828970884bf16f7e7e6174e3461888e3c4000d754454ba9794e1d2c99d6f2

# `main.py`

## Summary
- cmoc の Typer CLI の主入口。doctor、tui、indexing、feedback、および session・oracle・realization・run 系サブコマンドを登録し、各実装へ委譲する。
- CLI 引数解析エラーの cmoc 形式への変換、補完 probe の扱い、終了コード処理、oracle review の scope option など、CLI 全体の起動・登録契約を確認する入口である。

## Read this when
- トップレベル CLI コマンドやサブコマンドの登録・構成を変更するとき
- CLI 起動時の引数解析エラー、補完、終了コード、Typer/Click 互換処理を調査するとき
- 各サブコマンド実装へ委譲される境界を確認するとき

## Do not read this when
- 特定サブコマンドの本体挙動や業務ロジックを調査・変更するときは、対応する sub_commands 配下を直接読む
- oracle の仕様や CLI の詳細な利用契約を確認するときは、参照されている oracle/doc を読む

## hash
- 0e30eb38f5c8cfc39f52be0b414c66e3b115019772e3a803de854c472c56bc67

# `oracle.py`

## Summary
- `src` 起動時に正本側 `oracle.*` パッケージを解決するための互換用 package shim。`oracle/src/oracle` をパッケージパスとして再公開し、正本ソースが存在しない場合は `ModuleNotFoundError` を送出する。

## Read this when
- `src` だけを起動した際の `oracle.*` パッケージ解決や互換 import の挙動を確認するとき。

## Do not read this when
- 正本側 `oracle.*` の実装内容を確認するときは、直接 `oracle/src/oracle` 配下を読む。
- `src` の通常の CLI 実装や、package shim と無関係な import 経路を調査するとき。

## hash
- e476648f073484004b64741d40d6d373fab223e001be01ac8051f9c5ab15e095

# `sub_commands`

## Summary
- CLI サブコマンドの実装をまとめるディレクトリ。doctor、feedback、indexing、oracle、realization、run、session、tui など、各サブコマンドの実行入口と関連処理への入口を提供する。
- 未実装の apply と review も含むが、現時点では具体的な実装本文はない。

## Read this when
- CLI サブコマンドの構成や、対象サブコマンドの実装入口を確認するとき。
- 複数のサブコマンドにまたがる実行フローや、サブコマンド配下の処理へ進む入口を特定するとき。

## Do not read this when
- 特定サブコマンドの詳細な処理、共通ランタイム、oracle 文書、または個別の補助実装だけを確認したいときは、対応する下位要素や共通実装を直接読む。
- サブコマンドに関係しない処理を確認するとき。

## hash
- f5d75eeb39a47ae37b8fc340a824895b4b87df16f416e4f2f1ebceba38774b7f
