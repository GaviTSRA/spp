from .nodes import *

NODES = {
    # BEGIN START EVENT
    "flag_clicked": "event_whenflagclicked", 
    "key_pressed": "event_whenkeypressed",
    "sprite_clicked": "event_whenthisspriteclicked",
    # BEGIN MOTION
    "move": "motion_movesteps",
    "rturn": "motion_turnright",
    "lturn": "motion_turnleft",
    # START LOOKS
    # START SOUND
    # START EVENTS
    # START CONTROL
    # START SENSING
    # START OPERATORS
    # START VARIABLES
    # START MYBLOCKS
}
UNSUPPORTED_NODES = {
    # BEGIN START EVENT
    "backdrop_switch_to": "event_whenbackdropswitchesto",
    "greater_then": "event_whengreaterthan",
    "broadcast_received": "event_whenbroadcastreceived",
    # BEGIN MOTION
    "goto": "motion_goto",       #motion_goto_menu
    "gotoxy": "motion_gotoxy",
    "glide": "motion_glideto",   #motion_glideto_menu
    "glidexy": "motion_glidetoxy",
    "point": "motion_point_in_direction",
    "pointto": "motion_pointtowardsmotion_pointtowards", #motion_pointtowards_menu
    "changex": "motion_changexby",
    "setx": "motion_setx",
    "changey": "motion_changeyby",
    "sety": "motion_sety",
    "edgebounce": "motion_ifonedgebounce",
    "rotstyle": "motion_setrotationstyle"
    # START LOOKS
    #TODO
    # START SOUND
    #TODO
    # START EVENTS
    #TODO
    # START CONTROL
    #TODO
    # START SENSING
    #TODO
    # START OPERATORS
    #TODO
    # START VARIABLES
    #TODO
    # START MYBLOCKS
    #TODO
}

class Compiler:
    def __init__(self):
        self.res = ""
        self.index = 0

    def visit(self, node):
        method_name = f'visit_' + type(node).__name__
        method = getattr(self, method_name)
        return method(node)

    def visit_FileNode(self, node):
        self.res = '"blocks":{'
        for block in node.blocks:
            self.visit(block)
        self.res += "},"
        return self.res

    def visit_BlockNode(self, node):
        self.visit(node.start_condition)
        self.visit(node.body)

    def visit_StartConditionNode(self, node):
        result = "," if node.index > 0 else ""

        result += f'"{node.index}": ' + "{"
        try:
            result += f'"opcode": "{NODES[node.start_condition.lower()]}",'
        except:
            raise ValueError("Action not found or not supported: " + node.start_condition)
        result += f'"next": "{node.next}",' if node.next != None else '"next": null,'
        result += f'"parent": null,'
        result += '"inputs": {},'
        if node.start_condition.lower() in ["key_pressed"]:
            result += '"fields": {"KEY_OPTION":["' + node.arg + '", null]},'
        else: result += '"fields": {},'
        result += '"shadow": false,'
        result += '"topLevel": true'
        result += "}"
        
        self.res += result

    def visit_BodyNode(self, node):
        for expr in node.exprs:
            self.visit(expr)

    def visit_ExprNode(self, node):
        result = ""

        result += f',"{node.index}": ' + "{"
        try:
            result += f'"opcode": "{NODES[node.instr.value.lower()]}",'
        except:
            raise ValueError("Action not found or not supported: " + node.instr.value)
        result += f'"next": "{node.next}",' if node.next != None else '"next": null,'
        result += f'"parent": ' + f'"{node.previous}",' if node.previous != None else "null,"

        if node.instr.value.lower() in ["move"]:
            result += '"inputs": {"STEPS": [1,[4,'
            if node.value == None:
                raise ValueError("move instruction needs one value")
            result += f'"{node.value}"' + ']]},'
        elif node.instr.value.lower() in ["lturn", "rturn"]:
            result += '"inputs": {"DEGREES": [1,[4,'
            if node.value == None:
                raise ValueError("turn instruction needs one value")
            result += f'"{node.value}"' + ']]},'
        
        result += '"fields": {},"shadow": false,"topLevel": false}'

        self.res += result