# -*- coding: utf-8 -*-



def regroup_actions(actions_flat):
    regrouped_actions_dict = {}
    for action in actions_flat:
        group = hasattr(action, "group") and getattr(action, "group") or "autres"
        actions_in_group = regrouped_actions_dict.setdefault(group, [])
        actions_in_group.append(action)
    last_group = ("autres" in regrouped_actions_dict) and regrouped_actions_dict.pop("autres") or None

    return [(group, regrouped_actions_dict[group]) for group in sorted(regrouped_actions_dict.keys())] + \
            (last_group and [("autres", last_group)] or [])
