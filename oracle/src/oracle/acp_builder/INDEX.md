# `apply`

## Summary
- `cmoc apply fork` の AI エージェント呼び出し契約を扱う領域。fork 適用後の差分要約、ファイル単位の所見列挙、所見適用依頼について、prompt、Structured Output schema、モデル選択、ファイルアクセス制約の正本断片をまとめる。
- git 操作や fork 適用アルゴリズム本体ではなく、適用後の差分や仕様乖離を AI に調査・要約・修正させるための入力契約と出力契約へ進む入口となる。

## Read this when
- `cmoc apply fork` で、差分要約、実装所見の列挙、所見に基づく修正依頼を AI エージェントへどう渡すか確認したいとき。
- apply fork 系の prompt に含める role、summary、goal、補助入力、standard 群、placeholder、ファイルアクセスモードを確認または変更したいとき。
- apply fork 系の AI 呼び出しで使うモデルクラス、reasoning effort、Structured Output schema の選択根拠や境界を確認したいとき。
- fork 適用後の作業レポートやレビュー結果として、人間向け差分要約または修正所見リストの出力契約を確認したいとき。

## Do not read this when
- `cmoc apply fork` のブランチ作成、git diff 取得、実際のパッチ適用、commit 操作などの実行フローそのものを調べたいとき。
- oracle file、realization file、path keyword、AgentCallParameter、model class、file access mode などの共通概念の定義を確認したいとき。
- complete prompt の共通構築規則、markdown rendering、パス解決、構造化文書の汎用仕様を調べたいとき。
- apply fork 以外のサブコマンド用 prompt、一般的なルーティング文書、または実装・テスト変更種別ごとの個別判定ロジックを探しているとき。

## hash
- c471f88082c2cc273436db5b8e4e2bf40947e4b9a9c20ac95dd298f61404132a

# `basic.py`

## Summary
- AI コーディングエージェント呼び出しに渡す論理パラメータの基本型を定義する。モデルクラス、reasoning effort、ファイルアクセスモード、プロンプト、Structured Output schema の有無をひとまとまりの呼び出し条件として扱うための入口である。
- ここで定義される値は cmoc 上の論理名であり、バックエンドが実際に受理するモデル名やファイルアクセス指定へ解決する責務は realization 側に置かれる。

## Read this when
- エージェント呼び出しの入力として、モデル品質・推論量・ファイルアクセス権限・プロンプト・Structured Output schema をどの単位で保持するか確認したいとき。
- モデル選択の論理区分として、通常選択、品質最優先、効率重視、最安価相当の境界を確認したいとき。
- ファイルアクセスモードの論理区分を参照し、読み取り専用、oracle 読み取り、realization 書き込み、oracle 書き込み、repo 書き込みの呼び出し上の扱いを確認したいとき。
- Structured Output を要求しない呼び出しで schema path をどう表すか確認したいとき。

## Do not read this when
- 実際のバックエンド向けモデル名、reasoning effort、ファイルアクセス指定への変換規則を知りたいとき。この対象は論理値の定義だけを扱う。
- エージェント呼び出しを実行する処理、プロセス起動、外部 CLI 連携、戻り値解析を調べたいとき。
- プロンプト本文の生成規則やテンプレート内容を調べたいとき。
- Structured Output schema 自体の内容や schema ファイルの配置規則を調べたいとき。

## hash
- b29c0e8554c3f417d6684f400fb782525bfb74856125803ab5e7838779ee2620

# `indexing`

## Summary
- `cmoc indexing` で `INDEX.md` 用エントリーを生成するための正本仕様断片を収める領域。対象本文から人間向け要約・読む条件・読まなくてよい条件を構造化して返す出力契約と、その生成を AI エージェント呼び出しとして組み立てる入力・制約・モデル指定を扱う。

## Read this when
- `cmoc indexing` によるルーティング文書エントリー生成の出力契約と、AI 呼び出しパラメータの組み立て仕様を合わせて確認したいとき。
- 対象パスと対象内容を渡して、既存の目次情報ではなくオリジナル本文を根拠にエントリーを生成させる制約がどこで定義されているかを調べるとき。
- エントリー生成結果を検証する実装やテストで、期待される構造化出力と prompt 側の生成条件の両方を確認したいとき。

## Do not read this when
- 個別の対象について、実際にどのような要約や読む条件を書くべきかという内容判断だけをしたいとき。
- ルーティング文書全体の品質基準、INDEX.md の運用方針、または oracle/realization の一般原則を確認したいとき。
- path keyword の一般仕様、complete prompt の汎用構築、構造化 markdown 描画、または AI 呼び出しパラメータ型そのものの定義を調べたいとき。

## hash
- 04a6b74e91c790dccfdd14ced597201bc24e638e15a879eec0fe96e7a409ce26

# `review`

## Summary
- `cmoc review oracle` の oracle file レビュー処理で使う AI 呼び出しと応答契約の正本群。新規所見の列挙、所見を支持する理由と否定する理由の検証、人間へ提示するかの採否判定、所見リストの重複・矛盾整理という各段階への入口になる。
- 各段階は、レビュー対象や既知理由・既知所見などの補助入力を prompt に組み込み、oracle file を根拠にした読み取り専用の調査・判定・整理を行わせる責務を持つ。
- 出力契約は、所見がない場合や新規理由がない場合、整理不要の場合に空の一覧を返す境界も含めて定めているため、レビュー処理の段階別の入出力境界を選ぶための案内になる。

