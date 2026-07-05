# `__init__.py`

## Summary
- oracle 側の acp builder 実装を正本に保ちながら、既存の acp.builder 経由の import を成立させる互換入口。
- oracle package の検索結果を確認し、oracle 側の submodule search path をこの package に追加したうえで、既存参照向けに basic module を oracle 実装へ対応付ける。
- local wrapper を oracle 側 path より優先できる順序を保ち、互換が必要な出力だけ realization 側で適応できる余地を残す。

## Read this when
- acp.builder 経由の import 互換性、特に既存の acp.builder.basic 参照が oracle 側実装へ解決される仕組みを確認したいとき。
- oracle 側の acp builder package を正本としつつ、realization 側で package path や module alias をどう接続しているかを調べるとき。
- acp.builder.* 参照を削除または移行する作業で、この互換入口を残す条件や削除条件を確認したいとき。

## Do not read this when
- oracle 側 acp builder の正本仕様や canonical module の実装内容を確認したいだけなら、oracle 側の該当実装を直接読む。
- acp.builder 以外の acp package 公開面や import 互換性を調べる場合は、より上位または該当 subpackage の入口を読む。
- builder の個別変換処理や wrapper の詳細挙動を調べる場合は、その処理を持つ個別 module を読む。

## hash
- 7af83fea8ad03595625c00432641609f104d01f963904ec5b9ef0a1d8dc05693

# `apply`

## Summary
- apply 向け ACP builder の互換入口と apply fork 向け builder 群を含む領域。旧来の import 経路を維持する薄い互換層と、oracle 側 builder の生成結果を realization 側公開型へ適合させる apply fork 用 builder package への入口になる。

## Read this when
- apply 系 ACP builder のうち、旧来の import 互換 package が残っている理由や削除条件を確認したいとき。
- `cmoc apply fork` の agent call parameter 構築経路、oracle 側 builder 呼び出し、realization 側 `AgentCallParameter` への変換境界を確認・変更したいとき。
- apply fork 用 builder 共通の repo root 解決、oracle builder import 準備、oracle parameter 受け渡し境界を調べたいとき。

## Do not read this when
- apply 機能そのものの実装詳細、実行フロー、fork 作成、branch 操作、diff 生成、CLI 引数処理を調べたいときは、apply fork 実装や呼び出し元へ進む。
- agent prompt、出力条件、parameter 生成内容の正本仕様や人間意図を確認したいときは、対応する oracle 側 builder を読む。
- ACP parameter の公開型、汎用 git helper、path model、apply fork 以外の ACP builder 個別ロジックを調べたいだけのときは、それぞれの共通実装や対象 builder へ直接進む。

## hash
- 05cc984b2400570a44a7c6c6b73a2c6509fa2cfec997f63fba4f14eece4064b4

# `common`

## Summary
- 共通ビルダー処理を置くためのディレクトリだが、現在は対象本文となる通常ファイルを含まない。

## Read this when
- 共通ビルダー処理の置き場所を確認しており、この階層に本文ファイルが追加されているかを確かめる必要があるとき。

## Do not read this when
- 既存の共通ビルダー処理の実装詳細を探しているとき。現時点ではこの対象から読める本文がないため、より直接の実装ファイルまたは下位要素へ進む。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `indexing`

## Summary
- 正本側に集約された indexing index entry builder を、旧来の公開名前空間から参照し続けるための互換入口を収める。実処理や仕様本体ではなく、既存参照を成立させる薄い転送層と、その互換経路を残す理由・削除条件の確認入口として位置づけられる。

## Read this when
- 旧来の公開名前空間から正本側の indexing 実装へ到達する互換経路を確認したいとき。
- indexing index entry builder の import 経路互換性や、既存利用者向け参照を壊さないための薄い公開面を調べるとき。
- 互換入口を削除できるか判断するために、残存参照の有無や削除条件を確認したいとき。

## Do not read this when
- indexing の具体的な生成処理、探索処理、データ構造、入出力仕様を確認したいとき。実体を持つ正本側の実装を読む。
- builder 本体の実装、引数構築ロジック、新規機能追加、index entry 生成仕様そのものを調べたいとき。再公開先または実装側を読む。
- 単にパッケージ配下の通常モジュール構成や汎用的な import 規約を調べたいとき。

## hash
- 5ebe4d8f1b0167397eca53308c9fa3bff675bed78057d79508ec00483933f9c1

# `quota_probe.py`

## Summary
- Codex quota availability probe 用の AgentCallParameter を構築する薄い wrapper。実際の probe prompt と構築処理は oracle 側の canonical builder に委譲し、realization 側に正本 prompt を複製しないための入口を提供する。
- quota probe の parameter builder を呼び出す側から使われ、oracle 側 builder が存在しない場合は realization 側で代替せず import 失敗として扱う。

