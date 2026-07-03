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
- Codex quota availability probe 用の AgentCallParameter を組み立てる小さな builder。最小モデル、低 reasoning、readonly file access、固定プロンプトで Codex CLI の軽量な疎通確認呼び出しを表す。

## Read this when
- quota availability probe の agent call parameter がどのモデル class、reasoning effort、file access mode、prompt で作られるか確認したいとき。
- Codex CLI の quota 確認・疎通確認のための最小 agent call を生成する処理を変更するとき。
- quota probe 専用の prompt 文字列や exported builder の責務を確認するとき。

## Do not read this when
- 通常の agent call parameter 全般の構造や型定義を確認したいだけなら、AgentCallParameter や関連 enum の定義を直接読む。
- quota probe の実行タイミング、呼び出し元の制御、エラー処理を調べたいときは、この builder ではなく probe を呼び出す側の実装を読む。
- oracle 上の Codex CLI 実行規則や quota availability probe の根拠仕様を確認したいときは、対応する oracle doc を読む。

## hash
- 5bfbf50041f5503c29548fe6ee7eff79e4215b815946e39f30a665410c2625ab

# `review`

## Summary
- review builder 周辺の互換 import と review oracle 用 agent call parameter builder 群への入口を扱う領域。finding enumeration、judgment、merge、finding advocate/challenger validation に関する生成経路と、旧参照を維持する互換層を含む。
- 正本 prompt や canonical 実装そのものではなく、oracle src 由来の builder 結果を realization 側で接続・再公開し、必要な箇所だけ限定的な placeholder 表記補正を行う境界を担う。

## Read this when
- review oracle の finding 関連 agent call parameter 生成経路を確認・変更する。
- known findings、finding、既知理由などを入力にした review oracle prompt 組み立てが、structured output schema や canonical builder へどう接続されるかを追う。
- 旧 import 経路から canonical oracle path への移行状況、互換 shim の再 export 対象、削除可否を判断する。
- review builder 周辺の import 互換性、互換 package の残存理由、削除条件を確認する。
- oracle src 側に残る oracle root placeholder 表記ゆれを realization 側で最小補正している理由、範囲、削除条件を確認する。

## Do not read this when
- review oracle の正本 prompt 内容そのものを確認したい場合。対応する oracle src や prompt standard を直接読む。
- finding enumeration、judgment、validation の実処理や parameter 構築ロジックの本体だけを確認したい場合。canonical oracle path 側を直接読む。
- review builder の実処理や変換ロジックだけを調べたい。
- review workflow 全体、CLI、永続状態、git 操作など、agent call parameter builder や旧 import 互換と無関係な領域を調べる。
- AgentCallParameter 型そのものや共通 builder 基盤の仕様を確認したい場合。共通定義側を読む。

## hash
- 51a4ba5446c21a28ea8b262311c59e22347b93137dccbcf90e9cd6cfca7d7e4c

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
- TUI builder の旧公開 import surface を維持するための互換層。実体は oracle 側の canonical builder に置き、既存参照向けに薄い package 入口・再 export・TUI 用 file access mode 選択肢を提供する。
- TUI 起動パラメータや resolve parameter の仕様本体ではなく、realization 側と利用者向け公開面に残る既存 import 経路を oracle 側実体へ接続する位置づけを持つ。

## Read this when
- TUI builder 周辺の旧 import 経路を維持・移行・削除できるか判断する。
- 既存公開 import path から oracle 側の TUI 起動パラメータ生成や resolve parameter builder へどのように委譲しているか確認する。
- TUI 向け互換 surface が公開する名前や file access mode の選択肢を確認する。

## Do not read this when
- TUI 起動パラメータや resolve parameter builder の正本仕様・生成ロジックを確認したい場合は、oracle 側の実体を読む。
- TUI 画面の描画、イベント処理、端末 UI の挙動を調べたい場合。
- 新しい公開 API、起動仕様、CLI 挙動、または TUI 以外の builder や file access mode 全体を設計・確認したい場合。

## hash
- 360577811f86bbaa7e4bf65e6625f71f31b46acf97b662761a7b818fa854ceab
