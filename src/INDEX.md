# `acp`

## Summary
- AI Agent CLI/TUI へ渡す呼び出し契約を組み立てる実装領域。role、summary、goal、補助文脈、論理ファイルアクセスモード、モデル種別、reasoning effort、構造化出力 schema を、用途別のエージェント呼び出しパラメータとしてまとめる処理を扱う。
- エージェント呼び出しに含める標準プロンプト部品の生成領域でもある。ファイルアクセス規則、ルーティング規則、oracle/realization の基本説明、oracle・realization・review・INDEX.md エントリーの各標準を構造化文書として生成し、依存関係に従って完全なプロンプト列へ組み込む入口になる。
- 扱う用途は、実装所見の列挙・整理・修正・変更要約、oracle file レビュー、目次エントリー生成、merge conflict marker 解消、TUI 実行前のパラメータ選定に分かれる。サブコマンド本体ではなく、別エージェントに何を読ませ、どの権限・schema・モデル設定で起動するかを追うための上位入口である。

## Read this when
- サブコマンドが別エージェントを起動する際の prompt、補助文脈、構造化出力 schema、モデルクラス、reasoning effort、論理ファイルアクセスモードの対応関係を確認または変更したいとき。
- レビュー、適用、目次生成、TUI パラメータ選定、conflict 解消の処理で、対象パス、対象本文、git diff、所見、既知理由、conflict 対象、ユーザープロンプトなどがエージェント向け文脈へどう埋め込まれるかを追いたいとき。
- AI agent に渡す共通説明として、ファイルアクセス規則、INDEX.md を使った読み進め方、oracle file と realization file の責務境界、各種標準規範をどのように文章化しているか確認したいとき。
- 完全なプロンプト列の組み立て順、標準プロンプト部品の依存関係、用途ごとの標準規範の有無を調整したいとき。
- 新しいエージェント呼び出し用途や標準プロンプト部品を追加する前に、既存の呼び出し契約・schema・標準文書生成の置き場所と責務分担を確認したいとき。

## Do not read this when
- CLI のサブコマンド登録、引数解析、ファイル走査、git 操作、永続状態更新、結果保存、TUI 表示など、エージェント呼び出しパラメータを使う側の実行フローを調べたいとき。
- パス解決、構造化文書の低レベル型、Markdown レンダリング、AgentCallParameter やモデル種別・ファイルアクセスモードの共通型定義そのものを確認したいとき。
- oracle file、realization file、各種 standard の正本本文や、個別機能仕様の内容を読みたいだけのとき。ここにあるのはそれらを agent prompt へ載せるための生成処理である。
- 実際の修正対象ファイル、テスト実装、merge conflict の具体的な解消内容、またはレビュー所見に対する個別コード変更の中身を調べたいとき。
- Structured Output schema の利用者向け意味ではなく、保存済み結果やサブコマンド出力の後段処理を追いたいとき。

## hash
- fffff767eca88b1e63dae9267b57d9765e73306acee7fc73c5aa5c1c5c9da8ce

# `basic`

## Summary
- cmoc の realization implementation のうち、複数機能から参照される基礎的なデータ構造と小規模ヘルパーをまとめる領域。AI エージェント呼び出し条件、ルートトークン付きパス表記、規範データ構造、階層化文書の Markdown 生成を扱う。
- バックエンド実行や CLI 表層へ渡る前の抽象モデル、パス解決、仕様・文書表現の共通部品を確認する入口になる。

## Read this when
- エージェント呼び出しに渡す抽象的な条件、論理モデル、Reasoning effort、ファイルアクセスモード、Structured Output schema の有無を表す内部データ構造を確認・変更したいとき。
- cmoc で使う `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` 付きパス表記を実パスへ解決する挙動、または実パスをルートトークン表記へ戻す挙動を確認・変更したいとき。
- ルートトークンなし相対パスの拒否、ルートディレクトリ探索、linked worktree や git common dir を含む worktree 判定を調べたいとき。
- 規範をコード上で保持するための構造、要求ラベル、要求本文の単位、規範オブジェクトから構造化文書を生成する処理を確認したいとき。
- 階層化された自然言語文書、仕様断片、レポートなどを Markdown 見出し付きテキストとして生成する小さな文書レンダリング処理を確認・変更したいとき。
- Markdown の fenced code block 出力、見出し階層の増加、不正な子要素型の扱い、複数行文字列の空行除去や共通インデント解除を調べたいとき。

## Do not read this when
- 具体的なモデル名、API パラメータ、サンドボックス設定など、バックエンドが実際に受理する値への解決処理を確認したいとき。
- エージェント呼び出しの実行、プロセス起動、結果取得、エラー処理の制御フローを確認したいとき。
- プロンプト本文の生成規則、Structured Output schema ファイル自体の内容、または schema 検証仕様を確認したいとき。
- CLI サブコマンドの引数定義、利用者向け出力、終了コードなど、コマンド表層の挙動を調べたいとき。
- oracle file と realization file の所有関係、編集責務、正本仕様断片としての分類だけを確認したいとき。
- 個別の規範本文や、人間が責任を持つ正本仕様断片そのものを確認したいとき。
- Markdown の解析、既存 Markdown からの構造復元、Markdown AST 全般、または HTML・JSON・YAML など Markdown 以外の出力形式を扱う処理を探しているとき。
- テスト構成、fixture、テストケース追加先を探しているとき。

