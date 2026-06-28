# `AGENTS.md`

## Summary
- リポジトリ全体に適用される作業規則を示す文書。cmoc の略称、パス表記、ルーティング手順、閲覧・編集禁止対象、正本仕様断片と実装・テスト配置の基本方針を定める。
- 作業者がどの仕様断片を優先し、どこに実装や自動テストを書くべきかを判断するための入口になる。

## Read this when
- リポジトリ内で作業を開始し、全体に適用される前提ルール、用語、禁止事項を確認したいとき。
- パス表記として使われるルート系トークンの意味や、詳細定義をどこで確認するかを知りたいとき。
- 仕様断片、実装、自動テストの責務分担と配置先を確認したいとき。
- 閲覧・編集してはいけない領域や、編集してはいけない正本仕様・ルート文書を確認したいとき。
- 作業中にどの案内文書を起点にファイルを探すべきかを確認したいとき。

## Do not read this when
- 個別機能の詳細仕様、CLI の具体的な挙動、データ構造、テストケースの期待値を調べたいとき。この文書は全体規則だけを扱うため、該当する正本仕様断片や実装・テストを直接読む。
- 特定ディレクトリ内のファイル選択だけをしたいとき。全体規則を確認済みなら、その階層のルーティング情報へ進む。
- 実装コードや自動テストの具体的な修正箇所を探しているとき。配置先の基本方針を確認済みなら、対象の実装またはテストへ進む。

## hash
- c6f2df98ac0d979500fc13a35dd94143c5892db2faf71d604d2307c3c43fa94c

# `LICENSE`

## Summary
- ソフトウェアの利用・複製・変更・配布・再許諾・販売を許可するライセンス条件と、著作権表示および許諾表示の同梱義務、無保証・免責を定める法的文書。

## Read this when
- このソフトウェアを配布、再配布、再許諾、販売、または派生物に組み込む際の許可範囲と義務を確認したいとき。
- 著作権表示や許諾表示を、コピーまたは実質的な部分に含める必要があるか確認したいとき。
- 保証の有無、作者または著作権者の責任範囲、損害賠償責任の扱いを確認したいとき。

## Do not read this when
- CLI の仕様、実装方針、テスト方針、ルーティング文書の作成規則を確認したいとき。
- ソースコード、テスト、設定、開発手順、パスモデルなど、プロダクトの挙動や構造を調べたいとき。
- 正本仕様断片と実装ファイルの関係、または INDEX.md エントリー生成の基準を確認したいとき。

## hash
- a894f2547af0349f234986eb4661f0146f37b7d82f8b22a27a674d5c1236f08f

# `README.md`

## Summary
- cmoc の概要、初期セットアップ手順、基本ワークフローへの参照、ターミナルロック回避の Tips をまとめた、プロジェクト利用開始時の入口となる案内文書。
- AI が作業規約の詳細へ進むための参照先と、利用者がローカル環境で cmoc コマンドを使い始めるための最小手順を示す。

## Read this when
- cmoc が何を補助するツールなのか、略称を含めた全体像を最初に確認したいとき。
- リポジトリを取得して Python 仮想環境を作り、開発用にインストールする初期セットアップ手順を確認したいとき。
- 任意でコマンドの実行パスを通す方法を確認したいとき。
- 基本ワークフローの詳しい説明へ進むための入口を探しているとき。
- Ctrl+S によるターミナル停止を避けるためのシェル設定例を確認したいとき。

## Do not read this when
- AI の作業規約、編集制限、ルーティング規則などの詳細を確認したいときは、作業者向け規約の本文へ直接進む。
- cmoc の基本ワークフローそのものの詳細を確認したいときは、ワークフロー仕様の本文へ直接進む。
- 実装やテストの具体的なコード構造、関数、挙動を調査したいときは、実装またはテストの対象領域へ直接進む。
- oracle file、realization file、パスモデルなどの正本仕様断片を確認したいときは、該当する仕様本文へ直接進む。

## hash
- c6c3f3c5798ecc63f8611a40982f7bc8100116d8a934616bbd2b2a5b5e0a1afc

