# `__init__.py`

## Summary
- oracle src 側の acp builder 実装を複製せず、既存の `acp.*` import 参照を維持するための互換入口。実体は別 module 側に置き、この対象は移行期間中の公開 import 面を保つ役割に限定される。

## Read this when
- `acp.*` 参照を `oracle.*` または実体 module へ移行する作業で、互換入口を残す理由や削除条件を確認したいとき。
- realization 側または利用者向け公開面に残る `acp.*` import の扱いを判断したいとき。
- oracle src 由来の acp builder 互換 import がどこで維持されているかを確認したいとき。

## Do not read this when
- acp builder の実装内容や生成処理そのものを調べたいとき。この対象は実体を持たない互換入口なので、実装本体へ進む。
- 新しい acp 機能や API 仕様を追加する場所を探しているとき。この対象は互換維持専用であり、機能追加の入口ではない。
- `acp.*` 参照がすでに全公開面と realization 側から消えていることだけを確認済みで、互換入口の詳細を読む必要がないとき。

## hash
- 9376c267fa8194d94f175e9895f353889128d4ce8fff592333bfe1d50f96077f

# `builder`

## Summary
- ACP builder 領域の realization 側入口。oracle 側 builder を正本に保ちながら、旧来の公開 import 経路を維持する互換 package 群と、quota probe など realization 側で完結する小さな builder を扱う。
- apply、review、session、TUI、indexing、common などの builder 参照を oracle 側 canonical 実装へ接続し、必要な箇所では oracle builder の出力を realization 側公開型へ適合させる境界を持つ。
- 実処理や仕様本体よりも、既存 caller との import 互換性、oracle 側実装への委譲、互換層の残存理由や削除条件を確認するための入口になる。

## Read this when
- ACP builder 周辺で、旧来の公開 import 経路が oracle 側 canonical 実装へどのように接続されているかを確認したいとき。
- apply fork、review、session、TUI、indexing、common などの builder 互換入口を維持・移行・削除できるか判断したいとき。
- oracle 側 builder の生成結果を realization 側の agent call parameter や公開型へ変換・補正する境界を調べたいとき。
- quota availability probe 用の軽量な agent call parameter builder を確認・変更したいとき。
- 同名機能の実装が realization 側にあるように見える場合に、実体を持つ builder なのか互換 import 層なのかを切り分けたいとき。

## Do not read this when
- agent prompt、parameter 生成内容、判定仕様、出力条件などの正本仕様や人間意図を確認したい場合は、対応する oracle 側の仕様または canonical 実装を読む。
- apply、review、session、TUI など各機能そのものの実行フロー、CLI 引数処理、画面描画、git 操作、エラー処理を調べたい場合は、それぞれの機能実装や呼び出し元へ進む。
- AgentCallParameter の基礎データ構造、model、reasoning effort、file access mode、path model、汎用 git helper などの共通定義だけを確認したい場合は、共通実装側を直接読む。
- 個別 builder の変換処理や wrapper の詳細挙動を調べたい場合は、この領域全体ではなく、対象の個別 module または subpackage を読む。
- oracle 側実装への互換 import 経路と無関係な新規公開 API、別領域の builder、または通常の package 構成を調べたい場合は、より直接の対象へ進む。

## hash
- a7b36def9a2c6a687c45ec5430c3be8aeca60205364f8114c0fceebd7f305590
