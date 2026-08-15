# `doc`

## Summary
- oracle/doc は、cmoc の正本仕様と開発ルールを領域別に案内する上位ドキュメント群。CLI のアプリケーション仕様、branch・commit・worktree のモデル、不採用案の検討記録、開発規則への入口を提供し、具体的な仕様・実装・テスト手順へ進むためのルーティング起点となる。

## Read this when
- cmoc の正本仕様を横断して、CLI の外部挙動、状態・branch model、開発環境、実装配置、テスト要件や実行手順の参照先を選ぶとき
- 複数の仕様領域にまたがる変更や調査で、アプリケーション仕様、branch model、開発ルールなどの下位文書へ進む入口を判断するとき
- 採用されなかった realization refactor の方式や検査・状態管理案の背景を確認するとき

## Do not read this when
- 特定のアプリケーション仕様、branch・worktree の用語、開発規則、テスト実行手順だけを確認する場合は、対応する下位文書へ直接進む
- 実装ファイル、テストファイル、Structured Output schema、feedback の専門仕様など、oracle/doc 配下の案内だけでは足りない具体的内容を確認する場合

## hash
- ac75f00ae4c78e1711e5a9d36840d5b1a606ac0868dcb094d8e36d09f1787ece

# `src`

## Summary
- cmoc の各処理単位で使用する AI エージェント呼び出しの起動定義を扱う領域。共通データモデルを入口に、用途別の prompt・Structured Output schema・モデル・推論強度・アクセスモードなどの定義へ進む。

## Read this when
- 特定の cmoc 機能が起動する AI エージェントの prompt、Structured Output schema、起動パラメータを調べるとき。
- 共通の AgentCallParameter と用途別 agent call builder の責務分担を確認し、oracle review、feedback、realization、session、TUI、quota probe の呼び出し定義へ進むとき。

## Do not read this when
- AI エージェント呼び出しの実行処理、共通 prompt 生成規則、パス解決、ACP 基本型の実装だけを調べるとき。
- 個別の oracle file、realization file、feedback issue の具体的内容や、Structured Output schema の一般仕様を確認するとき。

## hash
- 71bc6def024199055722cb85991ec0e0389f2ed706e8093304fd54021047fe9d
