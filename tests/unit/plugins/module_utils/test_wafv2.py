# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.common.dict_transformations import snake_dict_to_camel_dict

from ansible_collections.community.aws.plugins.module_utils.wafv2 import wafv2_snake_dict_to_camel_dict


def _convert(rule):
    # The same two passes wafv2_web_acl applies to each rule.
    return wafv2_snake_dict_to_camel_dict(snake_dict_to_camel_dict(rule, capitalize_first=True))


def test_bot_control_config_key_keeps_aws_in_capitals():
    rule = {
        "statement": {
            "managed_rule_group_statement": {
                "vendor_name": "AWS",
                "name": "AWSManagedRulesBotControlRuleSet",
                "managed_rule_group_configs": [
                    {"aws_managed_rules_bot_control_rule_set": {"inspection_level": "COMMON"}},
                ],
            }
        }
    }

    statement = _convert(rule)["Statement"]["ManagedRuleGroupStatement"]

    assert statement["Name"] == "AWSManagedRulesBotControlRuleSet"
    assert statement["ManagedRuleGroupConfigs"] == [
        {"AWSManagedRulesBotControlRuleSet": {"InspectionLevel": "COMMON"}},
    ]


def test_ip_set_reference_still_converted():
    rule = {"statement": {"ip_set_reference_statement": {"arn": "arn:aws:wafv2:x"}}}

    assert _convert(rule) == {"Statement": {"IPSetReferenceStatement": {"ARN": "arn:aws:wafv2:x"}}}
