# `doc`

## Summary
- cmoc の正本仕様を機能領域別に案内するディレクトリ。CLI、workflow、feedback、ログ、Codex CLI 呼び出し、通知、自動補完、共通 lifecycle、branch・commit・worktree、開発規則などの個別文書への入口を提供する。
- 現行仕様だけでなく、採用しなかった設計案の検討記録にも分岐できる。

## Read this when
- cmoc の CLI や共通 lifecycle の仕様を確認・変更するとき
- Codex CLI 呼び出し、prompt、feedback、ログ、通知、自動補完、run・session・state・エラー処理・中断の仕様を確認するとき
- session fork、run の隔離、branch・commit・worktree、run report、apply、session join の関係を確認するとき
- Python、CLI 設計、開発環境、テスト要件、テスト実行・品質検査の適用文書を選ぶとき
- realization refactor で採用しなかった作業方式や状態管理方式の理由を確認するとき

## Do not read this when
- 特定の CLI サブコマンドや個別機能の詳細仕様を確認する場合は、対応する個別仕様へ直接進むとき
- 実装配置、テスト実行方法、Python 環境構築、依存関係追加など単一の開発手順だけを確認する場合は、対応する開発ルールや realization へ直接進むとき
- 一般的な利用手順だけを確認する場合は、利用手順書へ直接進むとき
- provider 固有の稼働、認証、推論品質、外部サービスの詳細を調査する場合は、このディレクトリを参照先にしないとき

## hash
- 224e8012753030db0c50694432c40e02d28b8d81b00fd3629c4fb658939d5754

# `src`

## Summary
- oracle src にある cmoc の正本実装群です。ACP 呼び出しパラメータ、完全な agent prompt、oracle・realization の規範、パス解決、設定モデル、構造化文書の Markdown 変換、feedback reporter 入力契約を扱います。用途別の実装を確認する場合は、ACP builder・prompt builder・other・feedback の下位領域が入口になります。

## Read this when
- cmoc の oracle src 実装を調査・変更するとき。
- サブコマンド別の ACP 呼び出し設定や prompt の構築を確認するとき。
- agent prompt に注入する oracle・realization・review・routing・file access などの共通規範を確認するとき。
- リポジトリ設定、パス解決、構造化文書モデル、Markdown 変換などの共通モデルを確認するとき。
- feedback reporter が collector へ渡す入力契約を確認するとき。

## Do not read this when
- oracle の正本ドキュメントや正本テストを確認する場合は、対応する oracle/doc または oracle/test を直接読む。
- realization 側の CLI 挙動や実装を確認する場合は、対応する realization implementation を直接読む。
- 特定の下位領域の責務が明らかな場合は、このディレクトリ全体を読む必要はなく、対応する下位ディレクトリへ直接進む。

## hash
- bc5b9604838954b2ee9dde0d538419d06e16b4c1f2a3f61d959e9e96a7bbeb5f
