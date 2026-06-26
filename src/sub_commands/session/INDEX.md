# `__init__.py`

## Summary
- session 系サブコマンド実装を収めるパッケージであることを示す、最小限のパッケージ初期化モジュール。
- 具体的な処理や公開 API は定義せず、下位モジュールへ進むための入口として位置づく。

## Read this when
- session 系サブコマンド実装のパッケージ境界や、パッケージ自体に初期化処理があるかを確認したいとき。
- session 配下の実装を調べる前に、この階層がサブコマンド実装用のまとまりかだけを確認したいとき。

## Do not read this when
- 個別の session サブコマンドの処理、引数、入出力、状態操作を調べたいとき。その場合は具体的な実装モジュールを読む。
- 共通 CLI ルーティング、サブコマンド登録、または session 以外のサブコマンド実装を調べたいとき。

## hash
- a2616b13a1c260f66ad6dfda2f7821fc573b581179e92bbad014a023d5958042

# `abandon.py`

## Summary
- active な session branch を home branch へ merge せず破棄する CLI サブコマンド実装を扱う。
- 実行時 wrapper 経由で本体処理を呼び、session branch・状態値・clean worktree・home branch 存在を確認したうえで、home branch へ切り替え、session state を abandoned に更新し、session branch を削除する。
- cleanup 失敗時は state と branch の rollback を試み、失敗内容・rollback 結果・branch/state file 情報を含む CmocError を返す。

## Read this when
- session abandon の事前条件、実行順序、成功時の branch 切り替え・state 更新・branch 削除の挙動を確認したいとき。
- active session を merge せず破棄する処理のエラー条件や、home branch が無い場合の扱いを変更・調査するとき。
- cleanup 失敗時の rollback 方針、CmocError の詳細情報、利用者向け再実行案内を確認したいとき。
- session abandon 成功時に表示される abandoned branch、切り替え先、session state の出力内容を確認したいとき。

## Do not read this when
- session abandon 以外の session サブコマンドの開始・一覧・適用・完了などを調べたいとき。
- session state の schema、永続化形式、branch から state を読み込む共通処理そのものを調べたいとき。
- git 操作 wrapper、worktree clean 判定、cmoc ignore 設定などの共通 runtime helper の実装詳細を調べたいとき。
- oracle 上の正本仕様や CLI 全体のコマンド登録構造を確認したいだけのとき。

## hash
- a116268c186c80736e9e3a46acdbb740ff0b890b55dcf846e15fa2d7245e4545

# `fork.py`

## Summary
- `cmoc session fork` の実行本体を担い、通常の local branch から新しい cmoc session branch を作成する処理をまとめている。
- CLI runtime 経由のサブコマンド実行、managed branch 上での拒否、clean worktree 要求、既存 active session の検出、session state の生成と保存、利用者向け結果表示を扱う。
- session fork 前に `.cmoc` を git 追跡対象外にできることを確認し、必要に応じて git exclude に追加する補助処理も含む。

## Read this when
- `cmoc session fork` の成功条件、拒否条件、作成される branch や session state の内容を確認したいとき。
- session fork 実行時に clean worktree、managed branch、既存 active session、`.cmoc` の ignore 状態がどの順序で検査されるかを調べたいとき。
- session fork の CLI 出力、git 操作、state file 書き込み、runtime 呼び出しとの接続を変更または検証したいとき。
- `.cmoc` を git の追跡対象外にするための exclude 更新や tracked/check-ignore 判定の失敗条件を確認したいとき。

## Do not read this when
- session fork 以外の session 操作、たとえば join、abandon、status などの挙動を調べたいとき。
- session state のデータ構造、保存形式、path 解決、git wrapper、runtime wrapper そのものの仕様を調べたいとき。
- managed branch 判定、active session 探索、worktree clean 判定の内部実装を確認したいとき。
- oracle の正本仕様やルーティング文書の一般規則を確認したいとき。

## hash
- 959bab3d8f355c87fdaf8eecd3283cbfc6156472faaa809d1a13050f450e4f5c

# `join.py`

## Summary
- active session branch を session home branch へ取り込む session join サブコマンドの実行処理を担う。
- indexing preflight、CLI runtime 経由の実行、session/apply state の事前条件確認、clean worktree 確認、home branch への switch と merge、状態更新、session branch 削除、結果表示までを扱う。
- merge conflict が発生した場合は、unmerged path を特定し、Codex CLI に conflict 解消を依頼した後、marker と unmerged path の残存確認、add、merge commit まで進める。

## Read this when
- session join の実行順序、事前条件、成功時の状態更新や出力内容を確認・変更したいとき。
- active session branch を session home branch へ merge する処理、session branch 削除、削除失敗時 warning の扱いを調べたいとき。
- session join 中の merge conflict を Codex CLI に解決させる流れ、conflict marker 検出、unmerged path 検出、commit までの制御を確認したいとき。
- session.state、apply.state、session_home_branch、clean worktree、cmoc ignore 設定など、session join 前提条件に関わる挙動を追うとき。

## Do not read this when
- session join 以外の session サブコマンドの入口や制御を調べたいとき。
- session/apply state のデータ構造、永続化形式、branch からの state 読み込み実装そのものを確認したいとき。
- Codex CLI へ渡す conflict resolution parameter の具体的な構築内容だけを調べたいとき。
- git コマンド実行、worktree 検査、repo/work root 解決、CmocError の共通実装を調べたいとき。

## hash
- d5c1454f235f4a5020626adc29ba518d6299d297f6c46c32b2c451a2f0da4c0a