## Read this when
- oracle file レビューで、所見の発見から検証、採否判定、整理までのどの段階の正本へ進むべきか判断したいとき。
- `cmoc review oracle` の AI 呼び出しで、対象所見、既知理由、既知所見、所見リストなどの入力文脈がどの段階に渡されるかを確認したいとき。
- oracle file を根拠に、新規所見だけを列挙する処理、所見の妥当性を支持・否定する理由を列挙する処理、所見を人間に提示するか判定する処理、所見リストを整理する処理の入口を探しているとき。
- レビュー処理の各段階が、読み取り専用アクセス、モデル種別、推論量、対応する応答契約とどう結びつくかを確認したいとき。

## Do not read this when
- oracle file 全般の定義、正本仕様断片としての記述原則、またはレビュー基準の共通ルールだけを確認したいとき。
- `cmoc review oracle` のサブコマンド実行フロー、CLI 入出力、所見の保存・表示・適用など、AI 呼び出し正本と応答契約の外側の実装を確認したいとき。
- 対象が単一段階に絞れており、その段階の prompt 本文または応答契約だけを直接確認すればよいとき。
- INDEX.md エントリーやルーティング文書の生成規則、またはこのディレクトリ外のレビュー標準を確認したいとき。

## hash
- 7370093ef92dff663fd969b7476e80fa1eb8d31a250d6403255eb66b0d226ba7

# `session`

## Summary
- `cmoc session join` が merge conflict marker 解消エージェントへ渡す agent parameter と prompt 制約を定める正本仕様断片を扱う。conflict 対象ファイルの実パス解決、prompt への列挙、編集範囲、oracle file 例外、git add/commit 禁止、marker 残存禁止、model class、reasoning effort、file access mode を確認する入口になる。

## Read this when
- `cmoc session join` の merge conflict marker 解消用エージェント呼び出し仕様を確認・変更したいとき。
- conflict 対象ファイル一覧がどの path 解決を経て prompt に渡されるかを確認したいとき。
- conflict 解消エージェントに課される編集範囲、oracle file 例外、git add/commit 禁止、marker 残存禁止などの制約を確認したいとき。
- session join が conflict marker 解消エージェントに指定する model class、reasoning effort、file access mode を確認したいとき。

## Do not read this when
- `cmoc session join` 全体の制御フロー、ブランチ操作、merge 実行、conflict 検出だけを調べたいとき。
- path keyword、実パス、work-root 解決の一般仕様を調べたいとき。
- 完全 prompt の共通組み立て処理、構造化 markdown rendering、agent parameter 型そのものを調べたいとき。
- merge conflict の内容をどう選んで解消するかという編集判断ルールを、session join 用 prompt 以外から調べたいとき。

## hash
- 5c74a34b38d44d8ccd1049c61e73da7fd68ce6299fb0acc6afbfde7ebbd6bea7

# `tui`

## Summary
- AI Agent CLI/TUI の起動前後で使う呼び出しパラメータを扱う正本仕様断片群。ユーザーの元プロンプトから、実行前パラメータ解決用の呼び出し内容と、その解決結果を受けた TUI 起動用の呼び出し内容を組み立てる流れを定義する。
- 役割・概要・ゴール、論理ファイルアクセスモード、各種標準文書の参照要否、完全プロンプト、モデル種別、reasoning effort、保存済みプロンプト参照指示、structured output schema への対応を確認する入口。

## Read this when
- AI Agent CLI/TUI がオリジナルプロンプトを実行する前に、どの作業条件や標準参照要否をどう解決させるか確認したいとき。
- TUI 起動時に、元プロンプトと解決済みパラメータから完全プロンプトを生成し、保存し、保存済みプロンプトを読むようエージェントへ渡す仕様を確認したいとき。
- TUI 系のエージェント呼び出しで使うモデル種別、reasoning effort、file access mode、入力指示、structured output schema の対応関係を確認したいとき。
- oracle、realization、review、index entry 系の標準文書を読むべきかどうかを、boolean と理由の組で表す実行前パラメータ schema を確認したいとき。

## Do not read this when
- 完全プロンプト本文の文書構造や各標準フラグの意味そのものを確認したいだけなら、完全プロンプトや標準文書を構築する対象へ進む。
- パス語彙、placeholder、repo root や work root の解決規則だけを確認したいなら、パスモデルの正本へ進む。
- TUI ではないサブコマンドのエージェント呼び出しパラメータや実行制御を調べたいなら、そのサブコマンドを扱う仕様断片へ進む。
- 画面操作、入力エディタ処理、または実際の CLI/TUI 実行フローを調べたいなら、パラメータ解決や起動パラメータ構築ではなく実行側の仕様断片へ進む。

## hash
- ba18d3a92643aee27315dd8cc29361c0c9df4125c7a5ca831d700ef07ad1b4e7
