# `acp_builder`

## Summary
- AI エージェント呼び出しパラメータと Structured Output schema を構成する oracle src 群への入口。基本パラメータ、各サブコマンド固有の prompt・出力契約、共通部品を扱う。
- 差分要約、レビュー所見、所見対応、INDEX.md エントリー生成、merge conflict marker 解消、TUI 起動時の呼び出し条件など、AI 呼び出しの正本仕様断片を領域別に探すためのまとまり。
- バックエンド実行処理や CLI 制御そのものではなく、AI に渡す role、prompt、権限、モデル方針、preflight 有無、Structured Output schema の正本値を確認する入口。

## Read this when
- cmoc の各機能が AI エージェントを呼び出す際のパラメータ、prompt、Structured Output schema の正本仕様断片を探すとき。
- agent call の基本構造と、個別機能ごとの呼び出し方針・出力契約のどちらを読むべきかを切り分けたいとき。
- レビュー、indexing、apply 後処理、session join conflict 解消、TUI 起動などで AI 呼び出しに渡す情報と応答 JSON の境界を確認したいとき。
- 複数の agent call builder に共通する状態、ルール、結果表現を確認してから個別領域へ進みたいとき。

## Do not read this when
- AI エージェント呼び出しではなく、CLI サブコマンドの実行制御、branch 操作、diff 取得、保存処理、表示整形、対象ファイル探索を調べたいとき。
- oracle standard、realization standard、apply review standard、index entry standard など、レビューや記述品質の標準そのものを確認したいとき。
- prompt builder の共通構成、path placeholder 解決、markdown rendering、StructDoc 表現など、呼び出しパラメータを支える汎用実装の詳細を調べたいとき。
- バックエンド固有のモデル名・reasoning effort 名への変換、プロセス起動、結果処理、エラー処理を確認したいとき。

## hash
- 088701378920a7e78a3df63c28f8263f11d74040889e5c8068c054903760dff0

# `other`

## Summary
- cmoc の正本実装断片のうち、複数領域から参照される基礎モデルや小さな文書生成 helper をまとめる領域。リポジトリ別設定、ルートパスプレースホルダと解決規則、規範文書モデル、構造化 Markdown レンダリングを扱う。
- 設定・パス表記・規範構造・Markdown 生成のように、個別 CLI フローより下位の共通概念を確認する入口になる。

## Read this when
- cmoc のリポジトリ別設定項目、設定ファイルの生成・同期・人間編集・json 変換の正本上の扱いを確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` などのルート概念、プレースホルダ付きパスと絶対パスの変換、相対パス禁止の根拠を確認したいとき。
- AI エージェント並列数、Codex CLI のモデル名・reasoning effort、ファイルアクセス規則違反時のリカバリ回数、apply fork や review oracle の処理予算に関わる実装やテストを変更するとき。
- 規範文書を背景・要求・判断例などの構造として保持するモデルや、要求ラベル付き要求要素の扱いを確認したいとき。
- 階層化された自然言語データやコードブロックを Markdown としてレンダリングする helper の挙動を確認・変更したいとき。

## Do not read this when
- CLI サブコマンドの利用者向け入出力、実行フロー、git 操作、状態ファイルの仕様を調べたいとき。
- INDEX.md のルーティング規則、oracle file と realization file の管理方針、実現ファイルに適用される品質基準そのものだけを確認したいとき。
- 設定の正本ではなく、実際の読み書き処理、シリアライズ処理、init コマンド側の実装だけを確認したいとき。
- 個別の規範本文や、生成済み Markdown 文書の意味・配置先を知りたいだけのとき。
- 特定の作業ディレクトリ内で読むべきファイルを探しているだけで、設定・パスモデル・規範モデル・構造化文書レンダリングを確認する必要がないとき。

## hash
- 66df4eca1718a6d6c335e5e8fbe9d102290d7754e653fb5b491faed31eb68e7c

# `prompt_builder`

## Summary
- agent call に渡すプロンプトの構築に関する基本型、完全プロンプトの組み立て処理、標準文書や読み書き規則などのプロンプト部品を扱う領域。
- 役割・概要・ゴール・補助プロンプト・ファイルアクセス制限・ルーティング規則・各種標準の注入指定を統合し、静的部分、動的部分、プレースホルダ定義の配置を決める入口になる。
- oracle file と realization file の責務境界、品質基準、INDEX.md エントリー規範、レビュー規範など、AI に渡す共通規範プロンプトを生成する下位要素への入口でもある。

## Read this when
- agent call 用の完全なプロンプトが、どの部品からどの順序で構築されるかを確認・変更したいとき。
- oracle standard、realization standard、review standard、apply review standard、index entry standard などの注入指定が、他のプロンプト部品の追加へどう波及するかを確認したいとき。
- ファイルアクセス制限、ルーティング規則、補助プロンプト、プレースホルダ定義を完全プロンプトへ統合する位置や責務を調べたいとき。
- プロンプトキャッシュヒット率を意識した、静的プロンプト、動的プロンプト、プレースホルダ定義の分離と配置を確認したいとき。
- プロンプト生成で使うプレースホルダ名から文字列またはパスへ置換する mapping の基本型を確認したいとき。
- AI に注入する共通規範として、oracle file、realization file、INDEX.md エントリー、ファイル読み書き、レビュー所見の標準文書を確認・変更したいとき。

## Do not read this when
- 特定の CLI サブコマンド、状態ファイル、入出力形式、パスモデルなど、個別プロダクト仕様を調べたいとき。
- 個別の標準文書本文だけを確認したいときは、この領域全体ではなく、該当するプロンプト部品を直接読む方が適切。
- 構造化ドキュメント、標準文書、要求、プレースホルダ mapping などの汎用データ構造そのものを調べたいだけのとき。
- 生成済みプロンプトが実際にどこで agent call へ渡されるかを追いたいときは、呼び出し側の実装を読む方が適切。
- cmoc のパス概念そのもの、または `<cmoc-root>` や `<work-root>` などの意味を調べたいとき。
- 実装ファイルやテストファイルの現在構造を把握して直接修正したいだけで、プロンプト生成や共通規範の注入に関係しないとき。

## hash
- 6d22edbfda78b6d2616c3e6aa3c260d395390f16d7efa659bc1815aa1b78e4f5
