# V3 Evidence — Release-Gated Manifest Verification

The file `v3.0.0-package-manifest.json` in this directory is a frozen,
release-management-approved artifact. It is tracked for checksum verification
only and is **not** part of any distribution package.

## Prerequisite

The `v3.0.0` tag must be approved and available by release management. The
package does not create or regenerate this file automatically; an operator
with access to the approved tag must check it out and use that checkout's own
builder to generate the manifest.

## Regeneration command

After checking out tag `v3.0.0` from the upstream repository:

```bash
cd <v3.0.0-checkout>
python3 scripts/build-distribution.py --target agent --output /tmp/v3-agent
cp /tmp/v3-agent/package-manifest.json docs/v3-evidence/v3.0.0-package-manifest.json
```

The resulting file must be committed to this directory and is verified by the
release-gated regression test `test_v3_regression.V3RegressionTests.test_v3_manifest_hashes_match_release_checkout`.

## Verification

The test compares each manifest entry's `sha256` against the corresponding
file in a checkout pointed to by the environment variable
`AGENT_EVAL_V3_RELEASE_CHECKOUT`. When the variable is absent, the test is
skipped. When present, every hash must match exactly.

This directory is not part of any distribution view — it is excluded from all
packages by `contracts/distribution-contract.yaml`.
