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
- cmoc の正本仕様断片を束ねる領域。人間が所有する oracle file と、AI が具体化する realization file の責務境界、正本仕様断片としての一般原則、実装・テスト・補助ファイルの肥大化抑制、ルーティング文書エントリーの作成基準を扱う。
- 下位には、自然言語で書かれた利用者向け挙動・git/session/run モデル・設計判断・開発規則の仕様断片と、Python 実装や設定形式で書かれた path model・設定モデル・AI 呼び出し境界などの仕様断片がある。
- 実装やテストを変更する前に、正本仕様として読むべき領域を、自然言語仕様、プログラム形式の仕様、oracle/realization の基本原則、INDEX.md エントリー基準のどれとして探すかを切り分ける入口になる。

## Read this when
- cmoc の正本仕様断片全体から、読むべき自然言語仕様またはプログラム形式の仕様を探したいとき。
- oracle file と realization file の定義、責務分担、編集主体、正本仕様から実装へ流れる関係を確認したいとき。
- oracle file をどの程度書くべきか、未定義部分をどう扱うか、用語・命名・矛盾・ベストプラクティスとの優先関係など、正本仕様断片の一般基準を確認したいとき。
- realization file の実装・テスト・補助ファイルについて、最小化、品質、分割、抽象化、公開面、依存、削除・統合余地の共通基準を確認したいとき。
- INDEX.md エントリーに何を書くべきか、対象本文との根拠関係、読む条件と読まなくてよい条件の境界、機械的情報を混ぜない基準を確認したいとき。
- CLI 挙動、実行時状態、git branch / commit / worktree モデル、Codex CLI 呼び出し、ログ、エラー処理、インデクシング、run 隔離、開発環境などの自然言語仕様へ進む入口を探したいとき。
- path キーワード、設定値、基礎型、Markdown レンダリング、AI 呼び出しパラメータ、Structured Output 契約など、プログラム形式の正本仕様断片へ進む入口を探したいとき。

## Do not read this when
- 既存 realization code の具体的な関数、クラス、CLI 実装、git 操作、永続状態更新、TUI 描画、テスト期待値だけを調べたいとき。
- 読むべき個別の正本仕様断片がすでに特定できており、その本文だけを確認すればよいとき。
- 自然言語仕様だけを確認したいことが明確で、下位の自然言語仕様領域へ直接進めるとき。
- path model、設定モデル、AgentCallParameter builder、Structured Output schema など、プログラム形式の仕様だけを確認したいことが明確で、下位の実装形式仕様領域へ直接進めるとき。
- 正本仕様断片やルーティング基準ではなく、生成物、実行ログ、一時ファイル、または作業メモを探しているとき。

## hash
- a6ee75fc12fb3905d402e6217213d05db2e4d2b275370043873941ccf78842de

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
- cmoc の realization implementation 全体の入口となる領域。公開 CLI の接続、サブコマンド本体、共通 runtime helper、設定、基礎モデル、AI agent 呼び出しパラメータ・プロンプト構築など、プロダクト挙動を具体化する実装を収める。
- この階層は正本仕様断片ではなく、oracle file の人間意図を実行可能な Python 実装として具体化する場所である。CLI から呼ばれる上位処理と、それらが共有する path、git、state、config、Codex 呼び出し、文書変換などの下位部品へ進むための起点になる。
- 同階層の下位対象は、CLI 登録と委譲、利用者操作ごとの orchestration、複数機能で使う runtime 基盤、AI への依頼内容の組み立て、共通モデル・文書処理、設定値、互換 import 境界に分かれている。

## Read this when
- cmoc の実装側で、CLI コマンドから内部処理、共通 helper、Codex 呼び出し、設定、基礎型までのどこを読むべきかを切り分けたいとき。
- realization implementation を変更する前に、既存の責務境界、同じまたは近い責務を持つ実装、上位処理と共通処理の配置を確認したいとき。
- サブコマンドの実行フロー、git・worktree・state・report・indexing・Codex 実行など、利用者操作がどの実装領域に分担されているかを追いたいとき。
- AI agent に渡す role、goal、補助入力、file access mode、model、reasoning、Structured Output schema、標準プロンプト部品などの構築経路を探したいとき。
- ルートトークン付き path、AgentCallParameter、FileAccessMode、規範文書モデル、Markdown rendering など、複数実装から参照される基礎概念のコード上の扱いを確認したいとき。
- リポジトリごとの設定データ構造、Codex CLI 用モデル名・reasoning effort 対応、並列数や処理上限など、実装が参照する設定面を確認したいとき。

