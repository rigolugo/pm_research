# Activity Boundaries — REV23 Finding 4 I0A

| Boundary | Status | Exact limit |
|---|---|---|
| Canonical read | AUTHORIZED | `rigolugo/pm_research` only |
| Source synchronization | AUTHORIZED | read-only fetch/clone/checkout to Sentinel-verified authorization-install HEAD only |
| Implementation-source authoring | AUTHORIZED | exact six source paths only |
| Test-source authoring | AUTHORIZED | exact six test-source paths only; unexecuted |
| Test execution | NOT AUTHORIZED | no pytest/unittest/test discovery |
| Project imports/execution | NOT AUTHORIZED | do not import or execute repository modules |
| Static standard-library tooling | AUTHORIZED | JSON/text/hash/AST parsing only; no imports of authored/project modules |
| Local repository source reads | AUTHORIZED | canonical source and accepted contracts only |
| Research/local data reads | NOT AUTHORIZED | no `C:/b1/data`, run artifacts, empirical outputs, credentials, or wallets |
| Network | LIMITED | read-only Git/GitHub synchronization only; no API/RPC/vendor/Dune/curl/general browsing |
| Subprocess/shell | LIMITED | git status/diff, file listing/comparison, checksums, ZIP packaging only |
| Artifact production | LIMITED | implementation review ZIP, static report, and checksum inventory only |
| Working-tree writes | AUTHORIZED | exact twelve paths only |
| Git history/remote writes | NOT AUTHORIZED | no commit, branch/ref, push, PR, merge, tag, or remote mutation |
| Dependencies/CLI/config | NOT AUTHORIZED | no additions or changes |
| P1/P2/P3/scoring/probe | NOT AUTHORIZED | no downstream progression or gate change |

Any need to exceed a boundary produces the first applicable accepted workflow halt.