# `bin`

## Summary
- 利用者が実行するコマンド入口のシェルラッパーを置く領域で、リポジトリルートと仮想環境内 Python を特定し、実体の Python エントリポイントへ制御を渡す起動経路を扱う。
- 仮想環境内 Python が存在しない、または実行できない場合の利用者向けエラー、初回セットアップ案内、表示用パス、行番号付きの簡易 call stack 出力を扱う。
- シェル補完プローブ時には通常の不足エラーを抑制し、仮想環境内 Python が使える場合だけ Python エントリポイントへ委譲する挙動を扱う。

## Read this when
- 利用者が実行するコマンドの起動経路、リポジトリルートの特定、仮想環境内 Python の検出、または Python エントリポイントへの委譲方法を確認・変更するとき。
- 仮想環境が未作成または壊れている場合のエラー出力、初回セットアップ案内、表示用パス、call stack 表示を確認・変更するとき。
- シェル補完時の挙動や、補完プローブで通常エラーを抑制する条件を確認・変更するとき。
- 利用者向けに表示されるスクリプト位置表記が、作業ツリー上の実パスではなく抽象パストークンに従っているか確認するとき。

## Do not read this when
- Python 側の CLI サブコマンド、引数解析、業務ロジック、または通常のコマンド出力内容を調べたいだけなら、委譲先の Python 実装を読む。
- 仮想環境の作成手順そのもの、依存関係定義、またはパッケージ設定を変更したいだけなら、セットアップやパッケージ管理を担う対象を読む。
- oracle file と realization file の概念、パストークンの定義、または正本仕様断片を確認したいだけなら、対応する oracle 側の文書や実装を読む。

## hash
- d95e290a70bec73f598a40b846824050bc085416d6211017dffdb386eb9c389f

# `codex_minimal_outrigger_cli.code-workspace`

## Summary
- VS Code ワークスペースの対象ルート、エディタ設定、Python 解析対象、Markdown 編集設定を定義する補助設定ファイル。
- 開発環境で除外表示する生成物やルーティング文書、Python の仮想環境・解析パス・整形設定を確認する入口となる。

## Read this when
- VS Code 上で cmoc のワークスペースを開く際の対象フォルダやエディタ挙動を確認したいとき。
- Python のデフォルトインタプリタ、解析対象パス、解析対象ディレクトリ、保存時整形設定を確認したいとき。
- エディタ上で非表示にされる生成物・補助文書の扱いを確認したいとき。
- Markdown 編集時のインデント幅やスペース利用設定を確認したいとき。

## Do not read this when
- cmoc の CLI 挙動、ドメイン仕様、出力互換性を確認したいとき。正本仕様断片または実装・テストを読む方が直接的である。
- Python 実装やテストの処理内容を調査・変更したいとき。対象は開発環境設定であり、実装ロジックは含まない。
- ルーティング文書そのものの内容や生成規則を確認したいとき。対象はエディタ上の表示除外対象として扱うだけで、ルーティング情報は含まない。
- パッケージ依存関係、テスト実行手順、ビルド手順を確認したいとき。対象はそれらの手順や依存定義を担わない。

## hash
- 1938307f70f255710d75d39c07d860ecb381acbb031ca19b2f2b6e565ac41acb

# `oracle`

## Summary
- cmoc の人間所有の正本仕様断片を集める領域。自然言語で書かれた仕様と、AI agent 呼び出し契約・prompt・Structured Output schema・設定・パス表記・標準文書生成を表す実装形式の仕様断片を扱う。
- 利用者向け CLI 挙動、Codex CLI 呼び出し、ログ、エラー処理、インデクシング、実行隔離、セッション状態、branch / commit / worktree モデル、不採用設計、realization code の開発規則、用途別 agent call parameter のどれへ進むべきかを切り分ける入口になる。
- ここに含まれる本文は realization file の根拠であり、実装側の現在値から正本仕様を逆算するための場所ではない。仕様断片に未定義部分がある場合は、既存実装・既存テストと整合する範囲で AI が補う余地を持つ。

