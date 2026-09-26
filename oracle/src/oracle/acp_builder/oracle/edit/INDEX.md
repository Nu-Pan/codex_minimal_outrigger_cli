# `fork`

## Summary
- エントリーを生成できません。対象には既存の INDEX.md しかなく、責務を説明する本文は確認できませんでした。

## Read this when
- 対象の責務を示す読み取り可能な本文が用意されたときに、内容を確認してエントリーを生成する。

## Do not read this when
- 現在の情報だけから対象の責務を判断する場合。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `launch_exec.py`

## Summary
- `cmoc oracle edit` の2回の呼び出しで共有する完全 prompt と起動パラメータを構築する。編集指示、判断材料、oracle 向け規定、ユーザー指示、呼び出し側が決めた文書検索範囲をまとめる。
- oracle edit 固有の prompt 内容や、両方の呼び出しで使う設定を調べ・変更するときの入口。handoff 用 prompt skeleton もこの構築経路を使う。

## Read this when
- oracle edit agent への共通指示、編集時の判断材料、文書検索範囲、または起動パラメータを確認・変更するとき。
- oracle edit の本体実行と handoff 用 skeleton で共有される prompt 構築を追うとき。

## Do not read this when
- oracle edit の実行順序、呼び出し回数、終了条件、編集境界など機能全体の意味を確認・変更するときは、サブコマンドの意味仕様へ進む。
- 完全 prompt に含める共通規定の構築方式を変更するときは共通 prompt builder、handoff ガイドの文面や構成を変更するときはガイド生成処理へ進む。

## hash
- e23bf352dcdfb81a2ac24bebce84d2730f194511ba833cacb978320aa65cc5d8
