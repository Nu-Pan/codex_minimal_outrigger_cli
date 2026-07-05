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
- ACP builder 群の realization 側領域。oracle 側 builder を正本に保ちながら、旧来の `acp.builder.*` import 経路を維持する互換入口と、apply fork・quota probe・review・session・TUI など個別用途の builder 接続層をまとめる。
- 主な責務は canonical oracle 実装への委譲・再公開、realization 側公開型への最小適合、既存 caller 移行までの互換維持であり、prompt 内容や正本仕様そのものは oracle 側に置く。

## Read this when
- `acp.builder.*` の旧 import path 互換がどの oracle 実装、互換 package、個別 builder へつながるかを調べるとき。
- ACP builder まわりで、oracle 側 builder を正本に保ちながら realization 側で package path、module alias、公開型変換、最小補正をどう扱っているか確認するとき。
- apply fork、quota availability probe、review oracle、session、TUI 起動などの AgentCallParameter 構築入口や、各用途の互換層をどこから読むべきか判断するとき。
- 旧 import 経路や再公開モジュールを削除・移行する作業で、残す理由、削除条件、canonical path への接続先を確認するとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容の正本仕様や人間意図を確認したいだけなら、対応する oracle 側 builder を読む。
- apply、review、session、TUI など各機能の実行フロー、画面挙動、branch 操作、finding 処理、イベントループなど builder 以外の本体実装を調べたいなら、該当機能の実装へ進む。
- AgentCallParameter の基本型、構造化出力 schema、path model、汎用 git helper、file access mode 全体など、builder 互換入口や個別 parameter 構築境界と無関係な共通定義を調べたい場合。
- 新しい公開 API や新規 import 経路を設計したい場合。既存互換面ではなく、正本仕様や利用者向け公開面を扱う対象を読む。

## hash
- e9da21bdefb5ed02aaf539bf4af976f769a5ac178b2f955b1f61501cc8451aa7
