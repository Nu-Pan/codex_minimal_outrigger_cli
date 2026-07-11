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
- `acp.builder` 配下の互換入口と正本側 builder への転送層を束ねる領域。旧 import path を維持する薄い公開面、正本実装へつなぐ再公開、最小補助実装をここから辿れる。
- 個別サブ領域は `apply`、`indexing`、`review`、`session`、`tui` に分かれており、いずれも既存参照の互換維持か、正本側実装への接続を主目的にしている。
- `common` は共通ビルダー処理の置き場だが、現時点では本文ファイルを持たない。
- `quota_probe.py` は quota 回復確認用の最小 probe 呼び出しを構築する。

## Read this when
- `acp.builder.*` の旧 import 互換を残すか削るか判断したい。
- 正本側の builder を旧公開名からどう辿るか、あるいはどの互換入口が残っているか確認したい。
- 各サブ領域の互換 wrapper と、正本側実装への接続境界を確認したい。
- quota 回復確認のための最小呼び出し内容を確認したい。

## Do not read this when
- 正本側の具体的な実装内容や仕様本体を確認したい場合は、`oracle` 側の各対象を読む。
- 互換入口ではなく個別機能の中身を確認したい場合は、各サブモジュールの実体を読む。
- `common` の実装詳細を探している場合は、現時点ではこの対象からは読めないので別の本文へ進む。
- `acp.builder` 以外の公開面や、互換以外の新規 API を探している場合はこの領域は対象外。

## hash
- 3b1b868c23f0567c2cb6b0771b4b4c0eed7c3dd56f510623612100ff50339996