## Read this when
- cmoc の実装・テスト・レビュー・インデクシング作業の前に、根拠にすべき正本仕様断片を探したいとき。
- CLI サブコマンド、実行時制御、状態ファイル、ログ、エラー処理、外部 CLI 呼び出し、run 隔離など、利用者に見える挙動や運用上の制約を確認したいとき。
- session / run / apply / review に関係する branch、commit、linked worktree、root path placeholder、作業ディレクトリ概念の定義を確認したいとき。
- AI agent に渡す role、summary、goal、標準プロンプト、Structured Output schema、model class、reasoning effort、ファイルアクセス権限などの呼び出し契約を確認したいとき。
- oracle file と realization file の責務分担、oracle standard、realization standard、ルーティング規則、INDEX.md エントリー生成規則など、開発・レビュー時の横断規範を確認したいとき。
- 採用しなかった workflow、AI 記憶、作業計画レビュー、apply 系 orchestration などの設計判断の境界や non-goal を確認したいとき。

## Do not read this when
- realization implementation や realization test の現在の関数、クラス、ファイル配置、既存テスト期待値だけを調べたいとき。この場合は実装・テスト側の対象へ直接進む。
- 読むべき特定の自然言語仕様、agent call parameter、prompt 部品、schema、設定、パスモデルがすでに分かっているとき。この場合は該当する下位対象を直接読む。
- 正本仕様ではなく、実行ログ、一時ファイル、生成物、現在の実行結果、利用者環境の状態だけを確認したいとき。
- oracle file の基本原則や開発規範を確認する必要がなく、既存 realization code の局所的な修正だけで完結することが明らかなとき。
- 禁止領域や既存のルーティング文書そのものを根拠にしようとしているとき。エントリー生成や仕様判断では、対象本文を根拠にする。

## hash
- e2048e400c080ec5cc30a3d104833374f24e0c174e7b30ac0c9622b90903f42a

# `pyproject.toml`

## Summary
- Python パッケージとしての配布設定、実行コマンドのエントリーポイント、対応 Python バージョン、実行時・開発時依存、パッケージ探索、テスト実行時の import 経路を定義するプロジェクト設定。
- CLI 名から実装上の main 関数へ接続する公開実行面と、setuptools によるビルド・モジュール配置・パッケージデータ同梱の前提を確認する入口。

## Read this when
- 依存パッケージ、対応 Python バージョン、ビルド backend、配布対象モジュール、パッケージデータ、CLI エントリーポイントを確認・変更する必要があるとき。
- テスト実行時に実装側または正本仕様側の Python モジュールが import される経路を確認する必要があるとき。
- 新しい実行時依存、テスト依存、公開コマンド、配布対象モジュール、同梱データを追加・削除する変更を検討するとき。

## Do not read this when
- 個別の CLI 挙動、コマンド処理、ランタイム処理、設定ファイル生成ロジックの実装詳細を調べたいとき。
- 正本仕様断片の内容や、実装が満たすべき仕様上の要求を確認したいとき。
- 個別テストケースの期待値、fixture、テスト対象の制御ロジックを調べたいとき。

## hash
- a1df0d9e48d52552fd4d13591133e0405f6a99fe2cdafa91a6470bcd1986bfb7

# `src`

## Summary
- cmoc の realization implementation 全体を置く実装ルート。最上位 CLI の Typer 配線、互換 import 入口、共通 runtime helper 群、利用者向けサブコマンドの orchestration へ進むための入口になる。
- 公開 CLI コマンドから、共通設定・状態・git・Codex 実行・INDEX.md preflight などの横断処理、さらに session/apply/review/indexing/TUI などの個別コマンド実装へ読み進める起点として使う。
- oracle file の正本仕様断片を具体化した AI 管理の実装領域であり、仕様そのものではなく、現在の CLI 挙動や runtime 境界が実際にどう組み立てられているかを確認するための対象である。

