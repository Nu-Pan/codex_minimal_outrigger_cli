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
- cmoc の正本仕様断片全体への入口。人間が所有する自然言語仕様、AI agent 呼び出し契約や標準プロンプトを定義する実装形式の仕様断片、正本性・実現物との関係を確認するための領域である。
- 利用者向け CLI 挙動、run/session/branch/worktree モデル、開発規則、non-goal、AI 呼び出しパラメータ、Structured Output schema、標準文書生成、共有データ構造など、realization file を正本仕様断片に沿わせるための根拠を探す起点になる。
- 下位には、自然言語で仕様判断を読む領域と、プロンプト・schema・設定・共有モデルを実装形式で読む領域があり、作業内容が公開挙動や設計判断なのか、AI 呼び出し契約や生成形式なのかで読む先を切り分ける。

## Read this when
- cmoc の仕様根拠を oracle file から確認し、realization implementation や realization test をどの意図に合わせるべきか判断したいとき。
- CLI の外部挙動、状態・ログ・出力、run 隔離、agent call 境界、session fork / join、branch / worktree 用語、開発規則、採用しない設計案の理由を確認したいとき。
- AI agent に渡す role、summary、goal、標準プロンプト、権限、モデル品質区分、reasoning effort、Structured Output schema、設定、パス表記、規範データ構造の正本仕様断片を確認したいとき。
- oracle file と realization file の関係、正本仕様断片として守るべき公開面・保存先・失敗時挙動・責務分担、または標準文書やルーティング規則がどうプロンプト化されるかを確認したいとき。

## Do not read this when
- 既存実装の具体的な関数、クラス、helper、git 操作、状態ファイル処理、外部プロセス起動、テスト期待値だけを調べたいときは、realization implementation または realization test を読む。
- 対象が自然言語仕様または実装形式の AI 呼び出し契約のどちらかに絞れているときは、この領域全体ではなく該当する下位領域へ直接進む。
- 個別の prompt builder、AgentCallParameter builder、schema、設定モデル、パスモデル、規範モデルなど、読むべき下位対象がすでに分かっているときは、その対象を読む。
- INDEX.md エントリー生成の一般基準、oracle file の正本性、realization file の編集責務など、提示済みの共通標準だけで判断でき、対象本文の仕様断片を追加で確認する必要がないとき。

## hash
- 4841c324d9619d505ed501af9f1d5ed78c83063821303c3727e251e92d9dee76

# `pyproject.toml`

## Summary
- Python パッケージとしてのプロジェクト名・バージョン・説明・要求 Python バージョン・依存パッケージを定義する設定。
- 実行コマンドから実装入口への対応、setuptools のソース配置・モジュール・パッケージデータ、テスト時の import 探索パスをまとめて扱う。

## Read this when
- 配布・インストール・ビルド設定、要求 Python バージョン、外部依存、パッケージに含めるモジュールやデータの扱いを確認または変更する時。
- 利用者が呼び出すコマンド名と実装入口の対応を確認または変更する時。
- テスト実行時に実装側または正本仕様側のモジュールが import できない問題を調べる時。

## Do not read this when
- 個別コマンドの挙動、実行時ロジック、入出力形式、状態操作を調べる時は、実装ソースやテストを直接読む。
- 正本仕様断片の内容や方針を確認する時は、正本仕様の文書またはソースを直接読む。
- 依存追加やパッケージ設定変更を伴わない局所的な実装修正・テスト修正だけを行う時。

## hash
- 731783d339cf2faeb792cb6989ecddd88a109934b3e5f1a9667ec546eb6a0182

# `src`

## Summary
- cmoc の realization implementation 全体を束ねる領域。公開 CLI の組み立て、利用者向けサブコマンド実装、複数処理で共有される runtime helper、ACP 呼び出しパラメータ builder、正本側実装への互換 import shim がここに置かれる。
- 実装本体と互換入口が混在しているため、この階層は cmoc の実行経路を大きく切り分け、CLI 層、サブコマンド層、共通 runtime、ACP builder、正本側再公開境界のどこへ進むべきかを選ぶ入口になる。
- realization implementation は正本仕様断片そのものではなく、oracle file で述べられた人間意図を具体化する実装側のコードとして扱う。

