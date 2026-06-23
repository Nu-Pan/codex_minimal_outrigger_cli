# `resolve_parameter.json`

## Summary
- AI Agent CLI/TUI がオリジナルプロンプトを実行する前に、必要な論理ファイルアクセスモードと、読むべき標準文書群を判定するための構造化出力スキーマを定義する。
- 読み取り・書き込み権限の過不足、oracle と realization の基本概念、oracle/realization/review/index entry など各標準を読む必要性を、値と理由の組で返させる入口になる。

## Read this when
- プロンプト実行前のパラメータ解決で、AI に許可すべき論理ファイルアクセス範囲を機械判定させる出力契約を確認したいとき。
- 対象作業に対して oracle と realization の基本、oracle standard、realization standard、review oracle standard、apply review standard、index entry standard のどれを読む必要があるかを判定するスキーマを確認したいとき。
- TUI/ビルダー側で、プロンプト解析結果として返すべき JSON の制約や enum の意味を確認したいとき。

## Do not read this when
- 個別の標準そのものの要求内容を読みたいとき。この対象は標準本文ではなく、標準を読む必要性を返すための出力契約だけを扱う。
- INDEX.md エントリーの書き方やルーティング文書の品質基準を確認したいとき。対象はそれを判定対象の一つとして含むだけで、エントリー生成規則本文ではない。
- 実際のファイルアクセス処理、権限制御、TUI 表示処理の実装詳細を調べたいとき。対象は実行時ロジックではなく、判定結果のデータ形状を定義する。

## hash
- 465e250b14fbc148fd90cb5d78badcabde428a58fc1a97f733b237525c31e0e1

# `resolve_parameter.py`

## Summary
- `cmoc tui` でユーザー入力プロンプトを AI Agent CLI/TUI に渡す前に、実行パラメータ選定用の AI 呼び出しパラメータを組み立てる正本仕様断片。
- 元プロンプト、リポジトリ・作業ルート、ファイルアクセスモード説明、各種標準プロンプトを統合し、読み取り専用のパラメータ解決 prompt とモデル設定を返す責務を持つ。
- TUI サブコマンド固有のパラメータ解決 prompt を調整する入口であり、汎用 prompt 部品や path 解決そのものへ進む前に、この呼び出し側の要求を確認する対象。

## Read this when
- `cmoc tui` の実行前に AI Agent CLI/TUI へ渡すモデル種別、推論強度、ファイルアクセスモード、出力先をどう選ぶか確認・変更したいとき。
- ユーザーがエディタ入力した元プロンプトを、パラメータ選定担当向けの complete prompt にどう埋め込むか確認したいとき。
- TUI のパラメータ解決で、根拠提示、読み取り専用制約、oracle・realization・review・index entry 系標準を prompt に含める条件を確認したいとき。
- TUI サブコマンドのパラメータ解決処理が、path model、file access rule、complete prompt 部品をどう組み合わせるかを把握したいとき。

## Do not read this when
- 実際に AI Agent CLI/TUI プロセスを起動する処理、端末 UI の描画、エディタ入力の取得やコメント除去の実装を探しているとき。
- path キーワードやリポジトリルート・作業ルートの定義そのものを確認したいときは、path model 側を直接読む。
- ファイルアクセスモードごとの詳細な説明文生成を変更したいときは、file access rule の prompt 部品を直接読む。
- complete prompt 全体の共通構成、oracle 標準、realization 標準、review 標準、index entry 標準の本文を変更したいときは、それぞれの prompt 部品または標準定義側を読む。
- TUI 以外のサブコマンドの実行パラメータ解決を調べているときは、そのサブコマンド固有のパラメータ構築対象へ進む。

## hash
- 719c02b1ca692f4a26bd3befdc7648aee221f900b16a2f3f9fbe453a3a5c5922
