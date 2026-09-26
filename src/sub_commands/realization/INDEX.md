# `__init__.py`

## Summary
- realization workloadのサブコマンド群をまとめるパッケージ宣言で、apply系・refactor系の実装へ進む入口です。

## Read this when
- realization workloadのサブコマンド構成を確認し、apply系またはrefactor系の実装を探すとき。

## Do not read this when
- 個別コマンドの処理を調べるときは、該当する下位パッケージの実装を直接確認してください。

## hash
- 45f2cdf62d9edd181a1f1cc14734db2757e556059630746b1486c1bd5d1101b4

# `apply`

## Summary
- `cmoc realization apply fork` の CLI workload を提供し、apply agent の実行から run の joinable/error 公開、fork report の保存までを統括する。
- apply 固有の差分処理と agent 変更の検査を扱うため、このコマンドの実行と run lifecycle の挙動を追う入口となる。

## Read this when
- `realization apply fork` が agent の変更をどのように検査し、joinable/error run として記録するかを調査・変更するとき。
- このコマンドの失敗時の処理や fork report の内容を調査・変更するとき。

## Do not read this when
- agent に渡す指示や call parameter の組み立てを変更するときは、agent call を構築する担当箇所を直接読む。
- 複数コマンドで共有する editing run の lifecycle を変更するときは、共通 runtime の担当箇所を読む。
- realization refactor の対象選択や調査・修正サイクルを変更するときは、refactor workload を直接読む。

## hash
- d40863185d77516049e19fc6bd849813830a8ac44b6937b71b84fb27e935f1e8

# `refactor`

## Summary
- `realization refactor fork` の full-cycle workload を統括し、対象の選択、file ごとの調査・修正、state 更新、処理単位の commit、完了・中断・エラー時の run と report の処理を担う。
- agent の変更と宣言された変更範囲を照合し、再調査対象と current fork 内の未解決所見を管理する。

## Read this when
- `realization refactor fork` の実行、run のライフサイクル、差分検査や commit、未解決所見、完了判定、report の振る舞いを確認するとき。
- 対象選択から file ごとの agent call、state 同期、変更検証までの連携を追うとき。

## Do not read this when
- agent に渡す調査・修正や変更要約の指示文を変更するときは、oracle 側の builder 正本を直接確認する。
- refactor state の列挙・検証・保存方法を調べるときは、共通 runtime の state 実装を直接確認する。
- oracle の差分を realization へ反映する処理を調べるときは、`realization apply fork` の実装を確認する。

## hash
- e2eb497d58ca644f6ff1784000a85f65d9f7ee3b535fad58c2eab768729b74fb