## hash
- d3aad06d83ff66fc13f8fb9d2b897568f32a25560a111334d1c889e5a85384b5

# `cmoc_runtime.py`

## Summary
- 互換用の薄い入口であり、実体のランタイム実装を別モジュールから読み込んで、この import path 自体を実装モジュールへ差し替える。
- 旧来の直接 import 経路や公開設定上の import 経路を残すための橋渡しで、責務固有のランタイム処理はここには置かない。

## Read this when
- トップレベルのランタイム import path がどの実装へ接続されるかを確認したいとき。
- 互換 import 経路の維持・削除条件や、直接 import している呼び出し元への影響を確認したいとき。
- ランタイム実装を移動・分割したあと、この互換入口を残す必要があるか判断したいとき。

## Do not read this when
- ランタイム処理そのものの挙動、引数処理、状態管理、出力生成を調べたいとき。その場合は実体の実装モジュールを読む。
- 新しいランタイム機能や責務固有の処理を実装したいとき。この互換入口ではなく実体側のモジュールを読む。
- パッケージ公開設定やエントリーポイント定義を確認したいだけのとき。その場合は設定ファイルを読む。

## hash
- 223b9df223b1746d08a7487389b45587c37917fa6e9b6d75d8dbb48985527074

# `commons`

## Summary
- cmoc の複数サブコマンドや上位モジュールから共有される runtime helper 群をまとめる実装領域。Codex CLI 呼び出し、profile 生成、設定同期、content hash、CLI 実行ラッパー、error 表示、Git 操作、logging、path 解決、実行結果型、session/apply 状態など、個別 command から横断的に使われる共通処理を扱う。
- 共有 runtime API の集約入口も含み、上位コードがどの helper・型・状態・git/path/logging 機能を import できるかを確認する入口になる。

## Read this when
- CLI サブコマンドに共通する実行フロー、進捗表示、終了コード化、例外表示、subcommand log、current logger 設定を確認または変更したいとき。
- Codex CLI の exec/TUI 呼び出し、profile/schema/environment の準備、Structured Output 検証、capacity/quota error の retry・待機・resume 制御、呼び出しログを調べるとき。
- Codex profile、file access mode からの sandbox/permission profile 生成、CODEX_HOME 検証、hashed profile/schema 準備、Codex 出力からの error/resume token 抽出を扱うとき。
- `.cmoc` 配下の config、sessions、reports、logs、worktrees、schema state など runtime 保存先の組み立て、root path 解決、timestamp、duration 表示、一時 cwd 変更を確認するとき。
- Git repository 状態検査、cmoc 管理 branch/worktree の作成・削除、worktree prune、`.cmoc` の ignore 保証、Git ignore 判定などの共通 Git helper を確認または変更したいとき。
- サブコマンド実行ログの JSON Lines record、経過時間、quota 待機時間、context-local logger の受け渡しを調べるとき。
- session/apply state の JSON schema、読み書き、branch 名からの session-id 抽出、active session 探索を確認または変更したいとき。
- 外部コマンド結果や Codex exec 結果として共有される型、または共通 runtime API の公開 symbol を追加・削除・移動するとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、引数定義、ファイル生成内容、ユーザー向け出力の順序だけを調べたいとき。その場合は該当 command 実装へ進む。
- path キーワードそのものの概念定義や、root path model の正本的な意味を確認したいだけのとき。その場合は path model を扱う仕様・実装へ進む。
- 設定 dataclass の項目定義や既定値そのもの、AgentCallParameter、FileAccessMode、model class、reasoning effort の入力構造だけを確認したいとき。その場合は basic/acp や config 定義側へ進む。
- ログを読む側、集計する側、表示する側の仕様や実装を探しているとき。この領域は主にログ生成・追記の共通 runtime を扱う。
- Codex CLI や Git を使う高レベルな command orchestration 全体を追いたいとき。共通 helper の詳細ではなく、呼び出し側の runner や command 実装から読む。
- INDEX.md の hash 更新ロジック、oracle/realization のルーティング生成仕様、または Git ignore 判定以外の index 管理処理を調べたいとき。

## hash
- 13124618470501c87b407d8bf5a0f946309adfd68053d52593d85cbb9c09361d

# `config`

## Summary
- 開発対象リポジトリごとに変わりうる cmoc の設定データ構造を扱う領域。
- 永続化される設定の最上位構造、Codex CLI に渡すモデル名・推論 effort 名への対応、apply 系および review oracle 系ループ回数上限の入口になる。

## Read this when
- 開発対象リポジトリごとの cmoc 設定項目、既定値、設定データクラスの構造を確認・変更したいとき。
- Codex CLI 呼び出しに使うモデル名または reasoning effort 名への対応を確認・変更したいとき。
- apply fork の apply ループや所見リスト改善ループの上限回数を確認・変更したいとき。
- review oracle の所見列挙・マージ・検証ループの上限回数を確認・変更したいとき。
- 永続化される config の dataclass 構造や Enum 系設定値を文字列値へ変換する前提を追うとき。

