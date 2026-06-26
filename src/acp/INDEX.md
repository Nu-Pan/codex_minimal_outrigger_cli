# `builder`

## Summary
- AI エージェント呼び出しに渡す prompt、補助文脈、ファイルアクセス条件、モデル設定、推論量、Structured Output schema の組み立てを、用途別に扱う実装領域。レビュー、適用、競合解消、TUI 実行前解決、ルーティング文書用エントリー生成など、cmoc の各工程で AI に何を読ませ、何を返させ、どの制約で作業させるかを確認する入口になる。
- 工程ごとの制御フローそのものではなく、AI 呼び出しパラメータと機械処理用の出力契約を追うための領域。oracle file、realization file、review standard、git diff、既知所見、conflict 対象、元プロンプトなどを、各エージェントへどの意味の文脈として渡すかを把握できる。

## Read this when
- cmoc の各サブコマンドや TUI で、AI エージェントへ渡す role、goal、補助 prompt、参照コンテキスト、ファイルアクセスモード、モデル種別、推論量を確認または変更したいとき。
- AI の Structured Output schema が、レビュー所見、理由、採否、所見整理操作、差分要約、ルーティング文書用エントリー、TUI 実行前の判定結果などとしてどの責務を持つか確認したいとき。
- oracle file だけを根拠にする、realization file への書き込みを許可する、git add・git commit を禁止する、conflict 解消時だけ oracle file の最小編集を例外的に許すなど、AI 作業制限の組み立てを追いたいとき。
- 既知の所見や理由、検出済み conflict、対象本文、作業後差分、元プロンプトなどの入力情報が、AI 呼び出しの補助文脈へどう反映されるかを調べたいとき。
- INDEX.md エントリー生成や TUI 実行前パラメータ解決のように、AI に判断させる内容とその返却契約を実装・テストしたいとき。

## Do not read this when
- CLI 引数解析、サブコマンド全体の実行順序、fork 作成、branch 操作、merge 実行、差分適用、保存、表示、集計など、AI 呼び出しパラメータ構築の外側にある orchestration を調べたいとき。
- oracle file、realization file、review standard、apply review standard、INDEX.md 運用規則などの正本仕様や基準本文そのものを確認したいとき。
- AgentCallParameter、ModelClass、ReasoningEffort、FileAccessMode、markdown rendering、構造化ドキュメント表現、パス解決などの共通基盤の定義や汎用実装を調べたいとき。
- 実際の変更対象ファイルの中身、個別差分の検出処理、変更カテゴリ分類、conflict marker 検出や解消アルゴリズム、TUI の表示・対話・入力取得を調べたいとき。
- 個別の INDEX.md エントリー本文を作成・評価したいだけで、エントリー生成に使う schema やエージェント呼び出しパラメータの実装を確認する必要がないとき。

## hash
- 3d80b6cf3c308bdfa53ab5b527a5ec024582d37bf2d5271809fd0cb5fab6a8cf

# `prompt_parts`

## Summary
- AI agent 呼び出しに渡す構造化プロンプトを、基本プロンプト、ファイルアクセス規則、ルーティング規則、任意追加文書、各種標準文書から組み立てる実装群を扱う。
- oracle file と realization file の基本概念、oracle file の記述標準、realization file の保守標準、oracle レビュー基準、oracle と realization の照合レビュー基準、INDEX.md エントリー基準、INDEX.md を使った読み進め方を、それぞれ StructDoc として生成する入口になっている。
- Codex CLI 向けに root token や用語を実パス・作業者向け表現へ置換し、要求された基準プロンプトに必要な前提基準を自動的に含める層でもある。

## Read this when
- AI agent に渡す完全なプロンプトが、どの規則・基準文書をどの順序で含めるか確認または変更したいとき。
- ファイルアクセス規則、INDEX.md ルーティング規則、oracle/realization の基本説明、oracle/realization の品質基準、レビュー所見基準、INDEX.md エントリー基準の本文生成を調整したいとき。
- 基準プロンプトの有効化フラグ、依存関係、注入順序、または Codex CLI 向けの用語・root token 置換を変更したいとき。
- agent に提示される規範文書の内容が、構造化文書としてどこで作られているかを探したいとき。

## Do not read this when
- 実際の CLI サブコマンド実行、永続状態操作、入出力 schema、作業ディレクトリ管理など、プロンプト生成ではない実行時挙動を調べたいとき。
- 構造化文書、標準項目、要求項目、パスモデル、ファイルアクセスモードの型定義や共通データ構造そのものを確認したいとき。
- 個別の oracle file が定めるプロダクト仕様や、特定機能の実装・テスト詳細を探しているとき。
- INDEX.md エントリー作成のために対象本文がすでに個別ファイルへ絞れており、プロンプト部品全体の構成を確認する必要がないとき。

## hash
- 40fcbd0059bc3f3d6b77da462b3ea48a0406fb0caac37ebd87aaa4e7154b201a
