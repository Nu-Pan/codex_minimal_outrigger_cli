# `__init__.py`

## Summary
- realization の apply workload を示すパッケージ説明です。実行処理を追う際は、配下の workload 実装が入口になります。

## Read this when
- realization の apply workload が refactor workload とどう区別されるか、パッケージ説明を確認するとき。

## Do not read this when
- コマンド登録や fork の実行手順を調べるとき。このファイルはパッケージ説明のみなので、登録箇所または workload 実装を確認してください。

## hash
- d6d2ca470e50cfd6872e3d6ceaaf3a134b7f0dc8205826c843ca70d79352d5f7

# `fork.py`

## Summary
- `cmoc realization apply fork` の実行を束ね、追従対象の差分範囲を確定して agent を起動し、変更の検査、INDEX 更新を含む処理単位の commit、joinable 公開と report 保存まで進める。
- 実行失敗や想定外差分では、処理単位の rollback、run の error 化、report 保存を行う。この対象は apply fork 固有の実行と回復の入口であり、agent 指示の構築や共通 run 処理の実装とは責務が異なる。

## Read this when
- realization apply fork の実行順序、変更の受け入れ検査、joinable/error への遷移、report、失敗回復を調べるとき。
- apply fork がどの差分範囲を agent に渡し、どの時点で生成 INDEX と realization の変更を処理単位として確定するかを追うとき。

## Do not read this when
- agent に渡す指示文、対象差分の選び方、起動パラメーターの構築を変更・調査するときは、apply fork の launch parameter builder を読む。
- editing run の作成・状態管理・commit・rollback など、apply fork に限らない共通 lifecycle の挙動を調べるときは、共通 run lifecycle の実装を読む。
- realization refactor fork の実行や結果処理が対象なら、refactor fork の workflow を読む。

## hash
- 3bf4b968b8db9501671e1ec9c2015fba2f3c8ddf1433425df2ea4a2868471ba3
