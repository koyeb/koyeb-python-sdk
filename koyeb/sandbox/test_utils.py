import unittest

from koyeb.api.models.egress_policy_mode import EgressPolicyMode
from koyeb.sandbox.utils import EgressPolicyError, build_network_policy


class TestBuildEgressPolicy(unittest.TestCase):
    """Tests for build_network_policy validation and normalization."""

    def test_both_unset_returns_none(self):
        self.assertIsNone(build_network_policy(False, None))
        self.assertIsNone(build_network_policy())

    def test_both_passed_raises(self):
        with self.assertRaises(EgressPolicyError):
            build_network_policy(True, ["1.2.3.4"])
        with self.assertRaises(EgressPolicyError):
            build_network_policy(True, [])

    def test_block_network_deny_all_without_allowlist(self):
        policy = build_network_policy(True, None)
        self.assertEqual(
            policy.egress.mode, EgressPolicyMode.EGRESS_POLICY_MODE_DENY_ALL
        )
        self.assertIsNone(policy.egress.allow_list)

    def test_bare_ipv4_normalized_to_slash_32(self):
        policy = build_network_policy(False, ["1.2.3.4"])
        self.assertEqual(
            policy.egress.mode, EgressPolicyMode.EGRESS_POLICY_MODE_DENY_ALL
        )
        self.assertEqual([d.cidr for d in policy.egress.allow_list], ["1.2.3.4/32"])

    def test_bare_ipv6_normalized_to_slash_128(self):
        policy = build_network_policy(False, ["2001:db8::1"])
        self.assertEqual(
            [d.cidr for d in policy.egress.allow_list], ["2001:db8::1/128"]
        )

    def test_cidr_passthrough(self):
        policy = build_network_policy(False, ["10.0.0.0/8", "2001:db8::/32"])
        self.assertEqual(
            [d.cidr for d in policy.egress.allow_list],
            ["10.0.0.0/8", "2001:db8::/32"],
        )

    def test_cidr_host_bits_normalized(self):
        policy = build_network_policy(False, ["10.0.0.1/8"])
        self.assertEqual([d.cidr for d in policy.egress.allow_list], ["10.0.0.0/8"])

    def test_invalid_entries_raise(self):
        for bad in [
            "example.com",
            "not-an-ip",
            "",
            "  ",
            "10.0.0.0/33",
            "1.2.3",
            "fe80::1%eth0",
        ]:
            with self.assertRaises(EgressPolicyError, msg=f"entry: {bad!r}"):
                build_network_policy(False, [bad])

    def test_empty_allowlist_means_deny_all(self):
        policy = build_network_policy(False, [])
        self.assertEqual(
            policy.egress.mode, EgressPolicyMode.EGRESS_POLICY_MODE_DENY_ALL
        )
        self.assertEqual(policy.egress.allow_list, [])

    def test_error_is_sandbox_error_and_exported(self):
        import koyeb.sandbox as sandbox_pkg
        from koyeb.sandbox.utils import SandboxError

        self.assertTrue(issubclass(EgressPolicyError, SandboxError))
        self.assertIs(sandbox_pkg.EgressPolicyError, EgressPolicyError)
        self.assertIn("EgressPolicyError", sandbox_pkg.__all__)


if __name__ == "__main__":
    unittest.main()
