# `launch_tui.py`

## Summary
- `cmoc tui` で AI Agent CLI/TUI を起動するための呼び出しパラメータを構築する正本仕様断片。
- role、summary、goal、file access mode、各種標準適用フラグ、ユーザーの元プロンプトから完全プロンプトを生成し、TUI 用ログへ保存したうえで、エージェント呼び出しに渡すモデル種別・推論努力・入力指示・対応する JSON パスを決める。
- TUI 起動時に完全プロンプトをどう保存し、その保存済みプロンプトを読むようエージェントへどう指示するかを確認する入口。

## Read this when
- `cmoc tui` の起動時に、AI エージェントへ渡す `AgentCallParameter` の組み立て方を確認したいとき。
- TUI 起動用の完全プロンプト生成、元プロンプトの埋め込み、標準適用フラグの渡し方、保存先ログの扱いを確認したいとき。
- TUI 起動で使用するモデルクラス、reasoning effort、file access mode、プロンプトファイル参照指示、対応 JSON パスの正本を確認したいとき。

## Do not read this when
- 完全プロンプトそのものの文書構造や各標準フラグの意味を確認したいだけなら、完全プロンプト構築側を読む。
- パス語彙や repo root 解決の定義を確認したいだけなら、path model 側を読む。
- TUI ではないサブコマンドのエージェント呼び出しパラメータや、実際の CLI/TUI 実行制御を調べたい場合は、その対象を扱う別の仕様断片へ進む。

## hash
- 390d6a06f8db7bb76dec61a29387c709f0d31413419e371c67698bd08f7f1e9b

# `resolve_parameter.json`

## Summary
- AI Agent CLI/TUI がオリジナルプロンプトを実行する前に、役割・作業概要・ゴール・`build_faprofile` 引数・各種標準文書を読む要否を、根拠付きで解決するための入力パラメータ schema を定義する。
- 権限設定は `oracle` / `realization` / `index` それぞれの deny / read / write として直接指定させ、oracle と realization の基本、oracle standard、realization standard、review oracle standard、apply review standard、index entry standard の参照要否を boolean と理由の組で表す。

## Read this when
- オリジナルプロンプトから、AI Agent CLI/TUI に渡す実行前パラメータを構造化して決める処理を実装・検証する。
- 作業の役割、概要、ゴール、必要最小限の `build_faprofile` 引数を、理由付きで出力する schema を確認する。
- oracle / realization 関連の標準文書を読むべきかどうかを、各標準ごとに boolean と根拠で表す出力仕様を確認する。
- TUI のパラメータ解決結果について、追加プロパティ禁止、必須項目、列挙値、各フィールドの意味を確認する。

## Do not read this when
- 実際の oracle file や realization file の編集方針そのものを確認したいだけで、TUI が実行前パラメータとしてそれらの参照要否をどう表すかは不要である。
- review oracle や apply review の個別コマンド挙動を知りたい場合。ここでは、それらの標準を読む必要があるかどうかを表す枠組みだけを扱う。
- INDEX.md エントリー自体の書き方を確認したい場合。ここでは index entry standard を読む要否を表す項目はあるが、標準本文の内容は定義しない。

## hash
- ab8a62116997e160f4a49279b56a75b8d414286104b93da95e0b4f30c266395e

# `resolve_parameter.py`

## Summary
- `cmoc tui` でユーザー入力プロンプトを AI Agent CLI/TUI に渡す前に、実行パラメータ選定用のエージェント呼び出し内容を組み立てる正本仕様断片。
- 元プロンプトを動的な補助文書として埋め込み、ファイルアクセスモード候補、パス placeholder、oracle/realization/review/index entry 系の固定プロンプトを含む完全プロンプトを作る入口になっている。
- 返却するエージェント呼び出し条件として、効率向けモデル、中程度 reasoning、readonly ファイルアクセス、生成した markdown prompt、対応する structured output schema を結び付ける。

## Read this when
- `cmoc tui` の実行前に、元プロンプトからどの AI Agent CLI/TUI 呼び出しパラメータを解決させるかを確認・変更したいとき。
- 実行パラメータ解決担当エージェントへ渡す role、summary、goal、補助文書、placeholder、標準プロンプト群の有効化範囲を確認したいとき。
- `cmoc tui` のパラメータ解決が readonly 前提で行われること、または選定根拠に元プロンプトやリポジトリ内ファイルの該当箇所を求めることを確認したいとき。

## Do not read this when
- 個別のファイルアクセスモード説明文そのものを確認したいだけのときは、その説明文を構築する対象を読む。
- リポジトリルートや作業ルートの定義・解決規則を確認したいだけのときは、パスモデルの正本を読む。
- エージェント呼び出しパラメータ、モデル種別、reasoning effort、ファイルアクセスモードの型定義を確認したいだけのときは、それらの基本定義を読む。
- `cmoc tui` の画面操作、入力エディタ処理、または実際のサブコマンド実行フローを調べたいときは、このパラメータ解決 prompt ではなく TUI 実行側の正本を読む。

## hash
- e180b35e78539c69acafa754147999ae37a1145db83a252aa0f4e3717913fb3d
