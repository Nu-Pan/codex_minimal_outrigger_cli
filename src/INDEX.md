# `acp`

## Summary
- acp 互換名前空間の公開入口と、oracle 実装へ委譲する builder adapter 群への上位入口を提供する。公開 import 経路や処理別 adapter の配置関係を確認する際の起点。

## Read this when
- acp という公開入口の存廃や既存参照から oracle 側実体への移行経路を判断するとき
- acp.builder 配下の互換 import 経路、共通 builder 処理、処理別 adapter の構成を確認するとき

## Do not read this when
- acp 配下の具体的な実装、仕様、入出力、利用箇所を調べるときは、対応する oracle 実装や参照元を直接読む
- 個別 builder adapter の詳細実装や、acp と無関係な CLI 処理だけを調べるとき

## hash
- 9086a870ac2e3d3c32195eba2c4441af8578b4de9f66aee07082e825f57eaf2b

# `basic`

## Summary
- `basic.*` の互換 import 公開面をまとめた realization 側の入口。ACP 型、path model、構造化文書 API の旧参照から、各互換モジュールまたは再公開元の正本へ進むための下位要素入口を提供する。

## Read this when
- `basic` 名前空間に残る互換 API の範囲や、旧 import から移行先を確認したいとき。
- ACP、path model、構造化文書の互換入口を横断して、個別モジュールを読むべきか判断するとき。

## Do not read this when
- 個別 API の実装、再公開内容、型定義、描画仕様を確認したいときは、`basic.acp`、`basic.path_model`、`basic.struct_doc`、またはそれぞれの正本実装を直接読む。
- 正本仕様そのものや、`basic` 名前空間と無関係な処理を調べるとき。

## hash
- ea7ec701e546985b90dda735f067c250cdd2609d2464948e58591d98ccf40fd2

# `cmoc_runtime.py`

## Summary
- 互換 import path から共通 runtime API を再公開する入口。公開名は共通 runtime の限定された公開面に従い、runtime と型チェッカーへ同じ互換名を伝える。

## Read this when
- 既存の互換 import path を利用する呼び出し元、または共通 runtime API の再公開・移行状況を確認するとき。

## Do not read this when
- 共通 runtime の実装内容や個別 API の責務を確認したいときは、直接 commons.cmoc_runtime を読む。
- 互換 import path の移行完了後に削除可否だけを判断するときは、移行対象の責務別 runtime module と pyproject の公開設定を直接確認する。

## hash
- 43fb961149b599635a1abdceb8611969195b689f50ec716e0231e113d978fded

# `commons`

## Summary
- cmoc の共有 runtime helper と実行基盤を集約する commons パッケージ。CLI、Codex 実行、設定、Git、ログ、パス、結果、状態、feedback、report、editing run など、複数の実行経路で共通利用される下位実装への入口。
- INDEX.md の生成・更新、prompt editor input、Codex TUI／exec、feedback、primary report、editing run lifecycle など、横断的な実行時処理を責務別モジュールへルーティングするディレクトリ。

## Read this when
- 複数の cmoc 実行経路で共有される runtime API や helper の配置・責務を確認するとき
- CLI、Codex、設定、Git、feedback、report、state、editing run などの共通実行時機能を調査・変更するとき
- 対象機能の下位実装を探し、責務別の runtime モジュールへ進む入口を確認するとき

## Do not read this when
- 特定の runtime helper の内部挙動だけを調査する場合は、commons 配下の対応する個別モジュールを直接読むとき
- 個別サブコマンドの業務ロジック、TUI 自体、正本仕様、またはテスト固有の期待値を確認する場合
- 共有 runtime を利用しない機能や、より下位の protocol・schema・renderer の具体的な内容だけを確認する場合

## hash
- 4bef3dfff552381de3924b8045893a80c5eb8ef78ffae5c29ea82ca72ccdac4e

# `config`

## Summary
- config.* 参照を維持するための互換入口。
- oracle 側の cmoc 設定型を realization 側の config.cmoc_config から再公開する経路への入口。

## Read this when
- config からの import 互換性を確認するとき。
- realization 側の config.cmoc_config における設定型の再公開経路を確認するとき。

## Do not read this when
- 設定型の定義や設定値の仕様そのものを確認したいとき。
- config.cmoc_config の参照経路を新規追加・変更する実装判断を行うとき。

## hash
- 8571722dab57a84f72fd99845c9e5c092cb64b05d9f5ac72e976209acca14524

# `main.py`

## Summary
- cmoc の CLI コマンドツリーと console script からの起動入口を定義する。
- Typer と Click の互換境界、および通常の引数解析エラーを cmoc 形式へ変換する実行制御を担う。
- doctor、tui、indexing、feedback、session、oracle、realization、run 各コマンドの CLI 入口を確認するための上位ルーティング対象。

## Read this when
- cmoc の CLI にコマンドまたはサブコマンドを追加・変更するとき。
- Typer・Click のバージョン互換、CLI 引数解析エラー、補完 probe、終了コードの扱いを調査するとき。
- console script の起動経路や、各 sub_commands 実装へ到達するコマンドツリーを確認するとき。

## Do not read this when
- 特定サブコマンドの業務ロジックや実装詳細だけを調査・変更するときは、対応する sub_commands 配下を直接読む。
- oracle、realization、session、run などの状態遷移や仕様を確認するときは、対応する正本仕様またはサブコマンド実装を直接読む。
- CLI の INDEX.md 更新処理そのものを調査するときは、indexing の実装対象を直接読む。

## hash
- f11839e2670e14ecf92530a722e415c9b151e155dd0e16e294c198cb8c216a31

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
- cmoc の各サブコマンド実装を収める上位パッケージ。doctor、feedback、indexing、oracle、realization、run、session、tui など、個別サブコマンドの CLI 入口や実行フローへ進むためのルーティング起点となる。
- apply と review は現時点で実装本文がなく、対応する実装追加後に確認するための空の配置先である。

## Read this when
- cmoc のサブコマンド実装の構成や、特定サブコマンドの CLI 入口を確認するとき。
- サブコマンド実装を横断して、対象となる個別パッケージへの入口を判断するとき。
- apply または review の実装追加状況を確認するとき。

## Do not read this when
- サブコマンド共通 runtime、共通仕様、または個別サブコマンドの詳細処理だけを確認したいときは、対応する共通実装・仕様文書・下位対象を直接読む。
- サブコマンドに関係しない処理を扱うとき。

## hash
- 71d04caba284f35cce58018fa4db2891f361009a47b6592eaccd178b3b90ac75
