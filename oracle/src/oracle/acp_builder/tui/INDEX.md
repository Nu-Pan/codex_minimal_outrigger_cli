# `launch_tui.py`

## Summary
- `cmoc tui` 用の完全 prompt と、Codex CLI の TUI 起動パラメータを組み立てる。ユーザー入力と呼び出し側で確定した閲覧範囲を使い、作業ディレクトリ、アクセスモード、editor input handoff を設定する。

## Read this when
- `cmoc tui` のユーザー入力を prompt に組み込む方法や、起動時の作業ディレクトリ、アクセスモード、閲覧範囲、editor input handoff を確認・変更するとき。

## Do not read this when
- `cmoc oracle investigation` の調査指示、oracle 内に限定した根拠範囲、read-only 起動設定を調べるときは、その用途専用の起動定義から読む。
- 呼び出し種別をまたぐ完全 prompt の共通生成ロジックを調べるときは、共有 prompt builder を直接読む。

## hash
- c88da10f9f490ef6fc49470b0ec33ac15558db6d8b28ad442e10bc6c1013bfc2