## Read this when
- Codex quota availability probe の AgentCallParameter がどこで構築されるかを確認したいとき。
- probe prompt を realization implementation に持たせず oracle src の builder に委譲する境界を確認したいとき。
- quota probe parameter builder の import 経路や公開関数名を確認したいとき。

## Do not read this when
- quota probe prompt の本文や正本仕様を確認したいとき。その場合は oracle 側の prompt・builder 定義を読む。
- AgentCallParameter のデータ構造そのものを確認したいとき。その場合は basic.acp 側を読む。
- quota probe の実行結果処理、quota 判定、agent call orchestration 全体を調べたいとき。

## hash
- dba354855e524ebce6625b4b8ccda6ffa1f3cffa5d85b377f0babd930411add9

# `review`

## Summary
- review builder 領域のうち、旧 import 経路を保つ互換 package と、review oracle 用 agent call parameter builder の互換入口・最小補正層をまとめる場所。
- canonical 実装への再 export、既存 caller 移行までの互換維持、oracle src 由来 builder 戻り値への既知 placeholder/typo 補正が主な責務であり、review finding の実処理本体や正本 prompt は扱わない。

## Read this when
- review builder 周辺で、古い import 経路から canonical 実装へつながる互換層を確認する。
- 既存 caller を canonical path へ移行する作業で、互換 package や互換モジュールの削除可否・削除条件を判断する。
- review oracle finding の列挙・判定・統合・検証に関して、旧 import 経路がどの canonical 実装へ委譲されるか確認する。
- oracle src 由来の agent call parameter に対して、prompt 内の oracle root placeholder 表記や静的 typo の最小補正がどこで行われるか確認する。
- finding や既知理由などの動的入力を改変せず保持する境界を確認する。

## Do not read this when
- review finding enumeration、judgment、validation の実処理や parameter 構築ロジックを確認したい場合は、canonical oracle path 側を読む。
- review builder の実処理や変換ロジックそのものを調べたい。
- レビュー一般の finding 統合仕様、prompt 本文、または oracle src 側の正本定義そのものを確認・変更したい。
- agent call parameter の基本構造、型責務、構造化出力 schema、path model、ファイルアクセスなど、互換 import 経路や既知表記補正と無関係な基礎仕様を調べる。
- 新しい公開 API、利用者向け機能の仕様、または新規 caller が利用すべき import path だけを確認したい。

## hash
- 5f3817838f319760619962a83f071479c50ecfdf4d4843e53f43904faad19e04

# `session`

## Summary
- session builder 配下の旧 acp.builder 系 import path 互換を扱う領域。session 本体の挙動ではなく、既存参照を canonical oracle 実装または互換入口へ中継する薄い公開面維持層をまとめる。

## Read this when
- acp.builder.session.* の旧 import path 互換がどの入口や canonical 実装へつながるかを確認したいとき。
- session builder 配下の互換 package や再公開モジュールを残す理由、公開面維持、削除条件を調べたいとき。
- session join builder の旧公開元や互換経路を追跡しているとき。

## Do not read this when
- session 実装の具体的な挙動、制御フロー、builder 呼び出し順を確認したいとき。
- conflict resolution parameter builder など canonical oracle 実装側の内容や仕様根拠を確認したいとき。
- 互換 import の実際の利用箇所や、利用者向け公開面から参照がなくなったかを判断したいとき。
- 新規機能の入口や通常の公開 API を探しているとき。

## hash
- d636121a29a1f6f7a6d22e0e3a8ad6b3f97e18b5065aec22c899dbab39d5d021

# `tui`

## Summary
- TUI 起動用 builder まわりの互換層を扱うディレクトリ。既存の `acp.builder.tui.*` import surface を維持しつつ、正本側 builder の再公開や realization runtime への complete prompt 保存を経由して TUI 用 AgentCallParameter を組み立てる入口を置く。

## Read this when
- 既存の `acp.builder.tui.*` import 互換性、公開名、削除可否を確認する。
- TUI 起動用 AgentCallParameter の組み立て、モデル種別、reasoning effort、file access mode、Structured Output schema 非指定の扱いを確認または変更する。
- TUI 起動時の complete prompt 生成、markdown 保存、保存先パス、agent へ渡す指示文の関係を確認する。
- TUI resolve parameter builder の呼び出し元を正本側 import path へ移行する。

## Do not read this when
- TUI 画面そのものの表示、入力処理、イベントループ、端末 UI の挙動を調べたい場合。
- prompt builder の正本仕様、StructDoc の markdown rendering、runtime のローカルディレクトリ配置や repo root 解決の一般仕様を調べたい場合。
- TUI 以外の builder や file access mode 全体の定義を確認したい場合。
- 新しい公開 API や新規 import 経路を設計したい場合。

## hash
- e24d457b6a6333995ae031725e52ee505ea421f7f2b703335e0eff1f3f22782b