## Do not read this when
- CLI 引数の定義、サブコマンドの実行フロー、または設定値を実際に読み書きする処理だけを調べたいとき。
- モデル区分や推論 effort 区分そのものの定義・意味を確認したいとき。
- 個別サブコマンドの処理内容や所見リストの生成・改善・検証ロジックを調べたいとき。
- リポジトリルート、作業ディレクトリ、実行ディレクトリなどのパス概念の定義を確認したいとき。

## hash
- a00a59142486c0b666d65e7da06ffecc853826b95c867ddee77e89591c4bb50b

# `main.py`

## Summary
- cmoc の最上位 CLI アプリケーションを組み立て、Typer/click の引数解析エラーを cmoc 形式のエラー表示へ変換する入口実装。
- init、tui、indexing、session、apply、review の各コマンドを登録し、実処理は対応するサブコマンド実装へ委譲する。
- Codex exec/tui 呼び出し前に indexing preflight を実行する薄いラッパーを提供し、indexing 自身や conflict resolution 用途では再帰的な事前 indexing を避ける。

## Read this when
- cmoc コマンド全体の起動入口、サブコマンド階層、コマンド名、CLI option の接続箇所を確認したいとき。
- Codex exec/tui を呼ぶ前に indexing preflight がどの条件で走るか、またはスキップされるかを確認したいとき。
- CLI 引数解析エラーが通常の Typer/click 表示ではなく cmoc のエラーレポートとして出る経路を調べたいとき。
- サブコマンド実装に渡される依存関数や引数が、CLI 層でどのように配線されているかを確認したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、永続状態操作、git 操作、oracle review、session/apply の詳細挙動を知りたいだけのとき。
- Codex runtime 呼び出し、エラー描画、リポジトリルート判定、work root 判定などの共通 runtime 実装を調べたいとき。
- 設定モデル、AgentCallParameter、または各サブコマンドのテスト観点を調べたいとき。
- INDEX.md エントリー生成そのものの仕様や、indexing preflight の内部処理を確認したいとき。

## hash
- e97a446e3d7fe4dc8d22fc8b8b0a3576381e37e5109f36170669b124d0aa9148

# `sub_commands`

## Summary
- cmoc の各サブコマンド実行本体を集めた領域で、初期化、対話型実行、INDEX.md maintenance、oracle review、apply lifecycle、session lifecycle の制御フローを扱う。
- CLI 入口定義より内側で、実行前提の検証、worktree・branch・state 操作、Codex CLI 呼び出し、report 生成、変更の commit・merge・cleanup といったサブコマンド固有の状態遷移を確認する入口になる。
- apply、review、session のように複数ファイルへ分かれた大きなサブコマンド領域では、統括フローから対象列挙、loop、INDEX.md 差分処理、report rendering、join/abandon までの下位要素へ進むための案内点になる。

## Read this when
- サブコマンド実行時の前提条件、clean worktree 要求、active session 制約、branch/worktree/state の作成・更新・削除、失敗時 cleanup の順序を確認・変更したいとき。
- 初期化、対話型実行、INDEX.md maintenance、oracle review、apply fork/join/abandon、session start/join/abandon の実行本体や利用者向け出力を追いたいとき。
- Codex CLI を呼び出すサブコマンド固有フロー、Structured Output の結果適用、finding loop、prompt 入力解決、report 生成など、CLI 登録より内側の orchestration を確認したいとき。
- INDEX.md 変更だけの commit/merge、INDEX.md conflict の限定的な自動解決、編集禁止領域や想定外差分の検査など、サブコマンド固有の差分制御を調べたいとき。
- session branch、review worktree、apply worktree など managed な branch/worktree を使う lifecycle 操作の責務境界を見極めたいとき。

## Do not read this when
- Typer の command 登録、option 定義、コマンド名の構造、CLI アプリ全体の組み立てだけを確認したいときは、サブコマンド入口やアプリ組み立て側を読む。
- repo root、work root、path keyword、git command wrapper、worktree helper、binary 判定、git ignored 判定、CmocError 表示などの共通 runtime utility 自体を調べたいときは、共通 runtime 側を読む。
- session state の schema、保存形式、session_id 生成、設定値定義、`.cmoc` 設定同期そのものを確認したいときは、状態モデルや設定管理側を読む。
- Codex CLI に渡す prompt 文面、AgentCallParameter builder、Structured Output schema の定義そのものを変更したいときは、各 builder 側を読む。
- oracle file、realization file、path keyword、INDEX.md エントリー規則などの正本仕様内容を確認したいときは、oracle 側の仕様本文を読む。
- 生成済み INDEX.md や過去の review/apply report の個別内容を確認したいだけのときは、この実装領域ではなく対象の生成物を読む。

## hash
- 083b66ae3dade45377c1ba7cdcf21a1c0dda70eb1e7a847691d5200cb3fa9723
