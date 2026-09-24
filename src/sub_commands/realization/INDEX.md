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
- `cmoc realization apply fork` の実行制御を担い、編集 run の開始、差分範囲の確定、agent 実行、変更検査と commit、joinable/error 状態の公開、fork report の保存までを扱う。失敗時は未確定差分を戻して error を記録する。

## Read this when
- apply fork の run lifecycle、agent 差分や生成 INDEX の検査・commit、状態公開、失敗時 cleanup を調べる、または変更するとき。
- apply report に記録する差分範囲、agent の終了結果、受理済み feedback、cleanup 警告の扱いを調べるとき。

## Do not read this when
- agent に渡す実行 parameter や prompt の組み立てを調べるときは、その生成処理へ進む。この対象は生成結果を使って runtime を制御する。
- apply の規範的な要件や利用者向け command semantics を確定するときは、正本仕様や command 定義を確認する。この対象は runtime 実装である。
- 共通の run lifecycle、process tracking、indexing の振る舞い自体を変更・調査するときは、該当する共通 runtime 処理へ進む。この対象は apply fork からそれらを呼び出す。

## hash
- 34f5bd87eebd7912ce893b5903b7f5ad75593ab25165f531e8f24f2407149894

# `refactor`

## Summary
- realization file を対象ごとに調査・修正する refactor fork の実行ライフサイクルを担います。対象選択、差分検査、refactor state と unresolved finding の管理、処理単位の commit、完了・中断・エラー時の report までを扱います。

## Read this when
- `realization refactor fork` の処理順序、対象の再調査、finding の扱い、または run の完了条件を調べるとき。
- refactor fork 固有の差分検査、commit、割り込み・エラー処理、report の生成を変更・調査するとき。

## Do not read this when
- oracle の差分をもとに realization を追従させる apply fork の動作を調べるときは、`realization apply` の実装へ進んでください。
- refactor agent に渡す指示文や出力仕様自体を調べるときは、その builder の正本である oracle 側の定義を確認してください。
- refactor に限らない run の共通 lifecycle を調べるときは、共有 runtime の実装へ進んでください。

## hash
- 3ce928d565a11c0b77ec274c84a07ee75ebf6e61799aaa1112966ce4aa056db6
