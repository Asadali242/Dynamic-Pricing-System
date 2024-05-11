import datetime
from services import expired_rule_wiper

def clear_expired_rules():
    print("Running ruleWiper which checks for and defaults any expired rules")
    expired_rule_wiper.wipeExpiredRules
    print("RuleWipe completed.") 