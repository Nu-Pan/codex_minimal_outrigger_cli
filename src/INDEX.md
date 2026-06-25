# `acp`

## Summary
- AI agent へ渡す呼び出し契約を組み立てる実装領域。用途別の role、summary、goal、補助文脈、Structured Output schema、model class、reasoning effort、ファイルアクセス権限と、共通プロンプトに含める標準規範・ルーティング規則・基本概念の生成を扱う。
- 変更要約、レビュー所見の列挙・判定・統合、所見への修正依頼、目次エントリー生成、merge conflict marker 解消、TUI 実行前のパラメータ選定など、cmoc の各機能が別 AI agent に何を読ませ、どの構造化結果を期待し、どの制約で実行させるかを追う入口になる。
- CLI や Git 操作の本体ではなく、cmoc から AI agent へ処理を委譲する境界で使うプロンプト文面、標準文書の注入条件、出力 schema、実行権限、モデル選択を確認するためのまとまり。

## Read this when
- cmoc の機能が AI agent を呼び出すときの prompt 構成、補助文脈、Structured Output schema、model class、reasoning effort、ファイルアクセス権限を確認または変更したいとき。
- 変更要約、apply review、oracle review、INDEX.md エントリー生成、merge conflict marker 解消、TUI 実行前パラメータ選定のいずれかについて、AI agent に渡す入力文脈と期待する構造化出力の契約を調べたいとき。
- oracle/realization の基本概念、ファイルアクセス規則、ルーティング規則、oracle standard、realization standard、review standard、apply review standard、INDEX.md エントリー標準を、agent 用プロンプトへどう組み込むか確認したいとき。
- 対象ファイル、差分、既存所見、ユーザー入力、conflict 対象パスなどの入力値が、agent 向けの完全なプロンプトや schema 指定へどう接続されるかを追いたいとき。
- 新しい AI 委譲処理を追加する、既存の委譲処理の標準文書注入条件を変える、または agent に許可する読み書き範囲やモデル選択の境界を調整したいとき。

## Do not read this when
- サブコマンド登録、CLI 引数解析、実行制御、Git コマンド実行、branch 作成、差分取得、conflict 検出、結果保存など、AI 呼び出しを使う側の処理フロー本体だけを調べたいとき。
- AgentCallParameter、ModelClass、ReasoningEffort、FileAccessMode などの基礎型や、パス解決、構造化文書、Markdown rendering といった共通 helper そのものの実装詳細を調べたいとき。
- 生成された prompt を外部プロセスへ渡す処理、標準入力・標準出力の扱い、agent 実行結果を受け取った後の利用側ロジックを調べたいとき。
- 個別の oracle file、realization file、テスト、変更対象ファイル、差分、conflict 本文の内容を直接確認したいだけで、AI agent への委譲契約や標準プロンプトを変更しないとき。
- oracle standard、realization standard、review standard、INDEX.md エントリー標準などの内容を正本仕様として検討したいとき。ここにあるのは agent prompt 用に生成される実装であり、仕様判断の正本は oracle 側を読む。

## hash
- eb347bc4b03d0d06052491d10afe834300fda275319c031724a4e5e76ae33d49

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
- cmoc の共有 runtime helper 群をまとめる領域。上位の CLI command や実行制御から使われる共通処理として、Codex CLI 呼び出し、profile・設定、content hash、CLI 実行ラッパー、error 表示、Git 操作、実行ログ、path 解決、外部コマンド結果型、session/apply 状態の扱いを担う。
- 個別サブコマンドの業務ロジックではなく、複数の command や上位 runtime から横断的に使われる実行時支援の入口として読む対象を選ぶための階層。

## Read this when
- CLI サブコマンド間で共通化された runtime 処理、例外処理、進捗表示、ログ記録、終了コード化、実行 summary の挙動を確認または変更したいとき。
- Codex CLI の exec/TUI 呼び出し、profile 生成、schema 準備、Structured Output 検証、capacity/quota retry、resume token 再利用など、Codex 実行の共通制御を追いたいとき。
- cmoc の設定ファイル読み書き、既定値補完、不正 JSON や不正設定値の利用者向けエラー化を扱うとき。
- hash 付き生成ファイル、binary 判定、共有データ型、session/apply 状態ファイル、active session 探索など、runtime 横断の補助機能を確認したいとき。
- repo/work/cmoc root の解決、.cmoc 配下の保存先導出、timestamp や duration 表示、作業ディレクトリ一時変更などの共通 path helper を扱うとき。
- Git repository 状態検査、一時 worktree/branch の作成・削除、.cmoc の Git 追跡除外、Git ignore 判定などの低レベル Git helper を確認したいとき。