## Do not read this when
- 正本仕様断片そのものを確認したいとき。cmoc の人間意図、oracle file、oracle doc、oracle src、oracle test の本文は oracle 側を読む。
- realization test の期待挙動やテスト fixture を確認したいだけのときは、テスト領域を読む。
- README、AGENTS、補助スクリプト、パッケージ設定、gitignore など、実装ソース以外の ancillary file を確認したいときは、該当する上位または補助領域を読む。
- 生成済みの INDEX.md エントリー内容を読むだけで、indexing の実装や更新処理を追う必要がないとき。
- 外部ライブラリ、Codex CLI 本体、Typer、Click、Git、jsonschema など、cmoc が包んで使っている外部仕様だけを調べたいとき。

## hash
- d899ec5d122f26f8aeb992e6627b92085aa3304609558ed576da0ddc2c3fd769

# `test`

## Summary
- cmoc の realization test 群を収める領域。CLI サブコマンド、Codex 実行ラッパー、runtime 共通契約、indexing、prompt/ACP builder など、oracle file の意図を実装側の外部挙動として固定するテストへの入口になる。
- 一時 Git リポジトリや fake Codex 実行を使い、apply/session/review/init/indexing などの状態遷移、worktree・branch・report・log・error・cleanup の観測結果を検証する。
- 共通補助関数も含み、個別テストが repository fixture、Codex home、profile 差し替え、偽実行ファイル、worktree path 解決の準備を重複して持たないための基盤を提供する。

## Read this when
- realization implementation の変更に対して、どの CLI 外部挙動や runtime 境界が既存テストで固定されているかを探すとき。
- apply の fork・join・abandon に関する branch、state、worktree、process、report、cleanup、dirty worktree、stale branch、merge conflict などの期待値を確認したいとき。
- session の fork・join・abandon に関する状態ファイル、branch 操作、linked worktree、dirty worktree 拒否、conflict 解決、cleanup 失敗時の挙動を確認したいとき。
- init、TUI 起動前処理、Markdown prompt 解析、設定ファイル生成、`.cmoc` ignore、既存 staged/unstaged 差分保護、linked worktree 初期化の期待値を確認したいとき。
- Codex CLI 呼び出し層の profile、cwd、sandbox、CODEX_HOME、schema 出力先、call log、retry、quota wait、process group、エラー変換、`.agents` 変更拒否を調べるとき。
- indexing preflight や indexing サブコマンドが routing document を生成・更新・commit する条件、hash 再利用、semantic validation、conflict 解決、linked worktree、memo 境界を確認したいとき。
- review oracle の対象選択、所見列挙・検証・judge・merge loop、report、review worktree、INDEX.md 変更取り込み、想定外差分拒否を確認したいとき。
- prompt part、routing rule、file access rule、standard 文書、ACP builder、structured output schema が最終 prompt や schema にどう反映されるかを回帰テストから確認したいとき。
- root token/path 解決、run/work/repo root の境界、config、Markdown error 表示、CLI error 変換、subcommand log、sandbox/profile 変換、binary 判定などの runtime 共通契約を確認したいとき。
- CLI テスト用の一時 repository、認証済み最小 Codex home、fake executable、Git helper、apply worktree path 解決などの共通 fixture や補助処理を使う、または変更するとき。

## Do not read this when
- 正本仕様断片そのものを確認・変更したい場合。この領域は realization test であり、oracle file の代替ではない。
- 実装本体の処理順、helper の内部構造、永続 state の読み書き、git worktree 操作、Codex 呼び出し実装だけを直接変更したい場合は、対応する implementation 側を先に読む。
- CLI や runtime と無関係な oracle doc、oracle src、oracle test の定義や標準を確認したい場合は、oracle 側の文書を読む。
- Codex CLI や LLM の出力品質そのものを検証したい場合。この領域の Codex 関連テストは fake executable や stub 応答を使い、cmoc 側の制御と副作用を検証する。
- 特定サブコマンドの利用者向け仕様を最初に知りたいだけで、既存 realization test の期待値や回帰観点を確認する必要がない場合は、関連する oracle または implementation の入口へ進む。
- routing document の本文生成規則だけを確認したい場合は、index entry standard や indexing 実装を読む方が直接的である。
- 共通 fixture の使い方ではなく、個別ケースのアサーションや出力期待値を探している場合は、対象機能のテストへ直接進む。

## hash
- 046e7f502dcf4d6da92d478f3efc03f10fb40ecca1bc427df4a342fcae488d11
