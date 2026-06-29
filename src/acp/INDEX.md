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
- ACP builder の realization 側互換入口をまとめる階層。正本側 builder 実装を既存の acp.builder 系 import path から利用できるようにする再公開・委譲の境界を扱う。
- apply、indexing、review、session、tui などの builder 領域ごとの互換 package へ進むための上位入口であり、quota probe だけは正本側専用 builder が未整備な制約を補う暫定 adapter を含む。
- この階層の主眼は builder 本体仕様や各機能の実処理ではなく、realization 側に残る公開参照、旧 import 経路、oracle 側実装との対応、互換層の削除条件を見分けることにある。

## Read this when
- acp.builder 系の公開 import path が oracle 側 builder 実装へどう接続されているかを確認したいとき。
- apply、indexing、review、session、tui の各 builder 領域について、実装本体ではなく互換入口・再公開層・委譲境界を探したいとき。
- 既存参照を維持するために残された互換 package や薄い wrapper の理由、対応する正本側実装、削除条件を確認したいとき。
- quota probe 用 AgentCallParameter の暫定 adapter が、runtime 側 prompt literal を避けるためにどこで扱われているか確認したいとき。
- builder 領域の下位構造を見て、apply fork、review oracle、session join、TUI 起動、indexing 互換公開面のどこへ進むべきか切り分けたいとき。

## Do not read this when
- oracle 側 builder の正本仕様、prompt、出力条件、具体的な AgentCallParameter 組み立てロジックを確認したいときは、対応する oracle 側実装または正本仕様断片を読む。
- apply fork、review、session join、TUI、indexing の実処理・制御フロー・データ構造・判定ロジックを調べたいときは、それぞれの処理本体へ進む。
- AgentCallParameter、FileAccessMode、model、reasoning、structured output schema などの共通型や基礎定義を調べたいときは、型定義を持つ基本モジュールを読む。
- 新しい builder 機能の本体実装や仕様変更の根拠を探しているときは、互換入口ではなく正本側 builder または該当機能の実装領域を読む。
- CLI 表示、branch 操作、diff 生成、quota 待機状態機械、TUI 画面処理など、builder 呼び出し準備より外側のワークフローを調べたいときは、該当する runtime や command 実装を読む。

## hash
- b5b380e64fbc75410aff5d5806720ea4c044844bbd1a1b130489457202a145b3
