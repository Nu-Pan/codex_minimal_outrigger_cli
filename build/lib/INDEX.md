# `acp`

## Summary
- AI エージェント呼び出しに渡すパラメータとプロンプト本文を構築する実装領域である。目次エントリー生成用の呼び出し条件、TUI 実行前のパラメータ選択依頼、ファイルアクセス規則、ルーティング規則、oracle・realization・レビュー・目次エントリー作成に関する標準文書のプロンプト化を扱う。
- 用途別の呼び出し入口と、共通の完全プロンプト組み立て入口、標準文書部品、Structured Output schema が接続されているため、AI 呼び出し時にどの役割・目標・補助入力・標準文書・出力 schema が渡るかを追う起点になる。

## Read this when
- 目次エントリー生成で、対象内容、読み取り専用のアクセス制約、エントリー生成規則、目次エントリー標準、出力 schema がどのように AI 呼び出しへ渡るか確認したいとき。
- TUI 実行前のパラメータ解決で、ユーザー入力プロンプト、選択候補となるファイルアクセスモード、oracle・realization 関連標準、レビュー関連標準、目次エントリー標準がどのようにプロンプトへ含まれるか確認したいとき。
- AI 呼び出し用の role、summary、goal、補助プロンプト、モデル種別、推論強度、ファイルアクセスモード、Structured Output schema 保存先の対応関係を調べたいとき。
- 完全なプロンプト列に標準文書部品がどの順序と依存関係で追加されるか、または標準注入フラグの変更が最終プロンプトにどう影響するか確認したいとき。
- ファイルアクセス規則、ルーティング規則、oracle と realization の基本説明、oracle 標準、realization 標準、oracle レビュー標準、apply review 標準、目次エントリー標準として AI に提示される文面を確認・変更したいとき。

## Do not read this when
- CLI サブコマンドの実行制御、対象探索、入出力、既存目次の読み書き、TUI の画面操作や起動フローそのものを調べたいとき。
- 構造化文書、標準、要求、パス解決、AgentCallParameter、モデル種別、推論強度、ファイルアクセスモードなどの基礎データ型や汎用 helper の内部実装だけを調べたいとき。
- 個別の oracle file、realization file、テスト、またはユーザーが指定した対象本文の内容を理解・評価したいだけのとき。
- 標準文書の正本仕様断片そのものを人間管理の仕様として確認したいとき。ここは AI に渡すプロンプト文面へ組み立てる実装側の領域であり、正本仕様の所有場所ではない。
- 生成済みの INDEX.md 本文、レビュー結果、TUI 実行結果など、AI 呼び出し後の成果物の内容を確認したいだけのとき。

## hash
- 30a3f9155fbac8ab7c5f7f2bb23da239ccb60921b0520ed2dc62b3ff3c851fad

# `basic`

## Summary
- cmoc の基礎的な内部モデルと軽量ユーティリティを集めた領域。AI エージェント呼び出しに渡す論理的な設定値、ルートトークン付きパスと実パスの相互変換、規範データ構造、構造化された自然言語文書の Markdown 生成を扱う。
- 上位の CLI 実行処理や個別コマンドから利用される基本型・変換 helper の入口であり、cmoc 固有の path token、standard、Structured Output 周辺の内部表現を確認するための起点になる。

