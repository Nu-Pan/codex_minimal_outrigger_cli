# `launch_exec.py`

## Summary
- realization apply fork の本命 agent 呼び出しに渡す prompt と AgentCallParameter を構築する。指定 commit 範囲の追従指示や、run worktree を使う起動条件の入口となる。

## Read this when
- realization apply fork の追従指示、差分の扱い、ファイルアクセス範囲、作業ディレクトリなど、agent call の prompt や起動パラメーターを変更・確認するとき。

## Do not read this when
- 追従対象 commit 範囲の決定、fork/join の lifecycle、report やエラー処理を変更・確認するときは、realization apply と編集 run の仕様を直接読む。

## hash
- 876d609de237c78fee621db6eaff66c92a25dfc2b5c7b820d1010f562adb13c5
