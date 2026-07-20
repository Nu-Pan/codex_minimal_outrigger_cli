# cmoc テスト実装規約

## 基本

- pytest を使用する
- realization test は `{{cmoc-root}}/test` に実装する
- `python-dev-skill` が pytest の隔離に使用する `tmp_path` を `{{test-root}}` とし、被テスト cmoc の HOME、repository、worktree、設定、および実行成果物をそのツリー内に構築する

## goal

- cmoc の決定論的な制御ロジックが仕様どおりに動作する事を検証する
    - e.g. git 状態の検査、作業ディレクトリの決定、対象ファイルの列挙、設定生成、ログ保存、状態更新、エラー処理、…
- Codex CLI 呼び出しを伴う経路では、実在の Codex CLI executable と実推論を使い、cmoc が責任を持つ結合動作を検証する
    - e.g. prompt 渡し、argv による設定、出力保存、schema 指定、response 後の処理、…

## non-goal

- LLM の回答品質や、Codex CLI に依頼した仕事の意味的な成功は cmoc の自動テストの目的としない
- Codex CLI 自体、model provider、有料クラウド backend の正しさや安定性を保証することは目的としない
- GPU 推論の成功または確認を test の成功条件とせず、CPU 推論への fallback を許容する

## 実経路統合テスト

- 実経路統合テストとは、利用者向け CLI entrypoint を独立 process で実行し、本番と同じ code path、実在の外部 executable、および必要な実推論を使って、response 後の処理と外部から観測可能な結果まで検証する realization test である
- 実行時点で公開されている全末端サブコマンドを対象とし、各 test case は終了 code とコマンド固有の外部から観測可能な結果を検証する
- 公開末端サブコマンドと test case の対応は機械的に比較可能にする。公開末端サブコマンドの追加または rename に対して対応する test case がなければ test を失敗させる
- Codex CLI 呼び出しには、実在の Codex CLI executable、実在の Ollama executable、および test-local Ollama による実推論を使用する。Fake、mock、stub、記録済み response、または起動確認だけでは実経路統合テストを代替できない
- 本番との差は、`{{test-root}}` による隔離、決定論的な入力と対話操作の自動化、test-local Ollama、テスト用 SLM、および有料クラウド backend 禁止のために必要な範囲だけ許容する
- `--help`、shell completion、不正入力、事前条件違反、handler の直接呼び出し、または process を分離しない確認は、実経路統合テストとはみなさない
- realization implementation または realization test の変更後は全件を fresh に実行する。新規サブコマンドには同じ作業で test case を追加し、実行結果、Real Codex CLI 呼び出し、および本番との差を報告する。未実行、未検証、失敗、または許容外の差があれば作業を完了扱いにしない

## test-local Ollama

- Codex CLI 呼び出しを行う各 test case は、専用の Ollama process を `{{test-root}}` 内で都度起動する
- Ollama の process runtime directory、HOME、model working directory、binary、PID、log、および port は test case ごとに独立させる
- Ollama は loopback interface の動的空き port で listen させ、固定 port または既存の Ollama service に依存してはならない
- 同じ cache root を使用する実経路統合テスト全体で、同時に稼働する test-local Ollama process は最大 1 つとする
- 各 test case は Ollama 起動前に排他的な Ollama execution lock を取得し、process group の teardown が完了するまで保持する。並列実行された別の test case は lock の解放を待つ
- Ollama execution lock は同時実行数を制限するものであり、異なる test case 間で Ollama process を共有するために使用してはならない
- 同じ test case 内の複数 Codex CLI 呼び出しに限り、その test case の Ollama process を共有してよい
- test case は Ollama を専用 process group として起動し、success、failure、timeout のいずれでも、その test case が起動した process group だけを teardown する
- test-local Ollama は `CmocConfig` の通常の model provider 設定によって Codex CLI 呼び出し単位で選択し、test 専用の特殊な provider ID または provider 起動機能を cmoc に追加してはならない
- テスト用 SLM は `qwen3:4b-instruct-2507-q4_K_M` とする
- test-local Ollama は利用可能な GPU による推論をベストエフォートで優先し、GPU が利用できない場合、GPU 推論を開始できない場合、または GPU 推論を確認できない場合は CPU 推論へ fallback する
- GPU 利用の失敗だけを理由に test を skip または failure としてはならない

## test-local Ollama cache

- Ollama archive、versioned binary、および pull 済み model は、system temporary directory 上の test 専用 cache にベストエフォートで半永続化する
- cache の既定 root は、`tempfile.gettempdir()` で得た system temporary directory 配下で、OS user と cache schema version によって namespacing した directory とする
- 明示的な test 専用環境変数による cache root の override を許容する
- cache root に `{{cmoc-root}}` または `{{work-root}}` の配下を使用してはならず、cache path を `CmocConfig` に追加してはならない
- cache root は使用前に、owner、directory であること、symlink でないこと、permission、読み書き、atomic rename、および file lock の利用可能性を検証する
- system temporary directory が sandbox 内で利用できない場合は pytest session 用一時 directory へ fallback する。cache 永続化だけを理由に sandbox 外実行または追加の writable root を要求してはならない
- system reboot、OS cleanup、利用者操作などによる cache の欠落、削除、または破損は正常な cache miss として扱い、必要な内容を再構築する。test の正しさを cache の存在に依存させてはならない
- 通常の test teardown では cache を能動的に削除しない
- cache の更新は排他的 lock の保持中に staging directory で構築し、完成後に atomic publish する。不完全な内容を cache hit として観測可能にしてはならない
- 各 test case は cache から `{{test-root}}` 内へ独立した working set を materialize し、その working set から Ollama を起動する。cache を Ollama の live working directory として直接共有してはならない
- materialize は、test case が共有 cache を変更せず、test 中に cache が消えても working set が影響を受けない方式とする。これを満たす具体的な方式は realization の裁量とする

## クラウド backend

- テスト目的の Real Codex CLI 呼び出しで、ChatGPT subscription 枠や従量課金の cloud API などの有料クラウド backend を使用してはならない

## Fake Codex CLI

- Fake Codex CLI は、実経路統合テスト以外で Real Codex CLI が不要な場合に限り、決定論的な制御ロジックの検証に使用してよい
