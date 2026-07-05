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
- ACP builder 領域の実装入口。正本側 builder を維持しながら旧来の公開名前空間や import 経路を成立させる互換層と、apply fork・review・session・TUI・quota availability probe 向けの AgentCallParameter 構築境界を扱う。
- 多くの下位要素は実処理本体ではなく、canonical 実装への再公開、oracle 側 builder 戻り値の realization 側公開型への適合、既存 caller 移行まで残す薄い公開面維持を責務にする。

## Read this when
- ACP builder 全体で、旧 import 経路と canonical oracle 実装または realization 側 wrapper の接続関係を確認したいとき。
- apply fork、review、session、TUI、quota availability probe のいずれかの AgentCallParameter builder の入口を探しているとき。
- oracle 側 builder を正本に保ちつつ、realization 側で package path、module alias、戻り値変換、既知の最小補正をどこで行うかを調べるとき。
- acp.builder 配下の互換 package や再公開モジュールを削除できるか判断するために、残す理由・削除条件・移行対象を確認したいとき。
- 通常の agent call parameter 生成ではなく、quota failure 後の readonly availability probe 用 parameter 生成箇所を探しているとき。

## Do not read this when
- agent call parameter、path model、file access mode、Structured Output schema などの基礎型や共通仕様だけを確認したい場合は、それぞれの共通実装や正本仕様を読む。
- prompt 本文、出力条件、parameter 生成内容の人間意図、canonical builder の正本定義を確認したい場合は、対応する oracle 側の文書または実装を読む。
- apply、review、session、TUI の機能本体の制御フロー、CLI 引数処理、画面挙動、branch 操作、finding 処理などを調べたい場合は、各機能の実装側へ進む。
- 新しい公開 API や新規 import 経路を設計したいだけの場合は、互換維持層ではなく公開面や呼び出し元の設計箇所を読む。

## hash
- 774669af8cb48bd45a1d04ce5b00eb73a958c8aa3e2ed10a3bef0deaa3cbee49
