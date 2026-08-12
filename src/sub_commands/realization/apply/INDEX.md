# `__init__.py`

## Summary
- realization の apply 処理に関する workload を扱うモジュール。apply workload の実装を確認する入口となる。

## Read this when
- realization の apply workload の内容を調査・変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。

## hash
- d6d2ca470e50cfd6872e3d6ceaaf3a134b7f0dc8205826c843ca70d79352d5f7

# `fork.py`

## Summary
- `realization apply fork` の実行フローを担当する CLI 実装。editing run を開始し、差分追従 agent を実行した後、想定外変更・agent による commit・遅延 child の書き込みを検査し、INDEX 生成を含む差分を処理単位として commit して joinable run と fork report を公開する。失敗時は変更を rollback し、error state と report を保存する。
- apply 差分の始点 commit、oracle diff、Codex 実行結果、cleanup 警告、accepted feedback の参照を report に反映するほか、agent の commit 検出、preflight commit の rollback、想定外差分の利用者向けエラー変換などの補助処理を含む。

## Read this when
- `cmoc realization apply fork` の CLI 実行、editing run の joinable/error 遷移、apply 差分の commit・rollback・report 保存の挙動を調査または変更するとき。
- realization apply agent が作成した変更と cmoc が生成する INDEX 差分の境界、agent の commit や遅延 Codex child の扱いを確認するとき。
- apply fork report の差分始点、Codex return code、accepted feedback、cleanup warning の記録内容を確認するとき。

## Do not read this when
- realization apply の agent 起動パラメータ自体を変更する場合は、agent launch parameter の実装を直接読む。
- editing run の共通ライフサイクル、git 操作、state 管理、index refresh の一般仕様を確認するだけの場合は、対応する `commons.runtime_run*` 実装または oracle/specification を直接読む。
- apply fork の利用者向け仕様や run isolation・indexing の正本仕様を確認する場合は、この実装ではなく参照されている app specification を読む。

## hash
- 1d5e79c19264330cf256f3cc06e908f15632a7decd4cccc080038ff69a5b7900