## Read this when
- cmoc の実装本体の入口を探し、CLI 定義、共通 runtime、または個別サブコマンド実装のどこへ進むべきかを選びたいとき。
- console script から Typer app、サブコマンド関数、共通 runtime helper、Codex exec/TUI 呼び出し、session/apply/review/indexing 処理へ至る実装上の流れを確認または変更したいとき。
- oracle の正本仕様断片に対して、現在の realization implementation がどのように具体化されているかを調査し、実装側を修正する対象を探したいとき。
- 設定読み書き、永続 state、git 操作、worktree 操作、ログ、パス解決、Structured Output 検証、INDEX.md 更新 preflight など、複数コマンドから共有される処理の実装入口を探したいとき。

## Do not read this when
- 正本仕様断片そのもの、oracle file の定義、path keyword の仕様、oracle/realization の基本概念を確認したいとき。その場合は oracle 配下の対象を読む。
- realization test の構成やテストケースを調べたいとき。その場合は test 配下へ進む。
- README、AGENTS、gitignore、パッケージ設定、補助スクリプトなど、実装ソース以外の ancillary file を確認したいとき。
- すでに調べたい対象が特定の共通 helper、サブコマンド package、または CLI 入口に絞れているときは、この階層全体ではなく該当する下位対象へ直接進む。

## hash
- 199cdfddb83c6ffd07583179ed64f16f6583531646d667748642ba5385b6151a

# `test`

## Summary
- realization test 全体の入口。CLI サブコマンド、Codex 実行 wrapper、runtime 基盤、prompt 構築、indexing、review、session/apply の外部挙動と制御ロジックを pytest で固定する領域である。
- 共通補助関数は fixture、Git repository 構築、Codex home/profile 差し替え、fake executable、worktree path 解決を集約し、個別テストは各機能の状態遷移、標準出力、終了コード、report、永続 state、worktree/branch cleanup、保護領域検査などの観測結果を扱う。
- 大きなテストファイルの一部は、同じ CLI 境界や run 状態、fake Codex 応答、Git 状態、report 文脈を一箇所に保つために凝集されており、実装詳細よりも現行仕様上意味のある外部挙動と回帰観点を読むための階層である。

## Read this when
- realization implementation を変更する前後に、対応する CLI 外部挙動、runtime 契約、prompt 生成、Codex 呼び出し制御、Git/worktree/state 副作用の既存期待値を確認したいとき。
- apply、session、review、indexing、init/TUI、Codex runtime、basic runtime などのサブシステムについて、成功条件、拒否条件、error report、stdout/stderr、commit、cleanup、retry、保護領域検査の回帰テストを探すとき。
- Codex 実行を fake に差し替えたテスト、最小 Git repository fixture、認証済み Codex home、profile 生成差し替え、branch/state/worktree 準備など、CLI テストの既存パターンを確認したいとき。
- routing document 更新、INDEX 生成 preflight、hash freshness、semantic field validation、root 直下 memo 除外と nested memo 対象化など、indexing workflow の観測点を確認したいとき。
- prompt part、standard 文書注入、structured output schema、AgentCallParameter builder、file access mode、model/reasoning 設定がどのように組み合わさるかをテスト側から確認したいとき。

## Do not read this when
- oracle file の正本仕様断片そのものを確認したいとき。この階層は realization test であり、仕様の正本ではない。
- 実装 helper、state persistence、Git 操作、Codex subprocess wrapper、path model、profile 生成などの本体コードを局所的に変更したいだけなら、対応する実装領域を直接読む方がよい。
- 個別サブコマンドのテスト期待値ではなく、CLI コマンド定義や API の一般構造だけを把握したいとき。
- Codex CLI や LLM の出力品質そのものを検証したいとき。この階層の多くは fake executable や fake response を使い、cmoc 側の制御と副作用を固定する。
- テスト共通 fixture の使い方ではなく、特定機能のアサーションだけを確認したい場合は、共通補助ではなく該当機能のテスト本文へ直接進む方がよい。

## hash
- 2daf900dd7f11bdc8d279d83ecb3c38b14eed26358914df0954165d8672caeb1
