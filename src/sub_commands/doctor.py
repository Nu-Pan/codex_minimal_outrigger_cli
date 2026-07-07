from commons.runtime_preprocess_command import run_preprocess_command


def cmoc_doctor_impl() -> None:
    """CLI runtime を通して doctor preprocess を明示実行する。"""
    run_preprocess_command("doctor")
