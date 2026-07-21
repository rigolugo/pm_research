# Source Gate

Before any source edit Claude MUST verify every condition in this order:

1. Sentinel has supplied the exact verified authorization-installation commit
   SHA.
2. Local `HEAD` equals that exact SHA.
3. `REV23_FINDING4_I0A_SCOPE_REVISION_09` and accepted archive SHA-256
   `4b05f25bf8f5c9e6295af94fdc801baa6d046df42fd007a877d08d736b7960a0`
   are the controlling specification identity.
4. The immutable baseline file
   `REV23_FINDING4_I0A_R1_TWELVE_PATH_BASELINE_SHA256SUMS.txt` contains exactly
   twelve unique repository-relative paths and has exact SHA-256
   `061e6d2cc03ee60e4b47838e4a2c3d2ac4785201d72fd26c708aefc3263ef6f7`.
5. `git status --short --untracked-files=all` contains exactly the twelve
   authorized untracked paths listed in that baseline, each represented by one
   `?? <path>` entry.
6. No thirteenth untracked path, tracked modification, deletion, rename, staged
   change, conflict, ignored generated output, cache, or bytecode path is
   present.
7. Each of the twelve paths has exact SHA-256 equality with its baseline row,
   including `prepared_evidence.py` at
   `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`.
8. The authorization manifest, authorization-directory checksum inventory,
   focused R1 inventory, and complete handoff inventory validate exactly.

After the gate passes, only
`pm_research/local_curl_per_side/prepared_evidence.py` may change. The other
eleven paths MUST remain byte-identical to the baseline. Failure of any condition
requires a halt before editing.

This gate does not require a generically clean worktree; it requires the exact
declared twelve-untracked-path state and no other change.
