# `doc`

## Summary
- cmoc の正本仕様断片のうち、自然言語の Markdown 文書で書かれた仕様群を収める領域。公開 CLI 挙動、run 隔離、branch / worktree モデル、セッション状態、ログ、インデクシング、Codex CLI 呼び出し規約、サブコマンド仕様、開発時の実装・テスト規則、採用しなかった設計方針を扱う。
- 利用者に見える挙動や AI 実装者が従う横断規則について、実装差を避けたい判断の起点になる。下位領域や個別文書は、アプリケーション仕様、開発規則、設計上の non-goal、branch モデルなど、目的別の正本仕様断片へ進む入口として使う。

## Read this when
- cmoc の CLI としての外部挙動、サブコマンドの事前条件・実行手順・状態遷移、stdout / stderr / ログ、エラー処理、補完、インデクシング、Codex CLI 呼び出し境界を確認したいとき。
- session branch、run branch、linked worktree、session state、apply state、oracle snapshot、run 隔離、merge / abandon / cleanup など、git 状態や永続状態をまたぐ仕様を実装・修正・テストするとき。
- Python 実装、CLI 構成、共通処理配置、開発環境、依存追加、pytest による決定論的制御ロジックの検証など、realization code を書く前に守るべき開発規則を確認したいとき。
- 新しい計画フェーズ、AI-generated memory / kaizen、自動注入される改善情報、人間による AI 計画レビューなどを追加すべきか判断する前に、過去に採用しなかった設計方針と理由を確認したいとき。
- oracle file の自然言語仕様から読む先を絞り込み、実装側へ進む前に人間意図・公開仕様・non-goal の境界を確認したいとき。

## Do not read this when
- oracle file と realization file の基本的な責務分担、正本仕様断片としての位置づけ、AI / 人間の編集権限だけを確認したいとき。
- パスキーワードや root model の定義そのものを調べたいとき。
- 特定の実装ファイル、テストファイル、既存関数、helper、schema、設定ファイルの現在のコード構造だけを確認したいとき。
- 個別の AgentCallParameter builder、Structured Output schema、ログ JSON の具体的な key など、自然言語仕様よりも実装・schema 側が正本になる詳細だけを確認したいとき。
- 対象のサブコマンド、開発規則、branch モデル、設計上の代替案など読むべき個別文書がすでに明確な場合。

## hash
- 93d8d6ea2309192265cb6167b4a23d15fc8a82f5581398fd7b49443ee3111175

# `src`

## Summary
- プログラミング言語・設定ファイルで記述された cmoc の正本仕様断片を集める領域。AI エージェント呼び出しパラメータと prompt 構築、複数領域で使う基礎モデル・パス表記・構造化文書 helper、リポジトリ単位の永続設定仕様へ進む入口になる。
- 自然言語仕様やテストではなく、実装形態で表された oracle file を根拠に、realization implementation が従うべきモデル、設定値、出力契約、標準文書の組み立て方を確認するための階層である。

## Read this when
- cmoc の正本仕様断片のうち、Python や JSON schema として定義された内容から読む先を選びたいとき。
- AI エージェント呼び出しに渡す role・summary・goal、補助文脈、モデルクラス、reasoning effort、ファイルアクセスモード、Structured Output schema の指定を確認したいとき。
- パスのルートトークン表記、実パス解決、agent call parameter、規範断片モデル、構造化 Markdown 生成など、複数機能が前提にする基礎概念を確認したいとき。
- リポジトリごとに永続化される cmoc 設定の構造、既定値、Codex CLI 向け設定、apply fork や review oracle の処理上限に関する正本仕様を確認したいとき。
- realization implementation を実装・修正する前に、対応する source 形式の oracle file がどの制約や契約を定めているか確認したいとき。

## Do not read this when
- oracle file と realization file の基本定義、oracle standard、realization standard など、自然言語で書かれた標準文書本文を確認したいだけのとき。
- oracle test による期待挙動やテスト観点を確認したいとき。
- CLI 引数解析、git 操作、プロセス起動、画面描画、ファイル保存、状態更新など、realization implementation の具体的な制御フローを調べたいとき。
- 特定の prompt、基礎モデル、設定仕様のどれを読むべきか既に分かっており、その下位領域へ直接進めるとき。
- 既存の INDEX.md 構成やルーティング文書そのものを確認したいとき。

## hash
- 8b750dccb55b46ae340b49b0f476cba9db37737982005e427cdfab16a850c685