## Do not read this when
- 特定サブコマンドの引数定義、業務ロジック、処理順、生成ファイル内容、利用者向け出力だけを調べたいとき。その場合は該当 command 実装へ進む。
- path キーワードそのものの概念定義や root 種別の正本仕様を確認したいとき。その場合は path model を扱う仕様・実装へ進む。
- AgentCallParameter、FileAccessMode、model class、reasoning effort などの入力データ構造そのものを確認したいとき。その場合は基本データ定義側へ進む。
- ログを読む側、集計する側、レポート表示側、または INDEX.md の hash 更新など、この階層の runtime helper を利用する上位機能を調べたいとき。
- テスト fixture や期待挙動から確認する方が直接的な場合、または個別 helper の利用箇所だけを探したい場合は、該当するテストや呼び出し側へ進む。

## hash
- e6177357ac1ae402aba338541033536f2d1e91b70866b35da262ccc08469a42d

# `config`

## Summary
- 開発対象リポジトリごとに変わる cmoc 設定を表す dataclass 群を扱う領域。
- AI エージェント呼び出しの並列数、Codex CLI 向けモデル名と reasoning effort、apply fork と review oracle のループ上限など、永続化される設定値の既定値を確認する入口になる。
- 人間が編集するリポジトリ別設定面に含まれる値の定義を追うための対象であり、設定ファイルの入出力処理そのものは別領域に分かれる。

## Read this when
- リポジトリ別に保持される cmoc 設定項目や既定値を確認・変更したいとき。
- 初期化時に生成・同期される設定ファイルへ含める値や、Enum 系の値を JSON 保存向けに扱う前提を確認したいとき。
- Codex CLI に渡すモデル名、reasoning effort 名、AI 呼び出し並列数、apply fork や review oracle の処理回数上限を調整したいとき。

## Do not read this when
- CLI 引数、サブコマンド構文、実行時の入出力フローを調べたいだけのとき。
- 設定ファイルの実際の読み書き、JSON 変換処理、または `.cmoc` 配下のパス解決処理を調べたいとき。
- oracle file、realization file、パスキーワード定義、INDEX.md 生成ルールそのものを確認したいとき。

## hash
- 324dfe3034cabedbb119cb79c0c59fcdd422ac0747dbbc5e095eba5140bb0d71

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
- cmoc のサブコマンド実装をまとめる領域。初期化、INDEX.md maintenance、対話型実行、oracle review、session lifecycle、apply lifecycle の各コマンド本体と、そのコマンド固有の補助処理を扱う。
- CLI 登録や低レベル runtime ではなく、サブコマンドを実行したときの前提条件確認、状態遷移、Git/worktree 操作、Codex 呼び出し、利用者向け出力や report 生成へ進むための入口になる。
- session と apply は下位ディレクトリに lifecycle 操作がまとまっており、review は対象列挙、finding loop、INDEX.md 取り込み、report 描画の補助モジュールへ分かれている。

## Read this when
- cmoc の特定サブコマンドがどの実装領域にあるかを切り分けたいとき。
- 初期化、INDEX.md maintenance、対話型実行、oracle review、session fork/join/abandon、apply fork/join/abandon の実行条件、状態更新、Git 操作、出力や report 生成を確認・変更したいとき。
- サブコマンド固有の Codex 呼び出しや、isolated worktree/branch を使う review・apply・session の上位フローを追いたいとき。
- サブコマンド実装変更やテスト追加のために、単体コマンド本体、review 補助、session lifecycle、apply lifecycle のどこへ進むべきか判断したいとき。

## Do not read this when
- Typer app へのコマンド登録、引数 parser、トップレベル dispatch だけを確認したいときは、CLI アプリ組み立て側を読む。
- repo root/work root の決定、git command wrapper、worktree 操作、branch 操作、設定読み込み、session state schema、path keyword などの共通 runtime helper 自体を調べたいときは、runtime や状態モデルの実装を読む。
- Codex prompt parameter の文面や Structured Output schema の定義そのものを確認したいときは、acp builder 側を読む。
- oracle file の正本仕様、realization file の定義、INDEX.md エントリー生成規則など、サブコマンド実行制御ではなく仕様断片やルーティング文書の規則を調べたいときは、oracle 側の本文を読む。

## hash
- 5f8fb834fb173d34f516432d519dbb803ca2925c1bb1abecd4a833dc9ba3e4e2
