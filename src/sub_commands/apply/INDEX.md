# `_runtime.py`

## Summary
- apply join/abandon で共有する branch/worktree/process cleanup helper。branch が checkout されている worktree の解決、apply branch 名から期待 worktree path への変換、running apply process の停止確認を扱う。

## Read this when
- apply join/abandon 共通の worktree 解決、apply worktree path 導出、apply process 停止制御を確認または変更したいとき。

## Do not read this when
- apply fork の finding loop、apply join の merge、apply abandon の state reset などサブコマンド本体を確認したいとき。

# `abandon.py`

## Summary
- `cmoc apply abandon` の実処理。未 join の apply run を破棄し、apply worktree/branch を cleanup して apply state を ready に戻す。
- session branch と apply branch のどちらから実行された場合も、対応する session worktree を基準に cleanup する。

## Read this when
- apply abandon の事前条件、running process 停止、worktree/branch 削除、state reset、warning 出力を確認または変更したいとき。

## Do not read this when
- apply fork の実行 loop や apply join の merge/force-resolve を確認したいとき。

# `fork.py`

## Summary
- `cmoc apply fork` の実処理。isolated apply worktree を作成し、finding 列挙・refine・適用 loop、禁止差分検査、commit 作成、report 生成を orchestrate する。
- apply scope から対象ファイルを列挙し、Codex CLI 呼び出しで finding enumeration/application と commit message 生成を行う。

## Read this when
- apply fork の事前条件、apply branch/worktree 作成、state 更新、loop 終了条件、対象 path 正規化、終了コードを確認または変更したいとき。
- finding 列挙、refine、application、commit message 生成、dirty target 更新、禁止差分検査の呼び出し順を追いたいとき。

## Do not read this when
- apply join/abandon の cleanup や merge、force-resolve、unexpected changes 判定を確認したいとき。
- apply fork report の Markdown frontmatter や change summary 表示だけを確認したいとき。

# `fork_report.py`

## Summary
- apply fork の通常 report と error report を Markdown + YAML frontmatter として生成する helper。
- apply branch の diff から Codex CLI による change summary を取得し、finding count、result label、変更要約を report file へ描画する。

## Read this when
- apply fork report の保存先、frontmatter、Result、Finding Count、Change Summary、error report の表示内容を確認または変更したいとき。

## Do not read this when
- apply fork の worktree 作成、finding loop、commit 作成、対象 path 正規化を確認したいとき。

# `join.py`

## Summary
- `cmoc apply join` の実処理。apply branch を session branch へ merge し、apply state を ready に戻す。
- unexpected changes の検出・force-resolve、INDEX.md conflict の機械解決、apply worktree/branch cleanup、join report 生成を扱う。

## Read this when
- apply join の事前条件、merge、force-resolve、unexpected changes 判定、INDEX.md conflict 解消、cleanup warning、report 生成を確認または変更したいとき。

## Do not read this when
- apply fork の finding loop や apply abandon の破棄処理を確認したいとき。

# `__init__.py`

## Summary
- apply subcommand package の入口。実処理の再公開や初期化は持たない。

## Read this when
- package としての存在確認だけが必要なとき。

## Do not read this when
- apply 各コマンドの実処理を確認したいとき。
