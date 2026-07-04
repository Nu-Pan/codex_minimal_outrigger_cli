# `doc`

## Summary
- cmoc の正本仕様断片のうち、自然言語で記述された仕様文書を束ねる領域。アプリケーション仕様、branch/worktree モデル、不採用設計案、開発ルールなど、外部挙動・共通境界条件・設計判断・実装時規約へ進む入口になる。
- 個別の実装ファイルやテストではなく、cmoc の利用者向け挙動、git branch/worktree の扱い、過去に退けた設計案、realization code/test の書き方を判断するための正本仕様文書を探す対象。

## Read this when
- cmoc の CLI 挙動、サブコマンド、共通前処理、エラー処理、ログ、索引生成、セッション状態、run 隔離、Codex CLI 呼び出し、プロンプト受け渡し、ローカル SLM 利用に関する仕様文書を探すとき。
- session fork/join、apply/review などの run が利用する git branch、commit、linked worktree、session/run 系 branch の意味や命名規則を確認したいとき。
- cmoc の現行設計に対して、過去に不採用となった代替案の背景や避けるべき理由を再確認したいとき。
- Python 実装、CLI 構成、共通処理の配置、開発環境、pytest を中心とした realization test の規約を確認したいとき。
- 個別仕様へ進む前に、cmoc の外部挙動、状態・ログ・ブランチ・agent call、または開発時の共通方針に関する読む先を絞りたいとき。

## Do not read this when
- oracle file と realization file の一般的な定義、責務境界、編集権限、追跡対象判定、INDEX.md エントリー作成規則、品質基準だけを確認したいとき。
- パスキーワードやルート種別の定義だけを確認したいときは、パスモデルを扱う仕様へ直接進む。
- AgentCallParameter builder の具体的な構築ロジック、実装ファイル、テストの内部構造、既存関数のシグネチャやテスト期待値だけを調べたいとき。
- 採用済み仕様ではなく実装コード上の現在値、または Codex CLI 本体・git ignore・permission profile など外部機能の一般仕様を調べたいとき。
- 個別サブコマンド、個別共通処理、開発規約など、読むべき仕様文書がすでに分かっており、その詳細だけを確認したいとき。

## hash
- 9586e65672078161cd566897bef1706c037ef09a475b82717130aa6f6489e5fe

# `src`

## Summary
- cmoc の oracle src 群のうち、AI エージェント呼び出し仕様と横断的な基礎モデルを扱う領域への入口。agent call parameter、prompt、Structured Output schema、パス表記、設定、規範文書モデル、Markdown helper などの正本仕様断片を下位領域へ振り分ける。
- プロンプト構築や共通規範注入、サブコマンド向け agent 呼び出し契約、複数領域から参照される補助モデルのどれを確認すべきか判断するためのルーティング対象。

## Read this when
- cmoc の oracle src にある正本仕様断片のうち、AI エージェント呼び出し、prompt、Structured Output schema、またはそれらを支える横断モデルを探すとき。
- agent call 用の共通 parameter、機能別 builder、完全プロンプトの構築順序、共通規範プロンプト、ファイルアクセス制限やルーティング規則の注入位置を切り分けたいとき。
- cmoc の設定値、ルートパスプレースホルダ、パス解決、規範文書の構造化、仕様文生成用 Markdown helper など、複数領域から参照される基礎概念の oracle src を確認したいとき。

## Do not read this when
- CLI 実行制御、branch 操作、diff 取得、レポート保存、対象ファイル探索、表示整形など、AI エージェント呼び出し仕様や横断モデルではない実装を調べたいとき。
- 特定サブコマンドの利用者向け入出力、実行手順、状態ファイル仕様だけを確認したいとき。
- realization code 側の prompt builder 実装、外部コマンド起動、バックエンド固有モデル名への変換、またはテスト構成を確認したいとき。

## hash
- ff377c45bb81945513029eb17fc138911907e756d1fd4e961bc79a5ad24dcd20
