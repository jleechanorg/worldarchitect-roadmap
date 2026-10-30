# Pilot deletion PR — status at 2026-10-29 evening PT

- Branch: `delete-intent-classifier-pilot-2026-10-29` in
  `jleechanorg/worldarchitect.ai`, from main `7dd4e55`.
- PR: #11012, open, DRAFT, marked [WIP]. DO NOT MERGE.
- Updates pushed: 39 files (production edits + 30 test files).
- Deletions landed (9 of 12): `mvp_site/intent_classifier.py`,
  `mvp_site/intent_classifier_warmup.py`, `scripts/preflight_model.py`,
  `mvp_site/tests/test_intent_classifier.py`,
  `test_intent_classifier_anchors_pr.py`,
  `test_intent_classifier_context.py`,
  `testing_mcp/test_classifier_simple.py`,
  `testing_mcp/test_combat_intent_classifier_real_e2e.py`,
  `testing_mcp/test_combat_intent_classifier_real_e2e_unit.py`.
- Still pending (3): `testing_ui/test_combat_intent_classifier_browser_e2e.py`,
  `testing_ui/test_cc_offreview_completion_browser_e2e.py`,
  `testing_mcp/capture_agent_selection_evidence.py`.
- Full drafted PR body: `pilot-pr-body.md` in this folder.
- Test suite never executed (compile + grep only); CI must run before merge.
