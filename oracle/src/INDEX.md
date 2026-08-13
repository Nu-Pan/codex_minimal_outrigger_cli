# `oracle`

## Summary
- AI エージェント呼び出しに必要な共通パラメータ、パスコンテキスト、モデル・推論設定、ファイルアクセスモードを定義する。agent call の用途別に、indexing、oracle review・edit・investigation、realization、feedback、session join、TUI、quota probe の prompt と起動パラメータを構築する。
- prompt_builder は完全 prompt と規則部品の組み立てを担い、other は設定・パスモデル・構造化 Markdown の共通モデルを担う。用途別の agent call 定義や共通モデルを確認する際の上位入口として、配下の indexing、oracle、realization、feedback、session、tui、prompt_builder、other へ進む。

## Read this when
- agent call の共通パラメータ、作業ディレクトリ、モデル・推論設定、Structured Output、indexing preflight、ファイルアクセスモードを確認・変更するとき。
- indexing、oracle、realization、feedback、session join、TUI、quota probe のいずれかで、用途別の prompt と起動パラメータの定義場所を判断するとき。
- prompt の共通規則、パス placeholder と worktree の解決、設定データモデル、構造化 Markdown の生成処理を調査・変更するとき。

## Do not read this when
- 特定用途の prompt、Structured Output、または起動パラメータの詳細が対象として明確なときは、その用途の下位定義を直接読む。
- prompt の共通部品だけを調べるときは prompt_builder 配下を直接読む。
- 設定、パス解決、構造化 Markdown のいずれか一つだけが目的のときは other 配下の該当モデルを直接読む。
- agent call の実行処理、対象ファイルの仕様、通常の session join 処理だけを調べるときは、それぞれの実行側・仕様側の対象を直接読む。

## hash
- 838781aafc655d65d27d71a9f4108601baf87218e37bb8211c147ef27d03ddc4
