# `oracle`

## Summary
- `cmoc` の ACP builder 群を束ねる正本仕様の入口。apply, review, session, tui などの各生成処理と、それらで共有する基本型・共通概念・INDEX エントリー契約を読むためのルーティング先。
- 実装差を避けたいのは、ACP builder 配下で共有される出力契約と共通型の境界であり、個別領域に進む前の起点として使う。

## Read this when
- ACP builder 配下のどの領域を読むべきかまだ特定できず、まず共通の正本仕様断片から入口を絞りたい。
- `cmoc` の agent call 生成に関わる各サブ機能の仕様を、個別実装に入る前に確認したい。
- apply, review, session, tui のいずれかが扱う入力条件、出力契約、共通型の境界を確認したい。
- INDEX.md エントリー生成の出力契約や、共通型の定義を基準にしたい。

## Do not read this when
- 特定のサブ機能の個別仕様だけを見たいときは、より下位の対象へ直接進む。
- 実装詳細やテストの挙動を確認したいときは、ここではなく対応する realization code を読む。
- ACP builder 以外の正本仕様や別サブコマンドの仕様を探している。

## hash
- 6a00d5916e32597e234373952a10bc6319826500d31cbfccc418590cd9682597
