# Stop-state packaging note

The exact frozen `STOP_STATE_TABLE_REV23.md` is installed unchanged from the approved target bytes. Final packaging introduces no new stop code and no precedence change. Packaging itself hard-stops on source mismatch, baseline mismatch, target mismatch, failed reconstruction, failed checksum, unsafe archive path, or authorization-flag expansion.
