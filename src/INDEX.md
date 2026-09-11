# `acp`

## Summary
- acp 互換の公開入口を扱い、既存の acp.* 参照を oracle.* または実体モジュールへ移行する際の入口となる。
- acp.builder 配下の builder adapter と共通処理をまとめ、oracle 実装への互換入口、処理種別ごとの adapter、共有プロンプト整形、indexing への入口を提供する。

## Read this when
- acp という公開名の存続・削除や、既存参照を oracle 側の実体へ切り替える導線を判断するときは __init__.py を読む。
- acp.builder の全体構成、処理種別ごとの builder adapter の入口、共有プロンプト整形や index-entry 生成の配置を確認するときは builder を読む。

## Do not read this when
- acp 配下の具体的な実装仕様や移行先の詳細だけを確認したい場合は、対応する実体モジュールを直接読む。
- 特定 builder の入力制約・生成結果、acp.builder の利用箇所、正本仕様や実装そのものを確認したい場合は、この階層の入口ではなく対象の下位要素や参照元を直接読む。

## hash
- c39cd6b24e8a598b8b78eb8acddb1ed600865b536a16aabbfd39d2696e960214

# `basic`

## Summary
- `basic.*` の旧公開 import を維持する互換名前空間。ACP 型、path model、構造化文書 API は正本を複製せず、既存実装の再公開または委譲によって利用者向け入口を提供する。

## Read this when
- `basic.*` の互換参照を維持・削除する条件や、利用者向け API の移行先を判断するとき。
- ACP 型、path model、構造化文書の旧 API 入口を確認し、正本実装への委譲関係を追跡するとき。

## Do not read this when
- ACP 型、path model、構造化文書の正本仕様・実装詳細を確認したいときは、各再公開元を直接読む。
- 個別モジュールの具体的な公開内容や利用箇所だけを調べるときは、`basic` 全体ではなく該当モジュールまたは参照元を直接読む。

## hash
- e66d85791589dac1aca9c82c3aeba73b5416451d343c2feb68cbe202afe895a9

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
- cmoc の共有 runtime helper をまとめた commons パッケージ。CLI、Codex 実行、設定、Git、ログ、パス、状態、feedback、report など複数の実行経路にまたがる共通基盤を確認・変更するときの入口。
- INDEX.md の検査・生成・鮮度確認・復元・commit を含む indexing lifecycle を確認するときに進むディレクトリ。
- Codex exec／TUI の subprocess 実行、retry、quota、preflight、Structured Output、process tracking、IPC などの実行境界を確認するときに進むディレクトリ。
- 設定、Git、runtime state、feedback、report、logging、path、editor input、run lifecycle など、個別の共通 runtime 責務の実装を確認するときに、該当する下位モジュールへ進むための入口。

## Read this when
- cmoc の複数サブコマンドや実行経路で共有される runtime API・状態管理・実行境界を調べるとき
- INDEX.md 更新、Codex 実行、設定永続化、Git worktree、feedback、report、logging、path、editor input、run lifecycle の共通実装を確認または変更するとき
- 特定の commons runtime module の責務を特定し、該当する個別実装へ進む必要があるとき

## Do not read this when
- 利用者向けのサブコマンド仕様や業務フローだけを確認したいとき
- 特定モジュールの正本仕様、入力 schema、結果型、低レベル実装など、commons 配下の個別対象を直接読むべき場合
- commons と無関係な CLI・ドメイン処理や、INDEX.md のルーティング情報だけを更新する場合

## hash
- 7f0dea06fb4c813169fc03fc05fdcdfebec3efd7d9eaffb387ab7609d47de373

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
- cmoc の Typer/Click CLI ツリーと起動入口を定義する。トップレベルおよび session、oracle、realization、run、feedback 配下の各コマンドを、対応するサブコマンド実装へ接続する。
- Click/Typer の互換性補正、補完 probe の扱い、CLI 引数解析エラーの cmoc 形式への変換など、CLI 起動時の境界処理を担う。

## Read this when
- cmoc の CLI コマンド追加・変更や、コマンド階層とサブコマンド実装の接続先を確認するとき。
- Typer/Click の版差による help 表示、補完、引数解析エラー、終了コードの挙動を調査・変更するとき。
- console script からの起動経路や、feedback report の遅延ロードを確認するとき。

## Do not read this when
- 個別コマンドの業務処理や、各サブコマンド実装の詳細を変更・調査するときは、対応する sub_commands 配下を直接読む。
- oracle、realization、session、run などの内部ワークフロー仕様だけを確認したいときは、対応する正本仕様や実装を直接読む。
- INDEX.md の生成規則や一般的なエラー処理仕様だけを確認したいときは、該当する仕様文書を直接読む。

## hash
- 9779ae11e83145b4d1e6f180791ff3855507369621957c37448f8d4a6caed407

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
- cmoc の各サブコマンド実装と、realization・run・session・feedback・oracle などのサブパッケージをまとめる上位入口。
- 特定のサブコマンドや共通処理の詳細を確認する前に、対象の実装領域を振り分けるために利用する。

## Read this when
- cmoc のサブコマンド構成や、目的の処理がどのサブパッケージ・実装入口に属するかを確認するとき。
- doctor・indexing・tui の単独サブコマンド、feedback・oracle・run・session・realization の配下へ進む前に、実装の階層と責務の範囲を把握するとき。

## Do not read this when
- 特定サブコマンドの具体的な処理順序、入力、状態遷移、runtime、または成果物を確認したいときは、該当する実装ファイルや下位パッケージを直接読む。
- サブコマンド以外の共通仕様や、対象ディレクトリ外の実装を調べるとき。

## hash
- 4538b42e8e68a426f6f8a6a48857fae9c8e26932113a2dc213ee4de15fdbbc36