## Read this when
- cmoc 内で共有される基本型、列挙値、データクラス、軽量 helper の責務を確認したいとき。
- エージェント呼び出しの設定値として、モデルクラス、reasoning effort、ファイルアクセスモード、プロンプト、Structured Output schema、追加書き込み許可パスをどう保持するか確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` の意味、探索規則、ルートトークン付きパスと実パスの変換規則を調べたいとき。
- 規範を背景・要求・判断例からなる構造として表し、構造化ドキュメントへ変換する内部表現を確認したいとき。
- プログラム内で組み立てた見出し階層、本文、コードブロックを Markdown としてレンダリングする処理や、インデント正規化・空行圧縮の挙動を調べたいとき。

## Do not read this when
- 個別 CLI コマンドの引数、出力 schema、ユーザー向けメッセージ、サブコマンド実行フローを調べたいとき。
- Codex など具体的なバックエンドに渡す実モデル名、reasoning effort 名、サンドボックス設定への変換処理を確認したいとき。
- 実際のエージェントプロセス起動、入出力処理、実行結果解析、エラー処理の流れを確認したいとき。
- 実ファイルの読み書き制御、書き込み可否判定、禁止範囲の適用そのものを調べたいとき。
- oracle file や realization file が従う具体的な規範本文、INDEX.md の生成規則、ルーティング文書の記述方針を確認したいとき。
- Markdown ファイルの本文内容や、特定ドキュメントの仕様記述そのものを読みたいとき。

## hash
- 5f92799c73d8c09813f391faf16a543da6433606f0b904851a63078ad1ef0d34

# `cmoc_runtime.py`

## Summary
- 旧来の直接 import 経路を、実体実装へ委譲する互換レイヤー。公開されているトップレベル import 名と、責務別 runtime module へ移行中の呼び出し元との間をつなぎ、実行時には実体 module と同一として扱わせる。

## Read this when
- 互換 import 経路がどの実装へ転送されるかを確認したいとき。
- トップレベル runtime 名を使う呼び出し元を整理し、互換レイヤーを削除できる条件を判断したいとき。
- パッケージ公開名と内部実装 module の対応を調べる必要があるとき。

## Do not read this when
- runtime の実際の処理内容、状態管理、入出力、例外処理を調べたいときは、委譲先の実体実装を読む。
- 新しい runtime 機能を追加・変更したいときは、互換レイヤーではなく責務別の実装 module を読む。
- ビルド成果物ではなく正本の実装や仕様断片を確認したいときは、対応するソースまたは oracle file を読む。

## hash
- 223b9df223b1746d08a7487389b45587c37917fa6e9b6d75d8dbb48985527074

# `commons`

## Summary
- cmoc のビルド成果物側に含まれる共有 runtime helper 群のディレクトリ。Codex 呼び出し、CLI 共通実行 wrapper、設定入出力、content-addressed 保存、共通エラー表示、Git 操作、runtime logging、実行時パス、結果型、session/apply state など、複数サブコマンドから使われる実行時基盤への入口になる。
- 個別責務は各 runtime 系モジュールに分かれており、集約 import の入口、Codex exec/TUI/preflight/profile/logging、CLI lifecycle、config、content、errors、git、logging、paths、results、state のどこを読むべきかを選ぶための階層である。

## Read this when
- ビルド成果物側の commons 実行時基盤で、Codex 実行、CLI wrapper、設定、Git、ログ、パス、結果、永続 state などのどの補助モジュールへ進むべきかを切り分けたいとき。
- 複数サブコマンドにまたがる runtime 共通処理の import 経路、責務境界、または公開名の集約位置を確認したいとき。
- Codex CLI の非対話実行、TUI 起動、preflight、profile 生成、quota/capacity retry、Structured Output 検証、call log 記録など、Codex 呼び出し周辺の共有実行制御を調べたいとき。
- サブコマンド共通の開始・完了表示、終了コード化、例外表示、logger 設定、runtime state/log の配置など、CLI lifecycle の共通処理を調べたいとき。
- 設定ファイル、content hash、利用者向けエラー整形、git 境界処理、JSONL runtime log、実行時パス、実行結果オブジェクト、session/apply state の共通 helper を探しているとき。

## Do not read this when
- 正本の実装を変更したいとき。ここはビルド成果物側なので、対応する実装元を確認する方が直接的である。
- 個別サブコマンドの業務ロジック、CLI option 宣言、入力検証、出力 schema、利用者向けコマンド定義を調べたいとき。該当するサブコマンド実装へ進む。
- oracle file、realization file、パス語彙、INDEX.md 生成規則などの正本仕様断片を確認したいとき。仕様側の文書や oracle 側の対象を読む。
- テストの期待値、fixture、または検証観点だけを確認したいとき。対応するテスト配置を直接読む。
- 特定 helper の内部挙動だけを確認したいときは、このディレクトリ全体ではなく、config、content、errors、git、logging、paths、results、state、Codex 実行系など責務が一致する個別モジュールを読む。

## hash
- 23467b81ee473014ecad5eb534df0a913d8b02d3bb3d906d07eda9dabcedc51a

# `config`

## Summary
- cmoc のリポジトリ単位設定を表す dataclass 群を扱う領域。AI 呼び出し並列数、Codex CLI 向けモデル・reasoning effort 対応、apply fork と review oracle の処理予算など、設定 JSON として永続化される設定値の構造と既定値を確認する入口になる。

## Read this when
- リポジトリごとの cmoc 設定項目、既定値、設定クラスの構造を確認または変更したいとき。
- Codex CLI に渡すモデル名や reasoning effort 名が、内部のモデル分類・推論努力分類とどう対応するかを調べたいとき。
- apply fork や review oracle の処理件数、ループ回数など、サブコマンド別の挙動予算に関わる設定を確認したいとき。
- 設定 JSON に保存される enum 系の値や、初期化時に生成・同期されるリポジトリ設定の意味を把握したいとき。

## Do not read this when
- 設定ファイルの読み書き、JSON 変換、初期化時の生成・同期処理そのものを調べたいとき。
- 個々のサブコマンドの実行フロー、apply fork の実処理、review oracle の所見列挙・マージ・検証ロジックを追いたいとき。
- モデル分類や reasoning effort 分類そのものの定義を確認したいとき。
- ユーザー向け CLI 引数やコマンド体系の定義を調べたいとき。

## hash
- 522619019f4747cce40a0cdee8aaee0de41f1b8611875fced0e03d9eea250f94

# `main.py`

## Summary
- cmoc の CLI エントリーポイントとして Typer アプリを組み立て、トップレベルコマンドと `session`・`apply`・`review` 配下のサブコマンドを各実装関数へ接続する。
- 通常の CLI 引数解析エラーを cmoc 共通のエラー表示へ変換する TyperGroup 拡張を含み、シェル補完時は通常の Typer/Click 処理に委ねる。
- 実行時の入口ではアプリケーション名を指定して Typer アプリを起動する。

## Read this when
- CLI の公開コマンド構成、サブコマンド階層、各コマンドがどの実装関数へ委譲されるかを確認したいとき。
- 引数解析失敗時のエラー整形、終了コード、補完時の例外処理の扱いを調べたいとき。
- `--scope` や `--force-resolve` など、CLI 層で定義されている option の既定値や渡し先を確認したいとき。
- 新しいトップレベルコマンドまたは既存グループ配下のサブコマンドを CLI に登録する変更を検討するとき。

## Do not read this when
- 各サブコマンドの業務処理、永続状態操作、git 操作、レビュー処理、TUI 処理の詳細を調べたいだけなら、委譲先の実装を直接読む。
- cmoc 共通エラー型やエラー表示フォーマットそのものを変更・確認したいだけなら、エラー定義と描画を担う runtime 側を読む。
- Typer/Click の一般的な使い方や外部ライブラリ仕様を調べたいだけなら、この対象ではなくライブラリ文書を参照する。
- ビルド成果物ではなく正本の実装を変更したい場合は、対応するソース側の CLI エントリーポイントを読む。

## hash
- b6ef09b427ea27ff526149b8d840553659470844d3284c42e959505fec5a9395

# `sub_commands`

## Summary
- 利用者向けサブコマンドの実行処理を集めた実装領域。初期化、対話 TUI、目次保守、session 操作、apply 操作、oracle review など、CLI から呼ばれる主要 workflow の入口になる。
- 各サブコマンドは、共通 runtime helper や設定・状態モデルを使いながら、実行前条件の検証、git branch/worktree 操作、Codex 呼び出し、レポート生成、INDEX.md 更新 commit、後片付けなどの上位 orchestration を担う。
- session、apply、review は下位 module に処理が分割されており、この階層は目的のサブコマンド実装または下位領域へ進むための入口として位置づく。

## Read this when
- 利用者が実行するサブコマンドの制御フロー、前提条件、副作用、成功時出力、失敗時エラー化を確認・変更したいとき。
- init、tui、indexing、session、apply、review oracle のどの実装領域へ進むべきかを判断したいとき。
- サブコマンドが session state、apply state、git branch/worktree、report、INDEX.md 更新、Codex 実行 parameter とどう接続されるかを追いたいとき。
- review oracle や apply のように、複数 module に分割された workflow の上位入口と下位 helper の責務境界を確認したいとき。
- CLI の preflight として目次更新が実行される位置や、サブコマンド実行後に専用 commit・merge・cleanup が行われる流れを調べたいとき。

## Do not read this when
- Typer アプリ全体のサブコマンド登録、ルート CLI dispatch、共通引数 parser だけを確認したいとき。
- git 実行 wrapper、設定読み込み、path keyword、session/apply state schema、report 保存先、timestamp 生成などの低レベル共通基盤だけを調べたいとき。
- Codex に渡す prompt や Structured Output schema の本文定義だけを変更したいとき。
- oracle 正本仕様、INDEX.md エントリー生成基準、realization 標準そのものを確認したいとき。
- 特定の下位責務がすでに分かっており、apply、session、review loop、review report、review targets、review index などの個別 module を直接読む方が狭く済むとき。

## hash
- a9ee3d32f70c81cd3ad409616f5fff722881dbd962ca1692819f69e98b1815ae
