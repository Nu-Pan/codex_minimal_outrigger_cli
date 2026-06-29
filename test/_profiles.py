from oracle.other.file_access_profile import FAProfile, build_faprofile

READONLY_PROFILE: FAProfile = build_faprofile(
    oracle="read",
    realization="read",
    index="read",
)
ORACLE_ONLY_READ_PROFILE: FAProfile = build_faprofile(
    oracle="read",
    realization="deny",
    index="read",
)
REALIZATION_WRITE_PROFILE: FAProfile = build_faprofile(
    oracle="read",
    realization="write",
    index="read",
)
ORACLE_WRITE_PROFILE: FAProfile = build_faprofile(
    oracle="write",
    realization="read",
    index="write",
)
REPO_WRITE_PROFILE: FAProfile = build_faprofile(
    oracle="write",
    realization="write",
    index="write",
)
