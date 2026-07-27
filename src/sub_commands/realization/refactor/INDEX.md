# `__init__.py`

## Summary
- realization のリファクタリング作業を扱うパッケージ。関連するリファクタリング処理への入口となる。

## Read this when
- realization のリファクタリング作業の内容や構成を確認するとき。

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき。

## hash
- d070e139f0ebc38e439ff4bf3b37f76a7a536a3424248e4afcc0525de0573746

# `fork.py`

## Summary
- realization refactor fork の一連の実行ライフサイクルを担う CLI 実装。run の開始・初期化、realization file 単位の agent 調査と修正、差分検証、refactor state 更新、commit、完了判定、割り込み・エラー時の cleanup、fork report 生成までを同一の進捗状態で管理する。
- realization refactor の fork サブコマンドの処理順序、unresolved finding の保持、調査対象 state と report の整合性を確認するための主要な入口。個別の agent parameter や report 描画ロジック自体を変更・調査する場合は、対応する import 先の実装を直接読む。

## Read this when
- realization refactor fork サブコマンドの挙動、処理単位、完了条件、commit 単位を変更または調査するとき
- refactor state と unresolved finding の整合性、調査対象の再投入条件を確認するとき
- fork の joinable・error・user interruption 遷移、cleanup、report 保存を確認するとき
- realization file 以外の差分拒否や run worktree の変更分類を調査するとき

## Do not read this when
- realization refactor の agent 入力パラメータや change summary の schema だけを確認するときは、対応する builder 実装を直接読む
- 共通 run lifecycle、process tracking、state 永続化、report 基盤の一般挙動だけを確認するときは、各 commons モジュールや oracle specification を直接読む
- INDEX 更新処理そのものだけを調査するときは、indexing 関連の実装を直接読む

## hash
- 62419f1781b0cbe23b07e0ecd6866939f0b68626f9ea44d4aa32d4e850e453b8