## Read this when
- cmoc の実装を変更する前に、公開 CLI、サブコマンド処理、共有 runtime、ACP builder、正本側 import 互換境界のどの領域を読むべきか判断したいとき。
- CLI コマンドがどの実装関数へ委譲され、そこから session、apply、review、indexing、TUI、初期化などの処理へどう進むかを確認したいとき。
- Codex exec/TUI 呼び出し、設定、状態ファイル、git 操作、ログ、path、INDEX.md 更新、Structured Output 検証など、複数機能で共有される runtime 処理の実装場所を探したいとき。
- ACP 用の prompt・model class・file access mode・structured output schema path など、Codex 呼び出しに渡す AgentCallParameter の構築経路を探したいとき。
- 通常起動時に realization 側の import path から正本側実装や互換 module がどう解決されるか、再公開境界を確認したいとき。

## Do not read this when
- 正本仕様断片としての要求、概念定義、CLI 出力仕様、oracle file の編集責任を確認したいとき。その場合は oracle 側の該当文書を読む。
- テスト観点、fixture、期待される外部挙動の検証内容を確認したいとき。その場合は realization test 側を読む。
- 個別の path model、構造化ドキュメント、設定定義、ACP builder の正本側本文など、互換再公開元の具体的内容だけを確認したいとき。その場合は正本側実装を直接読む。
- パッケージ設定、依存関係、console script 登録、配布設定、補助スクリプトなど、実行時実装ではなく ancillary な構成を調べたいとき。
- INDEX.md 生成用の既存エントリーやルーティング文書そのものを確認したいとき。この領域の本文は実装コードであり、ルーティング情報の正本ではない。

## hash
- 462a09847dfb5f7ed01d7b2d1096ee5a7b71c2195d7fb90ae396b0fa19f8e721

# `test`

## Summary
- cmoc の realization test 群への入口。CLI サブコマンド、Codex 実行 wrapper、runtime 基盤、prompt 構築、indexing、review、apply/session 状態遷移など、oracle file で述べられた意図を実装がどう外部挙動として満たすかを pytest で固定している。
- 一時 Git repository、Codex home、fake Codex executable、linked worktree、state file、report、log、branch/worktree cleanup など、外部コマンドと永続状態を伴う回帰確認の文脈が集約されている。
- 下位項目は機能領域ごとの realization test と共通 test support に分かれており、実装変更時にどの外部挙動・境界条件・副作用を確認すべきかを選ぶための案内になる。

## Read this when
- cmoc の実装変更に対して、対応する realization test や既存の回帰観点を探したいとき。
- CLI の終了コード、標準出力・標準エラー、report、state 更新、Git branch/worktree 操作、cleanup、commit、dirty worktree 拒否などの外部挙動を確認・変更するとき。
- Codex CLI 呼び出しの profile、CODEX_HOME、sandbox、retry、quota retry、process group、prompt/schema/log など runtime 側の期待挙動を検証したいとき。
- init、TUI、session、apply、review oracle、indexing など複数のサブコマンドにまたがる状態遷移や境界条件を、テスト上の観測点から追いたいとき。
- 新しいテストを追加する前に、同じ観点の既存ケースへ統合できるか、共通 fixture や helper を使えるかを確認したいとき。
- realization file の変更後に、現行仕様上意味のある外部挙動または制御ロジックが既存テストでどう固定されているかを確認したいとき。

## Do not read this when
- oracle file の正本仕様断片そのものを確認・変更したいとき。この階層は realization test であり、仕様本文の代替ではない。
- 実装本体の責務分割、関数内部、schema 定義、状態操作 helper などを直接変更する目的なら、対応する実装側を読む方が先である。
- 個別サブコマンドや runtime 領域がすでに特定できており、該当する下位テストまたは実装へ直接進めるとき。
- Codex CLI や LLM の出力品質そのものを評価したいとき。この階層のテストは fake/stub を使って cmoc 側の制御と副作用を検証する。
- routing document 生成規則、oracle/realization の概念定義、path token の正本定義だけを調べたいときは、対応する oracle 側文書を読む。

## hash
- 47788f35b6f1da0d73a3699e944b3bf4cabd142c24246eb64fae2aba782c0953
