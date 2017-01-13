
import os, sys

import rules_engine
sys.path.append(os.path.dirname(os.path.dirname(rules_engine.__file__)))
import Qt5Ruleset

def local_function_rules():
    return [
        ["MyObject", "fwdDecl", ".*", ".*", ".*", rules_engine.function_discard],
        ["MyObject", "fwdDeclRef", ".*", ".*", ".*", rules_engine.function_discard],
        ["TypedefUser", "setTagPattern", ".*", ".*", ".*", rules_engine.function_discard],
    ]

def local_typedef_rules():
    return [
        [".*", "TagFormatter", rules_engine.typedef_discard],
    ]

def methodGenerator(function, sip, entry):
    sip["code"] = """
        %MethodCode
            sipRes = {} + myAcumulate(a0);
        %End
    """.format(entry["param"])


class RuleSet(Qt5Ruleset.RuleSet):
    def __init__(self):
        Qt5Ruleset.RuleSet.__init__(self)
        self._fn_db = rules_engine.FunctionRuleDb(lambda: local_function_rules() + Qt5Ruleset.function_rules())
        self._typedef_db = rules_engine.TypedefRuleDb(lambda: local_typedef_rules() + Qt5Ruleset.typedef_rules())
        self._modulecode = rules_engine.ModuleCodeDb({
            "cpplib.h": {
            "code": """
%ModuleCode
int myAcumulate(const QList<int> *list) {
    return std::accumulate(list->begin(), list->end(), 0);
}
%End\n
            """
            }
            })

        self._methodcode = rules_engine.MethodCodeDb({
            "SomeNS": {
                "customMethod": {
                    "code": """
                    %MethodCode
                        sipRes = myAcumulate(a0);
                    %End
                    """
                }
            },
            "cpplib.h": {
                "anotherCustomMethod": {
                    "code": methodGenerator,
                    "param": 42
                }
            }
            })
