# `launch_exec.py`

## Summary
- `cmoc realization apply fork` の AgentCallParameter 構築定義。oracle file の差分をリポジトリ全体の realization file へ追従させるための完全 prompt を組み立て、対象 worktree、アクセスモード、モデル・推論設定、検証方針などの起動条件を固定する。realization の差分追従処理や、その起動パラメータの変更を行うときの入口。

## Read this when
- `realization apply fork` の launch exec パラメータ、prompt 構築、差分追従対象、または AgentCallParameter の起動設定を変更・確認するとき。

## Do not read this when
- realization file の具体的な反映実装やテスト内容だけを確認する場合。oracle file 自体の仕様や一般的な AgentCallParameter 定義を直接確認すべき場合。

## hash
- 9d1bba0d259d51d8797defedd2e096d2b459225e3e6e397b17f98459addbbdad
